#coding:utf8
#title:AV19
#comment:https://av19a.com/
import downloader
from utils import Downloader,clean_title
from m3u8_tools import M3u8_stream
from io import BytesIO
@Downloader.register
class Downloader_av19(Downloader):
    type = 'av19'
    URLS=['av19.org','av19.gg','av19a.com']
    single=True
    display_name='AV19'
    icon='base64:AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////AP7//wD///8A////AP/+/wD///8A////AP///wD+/v8A////AP7//wD///8B////AP7//wH///8A/v7/AP/+/wD+//8A////AP///wD///8A////AP7//wD//v8A////AP7+/wD+/v8A/v//AP7//wD//v8B////AP/+/wD///8A/v//Af///wAA//8AAP//Af///wD///8A////AP///wD///8A/v//AP///wD//v8A/v//Af/+/wD///8B//7/AP/+/wD///8BAP//AQD//wAA/v8B////AP///wD///8A////AP///wD///8B//7/AP7//wD//v8A/v//AP///wH///8A////AP7+/wAB//8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8A////Af///wD+/v8A//7/AP///wD//v8B////AP///wD///8AAAH/AP///wD+/v8B////AP7//wD//v8B////AAAA/wD///8A/v//AP/+/wD///8A//7/AP7//wD//v8AAAD/AP7//wH///8A////Af///wH//v8A//7/AP///wD///8BAAD/Af7//wD///8A/v//Af/+/wH///8AAQD/AP///wABAP8B/v//AP/+/wD///8B////AP///wD+//8AAAH/Af///wAAAP8B//7/AP7//wD//v8A////AP///wH///8A//7/AP7//wD///8A//7/AP///wD///8B/v//AP/+/wH+//8A////Af///wD///8A////AP///wH//v8A/v//AP///wD+//8A////AP///wD///8A//7/AP7//wD///8B////AP7//wD///8A////Af///wD///8A//7/AP7//wH//v8AAAH/AP///wD///8A/v//AP///wAAAP8A////AP///wD//v8A////AP///wD///8A////AP/+/wD///8AAAD/AQEA/wAAAf8A////AP7//wEAAP8AAAD/AAAA/wH+//8A/v//Af7//wD///8A//7/Af///wD///8A/v7/AP///wAAAP8B/v//AP7//wD//v8A////AQEA/wD///8A//7/AP///wD+/v8A/v7/AP///wH+/v8B////AP7//wH///8A/v//AP///wD+//8A////AP/+/wD///8A/v//Af///wD///8A/v//AP7//wD+/v8B////AP/+/wD///8A/v//Af/+/wD//v8A////AP7//wH//v8B////AP/+/wD//v8A////AP///wH//v8B/v//AP7//wH+//8B/v//AP7+/wH+//8A/v7/AP///wD///8A//7/AP///wD+//8A/v//AP/+/wD//v8A////'
    MAX_PARALLEL=2

    def read(self):
        REF='https://av19a.com/'
        REZ='https://david.cdnbuzz.buzz/'
        soup=downloader.read_soup(self.url,**{'referer':REF})
        self.title=clean_title(soup.find('title').text.strip())+'.mp4'
        urlx=soup.find('iframe')['src']
        dex,u1,ini=(corta,urlx.find('n=')+2,'https://z124fdsf6dsf.onymyway.top/')if'/i2.php'in urlx else(None,urlx.find('poster=')+7,'https://cdn1.thisiscdn.top/')
        u2=urlx.find('&',u1)
        thumb=BytesIO()
        downloader.download(urlx[u1:u2],buffer=thumb,referer=REF)
        u1=urlx.find('vvv=')+4
        u2=urlx.find('&',u1)
        m=M3u8_stream(ini+urlx[u1:u2],referer=REZ,n_thread=4,referer_seg=REZ,deco=dex)
        self.urls.append(m)
        self.filenames[m]=self.title
        self.setIcon(thumb)
def corta(dato):
    return dato[8:]
