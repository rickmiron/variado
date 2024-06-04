#coding:utf-8
#title_en:Allporncomic
#comment:https://allporncomic.com/
import downloader
from utils import clean_title,try_n,Downloader
from translator import tr_
class Downloader_allporncomic(Downloader):
    type = 'allporncomic'
    URLS=['allporncomic.com']
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAABBVBMVEUAAAD+/v4AAAD////+//7//v4BAQEBAAD+/v8AAQAAAAD7+/v//v8AAAEFBAT+//////7X19cDAwL9/f0AAAAAAAAAAAD8/PwAAAATExMQEBAAAAAAAACRkZAPDw4FBQUAAAD39/cBAADY2NgmJiYAAAASEhIPDw8AAAEAAAAAAAAoKCgAAACPj48AAAIAAAAAAADr6+sBAAEBAAAAAAILCwsAAAD29vYBAQAAAAEAAAEAAAAAAAAHBwcAAQAAAQAAAAABAQFMTE0AAACNjY0kJCRISEgAAABkZWUCAAABAADg4OEBAAAAAAAAAACVlZUAAAEAAAAAAAAAAADt7e0AAAIAAACZoXzwAAAAV3RSTlMA////////////b/////////////6BAf8E///1+/////n/6v//DP//meMb/w7/gQq5/9wgk/8x/xU+Ku2//4rWwd//Tv///9H/n2z/sIRw/6c383f/nSPbdty8AAACSUlEQVR4nG1TiXbaMBD07kqyFdsYbIcbQoBckNAkTZr76n3f7f9/Ske4UCAdv+dneWdHs6uVt4jR7l6r9XB7vvRzjq0+c3vv8LCf+/au/ihcveLW09niW5vfrMR/c3y7PlkvMFmf7HK+tRh/YTZKeNgaBtKNEmDmgp73jF9GWogoNUCaKdKkn5u5RpXfSpmigCgEo5RlSukkiMZmRujdCAkFChKhSUnAxrdQ6aGIX3IoQloSgnKnAoJEeCQ5MkW1bRMihxqbUKCDgZTB4CwQrW6uXLzOcejUm45Q7gxEFAiktUiDHeHE+jXIq+amCqR8MFDOMFNCEjXshbN4HdcgC4UI23cGCEBBKywafAcCX3ANstQ8I0oCmHQVMDq1UWLOHWHf1FzSdggLAgJplfjMvmW8HWELHpCEQpQknYqGV0E8tmz/EjhUaK0rko5MRQXBlIB0wBFGDHHo4gR+pn6F0HLxM6C27TsP+Q8Op+mazlJjHUGLj7WiBvdAOO45gqYdyLLhCjpQjixkdNLgE3fWxm0RgBA725UIqWJJgbLNT1wrje88qK7v4owqtNY83bLpLHjetQnBpi6buCDAJGaGKPPXivPmLwFK6FoIxHyKyaAkSxQFrwsBz3uf1tD6LrOxsTWnznGAtn0wl7OR6qdhJF2OLboT845yx0Gb8f2/qe2lr4bYH63FLqY5Hg+Hw7S/OPct/rW2hHs+Xr45X833ac0Fztv+55Wr5dVbnO/uV3EJRh9z3sPHI9Tf5YwycIU//S9coFqvrwT/AJ/XKj2QQ3/VAAAAAElFTkSuQmCC'
    MAX_CORE=3
    display_name='Allporncomic'
    ACCEPT_COOKIES=[r'(.*\.)?allporncomic?\.com']
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

    def read(self):
        self.title,self.urls,self.filenames=(get_imgs_all if len(self.url[10:-1].split('/'))==3 else get_single)(self.url,self.cw)
        if '.mp4'==self.urls[0][-4:]:
            self.enableSegment()
        
class Page:
    def __init__(self,url,title):
        self.url=url
        self.title=title
def get_single(url,_):
    soup=downloader.read_soup(url)
    title=soup.find(class_='breadcrumb').findAll('a')[-1].text.strip()
    titl=soup.find(class_='breadcrumb').find(class_='active').text.strip()
    imgs=[]
    fn={}
    view=soup.find_all(class_='wp-manga-chapter-img')
    if view:
        for img in view:
            src=img['data-src']
            point=src.rfind('.')
            ext=src[point:] if point>25 else '.gif'
            fn[src]=f'{titl}/{len(imgs):04}{ext}'
            imgs.append(src)
    else:
        src=soup.find('source')['src']
        fn[src]=titl+'.mp4'
        imgs.append(src)
    return title,imgs,fn
@try_n(2)
def get_imgs(page):
    soup=downloader.read_soup(page.url)
    view=soup.find_all(class_='wp-manga-chapter-img')
    imgs=[]
    fn={}
    if view:
        for img in view:
            src=img['data-src']
            point=src.rfind('.')
            ext=src[point:] if point>25 else '.gif'
            fn[src]=f'{page.title}/{len(imgs):04}{ext}'
            imgs.append(src)
    else:
        src=soup.find('source')['src']
        fn[src]=page.title+'.mp4'
        imgs.append(src)
    return imgs,fn

def get_pages(url):
    info={}
    soup=downloader.read_soup(url)
    info['title']=clean_title(soup.find('h1').text.strip())
    pages=[]
    for li in soup.findAll(class_='wp-manga-chapter'):
        li=li.find('a')
        pages.append(Page(li['href'],clean_title(li.text.strip())))
    info['data']=pages[::-1]
    return info

def get_imgs_all(url,cw):
    pages=get_pages(url)
    fn={}
    imgs=[]
    p=1
    for page in pages['data']:
        gts,fns=get_imgs(page)
        imgs+=gts
        fn.update(fns)
        cw.setTitle(f"{tr_('읽는 중...')}{pages['title']} {p}/{len(pages['data'])}")
        p += 1
    return pages['title'],imgs,fn
