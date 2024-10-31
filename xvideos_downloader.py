#coding:utf8
#title_en:Xvideos
#comment:https://www.xvideos.com/
import downloader
from utils import Downloader, try_n, LazyUrl, get_print,Soup,clean_title,get_resolution
from m3u8_tools import M3u8_stream
from io import BytesIO
REFER = 'https://www.xvideos.com/'

class Video:
    def __init__(self, url, cwz):
        self.cw = cwz
        get_print(cwz)('Get ofuscado')
        urlv = self.get(url)
        m = lambda: M3u8_stream(urlv,referer=REFER, n_thread=6)
        try:
            m = m()
        except Exception as e:
            raise e
        if getattr(m, 'live', None) is not None:
            m = m.live
        self.thumb = BytesIO()
        downloader.download(self.urlthumb, buffer=self.thumb)
        self.url = LazyUrl(REFER, lambda _: m, self)

    @try_n(2)
    def get(self, url):
        soup = Soup(downloader.read_html(url,user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'))
        uno = url.find('/v')+1
        id_ = url[uno+6:url.find('/',uno)]
        title = soup.find('title').text[: -14]
        canal = soup.find('li', class_='main-uploader').find('span', class_='name').text.strip()
        actor = '('
        for model in soup.findAll('li', class_='model'):
            actor += model.find('span', class_='name').text.strip()+'-'
        actor=actor[:-1]
        lentitle = len(actor)
        if lentitle>80:
            actor = actor[:80]
            lentitle = 80
        lentitle=len(canal)+len(title)+lentitle+len(id_)-248
        if lentitle>0:
            title=title[:-lentitle]
        self.filename = clean_title(f'{canal}){title}{actor}({id_}.mp4')#.format(canal, title, actor, id_)#[:-1])
        self.urlthumb = soup.find('meta', {'property': 'og:image'}).attrs['content']
        def sin_atributos(tag):
            return tag.name == 'script' and not tag.attrs
        script = soup.find(id ='video-player-bg').findAll(sin_atributos)[1].text
        uno = script.find('.setVideoHLS') + 14
        script = script[uno:script.find(')',uno) - 1]
        file = downloader.read_html(script,referer=REFER)
        res=get_resolution()//100
        for ele in [10,7,4,3,2]:
            if ele>res:
                continue
            uno = file.find('"'+str(ele))
            if uno == -1:
                continue
            uno = file.find('\n',uno)+1
            file = file[uno:file.find('\n',uno)]
            break
        return script.replace('hls.m3u8',file)

class Downloader_xvideos(Downloader):
    PRIORITY = -1
    type = 'xvideos'
    single = True
    strip_header = False
    URLS = ['xvideos.com/']
    display_name = 'Xvideos'
    MAX_PARALLEL = 2
    icon = 'base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAA4VBMVEX////hNR////7+/////v/gNR/hNB/hNR7//v7+/v/56Of+//7////////////56Ob56ejso6D/+/v88fH//P0AAAD////99/b++fn77e3kXlX55eTlZl/uq6jpjIj89PP77+/hOCTjSj3qlJHvsrDhNyHxwb7kWlD33Nrnf3nzy8jrnZnlbmfhPSr22df44N/jUETne3bxv7zpi4bwtrP21tTpj4viSDn44uHzzMvohX/55ubwurj00dHmdW/ohYDiPSzwuLfiRDXogn3iQzPrmpbyxcPsoZ3oiYTmeHL32tro2cfvAAAAS3RSTlP///////////////8lrfT///////8A7v/////////////////////////////////////////////////////////////////////n40T0AAACO0lEQVR4nE1Th3YiMQyUZHsryy6wCST09F4uvVzv9/8fdCN5X14MD2NJlmY0Mm30qj69W56cbULe9aveBvU2YXCURbeQ4Os8AmAW2uxR5cRcOJdqsgyaBDmwVWT5pS3qpijqUYkAoWxc4FA35DO4xbmc6IY55XBNOfyULXBgPkB0txy97HPCaTgygB/gTZIB0GiE90ggNEBA4D9qnJ7r/c9D0tQgY9z8ageXOH0kmpwlqDZbKkijbH6hr7jFvFsiV0jTndrqg70SszXZDowiTbuteO/QB9ABYrg1Bv150gxhIArxVa3WuK6BGYq1fzVivTV+4FP1OPFlxAAyFvkPRBKe0/x4KLG/eSzf+cnfa40fy61RvFZ2BbQPWi2nZg2U4VZcpldMCwNJTgk7L6srEOETNUI407YroQeh4bXyPJXWjCY4ArteYZff6HAyG2/tWk6TPYoBn0b/UonWl8PjcGHdkVgHTPRD9HiubXjN9jh80iI6cxFDhDBCh5mf2yPdTnSw9F4JZ+4oB8DnBAivVu0hNOXDSXcRHTCQ4ucKIP0o9BOqJ3z7Bj6qlT2BQEgH+PvCAePwMCJXGsa4pt/gD2cTZXef6kAi1ubJ6ObLmdq+TO2BXNrg7Nda3+sPdF5gRAIfeEBHju9AyWFhLYo67OGc8E18XI7uEAxNLjot+5LhlWCN3waoaJqmLlRzkT5VpiqUybrhxK/CRz2k8xUer46uso76m4ZKHXvm8Hjt+cOAryJElDKL7dfn/x/2GxxnisHJ4wAAAABJRU5ErkJggg=='
    ACCEPT_COOKIES = [r'(.*\.)?(xvideos)\.(com)']
    
    @try_n(2)
    def read(self):
        video = Video(self.url, self.cw)
        self.setIcon(video.thumb)
        self.urls.append(video.url)
        self.title = video.filename