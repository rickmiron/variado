#coding:utf8
#title_en: Missav
#comment: https://missav.com/
#author: Rickelpapu
import downloader
from utils import Downloader,try_n,LazyUrl,get_print,Soup,clean_title,Session,get_resolution
from translator import tr_
from m3u8_tools import M3u8_stream
from io import BytesIO
from PIL import Image
from ffmpeg import convert,run
from os import remove,makedirs,path
USERAGEN='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
class Video:
    def __init__(self,url,cwz,dir):
        self.cw=cwz
        self.dir=dir
        pt_=get_print(self.cw)
        pt_('Get ofuscado')
        urlv=self.ofuscado(url)
        pt_(urlv)
        sesion=Session()
        sesion.cookies.clear()
        sesion.headers.clear()
        sesion.headers.update({'Origin':'https://missav.com','User-Agent':USERAGEN})
        if urlv[urlv.rfind('.'):]=='.m3u8':
            m=Strimin(urlv,session=sesion,n_thread=4)
            if getattr(m,'live',None)is not None:
                m=m.live
        else:
            m=urlv.replace('.mpd','.mp4')
        self.thumb=BytesIO()
        self.thumbz=BytesIO()
        self.cw.setTitle(f'{tr_("썸네일 다운로드")}...{self.filename}')
        pt_(self.urlthumb)
        downloader.download(self.urlthumb,buffer=self.thumbz)
        self.dirfile=f'{dir}\\{self.filename}'
        self.tojpg()
        self.havethumbnail()
        self.url=LazyUrl('https://missav.com/',lambda _: m,self,pp=self.pp)

    def havethumbnail(self):
        if path.exists(self.dirfile):
            mi=run(f'-i "{self.filename}"',self.dir,bin='ffprobe')
            for ee in mi:
                if isinstance(ee,str) and 'attached pic' in ee:
                    break
            else:
                self.cw.setTitle(f'{tr_("썸네일 고정")}...{self.filename}')
                self.pp(self.dirfile)

    def tojpg(self):
        self.thumbz.seek(0)
        bythz=self.thumbz.read()
        if len(bythz)>0:
            with open(self.dirfile+'.webp',"wb")as f:
                f.write(bythz)
            f.close
            imagen_webp=Image.open(self.thumbz)
            if imagen_webp.mode!="RGB":
                imagen_webp=imagen_webp.convert("RGB")
            imagen_webp.save(self.thumb,"JPEG",quality=90)
            self.thumbz.truncate(0)

    def ofuscado(self,url):
        soup=Soup(downloader.read_html(url,user_agent=USERAGEN))
        self.urlthumb=soup.find('meta',{'property':'og:image'})['content']
        title=soup.find('h1').text.strip()
        vid='/video/'not in url
        if vid:
            codigo=soup.find('meta',{'property':'og:url'})['content']
            codigo=codigo[codigo.rfind('/')+1:].upper()
            un=title.find(' ')
            if un==-1:
                un=len(title)
            title=codigo+title[un:]
        self.filename=clean_title(title,n=190)+'.mp4'
        codigo=soup.findAll('script',{'type':'text/javascript'})[-2].text
        un=codigo.find('eval(')
        codigo=codigo[un:codigo.find('.split(',un)-1]
        un=codigo.find('://')
        k_array=codigo[codigo.find(',\'',un)+2:].split('|')
        narray=[]
        for car in codigo[un-1:codigo.find(';',un)-2]:
            num=ord(car)
            narray.append((k_array[num-48]if 58>num>47 else k_array[num-87] if 96<num<123 else car)or car)
        url=''.join(narray)
        if not vid:
            return url
        codigo=downloader.read_html(url,headers={'Origin':'https://missav.com'},user_agent=USERAGEN)
        reso=get_resolution()
        for tex in codigo.split()[::-1]:
            if '#' not in tex:
                codigo=tex
            else:
                un=tex.find('x',tex.find('RESOL'))+1
                dos=tex.find(',',un)
                if not int(tex[un: None if dos<0 else dos])>reso:
                    break
        return url.replace('playlist.m3u8',codigo)

    def pp(self,filename):
        self.thumb.seek(0)
        bythum=self.thumb.read()
        if len(bythum)>0:
            pathum=f'{filename}.I'
            with open(pathum,'wb')as f:
                f.write(bythum)
            f.close
            convert(filename,filename,f'-i "{pathum}" -map 1 -map 0 -c copy -disposition:0 attached_pic',cw=self.cw)
            remove(pathum)
        return filename

class Strimin(M3u8_stream):
    def _pp(self,_):
        pass

class Downloader_missav(Downloader):
    type = 'missav'
    single=True
    strip_header=False
    URLS=['missav.com']
    display_name='Missav'
    MAX_PARALLEL=2
    #MAX_SPEED=0.7
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAaVBMVEX+Yo4AAAD/Yo7+Y47////+Yo//Yo////7+Y4/mvcbvYof/AADQWXHnYoD7YYyqVVX2YYn+Yo3+/////v//Y46ZMzP//f7mu8X9aZL//Pz9Z5H5ep31xdH52uLziqX9h6jxl6/2ztj73uab0JJXAAAAI3RSTlP/AP//////////zgErp/wD3/3///8F/////////////////8G0tiwAAAGzSURBVHicZVOLcoMwDDNxAi1QCpSytnvv/z9ykp3Qdssd4S6WZUV2pLqvfhw0qAxj/3C4Abq2lqQhiEgt0nZ/AQcEhNGUBCxJDk+A46QM4mMwIa4yHe+As5KWEEGENIY+F8CRZ/XO4k4TsANEDgIm5i4WpABwkAbf5ADoo6pcArvKzilqKJWq80iAisX2rAN7CB0AbUkTXd8sYGZ4lRYA2GOqRV7iHF910Z2og3BcSe/BANg+xni6+m38VEIvY740FgGxie/FVMJGGTRrEgWgAUeMH9kSrMF/yVTuG0ZjnJv1JlbJU1ki4XoKgMXJc3GRLijUC+4GDU0uEZvGAOZvMQX/PePGsV6srt1/kFTatLfk+RS/TFLNqwwyOpeJnC39B41gS1lcRxoFdiPBNed4veUEzA1WL1Wo2WM0GlY3p8/NAc4Vra5aaHHjdP2+O+SLzeowTRTFD03K9hj/ztrNgUloFYPBg9l74WjbyCHgQ4s8uO6dXOoyctWRKsrCHJHGQGVoq3Pufja3SNjGng/HszeJqPP4cPj0qJN5GGijeH569nhtKlCBGv4/3vz84bs+P/9fOZAMztosBq4AAAAASUVORK5CYII='
    ACCEPT_COOKIES=[r'(.*\.)?(missav)\.(com)']

    @try_n(2)
    def read(self):
        if not path.exists(self.dir):
            makedirs(self.dir)
        vi=Video(self.url,self.cw,self.dir)
        self.setIcon(vi.thumb)
        self.urls.append(vi.url)
        self.title=vi.filename
