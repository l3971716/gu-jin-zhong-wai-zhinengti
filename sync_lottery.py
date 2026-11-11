#!/usr/bin/env python3
# 彩票开奖数据同步：拉取官方最新开奖（双色球30期 + 大乐透30期）写入 lottery.json
# 供 GitHub Actions 每日定时执行，前端从 raw.githubusercontent.com 读取（支持跨域）
import json, ssl, sys, urllib.request
from datetime import datetime, timezone, timedelta

SSQ_URL = "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=30"
DLT_URL = ("https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"
           "?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.cwl.gov.cn/"})
    with urllib.request.urlopen(req, timeout=25, context=ctx) as r:
        return json.loads(r.read().decode("utf-8", "ignore"))


def sync_ssq():
    j = get(SSQ_URL)
    rows = []
    for o in (j.get("result") or j.get("data") or []):
        red = [int(x) for x in str(o.get("red", "")).replace("，", ",").split(",") if x.strip().isdigit()]
        blue_raw = str(o.get("blue", "")).replace("，", ",").split(",")
        blue = int(blue_raw[0]) if blue_raw and blue_raw[0].strip().isdigit() else 0
        if len(red) == 6 and blue:
            rows.append({"q": str(o.get("code")), "d": str(o.get("date", ""))[:10], "r": red, "b": blue})
    return sorted(rows, key=lambda x: x["q"])


def sync_dlt():
    j = get(DLT_URL)
    rows = []
    for o in ((j.get("value") or {}).get("list") or []):
        nums = [int(x) for x in str(o.get("lotteryDrawResult", "")).split() if x.isdigit()]
        if len(nums) >= 7:
            rows.append({"q": str(o.get("lotteryDrawNum")), "d": str(o.get("lotteryDrawTime", ""))[:10],
                         "f": nums[:5], "b": nums[5:7]})
    return sorted(rows, key=lambda x: x["q"])


def main():
    out = {"updated": "", "ssq": [], "dlt": [], "errors": []}
    for name, fn in (("ssq", sync_ssq), ("dlt", sync_dlt)):
        try:
            rows = fn()
            if not rows:
                raise RuntimeError("接口返回为空")
            out[name] = rows
            print(f"{name}: {len(rows)} 期，最新 {rows[-1]['q']}（{rows[-1]['d']}）")
        except Exception as e:
            out["errors"].append(f"{name}: {e}")
            print(f"{name} 同步失败: {e}", file=sys.stderr)
    tz = timezone(timedelta(hours=8))
    out["updated"] = datetime.now(tz).strftime("%Y-%m-%d %H:%M")
    with open("lottery.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print("written lottery.json, updated", out["updated"], "errors", out["errors"])


if __name__ == "__main__":
    main()
