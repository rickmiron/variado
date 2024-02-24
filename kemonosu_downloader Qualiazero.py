#coding: utf8
#title_en: Kemono.Su
#comment: https://kemono.su/

import downloader
from utils import Downloader, Soup, urljoin, get_ext, clean_title, get_print, print_error,format_title,format_filename
from translator import tr_

@Downloader.register
class Downloader_kemonosu(Downloader):
    type = 'kemono.party'
    URLS = ['kemono.party','kemono.su']
    icon = 'base64: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'
    display_name = 'Kemono.Su'
    MAX_PARALLEL = 1
    MAX_CORE = 4

    def read(self):
        if '/post/' in self.url:
            self.title, self.urls, self.filenames = read_post(self.url, self.cw)
            titu = self.filenames[self.urls[0]]
            self.cw.setTitle(titu[:titu.find('/')])
        else:
            self.title, self.urls, self.filenames = read_user(self.url, self.cw)
            #self.title = self.format_title(None, 'idp', 'username', None, None, None, None)
            #self.title = self.format_title('info.type', 'info.id', 'info.title', 'artist', 'group', 'series', 'lang')
        #self.enableSegment(chunk=2**20,n_threads=2)

def read_user(url, cw):
    soup = Soup(downloader.read_html(url))
    galerias = []
    #idp = soup.find('meta', {'name': 'id'})['content']
    username = soup.find('meta', {'name': 'artist_name'})['content']
    #titu  = clean_title(username +'('+ idp)
    titu  = clean_title(username)
    #titu = format_title('None1', idp, username, 'None2', 'None3', 'None4', 'None5','None6')
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
    title = soup.find('h1').text
    idp = soup.find('meta', {'name': 'id'})['content']
    #usid = soup.find('meta', {'name': 'user'})['content']
    usuar = soup.find('a', class_='post__user-name').text.strip()
    #tail = '({}'.format(idp)
    #info = '{}{}'.format(clean_title(title, allow_dot=True, n=-len(tail)), tail)
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
            src = urljoin(url, img['src'])
            ext = get_ext(src) or downloader.get_ext(src)
            filenames[src] = f'{info}/{len(imgs):04}{ext}'
            imgs.append(src)
        #for a in content.findAll('a'):
        #    href = a['href']
        #    ext = '.cont'#get_ext(href) or downloader.get_ext(href)
        #    filenames[href] = '{}/{:04}{}'.format(info, len(imgs), ext)
        #    imgs.append(href)
    #return clean_title(usuar +'('+ usid), imgs, filenames
    return clean_title(usuar), imgs, filenames