#coding: utf8
#title: SoGirl
#comment: https://krXX.sogirl.so/

import downloader
from utils import Downloader, LazyUrl,Soup,clean_title,get_resolution
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
REFER={'Referer': 'https://iframe.mediadelivery.net/'}

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
            if '//iframe' in infof['iframe']:
                if not os.path.exists(diir):
                    os.makedirs(diir)
                self.urls = getm3u8(infof['iframe'],sesion, diir,self.cw,domi)
            else:
                self.single = True
                self.enableSegment(chunk=2**20,n_threads=4)
                self.referer = f'https://{domi}.sogirl.so/'
                self.urls.append(getmp4(infof['iframe'],domi))
                self.filenames[self.urls[0]]=self.title+'.mp4'

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
                self.session.get(self.pinx[1],headers=REFER)
                clave = self.session.get(self.arstr[3]+str(ind),headers=REFER)
                while len(self.cifralis) != ind:
                    sleep(0.01)
                self.cifralis.append(Cipher(algorithms.AES(clave.content), modes.CBC(self.arstr[4]), backend=default_backend()))
                break
            else:
                sleep(0.01)
        descri = self.cifralis[ind].decryptor()
        pvid = self.session.get(urlx,headers=REFER)
        filedes = descri.update(pvid.content) + descri.finalize()
        ruta=self.arstr[5]+'/'+self.filename
        with open(ruta, 'wb') as file:
            file.write(filedes)
        return ruta

def getmp4(urlx,domi):
    he = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
    da = {'action': 'fv_fp_get_video_url', 'sources[0][src]': urlx,'sources[0][type]':'video/mp4'}
    dato = requests.post(f'https://{domi}.sogirl.so/wp-admin/admin-ajax.php',headers=he,data=da)
    texto=dato.text
    un=texto.find('https:')
    return texto[un:texto.find('"',un)].replace('\/','/')

def getinf(urlx,domi):
    info = {}
    sesion = clf2.solve(f'https://{domi}.sogirl.so/wp-json/')['session']
    soup = Soup(downloader.read_html(urlx,session=sesion))
    info['filename'] = clean_title(soup.find('meta', {'property': 'og:title'})['content'].strip())
    thumb = soup.find('meta', {'property': 'og:image'})['content']
    info['thumb'] = BytesIO()
    downloader.download(thumb, buffer=info['thumb'], session=sesion)
    thumb = soup.find('iframe')['data-lazy-src']
    if '//iframe' in thumb:
        info['iframe'] = thumb
    else:
        for a in soup.find(class_='fp-playlist-external').findAll('a'):
            if '#' == a['href']:
                daem=a['data-item']
                un=daem.find('https:')
                info['iframe']=daem[un:daem.find('.mp4',un)+4].replace('\/','/')
                break
    return info

def getm3u8(iframe,sesionx,ruta,cw,domi):
    arstri = []
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
    sesionx.get(pingg,headers=REFER)
    sesionx.get(urv+'/activate',headers=REFER)
    mdd5 = md5(f'{arstri[0]}_{arstri[1]}_0_true_720'.encode('utf8')).hexdigest()
    pingg= urv+'/ping?hash='+mdd5+'&time=0&paused=true&resolution=720'
    lista = sesionx.get(playlis,headers={'Referer': iframe}).text
    reso = get_resolution()
    for tex in lista.split()[::-1]:
        if '#' not in tex:
            lista = tex
        else:
            un = tex.find('x',tex.find('RESOL'))+1
            dos = tex.find(',',un)
            if not int(tex[un: None if dos<0 else dos])>reso:
                break
    linkm3u8 = playlis[:playlis.find('playlist')]+lista
    resm3u8 = sesionx.get(linkm3u8,headers=REFER).text
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
