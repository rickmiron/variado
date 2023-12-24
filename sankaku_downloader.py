#coding: utf-8
#title_en: Sankaku Complex
#comment: https://[chan|idol|www].sankakucomplex.com/
#https://beta.sankakucomplex.com/
#https://sankaku.app/
#http://white.sankakucomplex.com/
import downloader
import os
from utils import Downloader, LazyUrl, urljoin, get_print, Soup, Session, clean_title, check_alive
from translator import tr_
from timee import sleep
from error_printer import print_error
from constants import clean_url
from ratelimit import limits, sleep_and_retry
from urllib.parse import unquote
import errors

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
        self.session = Session()

    def read(self):
        if self.type_sankaku == 'www':
            info = get_imgs_www(self.url, self.session)
        else:
            info = get_imgs(self.url, self.type_sankaku, self.cw, session=self.session)
            self.single = info['single']
        self.urls = info['imgs']
        self.title = info['title']

def get_imgs_www(url, session):
    html = downloader.read_html(url, session=session)
    soup = Soup(html)
    info = {}
    info['title'] = '[www]' + soup.find('h1', class_='entry-title').text.strip()
    imgs = []
    view = soup.find(class_='entry-content')
    viewp = view.find('video')
    if viewp:
        imgs.append(viewp.find('a').attrs.get('href'))
    for img in view.findAll('a'):
        if not img.find('img'):
            continue
        imgx = img.attrs.get('href')
        imgx = urljoin(url, imgx)
        if imgx in imgs:
            continue
        imgs.append(imgx)
    info['imgs'] = imgs
    return info

@LazyUrl.register
class LazyUrl_sankaku(LazyUrl):
    type = 'sankaku'
    def dump(self):
        return {
            'id': self.image.id,
            'url': self._url,
            'referer': self.image.referer,
            'local': self.image.local,
            'cw': self.CW,
            'session': self.SESSION,
            }
    @classmethod
    def load(cls, data):
        img = Image(data['id'], data['url'], data['referer'], data['local'], data['cw'], data['session'])
        return img.url

class Image:
    filename = None
    def __init__(self, id, url, referer, local=False, cw=None,session=None):
        self.id = id
        self.referer = referer
        self.cw = cw
        self.local = local
        self.session = session
        if local:
            self.url = url
            self.filename = os.path.basename(url)
        else:
            self.url = LazyUrl_sankaku(url, self.get, self)

    def get(self, url):
        cw = self.cw
        print_ = get_print(cw)

        for try_ in range(2):
            wait(cw)
            html = ''
            try:
                html = downloader.read_html(url, referer=self.referer, session=self.session)
                soup = Soup(html)
                highres = soup.find(id='highres')
                url = 'https:' + (highres['href'] if highres else soup.find('meta', {'property': 'og:image'}).attrs['content'])
                break
            except Exception as e:
                e_msg = print_error(e)
                if '429 Too many requests' in html:
                    t_sleep = 120 * min(try_ + 1, 2)
                    e = f'429 Too many requests... wait {t_sleep} secs'
                elif 'post-content-notification' in html: # sankaku plus
                    print_(f'Sankaku plus: {self.id}')
                    return ''
                else:
                    t_sleep = 5
                print_(f'[Sankaku] failed to read image (id:{self.id}): {e}')
                sleep(t_sleep, cw)
        else:
            raise Exception('can not find image (id:{})\n{}'.format(self.id, e_msg))
        soup = Soup(f'<p>{url}</p>')
        url = soup.string
        ext = os.path.splitext(url)[1].split('?')[0]
        self.filename = f'{self.id}{ext}'
        return url

@sleep_and_retry
@limits(1, 3)
def wait(cw):
    check_alive(cw)

def get_imgs(url, tipe, cw, session=None):
    print_ = get_print(cw)
    info = {}
    if '/posts/' in url:
        info['single'] = True
        html = downloader.read_html(url, session=session)
        soup = Soup(html)
        idx = soup.find(id ='post_id').attrs['value']
        info['imgs'] = [Image(idx, url, url, cw=cw).url]
        info['title'] = f'[{tipe}]{idx}'
        return info
    info['single'] = False
    imgs = []
    url_old = f'https://{tipe}.sankakucomplex.com'
    title = url.split('?tags=')[1].split('&')[0].replace('%20',' ').replace('+',' ')
    while '  ' in title:
        title = title.replace('  ', ' ')
    title = unquote(title)
    if not title:
        title = 'N/A'
    title = clean_title(f'[{tipe}]{title}')
    cw.downloader.title = title
    dir = cw.downloader.dir
    try:
        names = os.listdir(dir)
    except Exception as e:
        print(e)
        names = []
    local_ids = {}
    for name in names:
        id = os.path.splitext(name)[0]
        local_ids[id] = os.path.join(dir, name)
    cw.setTitle('{}  {}'.format(tr_('읽는 중...'), title))
    url_imgs = set()
    while True:
        wait(cw)
        print_(url)
        try:
            html = downloader.read_html(url, referer=url_old, session=session)
        except Exception as e: #3366
            print_(print_error(e))
            break
        if '429 Too many requests'.lower() in html.lower():
            print_('429 Too many requests... wait 120 secs')
            sleep(120, cw)
            continue
        soup = Soup(html)
        err = soup.find('div', class_='post-premium-browsing_error')
        if err:
            if not imgs:
                raise errors.LoginRequired(err.text.strip())
            break
        for span in soup.find(class_='content').findAll('div', recursive=False)[1].findAll('span', recursive=False):
            idx = span.attrs['data-id']
            if idx is None: # sankaku plus
                continue
            url_img = f'https://{tipe}.sankakucomplex.com/posts/{idx}'
            localx = idx in local_ids
            if url_img not in url_imgs:
                url_imgs.add(url_img)
                if localx:
                    url_img = local_ids[idx]
                imgs.append(Image(idx, url_img, url, local=localx, cw=cw).url)
        try:
            url_old = url
            nexurl = soup.find('div', class_='pagination').attrs.get('next-page-url')
            if nexurl:
                nexurl = nexurl[:nexurl.rfind('&')].replace('&amp;','&')
                url = f'https://{tipe}.sankakucomplex.com{nexurl}'
            else:
                break
        except Exception as e:
            print_(print_error(e))
            break
        cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, len(imgs)))
    if not imgs:
        raise Exception('no images')
    info['imgs'] = imgs
    info['title'] = title
    return info
