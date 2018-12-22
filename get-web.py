import asyncio
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
import time
async def getContent(url,total=0):
   start = (datetime.now().timestamp())
   r=requests.get(url)
   soup = BeautifulSoup(r.content,'html.parser')
   data = soup.findAll('h3')
   #data = soup.findAll('div',attrs={'class':['g']})
   #data = soup.findAll('h3',href=re.compile('/wiki'))
   for a in data:
       total=total+1
       print(a.text)
       #asyncio.create_task(getContent(a['href'],0))
   end = (datetime.now().timestamp()) 
   print('total ',total," time ",((int)(end - start)))
  
   #print("visit link per time ",((int)(end - start))," ",pages)

async def main():
   total =0
   #url = 'https://en.wikipedia.org/wiki/'
   url = 'https://www.google.com/search?ei=4-EdXIGlC4vUvATlkp7IBQ&q=%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%8A%E0%B8%B2%E0%B8%98%E0%B8%B4%E0%B8%9B%E0%B8%B1%E0%B8%95%E0%B8%A2%E0%B9%8C&oq=%E0%B8%9E%E0%B8%A3%E0%B8%A3%E0%B8%84%E0%B8%9B%E0%B8%A3%E0%B8%B0%E0%B8%8A%E0%B8%B2%E0%B8%98%E0%B8%B4%E0%B8%9B%E0%B8%B1%E0%B8%95%E0%B8%A2%E0%B9%8C&gs_l=psy-ab.3..0i71l8.0.0..10351...0.0..0.0.0.......0......gws-wiz.uDssdTUUxtg'
   await asyncio.create_task(getContent(url,total))
   print("Total:",total)
# Python 3.7+

asyncio.run(main())

#time.sleep(5)

#print(((int)(end - start)))

