#coding: utf-8
#title_en: Sankaku Complex
#comment: https://[chan|idol|www].sankakucomplex.com/
#https://beta.sankakucomplex.com/
#https://sankaku.app/
#http://white.sankakucomplex.com/
import downloader
import os
from utils import Downloader,LazyUrl,urljoin,get_print,Soup,clean_title,check_alive,Session,get_max_range
from translator import tr_
from timee import sleep
from error_printer import print_error
from constants import clean_url
from ratelimit import limits,sleep_and_retry
from urllib.parse import unquote
import errors

class Downloader_sankaku(Downloader):
    type='sankaku'
    URLS=['chan.sankakucomplex.com','idol.sankakucomplex.com','www.sankakucomplex.com']
    MAX_CORE=4
    MAX_PARALLEL=1
    display_name='Sankaku Complex'
    ACCEPT_COOKIES=[r'(.*\.)?(sankakucomplex\.com|sankaku\.app)']

    def init(self):
        tipe=self.url.split('sankakucomplex.com')[0].split('//')[-1].strip('.').split('.')[-1]
        if tipe=='':
            tipe='www'
        if tipe not in ['chan','idol','www']:
            raise Exception('Not supported subdomain')
        self.type_sankaku=tipe
        self.url=self.url.replace('&commit=Search','')
        self.url=clean_url(self.url)
        self.session=Session()

    def read(self):
        if self.type_sankaku=='www':
            info=get_imgs_www(self.url,self.session)
        else:
            info=get_imgs(self.url,self.type_sankaku,self.cw,self.session)
            self.single=info['single']
        self.urls=info['imgs']
        self.title=info['title']

def get_imgs_www(url,sesion):
    soup=Soup(downloader.read_html(url,session=sesion))
    info={}
    info['title']='[www]'+soup.find('h1',class_='entry-title').text.strip()
    imgs=[]
    view=soup.find(class_='entry-content')
    viewp=view.find('video')
    if viewp:
        imgs.append(viewp.find('a').attrs.get('href'))
    for a in view.findAll('a'):
        if not a.find('img'):
            continue
        imgx=urljoin(url,a.attrs.get('href'))
        if imgx in imgs:
            continue
        imgs.append(imgx)
    info['imgs']=imgs
    return info

class Image:
    def __init__(self,idx,url,ref,local=False,cw=None,session=None):
        self.id=idx
        self.referer=ref
        self.cw=cw
        self.session=session
        if local:
            self.url=url
            self.filename=os.path.basename(url)
        else:
            self.url=LazyUrl('',self.get,self)
            self.urx=url

    def get(self,_):
        cw=self.cw
        print_=get_print(cw)
        url=self.urx
        for try_ in range(2):
            wait(cw)
            html=''
            try:
                html=downloader.read_html(url,referer=self.referer,session=self.session)
                soup=Soup(html)
                highres=soup.find(id='highres')
                url='https:'+(highres['href'] if highres else soup.find('meta',{'property':'og:image'}).attrs['content'])
                break
            except Exception as e:
                e_msg=print_error(e)
                if '429 Too many requests' in html or 'equest limit exceeded' in html:
                    t_sleep=120*min(try_+1,2)
                    e=f'429 Too many requests... wait {t_sleep} secs'
                elif 'post-content-notification' in html:
                    print_(f'Sankaku plus: {self.id}')
                    return ''
                else:
                    t_sleep = 5
                print_(f'[Sankaku] failed to read image (id:{self.id}): {e}')
                sleep(t_sleep,cw)
        else:
            raise Exception(f'can not find image (id:{self.id})\n{e_msg}')
        soup=Soup(f'<p>{url}</p>')
        url=soup.string
        ext=os.path.splitext(url)[1].split('?')[0]
        self.filename=f'{self.id}{ext}'
        return url

@sleep_and_retry
@limits(1, 3)
def wait(cw):
    check_alive(cw)

def get_imgs(url,tipe,cw,sesion):
    print_=get_print(cw)
    info={}
    info['single']='/posts/' in url
    if info['single']:
        soup=Soup(downloader.read_html(url,session=sesion))
        idx=soup.find(id='post_id').attrs['value']
        info['imgs']=[Image(idx,url,url,cw=cw).url]
        info['title']=f'[{tipe}]{idx}'
        return info
    imgs=[]
    url_old=f'https://{tipe}.sankakucomplex.com'
    title=url.split('?tags=')[1].split('&')[0].replace('%20',' ').replace('+',' ')
    while '  ' in title:
        title=title.replace('  ', ' ')
    title=unquote(title)
    if not title:
        title='N/A'
    title=clean_title(f'[{tipe}]{title}')
    cw.downloader.title=title
    dir=cw.downloader.dir
    try:
        names=os.listdir(dir)
    except Exception as e:
        names=[]
    local_ids={}
    for name in names:
        id=os.path.splitext(name)[0]
        local_ids[id]=os.path.join(dir,name)
    cw.setTitle(f'{tr_("읽는 중...")} {title}')
    url_imgs=set()
    max_pid=get_max_range(cw)
    while len(imgs)<max_pid:
        wait(cw)
        print_(url)
        try:
            html=downloader.read_html(url, referer=url_old, session=sesion)
        except Exception as e:
            print_(e)
            break
        if '429 Too many requests' in html or 'equest limit exceeded' in html:
            print_('429 Too many requests... wait 120 secs')
            sleep(120,cw)
            continue
        soup=Soup(html)
        err=soup.find('div',class_='post-premium-browsing_error')
        if err:
            if not imgs:
                raise errors.LoginRequired(err.text.strip())
            break
        for span in soup.find(class_='content').findAll('div',recursive=False)[1].findAll('article'):
            idx=span.attrs['data-id']
            url_img=f'https://{tipe}.sankakucomplex.com/posts/{idx}'
            localx=idx in local_ids
            if url_img not in url_imgs:
                url_imgs.add(url_img)
                if localx:
                    url_img=local_ids[idx]
                imgs.append(Image(idx,url_img,url,local=localx,cw=cw).url)
        try:
            url_old=url
            nexurl=soup.find('div',class_='pagination').attrs.get('next-page-url')
            if not nexurl:
                break
            nexurl=nexurl[:nexurl.find('&')]+nexurl[nexurl.rfind('&'):].replace('amp;','').replace('%25','%')
            url=f'https://{tipe}.sankakucomplex.com{nexurl}'
        except Exception as e:
            print_(e)
            break
        cw.setTitle(f'{tr_("읽는 중...")} {title} - {len(imgs)}')
    if not imgs:
        raise Exception('no images')
    info['imgs']=imgs
    info['title']=title
    return info
