#coding:utf8
#title_en:Spankbang
#comment:https://spankbang.com/
import downloader
from io import BytesIO
from utils import Downloader,Soup,try_n,LazyUrl,clean_title,get_resolution
UAG='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
class Video:
    def __init__(self,url,cwz,sgl):
        self.cw=cwz
        if sgl:
            urlx=self.get(url)
            self.url=LazyUrl(url,lambda _:urlx,self)
        else:
            self.url=LazyUrl(url,self.get,self)
        
    @try_n(2)
    def get(self,url):
        soup=Soup(downloader.read_html(url,user_agent=UAG))
        cod=soup.find('meta',{'property':'og:url'}).attrs['content']
        m1=cod.find('/',13)+1
        m2=cod.find('/',m1)
        self.filename=clean_title(soup.find('h1').text.strip())+'('+cod[m1:m2]+'.mp4'
        file=soup.find('main').find('script',{'type':'text/javascript'}).text
        MARRAY,reso=[2160,1080,720,480,320,240],get_resolution()
        for mo in MARRAY:
            if reso<mo:
                continue
            m1=file.find("[",file.find(f"'{mo}p':"if mo!=2160 else"'4k':"))
            m2=file.find("]",m1)
            if m2-m1>1:
                file=file[m1+2:m2-1]
                break
        self.thumb=soup.find('meta',{'property':'og:image'})['content']
        return file

def thumba(u):
    f=BytesIO()
    downloader.download(u,buffer=f)
    return f

class Downloader_spankbang(Downloader):
    type = 'spankbang'
    strip_header=False
    URLS=['spankbang.com']
    display_name='Spankbang'
    MAX_PARALLEL=2
    MAX_CORE=2
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAA/FBMVEUAAADkP1oAAADkP1vkPlrlP1oBAAClLUHtgJIAAQAAAAEAAAHePVfiPlmlLEAAAAC2MkgAAAAAAADhPVi8M0oBAQDjP1oAAACiLECwMETbPFXgPlnYO1QAAACDIzO/NEsAAADVOlMAAQHkSmQAAAGyMUYBAAE5DxbSOFEAAABsHSsVBQjse48AAQAAAQEwDBLHNk4KAgQAAACTKDphGiTrdYgrCxHDNU19ITDpZnsAAAAAAAAgCAwAAAGrLkOJJDVHEhvlT2nqcYUAAQAzDBOeKj6SJzkAAADMN1ApCg5mGydMFB0PBAXnU2yBIzOYKDs3DhQEAQIBAACMJjcXy3FwAAAAVHRSTlMA/////////////wr///8R/w4D//////7//////wf//xX////Y/+v///v////e7////4D/////////G7T/PP//////iv///yX/////////////jv8vD1r/AAAB20lEQVR4nJ1T53rbMAwUTiQtyZYtR/J2m9jZaVb33nul6/3fpQfScpO06ZcvsH9AwgF3OFLRZeNggMHW+5BvuAyDn2fKu4DTv7u10j1ECg13sCw/muONXRcrm0QBNyxTmdwEuqG+5tLWesJ3IvYB68WxxDEfPgBrHoA0f5iIUYDIKtAoLB8IyTME/vKr7zdiYjF7QJGTg6mU2I2iDrZNss8Oq2PJMnfFzGexkSPXjLZwfDdRuO9hfM6e3/d1/WEjytBKksCvLBKX7mMlRtk4EqDEcgkIJO5JxVrIKRNunLziXuwwlCnGYrtaSAgTUO2/JF51q0Eyzp7teLWW2yKLnuJbTR/G3sOv1ZBbmeAxfcJOrGB2K8DA9QpNSBF/wUoUvcYdRcfea5EjnsZewRbmMxyqlQOM/Nb6yr4DMqS926OWxBNKDIehCKsbmO+Y/kiNzMaUlAPN+jhxstkX0/+EF32p+hwV6p36QjRTnDQ0dDl1hJQtZNf+3KgOcH3YaLenaq83Icd8cV1CdIl4225zRLCA+k71exZgSA413M9XA85Gp5cSQA9ja0pX6z8/gxxcYezSv/oXOhqNXKR1QZ0sGdojS/5z+k6zuOG09vffM/hx9S6Yv9Txv/KV4jcRYRwXADKJVAAAAABJRU5ErkJggg=='
    ACCEPT_COOKIES=[r'(.*\.)?(spankbang)\.(com)']

    def read(self):
        cw=self.cw
        self.single='/video/'in self.url or'-'in self.url[self.url.find('/',13):self.url.find('/',self.url.find('/',13)+1)]
        if self.single:
            video=Video(self.url,cw,True)
            self.urls.append(video.url)
            self.title=video.filename
            self.setIcon(thumba(video.thumb))
        else:
            self.title,self.urls=get_videos(self.url,cw)
        self.enableSegment(chunk=2**20,n_threads=4)

@try_n(2)
def get_videos(url,cw):
    vids,title=[],''
    while True:
        soup=Soup(downloader.read_html(url,user_agent=UAG))
        if not title:
            title=clean_title(soup.find('em').text.strip())
        for wvid in soup.find('section',class_='main_content_container').findAll(class_='thumb'):
            vids.append(Video('https://spankbang.com'+wvid['href'],cw,False).url)
        nex=soup.find(class_='next')
        if not nex:
            break
        url=nex.find('a').attrs.get('href')
        if not url:
            break
        url='https://spankbang.com'+url
        cw.setTitle(f'{title}...{len(vids)}')
    return title,vids
