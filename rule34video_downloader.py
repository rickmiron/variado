#coding:utf8
#title_en:Rule34Video
#comment:https://rule34video.com/

import downloader
from utils import Downloader, Soup, try_n, LazyUrl, get_print, clean_title, check_alive, get_resolution
from error_printer import print_error
import subprocess
from timee import sleep
import os
USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

class Video:
    def __init__(self, url, cwz):
        self.cw = cwz
        self.referer = 'https://rule34video.com/'
        self.filex = ''
        self.url = LazyUrl(url, self.getx, self)

    def getx(self, urlz):
        if not self.filex:
            self.get(urlz)
        sleep(10)
        urlse = pythonexter(self.filex)
        get_print(self.cw)('getx fin '+urlse)
        return urlse

    @try_n(2)
    def get(self, url):
        print_ = get_print(self.cw)
        try:
            soup = Soup(downloader.read_html(url,user_agent=USERAGENT))
        except Exception as e:
            print_(print_error(e))
        title = soup.find('h1', class_='title_video').text.strip()
        infor = soup.find('div', class_='cols').findAll('div', class_='col')
        artis = ''
        for inf in infor:
            label = inf.find('div', class_='label').text.strip()
            if label == 'Artist:' :
                names = inf.findAll('span', class_='name')
                if len(names) < 4 :
                    artis = '-'.join(map(texto, names))
                    break
                continue
            elif label == 'Uploaded By:' :
                artis = inf.find('a', class_='name').text.strip()
        m1 = url.find('/',url.find('.') + 6) + 1
        m2 = url.find('/', m1)
        self.filename = artis + ')' + clean_title(title) +'('+ url[m1:m2] + '.mp4'
        reso = get_resolution()
        files = soup.find('div', class_='video_tools').find('div', class_='wrap').findAll('a')
        for iii in files:
            if reso < int(iii.text.replace('MP4','').replace('p','')):
                continue
            file = iii.attrs['href']
            break
        print_('getfile '+file)
        self.filex=file

def pythonexter(url):
    comans = [
        "python",
        "import requests",
        f"u = '{url}'",
        "r = requests.head(u,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'})",
        "if r.status_code == 302:",
        "   print(r.headers['Location'])",
        "elif r.status_code < 300:",
        "   print(u)",
        "else:",
        "   print(r.status_code)",
        ""
    ]
    proceso = subprocess.Popen(["cmd"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    for line in comans:
        proceso.stdin.write((line + "\n").encode("utf-8"))
    proceso.stdin.close()
    output, _ = proceso.communicate()
    output = output.decode("utf-8", errors="ignore")
    return output.splitlines()[-3] , output

def texto(f):
    return f.text.strip()

class Downloader_rule34video(Downloader):
    type = 'rule34video'
    strip_header = False
    URLS = ['rule34video.com']
    MAX_CORE = 2
    single =True
    display_name = 'Rule34Video'
    icon = 'base64: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'
    ACCEPT_COOKIES = [r'(.*\.)?(rule34video)\.(com)']
    user_agent = USERAGENT

    def read(self):
        self.single, self.title, self.urls  = get_videos(self.url, self.dir, self.cw)
        self.enableSegment()

@try_n(2)
def get_videos(url, dirx, cw=None):
    local = {dx[dx.rfind('(')+1:dx.rfind('.')]:raiz+'/'+dx for raiz, _, archivos in os.walk(dirx) for dx in archivos}
    vids = []
    singlex = '.com/v' in url
    if singlex:
        only = Video(url, cw)
        only.get(url)
        title = tte = only.filename
        tte = tte[tte.rfind('(')+1:tte.rfind('.')]
        vids.append(local[tte] if tte in local else only.url)
    else:
        if '.com/me' in url and '/favourites/' not in url and 's' not in url[-2:] :
            url += 'videos/' if '/' == url[-1:] else '/videos/'
        print_ = get_print(cw)
        soup = Soup(downloader.read_html(url,user_agent=USERAGENT))
        url_vids = set()
        if '.com/mo' in url:
            header = 'Artist'
            title = soup.find('h1').find('span').text.strip()
            url += '?mode=async&function=get_block&block_id=custom_list_videos_common_videos&sort_by=post_date&from='
        elif '.com/m' in url:
            header = 'Member'
            title = soup.find('div', class_='channel_info').find('h2').text.strip()
            if '/favourites/' in url:
                header += ' Favourite'
                url += '?mode=async&function=get_block&block_id=list_videos_favourite_videos&sort_by=&from_fav_videos='
            else:
                url += '?mode=async&function=get_block&block_id=list_videos_uploaded_videos&sort_by=&from_videos='
        elif '.com/c' in url:
            header = 'Category'
            title = soup.find('h1').find('span').text.strip()
            url += '?mode=async&function=get_block&block_id=custom_list_videos_common_videos&sort_by=post_date&from='
        elif '.com/t' in url:
            header = 'Tag'
            title = soup.find('h1').text.strip()
            title = title[title.find('h') + 2:]
            url += '?mode=async&function=get_block&block_id=custom_list_videos_common_videos&sort_by=post_date&from='
        elif '.com/s' in url:
            header = 'Search'
            title = soup.find('h1').text.strip()[12:]
            url += '?mode=async&function=get_block&block_id=custom_list_videos_videos_list_search&sort_by=&from_videos='
        elif '.com/p' in url:
            header = 'Playlists'
            title = soup.find('h1').text.strip()
            url += '?mode=async&function=get_block&block_id=playlist_view_playlist_view&sort_by=added2fav_date&from='
        if not title:
            raise Exception('No title')
        print_(title)
        title = f'{header}]{title}'
        view = soup.find('div', class_='pagination')
        ultimo = 2
        if view:
            pagi = view.findAll('a')
            last = pagi[len(pagi) - 3].attrs['data-parameters']
            pagi = None
            ultimo = int(last[last.rfind(':') + 1:]) + 1
            last = None
        for p in range(1, ultimo):
            check_alive(cw)
            if p > 1:
                try:
                    soup = Soup(downloader.read_html(url + str(p),user_agent=USERAGENT))
                except Exception as e:
                    print_(e)
            for wvid in soup.findAll('a', class_='th'):
                href = wvid.attrs['href']
                if href in url_vids:
                    continue
                m1 = href.find('/',href.find('.') + 6) + 1
                m2 = href.find('/', m1)
                tte = href[m1:m2]
                vids.append(local[tte] if tte in local else Video(href, cw).url)
                url_vids.add(href)
    return singlex, title, vids
