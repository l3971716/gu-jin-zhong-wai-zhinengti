#!/usr/bin/env python3
# 彩票开奖数据同步：拉取官方最新开奖（双色球30期 + 大乐透30期）写入 lottery.json
# 供 GitHub Actions 每日定时执行，前端从 raw.githubusercontent.com 读取（支持跨域）
import json, ssl, sys, urllib.request
from datetime import datetime, timezone, timedelta

SSQ_URL = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=500"
DLT_URL = ("https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"
           "?gameNo=85&provinceId=0&pageSize=100&isVerify=1&pageNo={page}")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get(url, referer):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Referer": referer,
        "Origin": referer.rstrip("/"),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    })
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def sync_ssq():
    j = get(SSQ_URL, "https://www.cwl.gov.cn/kjxx/ssq/kjgg/")
    rows = []
    for o in (j.get("result") or j.get("data") or []):
        red = [int(x) for x in str(o.get("red", "")).replace("，", ",").split(",") if x.strip().isdigit()]
        blue_raw = str(o.get("blue", "")).replace("，", ",").split(",")
        blue = int(blue_raw[0]) if blue_raw and blue_raw[0].strip().isdigit() else 0
        if len(red) == 6 and blue:
            rows.append({"q": str(o.get("code")), "d": str(o.get("date", ""))[:10], "r": red, "b": blue})
    return sorted(rows, key=lambda x: x["q"])


def sync_dlt():
    rows = []
    for page in range(1, 6):
        j = get(DLT_URL.format(page=page), "https://static.sporttery.cn/")
        for o in ((j.get("value") or {}).get("list") or []):
            nums = [int(x) for x in str(o.get("lotteryDrawResult") or "").split()]
            if len(nums) != 7:
                continue
            rows.append({
                "q": str(o["lotteryDrawNum"]),
                "d": str(o.get("lotteryDrawTime") or "")[:10],
                "f": sorted(nums[:5]),
                "b": sorted(nums[5:7]),
            })
    rows.sort(key=lambda x: x["q"])
    if not rows:
        raise RuntimeError("接口返回为空")
    return rows


def main():
    old = {}
    try:
        with open("lottery.json", encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        pass

    out = {"updated": "", "ssq": [], "dlt": [], "errors": []}
    fresh = 0
    for name, fn in (("ssq", sync_ssq), ("dlt", sync_dlt)):
        try:
            rows = fn()
            if not rows:
                raise RuntimeError("接口返回为空")
            out[name] = rows
            fresh += 1
            print(f"{name}: {len(rows)} 期，最新 {rows[-1]['q']}（{rows[-1]['d']}）")
        except Exception as e:
            out["errors"].append(f"{name}: {e}")
            kept = old.get(name) or []
            out[name] = kept
            print(f"{name} 同步失败({e})，保留已有 {len(kept)} 期", file=sys.stderr)

    tz = timezone(timedelta(hours=8))
    out["updated"] = datetime.now(tz).strftime("%Y-%m-%d %H:%M")

    if fresh == 0:
        print("两个彩种均未取到新数据，不写入文件（避免空数据覆盖）", file=sys.stderr)
        return 0

    with open("lottery.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("written lottery.json, updated", out["updated"], "errors", out["errors"])
    return 0


if __name__ == "__main__":
    main()
