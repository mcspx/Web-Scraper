import asyncio
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
import redis
import json
async def getContent(url='',political='',n=0):
    start = (datetime.now().timestamp())
    #print('connecting...')
    r=requests.get(url)
    #print('connected')
    soup = BeautifulSoup(r.content,'html.parser')
    #asyncio.create_task(countString(soup,political))
    await countString(soup,political,n)
    data = soup.findAll('a')
    #print('data->len',len(data))
    limit = 10
    links = []
    for a in data:
        #limit = limit - 1
        #if limit == 0:
        #    print('break')
        #    break
        try:
            fw_url = str(a['href'])
            fw_url = fw_url.replace('/url?q=','')
            if(fw_url.startswith('http') == True):
                if(fw_url.find('google') == -1):
                    #print('n = ',n)
                    if fw_url in links:
                        #print('dup url')
                        continue
                    else:
                        #print(a.text)
                        links.append(fw_url)
                        #await asyncio.create_task(getContent(fw_url,political)) 
                        asyncio.run(getContent(fw_url,political,n))
                #fw_url = "https://www.google.com/"+fw_url
            #print(tag_a.text,'->',fw_url)
        except:
            continue
            #print('error')
        
    end = (datetime.now().timestamp())  

async def getGGContent(url='',political='',n=0):
    start = (datetime.now().timestamp())
    r=requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    #asyncio.create_task(countString(soup,political))
    await countString(soup,political,n)
    data = soup.findAll(attrs={"class":"r"})
    for c in data:
        try:
            #total=total+1
            tag_a = c.find('a')
            fw_url = str(tag_a['href'])
            fw_url = fw_url.replace('/url?q=','')
            if(fw_url.startswith('http') == False):
                fw_url = "https://www.google.com/"+fw_url
            print(tag_a.text)
            if(fw_url.find('google') == -1):
                await asyncio.create_task(getContent(fw_url,political,n)) 
                #await asyncio.run(getContent(fw_url,political))

        except:
            continue
    end = (datetime.now().timestamp())  

async def getListPolitical():
    url = 'https://th.wikipedia.org/wiki/%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%8A%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%87%E0%B9%83%E0%B8%99%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B9%80%E0%B8%97%E0%B8%A8%E0%B9%84%E0%B8%97%E0%B8%A2'
    r=requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    data = soup.findAll(attrs={"class":"multicol"})
    data = data[0].findAll('li')
    political = []
    for li in data:
        a = li.find('a')
        political.append(a.text)
        #print(a.text)
    return political
async def countString(soup,str,n):
    await incSite()
    print("counting..")
    body = soup.findAll('body')
    cnt_str = 0
    for b in body:
        cnt_str = cnt_str + b.text.count(str)
    await countArticle(cnt_str,n)
    #print('total cnt str(',str,') = ',cnt_str)
async def countArticle(cnt,n=0):
    key = "n"+str(n)
    r = redis.Redis(host='localhost', port=6379, db=0)
    #print(r.get(key))
    if r.get(key) is None:
        r.set(key,1)
    else:
        cnt = int(r.get(key)) + cnt
        r.set(key,cnt)
    #print(int(r.get("n1")))
async def incSite():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('totalSite',int(r.get('totalSite'))+1)
async def main():
    #total =0
    url = 'https://www.google.co.th/search?q='
    # 10 political
    political = ['พรรคประชาธิปัตย์','พรรคประชากรไทย','พรรคมหาชน','พรรคกสิกรไทย','พรรคเพื่อฟ้าดิน','พรรคความหวังใหม่','พรรคเครือข่ายชาวนาแห่งประเทศไทย','พรรคเพื่อไทย','พรรคเพื่อแผ่นดิน','พรรคชาติพัฒนา']
    political = await getListPolitical()
    print(len(political))
    #url = 'https://en.wikipedia.org/wiki/'
    n = 0
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('totalSite',0)
    for p in political:
        n = n+1
        r.set('n'+str(n),0)
        await getGGContent(url+p,p,n)
    
    #await getGGContent(url+political[0],political[0],1)
    #r = redis.Redis(host='localhost', port=6379, db=0)
    for key in r.keys():
        print(key,'=',r.get(key))
    #await asyncio.create_task(getGGContent(url+political[0],political[0]))
    
# Python 3.7+
asyncio.run(main())
list_political = asyncio.run(getListPolitical())
#print(((int)(end - start)))

political_data = []
r = redis.Redis(host='localhost', port=6379, db=0)
i = 0
for p in list_political:
    i = i + 1
    val = int(r.get("n"+str(i)))
    #print(p,'=>',val)
    political_data.append({"id":i,"name":p,"count":val})

jdata = {}
jdata['political_data'] = political_data
jdata['totalSite'] = int(r.get("totalSite"))
#print(jdata)

with open("jdata.json","w") as outfile:
    json.dump(jdata,outfile)