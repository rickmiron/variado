#coding: utf8
#title: SoGirl
#comment: https://krXX.sogirl.so/

import downloader
from utils import Downloader, get_print,LazyUrl,Soup,clean_title
from io import BytesIO
import clf2
from hashlib import md5
import requests
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from ffmpeg import run
import os
from timee import sleep
import shutil

USERAGEN='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

@Downloader.register
class Downloader_sogirl(Downloader):
    type = 'sogirl'
    URLS = ['.sogirl.so']
    display_name = 'SoGirl'
    icon = 'base64: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'
    ACCEPT_COOKIES = [r'(.*\.)?(sogirl)\.(so)']
    MAX_CORE = 4
    MAX_PARALLEL = 2
    user_agent=USERAGEN

    def read(self):
        sesion = requests.session()
        sesion.headers['User-Agent'] = USERAGEN
        un = self.url.find('k')
        domi = self.url[un:self.url.find('.')]
        infof = getinf(self.url,domi)
        self.title=infof['filename']
        self.setIcon(infof['thumb'])
        diir = self.dir
        if os.path.exists(diir+'.mp4'):
            self.urls.append(diir+'.mp4')
            self.single = True
        else:
            if not os.path.exists(diir):
                os.makedirs(diir)
            self.urls = getm3u8(infof['iframe'],sesion, diir,self.cw,domi)

    def post_processing(self):
        if not self.single:
            ini = 0
            fin = len(self.urls)
            finx = 2044
            ext ='.ts'
            name0 = ''
            name1 = 'x0'
            self.cw.setTitle('Joining parts...'+self.title)
            while True:
                if not fin>finx:
                    finx = fin
                    name1 = self.title
                    ext = '.mp4'
                partes = [str(ele) for ele in range(ini,finx)]
                run(f'-i concat:{name0}{"|".join(partes)} -c copy "{name1}{ext}"', self.dir)
                if ext == '.mp4':
                    break
                name0 = name1+ext+'|'
                name1 = 'x1' if name1=='x0' else 'x0'
                ini = finx
                finx += 2044
            self.cw.setTitle('Cleaning...'+self.title)
            os.rename(self.dir+'/'+self.title+'.mp4', self.dir+'.mp4')
            shutil.rmtree(self.dir)
            self.cw.setNameAt(0, self.dir+'.mp4')
            self.single = True
            self.cw.setTitle(self.title)

class Video:
    def __init__(self, url, sesion, cw, pos ,cifralis,pinx,arstr):
        self.session = sesion
        self.cw = cw
        self.url = LazyUrl(url, self.get, self)
        self.pos=pos
        self.filename = str(pos)
        self.cifralis =cifralis
        self.pinx=pinx
        self.arstr=arstr
    
    def get(self,urlx):
        ind = self.pos//3
        while len(self.cifralis) <= ind:
            if self.pos%3==0:
                if self.pos%12==0:
                    ackey = ind*12
                    mdd5 = md5(f'{self.arstr[0]}_{self.arstr[1]}_{ackey}.000001_false_720'.encode('utf8')).hexdigest()
                    self.pinx[1]=f'{self.arstr[2]}/ping?hash={mdd5}&time={ackey}.000001&paused=false&resolution=720'
                self.session.get(self.pinx[1],headers={'Referer': 'https://iframe.mediadelivery.net/'})
                clave = self.session.get(self.arstr[3]+str(ind),headers={'referer': 'https://iframe.mediadelivery.net/'})
                while len(self.cifralis) != ind:
                    sleep(0.01)
                self.cifralis.append(Cipher(algorithms.AES(clave.content), modes.CBC(self.arstr[4]), backend=default_backend()))
                break
            else:
                sleep(0.01)
        descri = self.cifralis[ind].decryptor()
        pvid = self.session.get(urlx,headers={'Referer': 'https://iframe.mediadelivery.net/'})
        filedes = descri.update(pvid.content) + descri.finalize()
        ruta=self.arstr[5]+'/'+self.filename
        with open(ruta, 'wb') as file:
            file.write(filedes)
        return ruta

def getinf(urlx,domi):
    info = {}
    sesion = clf2.solve(f'https://{domi}.sogirl.so/wp-json/')['session']
    soup = Soup(downloader.read_html(urlx,session=sesion))
    info['filename'] = clean_title(soup.find('meta', {'property': 'og:title'})['content'].strip())
    urlthumb = soup.find('meta', {'property': 'og:image'})['content']
    info['thumb'] = BytesIO()
    downloader.download(urlthumb, buffer=info['thumb'], session=sesion)
    info['iframe'] = soup.find('iframe')['data-lazy-src']
    return info

def getm3u8(iframe,sesionx,ruta,cw,domi):
    arstri = []
    #print_ = get_print(cw)
    sop = sesionx.get(iframe,headers={'Referer': f'https://{domi}.sogirl.so/'}).text
    un = sop.find('loadUrl("')+9
    urb = sop[un:sop.find('"',un)]
    un = sop.find('.loadSource(',un)+13
    playlis = sop[un:sop.find(')',un)-1]
    arstri.append(playlis[playlis.find('&')+8:])
    urv = urb[:urb.rfind('/')]
    arstri.append(urv[urv.rfind('/')+1:])
    mdd5 = md5(f'{arstri[0]}_{arstri[1]}_0_true_0'.encode('utf8')).hexdigest()
    arstri.append(urv)
    pingg= urv+'/ping?hash='+mdd5+'&time=0&paused=true&resolution=0'
    sesionx.get(pingg,headers={'Referer': 'https://iframe.mediadelivery.net/'})
    sesionx.get(urv+'/activate',headers={'Referer': 'https://iframe.mediadelivery.net/'})
    mdd5 = md5(f'{arstri[0]}_{arstri[1]}_0_true_720'.encode('utf8')).hexdigest()
    pingg= urv+'/ping?hash='+mdd5+'&time=0&paused=true&resolution=720'
    lista = sesionx.get(playlis,headers={'Referer': iframe}).text
    linkm3u8 = playlis[:playlis.find('playlist')]+lista.split()[-1]
    resm3u8 = sesionx.get(linkm3u8,headers={'Referer': 'https://iframe.mediadelivery.net/'}).text
    nkey = True
    inf = False
    archunk = []
    pos = 0
    cifralis = []
    pinx=[0,pingg]
    tup = None
    for linea in resm3u8.split():
        if inf:
            archunk.append(Video(linea,sesionx,cw,pos,cifralis,pinx,tup).url)
            pos+=1
            inf=False
        elif '#EXTI' in linea:
            inf = True
        elif nkey and '#EXT-X-K' in linea:
            un = linea.find('URI')+5
            arstri.append(linea[un:linea.find('"',un)-1])
            un = linea.find('IV=')+5
            arstri.append(bytes.fromhex(linea[un:]))
            arstri.append(ruta)
            tup=tuple(arstri)
            nkey=False
    return archunk
