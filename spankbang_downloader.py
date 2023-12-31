#coding:utf8
#title_en: Spankbang
#https://spankbang.com/
'''
Spankbang Downloader
'''
import downloader
from io import BytesIO
from utils import (Downloader, Soup, try_n, LazyUrl, get_print,
                   Session, filter_range,
                   clean_title, check_alive)
from error_printer import print_error

class Video:
    '''
    Video
    '''
    def __init__(self, url, cwz, session):
        self.url = LazyUrl(url, self.get, self)
        self.cw = cwz
        self.session = session

    @try_n(2)
    def get(self, url):
        '''
        get
        '''
        cw = self.cw
        session = self.session
        print_ = get_print(cw)
        try:
            ##html = downloader.read_html(url, session=session)
            html = downloader.read_html(url)
            soup = Soup(html)
        except Exception as e: #3511
            print_(print_error(e))
        # 1968
        title = soup.find('h1').text.strip()
        code = soup.find('meta', {'property': 'og:url'}).attrs['content']
        m1 = code.find('/', 13) + 1
        m2 = code.find('/', m1)
        title = title +'('+ code[m1:m2] + '.mp4'
        file = soup.find('main').find('script',{'type': 'text/javascript'}).text.strip()
        MARRAY = ["'1080p':","'720p':","'480p':","'320p':","'240p':"]
        for mo in MARRAY:
            uno = file.find(mo)
            uno = file.find("[",uno)
            dos = file.find("]", uno)
            if dos - uno > 1 :
                file = file[uno+2:dos-1]
                break
        self.filename = clean_title(title)
        self.thumb = soup.find('meta', {'property': 'og:image'}).attrs['content']
        return file

def texto(f):
    return f.text.strip()

def thumba(url_thumb):
    f = BytesIO()
    downloader.download(url_thumb, buffer=f)
    return f

