import ssl, urllib.request, json, sys
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
URLS=[
 "https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=30",
 "https://api.vvhan.com/api/lottery/ssq",
 "https://api.pearktrue.cn/api/ssq/",
 "https://api.oioweb.cn/api/common/ssq",
 "https://api.52vmy.cn/api/query/lottery?type=ssq",
 "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1",
 "https://api.vvhan.com/api/lottery/dlt",
 "https://api.pearktrue.cn/api/dlt/",
]
for u in URLS:
    try:
        req=urllib.request.Request(u,headers={"User-Agent":UA,"Accept":"*/*","Referer":"https://www.baidu.com/"})
        with urllib.request.urlopen(req,timeout=20,context=ctx) as r:
            body=r.read()[:400].decode("utf-8","ignore")
            print("OK",r.status,len(body),u[:70],"|",body.replace("\n"," ")[:200])
    except Exception as e:
        print("ERR",type(e).__name__,str(e)[:80],u[:70])
