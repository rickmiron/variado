#coding: utf8
#title_en: Kemono.Su
#comment: https://kemono.su/

import downloader
from utils import Downloader, Soup, urljoin, get_ext, clean_title, get_print, print_error,LazyUrl
from translator import tr_
import os
KEM='https://kemono.su'

@Downloader.register
class Downloader_kemonosu(Downloader):
    type = 'kemono.party'
    URLS = ['kemono.party','kemono.su']
    icon = 'base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAABpUExURQAAAAAAAAAAAAAAAAAAAAgDAQUCAQoFAioUCDQZCgAAAGIvFBEIA0MgDQQCAA0GAhIIAz0eDItEHHo7GA8HA04lEKhSIrNXJJlKH91rLcBdJ89lKl4tE3E3F+lxL+ZwLyQRBwEAAP///x3CqNsAAAAVdFJOUwAoCRVAd66L77pR5p7WY8Xb+f72/e5VQwgAAAABYktHRCJdZVysAAAAB3RJTUUH6AQBEQoHApBGhAAAAcFJREFUOMt1U9uCqyAMRARRRBEsICgX//8nN2q39exp5wVjhsmFBFUYfUdNMKK0/u5vGEKk7cj7F69r/jKqzoCBO9s/RWqOBeUNJpdJBtdXcI6LXy6RWjIxSTnK6hTrw9odCVZ9sO4SGdt2M6oV8Ilp75ylp5QISwz6EKkG7cBgGNVsdnGdr+y4TlrZoISYdAaEuaPd4pT1wzO3wWddtN733Vifcsrr4myZUxDPcphLaylhKfv+MA4IOaW467SMpxvzEchF5xQMiDy2AJTkzZb76grBpnYNR/TkdTkoMazBxrJNQkCZFSESLl24RPZHeZyHJBijqpna6PMvw8f9CWDJpjmKb5TNL0C6lz9CR4wEP5Xt5vIN2+k3PiVnJOOQA2utv0nYI34JUKxVDRAQn5RxN4aPqhQN/jWqBp4NjyNVRi+3IN6vcMFFJRp2PCduGqGmQzPfI0XZMnx2qqY1laT3/xDWYaJEvKZx5Igud4mkR0rRe1ohUt2tb0aCWcJ/h5nPN4WZo/+AhfuVgEn4tC3V8MqzJ+gTRn1JJMe+LFJ3NcOf6/AJpD/amJ7T/glsM0Vtw/dtrabjqUf0HZyxP+v+AyXlNz7GmJY3AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI0LTA0LTAxVDE3OjEwOjA2KzAwOjAwVR9kVQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNC0wNC0wMVQxNzoxMDowNiswMDowMCRC3OkAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjQtMDQtMDFUMTc6MTA6MDcrMDA6MDDVIPaCAAAAAElFTkSuQmCC'
    display_name = 'Kemono.Su'
    MAX_PARALLEL = 1
    MAX_CORE = 4
    single=True

    def read(self):
        dix=self.dir
        self.single=False
        if '/post/' in self.url:
            self.title, self.urls, self.filenames= read_post(self.url, self.cw,dix)
            titu = self.filenames[self.urls[0]]
            self.cw.setTitle(titu[:titu.find('/')])
        else:
            self.title, self.urls, self.filenames= read_user(self.url, self.cw,dix)

def read_user(url, cw, dix):
    soup = Soup(downloader.read_html(url))
    galerias = []
    username = soup.find('meta', {'name': 'artist_name'})['content']
    titu  = clean_title(username)
    nga = 0
    elementos = soup.find('div', class_='card-list__items').findAll('a')
    for a in elementos:
        galerias.append(a.attrs['href'])
    Next = soup.find('a', class_='next')
    cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), titu, nga))
    while Next:
        href = Next.attrs['href']
        soup = Soup(downloader.read_html(KEM+href))
        elementos = soup.find('div', class_='card-list__items').findAll('a')
        for a in elementos:
            galerias.append(a.attrs['href'])
        Next = soup.find('a', class_='next')
    files = []
    namefiles = {}
    for gale in galerias:
        _, urls, filenames= read_post(KEM+gale, cw,dix)
        files += urls
        namefiles.update(filenames)
        nga += 1
        cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), titu, nga))
    return titu, files, namefiles

def read_post(url, cw,dix):
    print_ = get_print(cw)
    soup = Soup(downloader.read_html(url))
    title = soup.find('h1').text
    idp = soup.find('meta', {'name': 'id'})['content']
    usuar = clean_title(soup.find('a', class_='post__user-name').text.strip())
    info = clean_title(f'{idp}-{title}-{usuar}')
    imgs = []
    filenames = {}
    # Downloads
    for item in soup.findAll('li', class_='post__attachment'):
        href = urljoin(url, item.find('a')['href'])
        ext = get_ext(href) or '.item'
        filenames[href] = '{}/{:04}{}'.format(info, len(imgs), ext)
        imgs.append(href)
    # Files
    files = soup.find('div', class_='post__files')
    if files:
        for item in files.findChildren(recursive=False):
            a = item if 'href' in item.attrs else item.find('a')
            href = urljoin(url, a['href'])
            # Imgur
            if 'imgur.com/' in href:
                print_('Imgur: {}'.format(href))
                try:
                    from extractor import imgur_downloader
                    for img in imgur_downloader.get_imgs(href):
                        ext = get_ext(img) or downloader.get_ext(img)
                        filenames[img] = '{}/{:04}{}'.format(info, len(imgs), ext)
                        imgs.append(img)
                except Exception as e:
                    print_(print_error(e))
                continue
            ext = get_ext(href) or '.file'
            filenames[href] = '{}/{:04}{}'.format(info, len(imgs), ext)
            imgs.append(href)
    # Content
    content = soup.find('div', class_='post__content')
    if content:
        for img in content.findAll('img'):
            src=img.get('src')
            if not src:
                continue
            src = urljoin(url, src)
            ext = get_ext(src) or downloader.get_ext(src)
            filenames[src] = f'{info}/{len(imgs):04}{ext}'
            imgs.append(src)
        tex=[]
        for a in content.findAll('br'):
            a.replace_with('\n')
        for a in content.findAll(recursive=False):
            tex.append(a.text)
        for a in content.findAll('a'):
            src = a.get('href')
            if src:
                if 'http' not in src:
                    src=KEM+src
                tex.append(src)
        if tex:
            imgs.append(Text(dix+'/'+usuar+'/'+info,info,'\n'.join(tex)).url)
    return usuar, imgs, filenames

class Text:
    def __init__(self, dix, name, cont):
        self.filename = name+'/content.txt'
        self.cont = cont
        self.url = LazyUrl(dix, self.ruait, self)
    
    def ruait(self, dix):
        try:
            os.makedirs(dix)
        except:
            pass
        with open(dix+'/content.txt', "wb") as f:
            f.write(self.cont.encode())
        return dix+'/content.txt'
