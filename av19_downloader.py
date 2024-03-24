#coding: utf8
#title: AV19
#comment: https://av19.org/

import downloader
from utils import Downloader, clean_title
from m3u8_tools import M3u8_stream
from io import BytesIO

@Downloader.register
class Downloader_av19(Downloader):
    type = 'av19'
    URLS = ['av19.org','av19.gg']
    single = True
    display_name = 'AV19'
    icon = 'base64:AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP7//wD///8A////AP/+/wD///8A////AP///wD+/v8A////AP7//wD///8B////AP7//wH///8A/v7/AP/+/wD+//8A////AP///wD///8A////AP7//wD//v8A////AP7+/wD+/v8A/v//AP7//wD//v8B////AP/+/wD///8A/v//Af///wAA//8AAP//Af///wD///8A////AP///wD///8A/v//AP///wD//v8A/v//Af/+/wD///8B//7/AP/+/wD///8BAP//AQD//wAA/v8B////AP///wD///8A////AP///wD///8B//7/AP7//wD//v8A/v//AP///wH///8A////AP7+/wAB//8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8A////Af///wD+/v8A//7/AP///wD//v8B////AP///wD///8AAAH/AP///wD+/v8B////AP7//wD//v8B////AAAA/wD///8A/v//AP/+/wD///8A//7/AP7//wD//v8AAAD/AP7//wH///8A////Af///wH//v8A//7/AP///wD///8BAAD/Af7//wD///8A/v//Af/+/wH///8AAQD/AP///wABAP8B/v//AP/+/wD///8B////AP///wD+//8AAAH/Af///wAAAP8B//7/AP7//wD//v8A////AP///wH///8A//7/AP7//wD///8A//7/AP///wD///8B/v//AP/+/wH+//8A////Af///wD///8A////AP///wH//v8A/v//AP///wD+//8A////AP///wD///8A//7/AP7//wD///8B////AP7//wD///8A////Af///wD///8A//7/AP7//wH//v8AAAH/AP///wD///8A/v//AP///wAAAP8A////AP///wD//v8A////AP///wD///8A////AP/+/wD///8AAAD/AQEA/wAAAf8A////AP7//wEAAP8AAAD/AAAA/wH+//8A/v//Af7//wD///8A//7/Af///wD///8A/v7/AP///wAAAP8B/v//AP7//wD//v8A////AQEA/wD///8A//7/AP///wD+/v8A/v7/AP///wH+/v8B////AP7//wH///8A/v//AP///wD+//8A////AP/+/wD///8A/v//Af///wD///8A/v//AP7//wD+/v8B////AP/+/wD///8A/v//Af/+/wD//v8A////AP7//wH//v8B////AP/+/wD//v8A////AP///wH//v8B/v//AP7//wH+//8B/v//AP7+/wH+//8A/v7/AP///wD///8A//7/AP///wD+//8A/v//AP/+/wD//v8A////'
    REFERER = 'https://david.cdnbuzz.buzz/'

    def read(self):
        soup = downloader.read_soup(self.url,**{'referer':'https://av19.gg/'})
        self.title = clean_title(soup.find('title').text.strip())+'.mp4'
        urlx=soup.find('iframe')['src']
        html = downloader.read_html(urlx, referer=self.REFERER)
        nu = html.find('ht', html.find('<source' if '/test.php' in urlx else'file:'))
        m = lambda: M3u8_stream(html[nu: html.find('"',nu)],referer=self.REFERER, n_thread=8, referer_seg=self.REFERER)
        try:
            m = m()
        except Exception as e:
            raise e
        thumb = BytesIO()
        nu = html.find('ht', html.find('poster=' if '/test.php' in urlx else'image:'))
        downloader.download(html[nu: html.find('"',nu)], buffer=thumb, referer=self.REFERER)
        self.urls.append(m)
        self.filenames[m] = self.title
        self.setIcon(thumb)
