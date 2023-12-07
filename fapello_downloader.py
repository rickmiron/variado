#coding: utf-8
#title_en: Fapello
#comment: https://fapello.com/
import downloader
from utils import Downloader, Soup, clean_title, LazyUrl
from translator import tr_
USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

class Downloader_fapello(Downloader):
    type = 'fapello'
    URLS = ['fapello.com']
    icon = 'base64:AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAODQ3/Hx0b/x8cG/8fHRv/Hx0b/x8dGv8eHBr/Hx0b/x8cG/8fHBv/Hxwb/x8dG/8fHRv/Hh0b/x8cGv8PDQ3/Hxwa/0A8N/9BPDj/Qj06/0I8Ov9DPT7/REBL/0M+QP9CPT3/Qz07/0I8Ov9CPTj/Qj06/0I9Of9BPDn/Hxwa/yAeJP9HQ17/RkFV/0E9Pf9AOzf/SENi/1tZ2f9PS4z/R0Nh/0E7Nv9BPDv/Qz0//0A8OP9CPT//QjxB/x4cG/8oJE3/Ylzq/11Xz/9IQ2D/Pjo1/0U/Tf9YU7n/YVre/01Ifv9EPkr/VlCp/1tVwP9EP1D/Tkl//0pEb/8eHB3/IB4p/09Ig/9mXOL/WE+i/z86Nv8+ODP/QTxB/2BXyv9iWdX/ZVnV/21i/v9sYfr/TUd1/1BLh/9APEL/HBsZ/xwaGf89ODT/SkNn/11Rrv9ZTJj/Rz9X/0tDY/9tXOD/dWP//3Ri//90Y/7/cmH4/05Gdf9VS4n/Pjg6/x0aGf8cGhj/PDc0/zs2Mf8+OTz/VUqI/2tYyv91X+b/emP7/3xl//99ZP//c17i/3li9P9cTZj/Wk2V/z04OP8cGhj/GxgY/zo1M/86NTP/OjQz/zo0Mf9FPVL/VEd+/2ZTsP+GZv7/g2T5/1tLjv94Xtz/gWPz/3Rb0f9BOkT/GhkW/xoYF/85NTH/OTQw/zk0MP85NDH/ODQu/zYyKv9cSof/j2j+/29Usv8+OEP/eVrI/5Bp//+KZfT/TUFh/xkYFP8aGBb/NzMx/zczMP82MzH/NzIw/zczMP83Miz/WEZ4/4dg3P9EOkz/OjQ2/3FVsP+MY+v/lWj6/1ZFcv8YFhL/GRcW/zYxLv82MC//NzAu/zcxLv83MS7/NTEt/z82Qf9LPVr/NjEu/zYxL/85MjX/XUZ//5hn8f9UQ2r/FxYS/xgXFf80MCz/NTAt/zQwLf81MC3/NDAs/zUwLf80MCz/Mi8r/zQwLf81MC3/NDAt/3NQn/+ka/z/hVvB/yMbJP8YFxX/My8s/zMvLf8yLiz/My8s/zMvLP8zLy3/My8s/zMvLP8zLyz/My8t/zYwMP+IW7//sG///6Zq8f83JUj/FxQU/zIsKv8yLiv/Mi4r/zIuK/8yLiv/Mi4r/zMuK/8yLyv/Mi8r/zIvKv8yLSr/YkZ6/5ti2f+BVa3/Ihsm/xcUFf8xLSv/MSwq/zAsKv8xLCr/MSwq/zEsKv8wLCr/MCwq/zAsKv8xLCr/MSwq/zMtK/86MTn/NS4x/xYUEv8LCwn/FhQT/xcVEv8WFBP/FhQT/xYUEv8XFBP/FxUS/xcUEv8XFRP/FhUS/xYVE/8XFBP/FhQS/xYVEv8LCwj/'
    display_name = 'Fapello'
    PARALLEL = 2
    MAX_CORE = 2
    ACCEPT_COOKIES = [r'(.*\.)?(fapello\.com)']
    user_agent = USERAGENT

    def read(self):
        self.title, imvs = get_imgs(self.url,self.cw)
        for i in imvs:
            self.urls.append(i.url)

class Image:
    def __init__(self, idc, url,idd):
        self.referer = idc
        self.filename = idd
        self.url = LazyUrl(idc, lambda _: url, self)

class Video:
    def __init__(self, idc, url,idd):
        self.referer = idc
        self.filename = idd
        self.segment = {'chunk': 2**20, 'n_threads': 4, 'overwrite': False}
        self.url = LazyUrl(idc, lambda _: url, self)

def get_imgs(url,cw):
    soup = Soup(downloader.read_html(url,user_agent=USERAGENT))
    title = clean_title(soup.find('h2').text.strip())
    imgs = []
    imga = soup.find(id='content').findAll('a')
    for a in imga:
        href = a.attrs.get('href')
        idd = href[href.find('/',20)+1: -1]
        url = a.find('img').attrs.get('src')
        url = url[:url.rfind('_')]
        imgs.append(Image(href, url+'.jpg', idd+'.jpg'))
        if a.find('img', class_='w-16 h-16'):
            resu = downloader.requests.head(url+'.mp4',headers={'Referer':'https://fapello.com/'})
            if resu.status_code != 404:
                imgs.append(Video('https://fapello.com/', url+'.mp4', idd+'.mp4'))
            else:
                imgs.append(Video('https://fapello.com/', url+'.m4v', idd+'.m4v'))
    show = soup.find(id='showmore')
    if show:
        cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, 32))
        model = soup.find('link', {'rel': 'canonical'}).attrs['href'][20:-1]
        last = int(show.attrs.get('data-max')) + 1
        for p in range(2,last):
            url = f'https://fapello.com/ajax/model/{model}/page-{p}/'
            soup = Soup(downloader.read_html(url,user_agent=USERAGENT))
            imga = soup.findAll('a')
            for a in imga:
                href = a.attrs.get('href')
                idd = href[href.find('/',20)+1: -1]
                url = a.find('img').attrs.get('src')
                url = url[:url.rfind('_')]
                imgs.append(Image(href, url+'.jpg', idd+'.jpg'))
                if a.find('img', class_='w-16 h-16'):
                    resu = downloader.requests.head(url+'.mp4',headers={'Referer':'https://fapello.com/'})
                    if resu.status_code != 404:
                        imgs.append(Video('https://fapello.com/', url+'.mp4', idd+'.mp4'))
                    else:
                        imgs.append(Video('https://fapello.com/', url+'.m4v', idd+'.m4v'))
            cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), title, p*32))
    return title, imgs
