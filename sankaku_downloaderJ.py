#coding: utf-8
#title_en: Sankaku Complex
#comment: https://[chan|idol|www].sankakucomplex.com/
#https://beta.sankakucomplex.com/
#https://sankaku.app/
#http://white.sankakucomplex.com/
import os
from utils import Downloader, LazyUrl, Soup, clean_title, clean_url, Session
from translator import tr_
from timee import sleep
from urllib.parse import unquote
import requests

class Downloader_sankaku(Downloader):
    type = 'sankaku'
    URLS = ['chan.sankakucomplex.com', 'idol.sankakucomplex.com', 'www.sankakucomplex.com']
    MAX_CORE = 4
    MAX_PARALLEL = 1
    display_name = 'Sankaku Complex'
    ACCEPT_COOKIES = [r'(.*\.)?(sankakucomplex\.com|sankaku\.app)']

    def init(self):
        tipe = self.url.split('sankakucomplex.com')[0].split('//')[-1].strip('.').split('.')[-1]
        if tipe == '':
            tipe = 'www'
        if tipe not in ['chan', 'idol', 'www']:
            raise Exception('Not supported subdomain')
        self.type_sankaku = tipe
        self.url = self.url.replace('&commit=Search', '')
        self.url = clean_url(self.url)

    def read(self):
        if self.type_sankaku == 'www':
            info = get_imgs_www(self.url)#, self.session)
        else:
            info = get_imgs(self.url, self.type_sankaku, self.cw)
            self.single = info['single']
        self.urls = info['selfurls']
        self.title = info['title']

def get_imgs_www(url):
    html = requests.get(url).text
    soup = Soup(html)
    info = {}
    info['title'] = clean_title('[www]' + soup.find('h1', class_='entry-title').text.strip())
    imgs = []
    view = soup.find(class_='entry-content')
    viewp = view.find('video')
    if viewp:
        imgs.append(viewp.find('a').attrs.get('href'))
    for img in view.findAll('a'):
        if not img.find('img'):
            continue
        imgx = img.attrs.get('href')
        if not 'https:' in imgx:
            imgx = 'https:'+imgx
        #imgx = urljoin(url, imgx)
        if not imgx in imgs:
            imgs.append(imgx)
    info['selfurls'] = imgs
    return info

def get_imgs(url, tipe, cw):
    info = {}
    info['single'] = '/posts/' in url
    cuki = getcuki(tipe)
    if info['single']:
        response = requests.get(f'https://{tipe}.sankakucomplex.com/posts.json?'+url+nex, allow_redirects=False, cookies=cuki)
        if response.status_code==200:
            jo = response.json()[0]
            idx=jo['id']
            arxids.append(idx, 'https:'+jo['file_url'])
            #sincro[0]=len(arxids)
        else:
            raise Exception ('charge cookies')
        info['imgs'] = [Image(1, f'https://{tipe}.sankakucomplex.com/posts.json?'+url, local_ids, arxids,cuki,sincro).url]
        info['title'] = f'[{tipe}]{idx}'
        return info
    url = url[url.find('?')+1:]
    arxids = []
    nex = ''
    tags = []
    pri = ''
    prix = ''
    for ii in url.split('&'):
        if 'next=' in ii:
            nex = '&'+ii
        elif not 'page=' in ii:
            if 'tags=' in ii:
                ii = ii[ii.find('tags=')+5:].replace(' ','%20').replace('+','%20')
                for jj in ii.split('%20'):
                    if 'id_range%3A' in jj or 'id_range:' in jj:
                        prix = '%20'+jj
                        iia = unquote(jj)[9:]
                        if '>' in iia:
                            if '=' in iia:
                                pri = iia[2:]
                            else:
                                pri = iia[1:]
                                pri = str(int(pri)+1)
                        elif '.' == iia[-1]:
                            pri = iia[:-2]
                        elif not '.' == iia[0] and '..' in iia:
                            pri = iia[:iia.find('..')]
                    tags.append(jj)
            else:
                arxids.append(ii)
    arxids.append('%20'.join(tags))
    url ='&'.join(arxids)
    title = url.replace('%20',' ')
    while '  ' in title:
        title = title.replace('  ', ' ')
    title = unquote(title)
    if not title:
        title = 'N/A'
    title = clean_title(f'[{tipe}]{title}')+nex
    cw.downloader.title = title
    dirx = cw.downloader.dir
    try:
        names = os.listdir(dirx)
    except Exception as e:
        print(e)
        names = []
    local_ids = {}
    for name in names:
        id = os.path.splitext(name)[0]
        local_ids[id] = os.path.join(dirx, name)
    cw.setTitle('{}  {}'.format(tr_('읽는 중...'), title))
    arxids = []
    sincro = [0,False]
    response = requests.get(f'https://{tipe}.sankakucomplex.com/posts.json?tags='+url+prix, allow_redirects=False, cookies=cuki)
    if response.status_code==200:
        if 'Content-Length' in response.headers:
            raise Exception ('Empty urls')
        for jo in response.json():
            idz = jo['id']
            idx=str(idz)
            url_img = local_ids[idx] if idx in local_ids else 'https:'+(jo['file_url'] or jo['sample_url'])
            arxids.append((idz, url_img))
        sincro[0]=len(arxids)
    else:
        raise Exception ('Charge cookies')
    info['selfurls'] = [Image(iii, f'https://{tipe}.sankakucomplex.com/posts.json?tags='+url+f'%20id_range%3A{pri}..', local_ids, arxids,cuki,sincro).url for iii in range(4000)]
    info['title'] = title
    return info

def getcuki(tipe):
    dom, nam = ('.chan.sankakucomplex.com','_sankakuchannel_session') if tipe == 'chan' else ('.idol.sankakucomplex.com','_idolcomplex_session')
    for cookie in Session().cookies:
        if dom == cookie.domain and cookie.name == nam :
            return {cookie.name: cookie.value}

class Image:
    def __init__(self, pos, referxr, arlocal,arid,coki,sincrx):
        self.pos = pos
        self.referxr = referxr
        self.arlocal = arlocal
        self.arid = arid
        self.coki=coki
        self.sincro = sincrx
        #self.url = LazyUrl(f'https://chan.sankakucomplex.com/es/posts/{pos}', self.get, self)
        self.url = LazyUrl(None, self.get, self)

    def get(self, _):
        pox = self.pos
        while not self.sincro[0] > pox:
            if self.sincro[1]:
                self.filename = 'N'
                return
            sleep(0.001)
        arix = self.arid
        idz = arix[pox][0]
        if idz == arix[-1][0]:
            urx = f'{self.referxr}{idz-1}'
            json(urx,self.arlocal,arix,self.coki,self.sincro)
        ext = os.path.splitext(arix[pox][1])[1].split('?')[0]
        self.filename = f'{idz}{ext}'
        return arix[pox][1]

def json(url,arraylocal,arrayid,cuki,sincro):
    response = requests.get(url, allow_redirects=False, cookies=cuki)
    if response.status_code==200:
        sincro[1]='Content-Length' in response.headers
        for jo in response.json():
            idz = jo['id']
            idx = str(idz)
            url_img = arraylocal[idx] if idx in arraylocal else 'https:'+(jo['file_url'] or jo['sample_url'])
            arrayid.append((idz,url_img))
        sincro[0]=len(arrayid)
    else:
        sincro[1]=True
