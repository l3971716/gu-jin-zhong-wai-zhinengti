import ssl, urllib.request, urllib.parse
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
SSQ="https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice?name=ssq&issueCount=30"
DLT="https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry?gameNo=85&provinceId=0&pageSize=30&isVerify=1&pageNo=1"
URLS=[
 "https://api.allorigins.win/raw?url="+urllib.parse.quote(SSQ,safe=''),
 "https://api.codetabs.com/v1/proxy?quest="+urllib.parse.quote(SSQ,safe=''),
 "https://api.allorigins.win/raw?url="+urllib.parse.quote(DLT,safe=''),
 "https://api.codetabs.com/v1/proxy?quest="+urllib.parse.quote(DLT,safe=''),
 "https://corsproxy.io/?"+urllib.parse.quote(SSQ,safe=''),
]
for u in URLS:
    try:
        req=urllib.request.Request(u,headers={"User-Agent":UA,"Accept":"*/*"})
        with urllib.request.urlopen(req,timeout=25,context=ctx) as r:
            body=r.read()[:400].decode("utf-8","ignore")
            print("OK",r.status,len(body),u[:80],"|",body.replace("\n"," ")[:180])
    except Exception as e:
        print("ERR",type(e).__name__,str(e)[:70],u[:80])
