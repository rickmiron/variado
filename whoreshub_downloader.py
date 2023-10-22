#coding:utf8
#title_en: Whoreshub
#https://www.whoreshub.com/

import downloader
from io import BytesIO
from os import path, makedirs
from utils import (Downloader, Soup, try_n, LazyUrl, get_print,
                   clean_title)
from error_printer import print_error

class Video:
    def __init__(self, url, cwz):
        self.cw = cwz
        self.referer = url
        self._url = ''
        self.url = LazyUrl(url, lambda _: self._url, self)

    @try_n(2)
    def get(self):
        cw = self.cw
        print_ = get_print(cw)
        print_('ini get')
        print_('downloader.read_html')
        try:
            soup = Soup(downloader.read_html(self.referer))
        except Exception as e: #3511
            print_(print_error(e))
        # 1968
        print_('soup.find')
        self.thumb = soup.find('meta', {'property': 'og:image'}).attrs['content']
        script = soup.find('div', class_='player-holder').findAll('script')[1].text.strip()
        un = script.find('video_id:') + 11
        videoid = script[un:script.find("',",un)]
        un = script.find('video_title:',un)+14
        videotitle = script[un:script.find("',",un)]
        videourl = ''
        for i in ['5','4','3','2','']:
            dos = script.find(f'video_alt_url{i}:',un)
            if dos > -1:
                if not i:
                    dos -= 1
                videourl = script[dos + 17:script.find("',",dos)]
                break
        else:
            dos = script.find('video_url:',un)
            if dos > -1:
                videourl = script[dos + 12:script.find("',",dos)]
        er = ['_360p','','_720p','_1080p','_1440p','_2160p']
        for i in range(7,1,-1):
            dos = script.find(f'preview_url{i}:',un)
            if dos > -1:
                self.thumb = self.thumb.replace('preview',f'preview{er[i-2]}.mp4')
                break
        title = f'{videotitle}({videoid}).mp4'
        self.filename = clean_title(title)
        self._url = videourl
        print_('fin get')

def thumba(url_thumb, dir,cw):
    print_ = get_print(cw)
    print_('ini thumba')
    th = BytesIO()
    if not url_thumb.startswith("http"):
        url_thumb = 'https:' + url_thumb
    print_('ini download thumba')
    downloader.download(url_thumb, buffer=th)
    print_('fin download thumba')
    th.seek(0)
    byth = th.read()
    if len(byth) > 0:
        print_('if thumba')
        with open(dir, "wb") as f:
            f.write(byth)
        f.close
    print_('return thumba')
    return th

class Downloader_whoreshub(Downloader):
    type = 'whoreshub'
    URLS = ['whoreshub.com'] #4835
    icon = 'base64:AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAABSAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD4/1EB9/9SAPr/UgD6/1EB9/9SAPj/UgD6/1IA+f9RAff/UgD5/1IA+v9SAPn/UQH3/1IA+f9SAPr/UgD5/1MA/f9UAP//UgD6/1IA+v9UAP//UwD8/1IA+f9TAPz/VQD//1MA+/9SAPn/UwD8/1UA//9TAPv/UgD4/1QA//9HDL3/PRaH/1MA//9SAPn/PBeA/0kKxv9VAP//SgjN/zgba/9OBOX/VAD//0sH1P84G2z/TQXf/1IA+P9UAP//NR5c/ygtEP9OBOX/TAfW/yYuCP84HGn/VwD//0ERn/8mLwT/SArF/1YA//9DEKj/Ji4H/0cMvf9TAP//TwTm/y4mNf8pLBX/RQ+u/0ISn/8oLBP/MCQ7/1MA/f9ED6v/KSwV/0sJzv9ZAP//Rg6y/ykrGP9IC8H/VQD//0UOsP8qKh3/Kyki/zcdY/81Hlr/Kykj/yoqHf9KCcz/RQ6x/ykrFv8zIUz/NR9Z/zEjRf8qKh//Rwu+/1UA//84HGr/LyQ6/zsYe/8qKh//Kykh/z0XhP8tJy7/PRaH/0YNtf8pLBX/MyFO/zYeXP8yIkf/Kiof/0cLvv9RAvH/LiYw/zoac/9LCc//Kiof/ywoJv9NBtv/Nh5d/zIiSf9DEKf/KSsX/0sJzf9ZAP//Rg6y/ykrGP9IC8H/Rgy5/yYvBv9ED63/VAD//ywoKP8vJTj/VQD//0ATlv8oLBX/Ohp0/yctD/9IC8P/VgD//0MQqP8mLgf/Rwy9/00G3P87GHv/TgTk/1UA//9CEaL/RA+r/1UA//9MBtr/PBeA/0YMuv85GnD/TgTk/1QA//9LB9T/ORtt/00F3/9TAPz/VQD//1IA+/9SAPn/VAD+/1QA/v9SAPn/UwD7/1UA//9UAP7/VAD//1MA+/9SAPn/UwD8/1UA//9TAPv/UgD5/1EB9/9SAPn/UgD6/1IB9/9SAPj/UgD6/1IA+f9RAff/UgD4/1EB9/9SAPn/UgD6/1IA+f9RAff/UgD5/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/UgD6/1IA+v9SAPr/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='
    single = True
    MAX_PARALLEL = 2
    display_name = 'Whoreshub'
    ACCEPT_COOKIES = [r'(.*\.)?(whoreshub)\.(com)']

    @try_n(2)
    def read(self):
        cw = self.cw
        print_ = get_print(cw)
        if not path.exists(self.dir):
            makedirs(self.dir)
        if '/albums/' in self.url:
            self.single = False
            info = get_album(self.url)
            for photo in info['photos']:
                self.urls.append(photo.url)
            self.title = info['title']
        elif '/videos/' in self.url:
            print_('ini video')
            video = Video(self.url, cw)
            video.get()
            self.urls.append(video.url)
            self.title = video.filename
            print_('seticon')
            self.setIcon(thumba(video.thumb,f'{self.dir}\\{video.filename}.webp',self.cw))
            print_('enablesegment')
            #self.enableSegment()
            self.enableSegment(n_threads=8)
            #self.enableSegment(chunk=524288)
            #self.enableSegment(overwrite=True)

class Image:
    def __init__(self, url, nu):
        self.filename = str(nu) + url[url.rfind('.'):]
        self.url = LazyUrl(url, lambda _: url, self)

def get_album(url):
    un = url.find('s/')+2
    id_album = url[un:url.find('/',un)]
    photos = []
    soup = downloader.read_soup(url)
    swiperslide = soup.find('div',class_='swiper-container gallery-top')
    private = swiperslide.find('div',class_='item private swiper-slide')
    if private:
        swiperslide = soup.find('div',class_='swiper-container gallery-thumbs')
        private = True
    un = 1
    for img in swiperslide.findAll('img'):
        href = img.attrs['src']
        if private:
            um = href.find('/main/')+6
            href = 'https://www.whoreshub.com/contents/albums/sources' + href[href.find('/',um):-1]
        photo = Image(href, un)
        un += 1
        photos.append(photo)
    info = {}
    title = soup.find('meta', {'property': 'og:title'}).attrs['content']
    info['title'] = clean_title(f'{title}({id_album})')
    info['photos'] = photos
    return info
