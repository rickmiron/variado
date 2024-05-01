#coding: utf-8
#title_en: Nhentai
#comment:https://nhentai.net/
from utils import Downloader,Soup,join,Session
import clf2

@Downloader.register
class Downloader_nhentai(Downloader):
    type = 'nhentai'
    URLS=['nhentai.net']
    display_name='Nhentai'
    MAX_CORE=4

    def read(self):
        self.print_('v1.0')
        self.urls,t=getimg(self.url)
        self.title=self.format_title(t[0],t[1],t[2],t[3],t[4],t[5],t[6])

def getimg(url):
    res=Session().get(url,headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/6.5.2 Chrome/108.0.5359.220 Safari/537.36'})
    soup=Soup(res.text if res.status_code!=403 else clf2.solve(url)['html'])
    files=[i.find('img')['src'].replace('/t','/i').replace('t.','.') for i in soup.find(class_='thumbs').findAll('noscript')]
    bb=['NA']*7
    bb[1]=soup.find(id='gallery_id').text[1:]
    bb[2]=soup.find('h1').text
    for tg in soup.find(id='tags').findAll(class_='field-name'):
        fie=tg.text.split()[0]
        if 'Tags' in fie or 'Pages' in fie:
            continue
        tx=tg.findAll(class_='name')
        if not tx:
            continue
        p=0
        for ts in ['Categories','*','*','Artist','Groups','Parodies','Languages']:
            if ts in fie:
                bb[p]=join([x.text for x in tx])
                break
            p+=1
    return files,bb