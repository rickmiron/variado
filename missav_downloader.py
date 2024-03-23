#coding:utf8
#title_en: Missav
#comment: https://missav.com/
#author: Rickelpapu

import downloader
from utils import Downloader, try_n, LazyUrl, get_print,Soup,clean_title,Session
from translator import tr_
from error_printer import print_error
from m3u8_tools import M3u8_stream
from io import BytesIO
from PIL import Image
from ffmpeg import convert, run
from os import remove, makedirs, path
USERAGEN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
class Video:
    def __init__(self, url, cwz, dir):
        self.cw = cwz
        self.dir = dir
        pt_=get_print(self.cw)
        pt_('Get ofuscado')
        urlv = self.ofuscado(url)
        pt_(urlv)
        sesion=Session()
        sesion.cookies.clear()
        sesion.headers.clear()
        sesion.headers.update({'Origin':'https://missav.com','User-Agent':USERAGEN})
        if urlv[urlv.rfind('.'):] == '.m3u8':
            m = lambda: M3u8_stream(urlv,session=sesion, n_thread=4)
            try:
                m = m()
            except Exception as e:
                raise e
            if getattr(m, 'live', None) is not None:
                m = m.live
        else:
            m = urlv.replace('.mpd','.mp4')
        self.thumb = BytesIO()
        self.thumbz = BytesIO()
        self.cw.setTitle(f'{tr_("썸네일 고정")}...{self.filename}')
        pt_(self.urlthumb)
        downloader.download(self.urlthumb, buffer=self.thumbz)
        self.dirfile = f'{dir}\\{self.filename}'
        self.tojpg()
        self.havethumbnail()
        self.url = LazyUrl('https://missav.com/', lambda _: m, self, pp=self.pp)
    
    def havethumbnail(self):
        if path.exists(self.dirfile):
            mi = run(f'-i "{self.filename}"', self.dir, bin='ffprobe')
            for ee in mi:
                if isinstance(ee, str) and 'attached pic' in ee:
                    break
            else:
                self.cw.setTitle(f'{tr_("썸네일 고정")}...{self.filename}')
                self.pp(self.dirfile)

    def tojpg(self):
        self.thumbz.seek(0)
        bythz = self.thumbz.read()
        if len(bythz) > 0:
            with open(self.dirfile + '.webp', "wb") as f:
                f.write(bythz)
            f.close
            imagen_webp = Image.open(self.thumbz)
            if imagen_webp.mode != "RGB":
                imagen_webp = imagen_webp.convert("RGB")
            imagen_webp.save(self.thumb, "JPEG", quality=90)
            self.thumbz.truncate(0)

    @try_n(2)
    def ofuscado(self, url):
        print_ = get_print(self.cw)
        try:
            soup = Soup(downloader.read_html(url,user_agent=USERAGEN))
        except Exception as e:
            print_(print_error(e))
        self.urlthumb = soup.find('meta', {'property': 'og:image'}).attrs['content']
        title = soup.find('h1').text.strip()
        vid = '/video/' not in url
        if vid:
            codigo = soup.find('meta', {'property': 'og:url'}).attrs['content']
            codigo = codigo[codigo.rfind('/')+1:].upper()
            un = title.find(' ')
            if un == -1:
                un = len(title)
            title = codigo + title[un:]
        self.filename = clean_title(title)+'.mp4'
        #if len(self.filename) > 209:
        #    self.filename = self.filename[:205] + '.mp4'
        codigo = soup.findAll('script', {'type': 'text/javascript'})[-2].text.strip()
        un = codigo.find('eval(')
        codigo = codigo[un:codigo.find('.split(',un) - 1]
        un = codigo.find('://')
        k_array = codigo[codigo.find(',\'',un) + 2:].split('|')
        narray = []
        for car in codigo[un-1:codigo.find(';',un)-2]:
            num = ord(car)
            narray.append((k_array[num - 48] if 58 > num > 47 else k_array[num - 87] if 96 < num < 123 else car) or car)
        url = ''.join(narray)
        if not vid:
            return url
        codigo = downloader.read_html(url,headers={'Origin':'https://missav.com'},user_agent=USERAGEN)
        un = codigo.find('\n',codigo.rfind('INF:'))+1
        return url.replace('playlist.m3u8',codigo[un:codigo.find('\n',un)])
    
    def pp(self, filename):
        self.thumb.seek(0)
        bythum = self.thumb.read()
        if len(bythum) > 0:
            pathum = f'{filename}.I'
            with open(pathum, 'wb') as f:
                f.write(bythum)
            f.close
            convert(filename, filename, f'-i "{pathum}" -map 1 -map 0 -c copy -disposition:0 attached_pic', cw=self.cw)
            remove(pathum)
        return filename