class Downloader_spankbang(Downloader):
    '''
    Downloader
    '''
    type = 'spankbang'
    single = True
    strip_header = False
    URLS = ['spankbang.com']
    display_name = 'Spankbang'
    MAX_CORE = 2
    icon = 'base64:AAABAAEAICAAAAEAIAAoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAABAAAAAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAEAABEAAAANAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAFJAAAA9AAAAOsAAAA0AAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAABAAAAAAAAAAAAAQAAAAAAAAAAAAAAAQAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAASQEAAPYFAwv/AgEG/wAAAO4AAAA2AAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAABAAEAAAAAAAAAAAAAAQAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAEgAAAD2BQMN/zUkiP8/LaL/AwIJ/wAAAO8AAAA3AAAAAAAAAQAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAABIAAAA9gQDDP8zI4T/STO8/1o/5P9BLab/AwIJ/wAAAPABAAA5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAASAAAAPYEAgz/NCSF/0Etpf9TOtT/Wj/k/1o/5P9CLqj/AwIJ/wAAAPAAAAA7AAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAABAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAEAAQABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEkAAAH2BAMM/zUjhf9BLaX/RC+t/1k/4/9aP+T/Wj/k/1o/5f9CLqn/BAIK/wAAAPEAAAA9AAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAABAAAAAAAAAQAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAQAAAAAAAAAAAABIAAAA9gQDDP80I4T/QS2l/0Etpf9MNcX/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9DLqv/BQML/wEAAPIAAAA+AAAAAAAAAAAAAAAAAQEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAASAAAAPYEAwz/NCOE/0Etpf9BLaX/QS2l/1c82/9aP+T/Wj/k/1o/5P9bP+T/Wj/k/1o/5P9FL63/BAML/wAAAPIAAABAAAAAAAAAAAAAAAAAAQAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAEkAAAD2AwIK/yocbP88KZv/QS2l/0Etpf9GMLT/Wj/k/1o/5P9aP+T/Wj/l/1o/5P9aP+T/Wj/k/1o+5P9EL67/BAMM/wAAAPMAAABCAAAAAAAAAQAAAAAAAAEAAAEAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAABIAAAA9gMCC/8pHGv/OymY/0EspP9BLaX/QS2l/083y/9aP+T/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9aP+T/Wj7k/1o/5P9FMLD/BQMN/wAAAPQAAABEAAAAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAAAAAAAAAQAAAAAASAAAAPYDAgr/Kh1t/z0qnP8/K6H/NCSF/zEif/84J4//Vzzd/1o/5P9aP+X/Wj/k/1k+4/9aP+T/Wz/k/1o/5P9aP+T/Wj/k/1o/5P9FMLD/BQMP/wAAAPUAAABFAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAEwBAAD3AwIL/ywecv9IMrj/UznT/1k94P9VO9n/RjGz/yoebv8PCif/KRxm/1I40P9aP+T/OSiS/0s1wf9aP+T/Wj/k/1s/5P9aP+T/Wj/k/1o/5P9HMLP/BQMO/wABAPUAAABHAAAAAAAAAAAAAAAAAAABAAAAAAABAAAwAAAA8wQDDv85J5P/Vz3e/1o/5P9aP+T/Wj7k/1o/5f9bP+T/Wj/k/1Q71/8iGVv/BgQR/0Aso/8ZEUL/Dgkk/1A4zf9PN8r/PCqZ/z4rnv9QOM7/Wj/k/1o/5P9GMLT/BgQP/wAAAPYAAABCAAAAAAAAAAAAAAAAAAAACQAAANcBAQT/OSeS/1g+4P9aP+T/Wj/k/1o/5P9aP+T/Wj7k/1o+5P9aP+T/Wj/k/1k+4/8vIHn/AQEF/wIBBf8AAAD/BwQS/wABBP8RDCz/Kh1r/zgnkv9TO9T/Wj7k/1o/5P9HMbX/BQMN/wABAOsAAAAbAAABAAAAAAAAAAGBAAAA/yQZYf9WPNz/Wj7l/1o/5P9bP+T/Wj/k/1o/5f9aP+T/Wj7k/1o/5P9aPuT/Wj/k/1k+4/8gFlP/AAAA/wAAAP8AAAD/Ixhc/0ozvv9XPd7/Wj/l/1o/5P9aP+T/Wj/k/1o/5f87KZj/AAAA/wAAAKwAAAAAAAAAEgAAAPILBxz/TjbJ/1o/5P9aP+T/Wj/k/1o+5P9aP+T/Wj/k/1o/5P9aP+T/Wz/k/1o+5P9aP+T/Wj/k/1I50f8EAwv/AAAA/w8KJ/9IMrj/WD3g/1o/5P9aP+T/Wj/k/1o/5P9bP+T/Wj/k/1g+4/8bEkX/AAAA/QAAADABAABsAAEA/y0fdP9YPuH/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9aP+X/Wj/l/1o/5P9aP+T/Wj/k/1o/5P9aP+X/Wj/k/yIYWf8AAQD/KRxo/082yP9aP+T/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9bP+T/Wj/k/0UwsP8AAAD/AAABjwAAALYCAAT/SjO9/35p6f9wWef/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9aPuX/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9bP+T/OymX/wAAAf8uIHf/UDfM/1o/5f9aPuT/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9aPuX/WT7i/wkGFv8AAADQAAAA4w0JIv9YQdH/kX/s/3lj6P9aP+T/Wj/k/1o/5P9aP+T/Wj/l/1o/5P9aP+X/Wj/l/1s/5P9aP+T/Wj/k/1o/5P9HMrb/AAAA/yIXV/9ONsj/Wz/k/1o/5P9aP+X/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9aPuT/Fg86/wAAAPIAAADwEQws/1tD1v+Rf+z/gW3q/1o/5P9aP+T/Wj7k/1o/5P9aP+T/Wz7k/1o/5P9aP+T/Wj/k/1o/5P9bP+T/Wj/k/0gyuf8AAAH/HRRL/042xv9aP+T/Wz/k/1o/5P9aP+T/Wj/k/1s/5P9aP+T/Wj/k/1o/5P8XED3/AAAA9QAAANsKBxz/VTvT/4587P+Neuz/Wj/k/1o/5P9aP+X/Wz/k/1o/5P9aP+T/Wj/k/1s/5P9aP+T/Wj/k/1o/5P9aP+T/Pyuf/wAAAP8fFU//TjbH/1o/5P9aP+T/Wj/k/1o/5f9aP+T/Wj/k/1o/5P9aPuX/WT7j/wwIH/8AAAHZAAAApQAAAf9GMLP/e2bp/5F/7P9nT+X/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9aP+T/Wj/l/1o/5P9aP+X/Wj/k/1o/5P8oG2f/AAEA/ygcaP9PN8n/Wj7k/1o/5P9bPuT/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9LNL//AAEA/wAAAJ0AAABLAAAA/yAWVP9hR+T/kH3s/39r6f9aP+X/Wz/k/1s/5P9aP+T/Wj/k/1o/5P9aP+T/Wj/k/1o/5P9aP+T/VTza/wkFFf8AAAD/OiiU/1E4z/9aP+T/Wj/k/1o/5P9aP+T/Wj/k/1o/5f9aP+T/WT7j/yEXVv8AAAD+AAAAQQAAAQIAAADIAQAD/0Iuqf9zW+f/kX/s/2lP5f9aP+T/Wj/k/1s/5P9aP+T/Wj/k/1o/5P9aP+T/Wj/k/1k+4/8pHGn/AAAA/w0IIv9HMbX/VTvY/1o/5P9aP+T/Wj/k/1o/5P9aPuX/Wj/k/1o/5P9BLqf/AAAC/wAAAMEAAAABAAAAAAAAAC0AAAH0BwUT/0s0v/93Yej/i3jr/19F5P9aP+T/Wz/k/1o/5P9aP+T/Wj7k/1o/5f9aP+T/OCeQ/wAAAv8AAAD/MSJ//0kyuf9ZP+L/Wj/k/1s/5P9aP+T/Wj/k/1o/5P9aP+T/STO6/wcEEf8AAADyAAAAJwAAAAAAAAAAAAAAAAAAAFEAAAD6BwUU/0Qvrv9tVub/gm7p/15F5f9aP+T/Wj7k/1o/5P9aP+T/Vz3f/yseb/8BAAL/AAAA/xEMLf9HMbX/UDfM/1o/5P9aP+T/Wj/k/1o/5P9bP+T/WT7j/zwpmf8FAw7/AAAA+AAAAEwBAAAAAAAAAAAAAAABAAAAAAEAAAAAAFMAAAD1AQAD/yUZXv9POML/Z0/k/1o/5P9ZPuP/UjnQ/zQkhP8MCCD/AAAA/wAAAP8AAAD/AAAA/xkRQP9IMrn/WT/j/1s/5P9aP+T/Vz3e/0AtpP8YET7/AAAA/wAAAOwAAABGAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAS4AAQDIAAAA/gAAAP8IBRX/DQkj/wkGF/8AAAL/AAEA/wAAAO8AAACAAAAAUgAAAFgBAAC1AAAA/gAAAP8JBhn/FA40/xEMLf8EAwv/AAAA/wAAAPwAAAGmAAAAGwAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAEAAABJAAAAnwAAAMoAAADYAAABzAAAAKcAAABiAQAADgAAAAAAAAAAAAABAAABAAAAAAA9AQAAmQAAANIAAADpAAAA4wAAAMAAAACAAAAAJwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    ACCEPT_COOKIES = [r'(.*\.)?(spankbang)\.(com)']

    @try_n(2)
    def read(self):
        cw = self.cw
        session = self.session = Session()
        videos = []
        if '/video/' in self.url:
            video = Video(self.url, cw, session)
            video.url()
            self.urls.append(video.url)
            self.title = video.filename
        else:
            self.single = False
            info = get_videos(self.url, session, cw)
            hrefs = info['vids']
            self.print_('videos: {}'.format(len(hrefs)))
            if not hrefs:
                raise Exception('no hrefs')
            videos = [Video(href, cw, session) for href in hrefs]
            video = self.process_playlist(info['title'], videos)
        self.setIcon(thumba(video.thumb))
        self.enableSegment()
        #self.enableSegment(n_threads=8)
        #self.enableSegment(chunk=524288)
        #self.enableSegment(overwrite=True)

@try_n(4)
def get_videos(url, session, cw=None):
    '''
    get_videos
    '''
    print_ = get_print(cw)
    html = downloader.read_html(url)
    soup = Soup(html)
    info = {}
    url_vids = set()
    vids = []
    title = soup.find('em').text.strip()
    if not title:
        raise Exception('No title')
    print(title)
    info['title'] = title
    while True:
        check_alive(cw)
        wvids = soup.find(id ='container').find('div', class_='video-list').findAll('a', class_='thumb')
        for wvid in wvids:
            href = 'https://spankbang.com' + wvid.attrs['href']
            if href in url_vids:
                continue
            url_vids.add(href)
            vids.append(href)
        view = soup.find('li', class_='next')
        if view:
            url = 'https://spankbang.com' + view.find('a').attrs['href']
            try:
                soup = downloader.read_soup(url, session=session)
            except Exception as e:
                print_(e)
        else:
            break
    
    if cw:
        vids = filter_range(vids, cw.range)
        cw.fped = True

    info['vids'] = vids
    return info
