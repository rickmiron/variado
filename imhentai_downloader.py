#coding: utf-8
#title_en: Imhentai
#https://imhentai.xxx/
import downloader
import time
import os
import requests
from utils import Downloader, LazyUrl, get_print, Soup, lazy, Session, clean_title
from timee import sleep
from error_printer import print_error
from translator import tr_


@Downloader.register
class Downloader_imhentai(Downloader):
    type = 'imhentai'
    URLS = ['imhentai.xxx']
    icon = 'base64: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'
    display_name = 'Imhentai'
    MAX_CORE = 4
    ACCEPT_COOKIES = [r'(.*\.)?(imhentai\.xxx)']

    def init(self):
        self.type_id = self.url[self.url.find('y') + 2:]
        bo = self.type_id.find('/')
        if bo != -1:
            self.type_id = self.type_id[:bo]
        self.session = Session()
        html = downloader.read_html('https://imhentai.xxx/gallery/' + self.type_id + '/', session=self.session)
        self.soup = Soup(html)

    @classmethod
    def fix_url(cls, url):
        return url.replace('http://', 'https://')

    @lazy
    def id(self):
        return clean_title(self.soup.find('h1').text.strip() + '(' + self.type_id)

    @property
    def name(self):
        return self.id

    def read(self):
        imgs = get_imgs_www(self.soup, self.name, cw=self.cw)
        for img in imgs:
            if isinstance(img, str):
                self.urls.append(img)
            else:
                self.urls.append(img.url)
        self.title = self.name

def get_imgs_www(soup, title=None, cw=None):
    imgs = []
    leng = soup.find('div', class_='gallery_th').find('img').attrs['data-src']
    prefim = leng[:leng.rfind('/')+1]
    leng = soup.find('li', class_='pages').text.strip()
    leng = int(leng[7:]) + 1
    EXTEN = ['.jpg','.png','.gif']
    inex = 0
    if cw is not None:
        cw.setTitle('{}  {}'.format(tr_('읽는 중...'), title))
    for i in range(1, leng):
        time.sleep(0.001)
        pref = prefim + str(i)
        if cw is not None:
            cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, i))
        else:
            print(len(imgs), 'imgs')
        for _ in range(3):
            response = requests.head(pref + EXTEN[inex])
            if response.status_code != 404:
                imgs.append(pref + EXTEN[inex])
                break
            if inex < 2:
                inex += 1
                continue
            inex = 0
    """
    exts = '.jpg'
    for i in range(1, leng):
        pref = prefim + str(i)
        response = requests.head(pref + exts)
        if response.status_code != 404:
            imgs.append(pref + exts)
            continue
        for j in EXTEN:
            if j == exts:
                continue
            response = requests.head(pref + j)
            if response.status_code != 404:
                imgs.append(pref + j)
                exts = j
                break
    """
    return imgs

@LazyUrl.register
class LazyUrl_imhentai(LazyUrl):
    type = 'imhentai'
    def dump(self):
        return {
            'type': self.image.type,
            'id': self.image.id,
            'url': self._url,
            'referer': self.image.referer,
            'cw': self.CW,
            'd': self.DOWNLOADER,
            'local': self.image.local,
            'session': self.SESSION,
            }
    @classmethod
    def load(cls, data):
        img = Image(data['type'], data['id'], data['url'], data['referer'], data['local'], data['cw'], data['d'], data['session'])
        return img.url

class Image:
    filename = None
    def __init__(self, type, id, url, referer, local=False, cw=None, d=None, session=None):
        self.type = type
        self.id = id
        self.referer = referer
        self.cw = cw
        self.d = d
        self.local = local
        self.session = session
        if local:
            self.url = url
            self.filename = os.path.basename(url)
        else:
            self.url = LazyUrl_imhentai(url, self.get, self)

    def get(self, url):
        cw = self.cw
        print_ = get_print(cw)

        for try_ in range(1):
            
            html = ''
            try:
                html = downloader.read_html(url, referer=self.referer, session=self.session)
                soup = Soup(html)
                highres = soup.find(id='post-info-size').find('a').attrs['href']
                url = highres
                break
            except Exception as e:
                e_msg = print_error(e)
                if '429 Too many requests'.lower() in html.lower():
                    t_sleep = 0 * min(try_ + 0, 1)
                    e = '429 Too many requests... wait {} secs'.format(t_sleep)
                else:
                    t_sleep = 0
                s = 'IM hentai failed to read image (id:{}): {}'.format(self.id, e)
                print_(s)
                sleep(t_sleep, cw)
        else:
            raise Exception('can not find image (id:{})\n{}'.format(self.id, e_msg))
        soup = Soup('<p>{}</p>'.format(url))
        url = soup.string
        ext = os.path.splitext(url)[1].split('?')[0]
        self.filename = '{}{}'.format(self.id, ext)
        return url