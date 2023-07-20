#coding: utf-8
#title_en: Allthefallen Moe
#https://booru.allthefallen.moe/
import downloader
import ree as re
import os
from utils import Downloader, LazyUrl, urljoin, query_url, get_max_range, get_print, Soup, lazy, Session, clean_title, check_alive
from translator import tr_
from timee import sleep
import constants
from error_printer import print_error
from constants import clean_url
from ratelimit import limits, sleep_and_retry
import errors

@Downloader.register
class Downloader_allthefallen(Downloader):
    type = 'allthefallen'
    URLS = ['booru.allthefallen.moe']
    icon = 'base64:AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAXoCkAF+ApABegaQAX4GkAF+BpQBfgqYAYIKmAGGEpwBihagAY4apAGOHqgBliKwAZYmsAGaJrQBmiq0AZ4quAGiLrwBojLEAao6yAGuPswBsj7UAbJC1AG2QtQBskbUAbZK3AG+TuABwk7kAb5S4AHCUuQBwlLoAcZS6AHCVugBxlboAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQDAwMDAgIEBAAAAAAAAAAEAwMEAQQDAwQABAAAAAAABAQEAwMCBAQEAAQDAAAAAAMDAwQDAwQDAwAEAQAAAAALCwoJCAYEAgQABwUAAAAAFBUUExIREA4MAA8NAAAAACAgHiAgHRoZFwAYFgAAAAAgICAgIR8fHiAAISEAAAAAIB4gISEgISAeAB4eAAAAAAAAAAAAAAAAAAAeIAAAAAAAICAcICAgICAgACAAAAAAAAAgIB4gIR8bICAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP//AACADwAAgAcAAIADAACAAQAAgAEAAIABAACAAQAAgAEAAIABAACAAQAAgAEAAMABAADgAQAA8AEAAP//AAA='
    display_name = 'Allthefallen Moe'
    MAX_CORE = 4
    ACCEPT_COOKIES = [r'(.*\.)?(allthefallen\.moe)']

    def init(self):
        self.type_prefijo = 'moe'
        borr = self.url.rfind('&',37)
        if borr == -1:
            borr = None
        self.url = self.url[:borr]
        self.url = clean_url(self.url)
        self.session = Session()

        #if self.type_prefijo == 'www':
        #html = downloader.read_html(self.url, session=self.session)
        #self.soup = Soup(html)

    @classmethod
    def fix_url(cls, url):
        return url.replace('http://', 'https://')

    @lazy
    def id(self):
        if '.moe/posts/' in self.url:
            id = get_id(self.url)
        else:
            qs = query_url(self.url)
            tags = qs.get('tags', [])
            tags.sort()
            id = ' '.join(tags)
            if not id:
                id = 'N/A'
        id = '[{}] {}'.format(self.type_prefijo, id)
        return clean_title(id)

    @property
    def name(self):
        return self.id

    def read(self):
        ui_setting = self.ui_setting
        self.title = self.name

        types = ['img', 'gif', 'video']
        if ui_setting.exFile.isChecked():
            if ui_setting.exFileImg.isChecked():
                types.remove('img')
            if ui_setting.exFileGif.isChecked():
                types.remove('gif')
            if ui_setting.exFileVideo.isChecked():
                types.remove('video')

        info = get_imgs(self.url, self.name, cw=self.cw, d=self, types=types, session=self.session)
        self.single = info['single']
        imgs = info['imgs']

        for img in imgs:
            if isinstance(img, str):
                self.urls.append(img)
            else:
                self.urls.append(img.url)

        self.title = self.name

@LazyUrl.register
class LazyUrl_allthefallen(LazyUrl):
    type = 'allthefallen'
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
            self.url = LazyUrl_allthefallen(url, self.get, self)

    def get(self, url):
        cw = self.cw
        #d = self.d
        print_ = get_print(cw)

        for try_ in range(4):
            wait(cw)
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
                    t_sleep = 120 * min(try_ + 1, 2)
                    e = '429 Too many requests... wait {} secs'.format(t_sleep)
                else:
                    t_sleep = 5
                s = 'Allthefallen Moe failed to read image (id:{}): {}'.format(self.id, e)
                print_(s)
                sleep(t_sleep, cw)
        else:
            raise Exception('can not find image (id:{})\n{}'.format(self.id, e_msg))
        soup = Soup('<p>{}</p>'.format(url))
        url = soup.string
        ext = os.path.splitext(url)[1].split('?')[0]
        self.filename = '{}{}'.format(self.id, ext)
        return url

def setPage(url, page):
    # Always use HTTPS
    url = url.replace('http://', 'https://')
    # Change the page
    if 'page=' in url:
        url = re.sub(r'page=[0-9]*', 'page={}'.format(page), url)
    else:
        url += '&page={}'.format(page)
    return url

@sleep_and_retry
@limits(1, 3)
def wait(cw):
    check_alive(cw)

def get_imgs(url, title=None, cw=None, d=None, types=['img', 'gif', 'video'], session=None):
    print_ = get_print(cw)
    print_('types: {}'.format(', '.join(types)))
    type = 'moe'
    info = {}
    info['single'] = False
    if '.moe/posts/' in url:
        info['single'] = True
        id = get_id(url)
        info['imgs'] = [Image(type, id, url, None, cw=cw, d=d)]
        return info
    # Range
    max_pid = get_max_range(cw)
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

    imgs = []
    page = 1
    url_imgs = set()
    url_old = 'https://booru.allthefallen.moe'
    if cw is not None:
        cw.setTitle('{}  {}'.format(tr_('읽는 중...'), title))
    while len(imgs) < max_pid:
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
        page += 1
        url_old = url
        soup = Soup(html)
        err = soup.find('div', class_='post-premium-browsing_error')
        if err:
            if not imgs:
                raise errors.LoginRequired(err.text.strip())
            break
        articles = soup.findAll('article')
        for article in articles:
            tags = article.attrs['data-tags'].split()
            if 'animated_gif' in tags:
                type_ = 'gif'
            elif 'animated' in tags or 'webm' in tags or 'video' in tags or 'mp4' in tags: # 1697
                type_ = 'video'
            else:
                type_ = 'img'
            if type_ not in types:
                continue

            id = article.attrs['data-id']
            url_img = 'https://booru.allthefallen.moe/posts/' + id
            if id is None:
                continue
            if id in local_ids:
                local = True
            else:
                local = False
            #print(url_img)
            if url_img not in url_imgs:
                url_imgs.add(url_img)
                if local:
                    url_img = local_ids[id]
                img = Image(type, id, url_img, url, local=local, cw=cw, d=d)
                imgs.append(img)
                if len(imgs) >= max_pid:
                    break

        try:
            # For page > 50
            pagination = soup.find('a', class_='paginator-next')
            url = urljoin('https://booru.allthefallen.moe', pagination.attrs['href'])
        except Exception as e:
            print_(print_error(e))
            #url = setPage(url, page)
            break

        if cw is not None:
            cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, len(imgs)))
        else:
            print(len(imgs), 'imgs')

    if not imgs:
        raise Exception('no images')
    info['imgs'] = imgs
    return info

def get_id(url_img):
    fina = url_img.find('?',37)
    if fina == -1:
        fina = None
    return url_img[url_img.find('/',36) + 1:fina]
