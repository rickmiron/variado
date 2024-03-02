#coding: utf-8
#title_en: Leakedzone
#comment: https://leakedzone.com/home

from utils import Downloader, clean_title, LazyUrl
from translator import tr_
from m3u8_tools import M3u8_stream
import requests
import base64
USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

class Downloader_leakedzone(Downloader):
    type = 'leakedzone'
    URLS = ['leakedzone.com']
    icon = 'base64:AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAQAAAJf/FgAA/gEAAAAAAAAAAACU8hMAAAEAAQABAACU/x0AAAAAAAABAAAAAAABAAAAAAABAAAAAQAAAQEAAAAAAQGW/ksAAAEAAQAAAAEAAAAFlvtHAQAAAAEAAAAFmPpFAAAAAAAAAQABAAEAAAEAAAEBAAABAQAAAQAAAACY/z4Amf4KAAAAAAAAAQAAAQAAA5b9SQAAAAAAAAAAAY7/EACX+jYAAAEAAAAAAAAAAQAAAAAAAAABAACV/wwAmP85AQAAAAEAAAAAAAAAAAAAAASX+kAAAQAAAAAAAAABAAADmPxPAAAAAAAAAQABAAAAAAAAAAEAAAAFl/tCAAH+AQEAAAAAAAEAAAABAAAAAAAElvozAAAAAAAAAAAAAAAAB5f/LACY/yUAAAEAAAAAAAAAAAABAAEABJn7RQABAAAAAAAAAAAAAAEBAAABmv8wAZf/WwAAAAAAAAAAAQAAAAAAAAADlfhXAQEAAAAAAAAAAAAAAQEBAASY/0gBAAEAAAABAAD//wEAmf9tAJb79ACY/rMAAAAAAQAAAAEAAAABAAAAApf9WAAAAAAAAAAAAAABAACL/wsAmftBAAABAACZ/woBmP6uAJn//wGY//8Alv3+AJf/NgAAAAABAAEAAAAAAAKX/FYAAQAAAAEAAAAAAAAAm/4cAJb6MwCf/wgBmP6+AJj//wCZ//8Amf7/AJn//wCV+9cAmf8UAQABAAAAAAADlvlOAAAAAAEAAQAAAAEAAJTqDAGY/0MAmP2fAJn//wGZ/PsAlv3yAJb98gGX/PcBl/z+AJn71gCV/ikAAAAABZb7RAABAAAAAQAAAAABAACZ/YkAmP2PAZn9jwCZ/zkAgP8GAAEAAAAAAAABAQAAAKP/CwCW/i4Bm/5dAJn+OQCY/YYBmv9dAAAAAAAAAAAAm/9dApf9hQAAAAAAAQAAAAABAAABAAABmP8qAQAAAAABAQABAAAAAAAAAAqY9RkAmf6gAJ3/DQEAAQAAAAAAAQD/AQWZ+jQBlv8WAAEBAAAAAAAAAQEAAQEAAAABAAAAAAAAAAABAAEAAAACmP1tAZr/KQAAAAABAQAAAQAAAAAAAAAA/v4BA5j/UgABAAAAAAAAAQABAAEAAAABAAAAAAAAAAEAAAAAAAAAA5j9VQAAAAAAAAAAAAEAAAAAAQAAAAAAAQAAAACV/ykAnP8kAAABAAAAAQAAAAAAAAAAAAABAAAAAAAAAAEAAASW+0IAAAEAAQAAAAAAAAAAAAAAAAEAAAABAAAAAAEAAAABAAEAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAABAAEAAAABAAABAAAAAAAA'
    display_name = 'Leakedzone'
    PARALLEL = 1
    MAX_CORE = 3
    ACCEPT_COOKIES = [r'(.*\.)?(leakedzone\.com)']
    user_agent = USERAGENT

    def read(self):
        self.title, self.urls, self.filenames = get_imgs(self.url,self.cw)

class Video:
    def __init__(self,url,idd):
        self.filename = idd
        self.url = LazyUrl(url, self.get, self)

    def get(self,url):
        m = lambda: M3u8_stream(url,referer='https://leakedzone.com/', n_thread=2)
        try:
            m = m()
        except Exception as e:
            raise e
        if getattr(m, 'live', None) is not None:
            m = m.live
        return m

def get_imgs(url,cw):
    url = url[url.find('.')+5:]
    for uo in ['/','?','#']:
        un = url.find(uo)
        if un!=-1:
            url = url[:un]
    title = clean_title(url)
    imgs = []
    filenames = {}
    for tipo in ['photo','video']:
        header = {'referer':f'https://leakedzone.com/{url}/{tipo}',
              'User-Agent':USERAGENT,
              'X-Requested-With':'XMLHttpRequest'}
        p=1
        foto = 'photo' == tipo
        while True:
            ped = requests.get(f'https://leakedzone.com/{url}/{tipo}?page={p}&type={tipo}s&order=0',headers=header)
            page = ped.json()
            if not page:
                break
            for ima in page:
                if foto:
                    file = 'https://leakedzone.com/storage/'+ima['image']
                    filenames[file]=str(ima['id'])+file[file.rfind('.'):]
                    imgs.append(file)
                else:
                    file = base64.b64decode(ima['stream_url_play'][16:][::-1][16:]).decode()
                    imgs.append(Video(file,str(ima['id'])+'.mp4').url)
            cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, p*48))
            p+=1
    return title, imgs, filenames