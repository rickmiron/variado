#coding: utf-8
#title_en: 3hentai
#https://3hentai.net/
import downloader
import time
import os
import requests
from utils import Downloader, LazyUrl, get_print, Soup, lazy, Session, clean_title
from timee import sleep
from translator import tr_


@Downloader.register
class Downloader_3hentai(Downloader):
    type = '3hentai'
    URLS = ['3hentai.net']
    icon = 'base64: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'
    display_name = '3hentai'
    MAX_CORE = 4
    ACCEPT_COOKIES = [r'(.*\.)?(3hentai\.net)']

    def init(self):
        self.type_id = self.url[self.url.find('d/') + 2:]
        bo = self.type_id.find('/')
        if bo != -1:
            self.type_id = self.type_id[:bo]
        self.session = Session()
        html = downloader.read_html('https://3hentai.net/d/' + self.type_id + '/', session=self.session)
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
        self.title = self.name
        imgs = get_imgs_www(self.url, self.soup, self.name, cw=self.cw, d=self)
        for img in imgs:
            self.urls.append(img.url)
        self.title = self.name

def get_imgs_www(url, soup, title=None, cw=None, d=None):
    imgs = []
    leng = soup.find('div', class_='single-thumb').find('img').attrs['data-src']
    prefim = leng[:leng.rfind('/')+1]
    #leng = soup.find('li', class_='pages').text.strip()
    leng = len(soup.findAll('div', class_='single-thumb'))

    local_ids = {}
    if cw is not None:
        dir = cw.downloader.dir
        try:
            names = os.listdir(dir)
        except Exception as e:
            print(e)
            names = []
        for name in names:
            id = os.path.splitext(name)[0]
            local_ids[id] = os.path.join(dir, name)

    url_imgs = set()
    type = 0
    if cw is not None:
        cw.setTitle('{}  {}'.format(tr_('읽는 중...'), title))
    for id in range(1, leng):
        time.sleep(0.02)
        url_img = prefim + str(id)
        if id % 25 == 0:
            if cw is not None:
                cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, id))
            else:
                print(len(imgs), 'imgs')

        if id in local_ids:
            local = True
        else:
            local = False
        if url_img not in url_imgs:
            info = Image(type , id, url_img, url, local=local, cw=cw, d=d)
            type = info.type
            url_imgs.add(info.url)
            if local:
                url_img = local_ids[id]
            imgs.append(info)
    return imgs

@LazyUrl.register
class LazyUrl_3hentai(LazyUrl):
    type = '3hentai'
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
            self.url = LazyUrl_3hentai(url, self.get, self)

    def get(self, url):
        EXTEN = ['.jpg','.png','.gif']
        cw = self.cw
        print_ = get_print(cw)
        try:
            for _ in range(3):
                response = requests.head(url + EXTEN[self.type])
                if response.status_code != 403:
                    url = url + EXTEN[self.type]
                    break
                if self.type < 2:
                    self.type += 1
                    continue
                self.type = 0
            else:
                url = ''
        except Exception as e:
            s = '3hentai failed to read image (id:{}): {}'.format(self.id, e)
            print_(s)
            sleep(1, cw)
        soup = Soup('<p>{}</p>'.format(url))
        url = soup.string
        ext = os.path.splitext(url)[1].split('?')[0]
        self.filename = '{}{}'.format(self.id, ext)
        return url