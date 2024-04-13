#coding: utf-8
#title_en: Visortmo
#comment: https://visortmo.com/
#author: Rickelpapu
from utils import LazyUrl,clean_title,try_n,Downloader,Soup,get_print
from translator import tr_
import downloader
import time
USERAGENT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
REFER='https://visortmo.com/'

class Downloader_visortmo(Downloader):
    type='visortmo'
    URLS=['lectortmo.com','visortmo.com']
    icon='base64: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'
    MAX_CORE=3
    MAX_PARALLEL=1
    display_name='Visortmo'
    ACCEPT_COOKIES=[r'(.*\.)?visortmo?\.com']
    user_agent=USERAGENT
    referer=REFER

    def read(self):
        imgs=getallgal(self.url,self.cw) if '/library/' in self.url else getagal(Page(self.url,''),self.cw)
        self.title=imgs['title']
        self.urls=imgs['data']

class Page:
    def __init__(self,url,title):
        self.url=url
        self.title=title

class Image:
    def __init__(self,url,page,p):
        point=url.rfind('.')
        ext=url[point:] if point>27 else '.webp'
        self.filename=f'{page.title}/{p:03}{ext}'
        self.url=LazyUrl(page.url,lambda _: url,self)

def getpage302(url,cw,p):
    print_=get_print(cw)
    for _ in range(3):
        try:
            soup=Soup(downloader.read_html(url,referer=REFER,user_agent=USERAGENT))
            if 'haciendo demasiadas peticiones' in soup.find('title').text.strip():
                p[0]=1
                print_('1 Estas haciendo demasiadas peticiones espera 60 segundos')
                time.sleep(61-p[1])
                p[1]=time.time()
                continue
            ur=soup.find('meta',{'property':'og:url'}).attrs['content']
            if not '/cascade' in ur:
                if '/view_uploads/' in ur:
                    ur=soup.find('script').text.strip()
                    num=-1
                    if ur:
                        num=ur.find('{uniqid')
                    if num>-1:
                        num=ur.find("'",num)+1
                        ur=ur[num:ur.find(',',num)-1]
                        ur=REFER+'viewer/'+ur+'/cascade'
                    else:
                        continue
                else:
                    ur=ur.replace('/paginated','/cascade')
                soup=Soup(downloader.read_html(ur,user_agent=USERAGENT))
                if 'haciendo demasiadas peticiones' in soup.find('title').text.strip():
                    p[0]=1
                    print_('2 Estas haciendo demasiadas peticiones espera 60 segundos')
                    time.sleep(61-p[1])
                    p[1]=time.time()
                    continue
            break
        except Exception as e:
            print_('Error getpage302:')
            print_(e)
            p[0]=1
            time.sleep(60)
            p[1]=time.time()
    else:
        soup=''
    return soup

def getagal(page,cw):
    soup=getpage302(page.url,cw,[1,time.time()])
    info={}
    info['title']=soup.find('h1').text.strip()
    if 'ONE' in soup.find('h4').text.strip():
        page.title='ONE SHOT'
    else:
        title=soup.find('h2').text.strip()
        arrtitle=title.split()
        if len(arrtitle)>1:
            title=arrtitle[1]
        page.title=clean_title(title)
    imgs=[]
    for img in soup.find(id='main-container').findAll('img'):
        imgs.append(Image(img.attrs.get('data-src'),page,len(imgs)).url)
    info['data']=imgs
    return info

@try_n(2)
def get_imgs(page,cw,p):
    soup=getpage302(page.url,cw,p)
    imgs=[]
    for img in soup.find(id='main-container').findAll('img'):
        imgs.append(Image(img.attrs.get('data-src'),page,len(imgs)).url)
    return imgs

def get_pages(url):
    #print(url)
    for _ in range(4):
        try:
            soup=Soup(downloader.read_html(url,user_agent=USERAGENT))
            if 'haciendo demasiadas peticiones' in soup.find('title').text.strip():
                time.sleep(61)
                continue
            view=soup.findAll('li',class_='upload-link')
            if not view:
                raise Exception('no view')
            break
        except Exception as e:
            e_=e
            #print(e,' get_pages')
            time.sleep(61)
    else:
        raise e_
    urls=set()
    info={}
    h1=soup.find('h1',class_='element-title')
    if h1.small:
        h1.small.extract()
    info['title']=clean_title(h1.text.strip())
    pages=[]
    if 'ONE' in soup.find('h1').text.strip():
        pages.append(Page(soup.find('div',class_='text-right').find('a')['href'],'ONE SHOT'))
    else:
        for li in view:
            href=li.findAll('div',class_='row')[1].find('div', class_='text-right').find('a')['href']
            if href in urls:
                continue
            urls.add(href)
            title=li.find('div',class_='row').find('a').text.strip()
            arrtitle=title.split()
            if len(arrtitle)>1:
                title=arrtitle[1]
            pages.append(Page(href,clean_title(title)))
    info['data']=pages[::-1]
    return info

def getallgal(url,cw):
    pages=get_pages(url)
    imgs=[]
    c=1
    p=[1]
    p.append(time.time())
    for page in pages['data']:
        imgs+=get_imgs(page,cw,p)
        cw.setTitle(f"{tr_('읽는 중...')}{c}/{len(pages['data'])} {pages['title']}")
        if p[0]==14:
            rest=(time.time()-p[1])%60
            time.sleep(62-rest)
            p[0]=0
            p[1]=time.time()
        p[0]+=1
        c+=1
    pages['data']=imgs
    return pages
