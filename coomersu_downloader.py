#coding: utf8
#title_en: Coomer.Su
#comment: https://coomer.su/

import downloader
from utils import Downloader, Soup, urljoin, get_ext, clean_title, get_print, print_error
from translator import tr_

@Downloader.register
class Downloader_coomer(Downloader):
    type = 'coomer.su'
    URLS = ['coomer.party','coomer.su']
    icon = 'base64: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'
    display_name = 'Coomer.Su'
    MAX_PARALLEL = 1
    MAX_CORE = 4

    def read(self):
        if '/post/' in self.url:
            self.title, self.urls, self.filenames = read_post(self.url, self.cw)
            titu = self.filenames[self.urls[0]]
            self.cw.setTitle(titu[:titu.find('/')])
        else:
            self.title, self.urls, self.filenames = read_user(self.url, self.cw)
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
        soup = Soup(downloader.read_html('https://coomer.su'+href))
        elementos = soup.find('div', class_='card-list__items').findAll('a')
        for a in elementos:
            galerias.append(a.attrs['href'])
        Next = soup.find('a', class_='next')
    files = []
    namefiles = {}
    for gale in galerias:
        _, urls, filenames = read_post('https://coomer.su'+gale, cw)
        files += urls
        namefiles.update(filenames)
        nga += 1
        cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), titu, nga))
    return titu, files, namefiles

def read_post(url, cw):
    print_ = get_print(cw)
    soup = Soup(downloader.read_html(url))
    title = soup.find('h1').text
    idp = soup.find('meta', {'name': 'id'})['content']
    usid = soup.find('meta', {'name': 'user'})['content']
    usuar = soup.find('a', class_='post__user-name').text.strip()
    tail = '({}'.format(idp)
    info = '{}{}'.format(clean_title(title, allow_dot=True, n=-len(tail)), tail)
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
            src = urljoin(url, img['src'])
            ext = get_ext(src) or downloader.get_ext(src)
            filenames[src] = '{}/{:04}{}'.format(info, len(imgs), ext)
            imgs.append(src)
        for a in content.findAll('a'):
            href = a['href']
            ext = '.cont'#get_ext(href) or downloader.get_ext(href)
            filenames[href] = '{}/{:04}{}'.format(info, len(imgs), ext)
            imgs.append(href)
    return clean_title(usuar +'('+ usid), imgs, filenames