import asyncio
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
async def getContent(url='',political=''):
    #print(url)
    start = (datetime.now().timestamp())
    r=requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    await countString(soup,political)
    data = soup.findAll('a')
    for a in data:
        try:
            fw_url = str(a['href'])
            fw_url = fw_url.replace('/url?q=','')
            if(fw_url.startswith('http') == True):
                await asyncio.create_task(getContent(fw_url,political)) 
                #fw_url = "https://www.google.com/"+fw_url
            #print(tag_a.text,'->',fw_url)
        except:
            pass
            #print('error')
        
    end = (datetime.now().timestamp())  

async def getGGContent(url='',political=''):
    start = (datetime.now().timestamp())
    r=requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    await countString(soup,political)
    data = soup.findAll(attrs={"class":"r"})
    for c in data:
        #total=total+1
        tag_a = c.find('a')
        fw_url = str(tag_a['href'])
        fw_url = fw_url.replace('/url?q=','')
        if(fw_url.startswith('http') == False):
           fw_url = "https://www.google.com/"+fw_url
        print(tag_a.text,'->',fw_url)
        if(fw_url.find('google') == -1):
            await asyncio.create_task(getContent(fw_url,political)) 
    end = (datetime.now().timestamp())  

async def countString(soup,str):
    body = soup.findAll('body')
    cnt_str = 0
    for b in body:
        cnt_str = cnt_str + b.text.count(str)
    print('total cnt str(',str,') = ',cnt_str)

async def main():
    #total =0
    url = 'https://www.google.co.th/search?q='
    # 10 political
    political = ['พรรคประชาธิปัตย์','พรรคประชากรไทย','พรรคมหาชน','พรรคกสิกรไทย','พรรคเพื่อฟ้าดิน','พรรคความหวังใหม่','พรรคเครือข่ายชาวนาแห่งประเทศไทย','พรรคเพื่อไทย','พรรคเพื่อแผ่นดิน','พรรคชาติพัฒนา']
    #url = 'https://en.wikipedia.org/wiki/'
    #for p in political:
    #    await asyncio.create_task(getGGContent(url+p,p))
    await asyncio.create_task(getGGContent(url+political[0],political[0]))
    
# Python 3.7+
#total = 0
asyncio.run(main())
#print("Total:",total)
#time.sleep(5)

#print(((int)(end - start)))

