import ssl, urllib.request
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
URLS=[
 ("zhcw_ssq","https://jc.zhcw.com/port/client_json.php?callback=cb&transactionType=10001001&lotteryId=1&issueCount=30&startIssue=&endIssue=&startDate=&endDate=&type=0&pageNum=1&pageSize=30&tt=0.123"),
 ("sina","https://lottery.sina.com.cn/dlt/"),
 ("sina2","https://match.lottery.sina.com.cn/lotto/api/list?lottoType=dlt&page=1&_=1"),
 ("cjcp","https://www.cjcp.com.cn/"),
 ("17500","https://www.17500.cn/"),
 ("zhcw_dlt","https://www.zhcw.com/kjxx/dlt/"),
]
for n,u in URLS:
    try:
        req=urllib.request.Request(u,headers={"User-Agent":UA,"Accept":"*/*","Referer":"https://www.zhcw.com/"})
        with urllib.request.urlopen(req,timeout=25,context=ctx) as r:
            body=r.read()[:300].decode("utf-8","ignore")
            print("OK",n,r.status,len(body),"|",body.replace("\n"," ")[:110])
    except Exception as e:
        print("ERR",n,type(e).__name__,str(e)[:55])
