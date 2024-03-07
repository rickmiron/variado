#coding: utf-8
#title_en: Allthefallen Moe
#comment: https://booru.allthefallen.moe/
import os
from utils import Downloader, LazyUrl, clean_title, get_print
from translator import tr_
from urllib.parse import unquote
import requests

@Downloader.register
class Downloader_allthefallen(Downloader):
    type = 'allthefallen'
    URLS = ['booru.allthefallen.moe']
    icon = 'base64:AAABAAEAEBAAAAEACABoBQAAFgAAACgAAAAQAAAAIAAAAAEACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAXoCkAF+ApABegaQAX4GkAF+BpQBfgqYAYIKmAGGEpwBihagAY4apAGOHqgBliKwAZYmsAGaJrQBmiq0AZ4quAGiLrwBojLEAao6yAGuPswBsj7UAbJC1AG2QtQBskbUAbZK3AG+TuABwk7kAb5S4AHCUuQBwlLoAcZS6AHCVugBxlboAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQDAwMDAgIEBAAAAAAAAAAEAwMEAQQDAwQABAAAAAAABAQEAwMCBAQEAAQDAAAAAAMDAwQDAwQDAwAEAQAAAAALCwoJCAYEAgQABwUAAAAAFBUUExIREA4MAA8NAAAAACAgHiAgHRoZFwAYFgAAAAAgICAgIR8fHiAAISEAAAAAIB4gISEgISAeAB4eAAAAAAAAAAAAAAAAAAAeIAAAAAAAICAcICAgICAgACAAAAAAAAAgIB4gIR8bICAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP//AACADwAAgAcAAIADAACAAQAAgAEAAIABAACAAQAAgAEAAIABAACAAQAAgAEAAMABAADgAQAA8AEAAP//AAA='
    display_name = 'Allthefallen Moe'
    MAX_CORE = 4
    MAX_PARALLEL = 1
    ACCEPT_COOKIES = [r'(.*\.)?(allthefallen\.moe)']

    def read(self):
        self.print_('v1.00')
        self.urls, self.single = get_imgs(self.url, self.cw)
        self.print_('fin')

def get_imgs(url, cw):
    print_=get_print(cw)
    arrurls = []
    single = '.moe/posts/' in url
    if single:
        un = url.find('?')
        if un != -1:
            url = url[:un]
        response = requests.get(url+'.json')
        if response.status_code==200:
            jo = response.json()
            idx = str(jo['id'])
            arrurls.append(Image(idx, jo['file_url']).url)
            cw.downloader.title = '[moe]'+idx
        return arrurls,single
    un=url.find('tags=')+5
    dos=url.find('&',un)
    if dos==-1:
        dos = None
    url = url[un:dos]
    title = url.replace('%20',' ').replace('+',' ')
    while '  ' in title:
        title = title.replace('  ', ' ')
    title = unquote(title).strip()
    if not title:
        title = 'N/A'
    title = clean_title(f'[moe]{title}')
    local_ids = {}
    cw.downloader.title = title
    dirx = cw.downloader.dir
    try:
        names = os.listdir(dirx)
    except Exception as e:
        names = []
    for name in names:
        idx = os.path.splitext(name)[0]
        local_ids[idx] = os.path.join(dirx, name)
    pos = 1
    while pos<31:
        try:
            response = requests.get(f'https://booru.allthefallen.moe/posts.json?page={pos}&limit=200&tags={url}+-status%3Abanned')
        except requests.exceptions.ConnectionError as e:
            print_("Error conexion:", e)
            raise
        except requests.exceptions.HTTPError as e:
            print_("Error HTTP:", e.response.status_code, e.response.reason)
            raise
        except requests.exceptions.RequestException as e:
            print_("Error:", e)
            raise
        if response.status_code!=200 or 'Content-Length' in response.headers:
            break
        pos+=1
        for jo in response.json():
            idx=str(jo['id'])
            url_img = local_ids[idx] if idx in local_ids else jo['file_url']
            arrurls.append(Image(idx, url_img).url)
        cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, len(arrurls)))
    cw.setTitle(title)
    return arrurls,single

class Image:
    def __init__(self, idx, urx):
        self.idx = idx
        self.urx = urx
        self.url = LazyUrl('', self.get, self)

    def get(self, _):
        self.filename = self.idx+os.path.splitext(self.urx)[1]
        return self.urx
