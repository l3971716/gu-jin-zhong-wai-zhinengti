import ssl, urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
URLS=[
 "https://www.zhcw.com/kjxx/ssq/",
 "https://www.cwl.gov.cn/kjxx/ssq/kjgg/",
 "https://www.lottery.gov.cn/kj/kjlb.html?dlt",
 "https://m.cwl.gov.cn/",
 "https://www.zhcw.com/kjxx/dlt/",
]
for u in URLS:
    try:
        req=urllib.request.Request(u,headers={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml","Accept-Language":"zh-CN,zh;q=0.9"})
        with urllib.request.urlopen(req,timeout=25,context=ctx) as r:
            body=r.read()[:300].decode("utf-8","ignore")
            print("OK",r.status,len(body),u,"|",body.replace("\n"," ")[:120])
    except Exception as e:
        print("ERR",type(e).__name__,str(e)[:60],u)