class Downloader_missav(Downloader):
    type = 'missav'
    single = True
    strip_header = False
    URLS = ['missav.com']
    display_name = 'Missav'
    MAX_PARALLEL = 2
    icon = 'base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAABSBJREFUWEedV99vFEUc/8zsbduo0AbRUBHbhpdqQuKDCW2qb0Zp0EeejCmctFDwD9DE4J01KCHqSwWt2mCM8aEQYgI0IUajtEpTo5hGFEJtQUtPI63Xn7e3P8bMzs7uzN7etnoPl93Zme/Pz/fz/Q4B/xEAzH8KnglAWLiWz+fowd+Mlk1G3f1LsJ+rZXS3Sc1Gg5FafsQFs2xmz1rEO38PzE/n3NJfJ1vcqXwu50mxQnagSFnkK9ovskV8msu+8Xg9ap63mfNUDTJNIL65ms2aAAZWhnPTJObFIqxPNg2+NKL6l6Qvvua/sz17jJkNj5xoRH1PipWJZ+Uid3QWxYGtiz8fokNnXOaHmXsgnoQjCeYV9r6241561wcG6M7EDCWGIMlPsebCG7vjrXRvOXVkQrWYf5VZCfP/fdeLOx6lLcMUZGuqewpk/Igpm6UpMnKMAB5jM1e8qc7HTvWHRvgGKMgD93wzvVsoT0tcqmUSwGqoxRo34m9vuXPLx0cmpMVhennOnQ07R2XY08Cp5jAeUq2YEsDK05FZHOsgQ0OuzKQv44/sq+8/gPqeABl6TBM8FgH6f2G6jeLAg4P5A6EBc9k3ealdqkB7tVD/F73BXvUIx0SRlZ/wSzSfy9FXbm08SQC/3CIwJWjZthmk91mwnyaBM6OA64YHOJoZl6zBMeaB8pkBA30PLfSSP7v6ttfT2i9qSKa5IqIxeWz/LtD2hwVPWGXgxDlgsgCsWuspGI0DbOZM/+NZTxI7e7zdYMaoZDiV43z9wR/hKN7fCdLW6hOJv892wSZvwz47AvNGISootS6lEEnt0ikG5hK3g8xnj/bXk7rDgaZ0ZuvuBG1rleqjvYzB/uoKjM8vgy5ZCs9FbBdxX3SsiNK7ZGXfsak6UtMscleJbZVU3O5OGG2tipFcbNAcANjzC6AXxoHL10BX9LQkoaPE7GliZ98qGRBdreKnaufNsXsXaJvAQEIYhAOuC29+Gc47p2EWioldS4rlXZR42bdD4FfDcJi2IAVJtsr4yW+sVIbz3jlkJm6m82ZoQKJ2vYhZkgFxzYE6ZtnwPhwG/WEy3QA1BWvxS6IB8Vx4HlhxBd7ABdDrM6nKXcIssrrv2FQtMZvjO+PG8HevW5ahdJOnPQqBs7QMen4c+O4XkMXSGtxAUGLlaTKXPdrfgLrD+u6ok2kUqqZADT1jcL6ZAD37LcjiaihKcyJ8iVb9Mixnj7dnNCKqPm7pKeBM4oFNzsL58keY4zeqeqzNQHEiKnT1bW8IqDgNA4QQuC88DUNSse2g/NEwzKu/gy6Lmk/tI0pcOJNazJkuciqWzYgCPdoEq/kjTHOb7kPm4DNwfr0F+tnXILYjuVoLu26MoAdlyJbGDrzOmxF/4+14I2ouGaEXMQbim0Ihki3FWOILUDDpP4rWWCUl4lwRvB2/PBLOhGIgaeipnHakijXGj6Sy0S8F4TTMB5Jtg/kDGoXoI5lQ6huzFjkEfq5rG2dq5o1lFsY6yOnYSMYFzKpDaUIAk9C8LsVBk/MQDKXKeK6N5VzY+F4+ljcPU9DYWF5dVZw1QgQpUODK1bFcRZk+CBGg0KVfTCKIq+DSbzghGmP3Pv5a7WISYDsZrPGrmW9x9LcGzYrP0dXs6iE+hlfiNJoldPoMyogfuCMmZnE5ZZkmUK3yKg0JL6eZi0WU/ctpCkWqwqrnOJfL0d4p9Xpu7DZJplEOMi48y2burEVc7Xqey+W8oJxi139pEsG/FsqCXEKpBFMAAAAASUVORK5CYII='
    ACCEPT_COOKIES = [r'(.*\.)?(missav)\.(com)']

    @try_n(2)
    def read(self):
        if not path.exists(self.dir):
            makedirs(self.dir)
        video = Video(self.url, self.cw ,self.dir)
        self.setIcon(video.thumb)
        self.urls.append(video.url)
        self.title = video.filename
