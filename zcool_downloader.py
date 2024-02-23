#coding: utf8
#title_en: Zcool
#comment: https://www.zcool.com.cn/

import downloader
from utils import Downloader, Soup, clean_title, get_print
from translator import tr_

@Downloader.register
class Downloader_zcool(Downloader):
    type = 'zcool'
    URLS = ['www.zcool.com']
    #icon = 'base64:'
    display_name = 'Zcool'
    MAX_PARALLEL = 1
    MAX_CORE = 4

    def read(self):
        if '/work/' in self.url:
            self.title, self.urls, self.filenames = read_post(self.url, self.cw)
            #titu = self.filenames[self.urls[0]]
            #self.cw.setTitle(titu[:titu.find('/')])
        #else:
        #    self.title, self.urls, self.filenames = read_user(self.url, self.cw)
        #self.enableSegment(chunk=2**20,n_threads=2)

def read_user(url, cw):
    soup = Soup(downloader.read_html(url))
    galerias = []
    idp = soup.find('meta', {'name': 'id'})['content']
    username = soup.find('meta', {'name': 'artist_name'})['content']
    titu  = clean_title(username +'('+ idp)
    nga = 0
    elementos = soup.find('div', class_='card-list__items').findAll('a')
    for a in elementos:
        galerias.append(a.attrs['href'])
    Next = soup.find('a', class_='next')
    cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), titu, nga))
    while Next:
        href = Next.attrs['href']
        soup = Soup(downloader.read_html('https://kemono.su'+href))
        elementos = soup.find('div', class_='card-list__items').findAll('a')
        for a in elementos:
            galerias.append(a.attrs['href'])
        Next = soup.find('a', class_='next')
    files = []
    namefiles = {}
    for gale in galerias:
        _, urls, filenames = read_post('https://kemono.su'+gale, cw)
        files += urls
        namefiles.update(filenames)
        nga += 1
        cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), titu, nga))
    return titu, files, namefiles

def read_post(url, cw):
    print_ = get_print(cw)
    soup = Soup(downloader.read_html(url))
    title = clean_title(soup.find('h1').text)
    #idp = soup.find('meta', {'name': 'id'})['content']
    imgs = []
    filenames = {}
    p=0
    for imgbox in soup.findAll('div', class_='imgbox'):
        print_(imgbox)
        src = imgbox.find('img')['data-src']
        un = src.find('?')
        if un > 0:
            src = src[:un]
        imgs.append(src)
        filenames[src] = str(p)+src[src.rfind('.'):]
        p+=1
    return title, imgs, filenames