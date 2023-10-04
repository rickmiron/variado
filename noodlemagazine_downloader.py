#coding:utf8
#title_en: Noodlemagazine
#https://noodlemagazine.com/
'''
Noodlemagazine Downloader
'''
import downloader
from io import BytesIO
from utils import (Downloader, Soup, try_n, LazyUrl, get_print,
                    filter_range,
                   clean_title, check_alive)
from error_printer import print_error

class Video:
    '''
    Video
    '''
    def __init__(self, url, cwz, session):
        self.url = LazyUrl(url, self.get, self)
        self.cw = cwz
        #self.session = session

    @try_n(2)
    def get(self, url):
        '''
        get
        '''
        cw = self.cw
        #session = self.session
        print_ = get_print(cw)
        try:
            headers0 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Referer':url
            }
            html = downloader.read_html(url)
            #html = downloader.read_html(url)
            soup = Soup(html)
        except Exception as e: #3511
            print_(print_error(e))
        # 1968
        if soup.find('div', class_='alert_warning'):
            raise Exception('Sorry, this video has been deleted.')
        title = soup.find('h1').text.strip()
        code = url[url.rfind('/')+1:]
        title = title +'('+ code + '.mp4'
        url = url.replace('/watch/', '/playlist/')
        try:
            headers1 = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                'Referer':url
            }
            ##html = downloader.read_html(url, session=session)
            html = downloader.read_html(url,headers=headers1)
        except Exception as e: #3511
            print_(print_error(e))
        uno = html.find('file')
        dos = html.find(',',uno)
        file = html[uno+8:dos-1]
        self.filename = clean_title(title)
        self.thumb = soup.find('meta', {'property': 'og:image'}).attrs['content']
        return file

def texto(f):
    return f.text.strip()

def thumba(url_thumb):
    f = BytesIO()
    downloader.download(url_thumb, buffer=f)
    return f

class Downloader_noodlemagazine(Downloader):
    '''
    Downloader
    '''
    type = 'noodlemagazine'
    single = True
    strip_header = False
    URLS = ['noodlemagazine.com']
    display_name = 'Noodlemagazine'
    MAX_CORE = 4
    icon = 'base64:AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAABILAAASCwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaAAAAAwMAAFQkAAB3VwAAh3YAAIp3AACAWgAAYCcAAA8EAAAlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABpAAAARhQAAH56AACa2QAAqPoAAK//AACy/wAAs/oAAKzcAACUggAAWhgAAJEAAAAAAAAAAAAAAAAAAABgAAAASxYAAIiiAACi+wAAqv8AAK3/AACx/wAAtf8AALn/AAC9/wAAvPwAAKarAABmGwAAgwAAAAAAAAAxAAAAAAQAAIGFAACf/QAApv8ODq3/QkK+/yEhuf8BAbT/AAC4/wAAvP8AAMD/AADB/gAApJEAABoGAABLAAAAegAAAGcwAACV5AAAov8AAKX/W1vB/+Li5v/Hx+H/ZmbN/xERvP8AALz/AADA/wAAxf8AAL7qAACMOgAAqwAAAOEAAAB/cAAAnP8AAKL/AACl/3V1yP/t7er/7e3s/+vr7P+zs+H/R0fM/wYGwf8AAMT/AADG/wAAqX0AAP8AAAAAAQAAiJcAAJ3/AACi/wAApf91dcn/7u7s/+3t7f/v7+//9PTx/+jo8P92dtr/AgLF/wAAyP8AALWkAAAABAAAAAIAAIqdAACe/wAAov8AAKX/dXXK//Dw7f/u7u7/8PDw//Pz8//7+/b/qKjl/wYGxf8AAMj/AAC4qgAACgUAAP8AAACIhAAAnf8AAKL/AACl/3d3y//x8e//8PDw//X18//q6vH/nZ3h/ygoyf8AAMT/AADH/wAAtJIAAAAAAACYAAAAgUsAAJv1AACi/wAApf9ycsr/9vby//Hx8v+7u+X/TU3M/wgIvv8AAL//AADE/wAAxfkAAKpXAADTAAAAbgAAAGYPAACVtwAAov8AAKX/MDC3/5+f2v9sbM7/FBS6/wAAuP8AALz/AADA/wAAxf8AAL3BAACOFQAAlgAAAB8AAAClAAAAhToAAJ7cAACm/wAAqf8DA67/AQGx/wAAtP8AALj/AAC8/wAAwf8AAMDiAACpQwAA3wAAADsAAAAAAAAAUQAAAP8AAACMQAAAocgAAKr9AACu/wAAsv8AALX/AAC5/wAAvf0AALvOAACqSQAAAAEAAHAAAAAAAAAAAAAAAAAAAAA3AAAA/wAAAIUaAACdagAAqK4AAK/LAACyzAAAs7EAAK5vAACbHgAA/wAAAFEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUAAAA/wAAAGsHAACJEwAAjBQAAHMIAAAAAAAAIAAAAAAAAAAAAAAAAAAAAAAA//8AAPAPAADgBwAAwAMAAIABAACAAQAAgAEAAAAAAAAAAAAAgAAAAIABAACAAQAAwAMAAOADAADwDwAA/B8AAA=='
    ACCEPT_COOKIES = [r'(.*\.)?(noodlemagazine)\.(com)']

    @try_n(2)
    def read(self):
        cw = self.cw
        session = self.session# = Session()
        videos = []
        if '/watch/' in self.url:
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
    view = soup.find('li', class_='next')
    url = None
    if view:
        url = view.find('a').attrs['href']
    while True:
        check_alive(cw)
        wvids = soup.find(id ='container').find('div', class_='video-list').findAll('a', class_='thumb')
        for wvid in wvids:
            href = 'https://spankbang.com' + wvid.attrs['href']
            if href in url_vids:
                continue
            url_vids.add(href)
            vids.append(href)
        
        if url:
            try:
                soup = downloader.read_soup('https://spankbang.com' + url, session=session)
                url = soup.find('li', class_='next').find('a').attrs['href']
            except Exception as e:
                print_(e)
        else:
            break
    
    if cw:
        vids = filter_range(vids, cw.range)
        cw.fped = True

    info['vids'] = vids
    return info
