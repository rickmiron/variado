#coding:utf8
#title_en: Missav
#https://missav.com/
#author: Rickelpapu
'''
Missav Downloader
'''
import downloader
from utils import (Downloader, try_n, LazyUrl, get_print,Soup,
                   clean_title)
from error_printer import print_error
from m3u8_tools import playlist2stream, M3u8_stream

class Video:
    def __init__(self, url,cwz):
        self.cw = cwz
        urlv = self.ofuscado(url)
        ms = [
            lambda: playlist2stream(urlv,referer='https://missav.com', n_thread=8),
            lambda: M3u8_stream(urlv,referer='https://missav.com', n_thread=8),
            ]
        for m in ms:
            try:
                m = m()
                break
            except Exception as e:
                e_ = e
        else:
            raise e_
        if getattr(m, 'live', None) is not None:
            m = m.live
        self.url = LazyUrl(url, lambda _: m, self)
    
    @try_n(2)
    def ofuscado(self, url):
        '''
        get
        '''
        print_ = get_print(self.cw)
        try:
            soup = Soup(downloader.read_html(url,user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'))
        except Exception as e:
            print_(print_error(e))
        codigo = soup.find('meta', {'property': 'og:url'}).attrs['content']
        codigo = codigo[codigo.rfind('/')+1:].upper()
        title = soup.find('h1').text.strip()
        un = title.find(' ')
        if un == -1:
            un = len(title)
        self.filename = clean_title(codigo + title[un:] + '.mp4')
        if len(self.filename) > 209:
            self.filename = self.filename[:205]+'.mp4'
        codigo = soup.findAll('script', {'type': 'text/javascript'})[2].text.strip()
        un = codigo.find('eval(')
        codigo = codigo[un:codigo.find('.split(',un) - 1]
        un = 0
        for _ in range(3):
            un = codigo.find('://',un + 1)
        inpu = codigo[un-1:codigo.find(';',un)-2]
        k_array = codigo[codigo.find(',\'',un) + 2:].split('|')
        narray = []
        for car in inpu:
            num = ord(car)
            if 47 < num < 58:
                narray.append(k_array[num - 48])
            elif 96 < num < 123:
                narray.append(k_array[num - 87])
            else:
                narray.append(car)
        return ''.join(narray)

class Downloader_missav(Downloader):
    '''
    Downloader
    '''
    type = 'missav'
    single = True
    strip_header = False
    URLS = ['missav.com']
    display_name = 'Missav'
    MAX_CORE = 8
    MAX_PARALLEL = 2
    icon = 'base64:AAABAAEAICAAAAEAIAAoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAABAAAAAAAAAAAAAAEAAAABAAEAgGPjEodi7luLYvmeimL2zYpi9+qNYfz+jWH8/opi9uqKY/bNi2L5nodi71uAY+MSAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAEAAAAAAAAAgGDsKIhi9Z6MYvr0jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OY/7/jmL+/4xi+vSJYvWegGDsKAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgWrVDIhf9I6MYvz4jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmP+/45i/v+MYvz4iV/1joBq1AwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAINk7CmKYfnTjmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+PYv7/jmL+/45i/v+OYv7/jmL+/49i/v+OYv7/jmL+/45i/v+OYv7/imH404Nk7CkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACCZOszjGH66Y5i/v+OY/7/jmL+/45i/v+PYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i//+OYv7/jmL+/45j/v+PYv7/jGH66YJk6zMAAQAAAAAAAAAAAAAAAQAAAAABAAAAAAAAAAAAg2TsKYxh+umOYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45j//+OYv7/jmL+/45i/v+PYv7/jmL+/45i/v+PYv7/jmL+/45j//+OYv7/jmL+/45i//+PYv7/jGH66YNk7CkAAAEAAAABAAAAAAAAAAAAAAABAIBq1AyKYfjTjmP+/45i/v+OYv7/jmL+/45j/v+OYv//jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45j/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/imH404Br1AwAAAAAAAAAAAAAAAAAAAAAiF/0jo5i/v+OYv7/jmL+/49i/v+OYv7/jmL+/45i//+OYv7/jmL//49i/v+PYv7/j2L+/45i/v+OYv7/jmP+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i//+OYv7/j2L+/45i/v+OYv7/iF/0jgABAAAAAQAAAAAAAIBh7CiMYvz4j2L+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv//jmL+/45i/v+OYv7/jmL+/45j/v+OYv7/jmL//45i/v+OYv7/jmL+/45i/v+OY/7/jmL+/45i//+OYv//j2L+/49i/v+MYvz4gGDsKAAAAAAAAAAAiWL0no5i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/597/f/g1vv/zLn9/5Zv/P+OYv7/jmL//45i/v+OYv7/jmP+/45j/v+PYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+JYvWeAAAAAIBj4xKNYvr0jmL+/45j//+OYv7/jmL+/45i/v+OYv7/jmP+/45i/v+OYv7/xrL4///+////////9fL+/7qh/P+QZP3/jmL+/49i/v+OYv7/jmL+/45j/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/4xj+vSAY+MSh2LuW45j/v+OYv//jmL+/45i/v+OYv7/jmL//45i//+OYv7/jmL+/45i/v/Itvj////+///////+/////////+be/P+oiPz/jmL+/45i/v+OYv7/j2L+/45i/v+OYv7/jmL+/45i/v+PYv7/jmL+/45i/v+OY/7/jmL+/4di7luLYvmejmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmP+/8i2+P////////////////////7///////39///Tw/z/mHL7/45i/v+OYv7/jmL+/49i/v+OYv7/jmL+/45i/v+PYv7/jmL+/45i/v+OYv//i2L4nopi9s2OYv7/j2L+/49i/v+OY/7/jmL+/45i/v+OYv7/j2L+/45i/v+OYv7/yLb4//7///////////////////////////////7////39f7/v6j6/5Fm/v+PYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45j/v+KYvbNimL36o5i/v+OYv7/jmL+/49i/v+OYv7/jmL+/45i//+OYv7/jmL+/45i/v/Itvj//v///////////////v////7//v//////////////////////6uL9/6uM/P+OYv7/jmL+/45i/v+OYv7/j2L+/45j/v+OYv7/jmL+/4pi9+qNYfz+jmL+/45i/v+OYv7/jmP+/45i/v+OYv7/jmL+/45j/v+OYv//jmL+/8i2+P////////7///7//v////////////////////////7//////////////v7//6aH+/+OY/7/jmL+/49i/v+OYv7/jmL+/45j/v+OYv7/jWH8/o1h/P6OYv7/j2L+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/yLb5/////////////v////////////////////7//////////v/////////9/f7/pIP6/45i/v+OYv7/jmP+/45i/v+OYv7/jmL+/45i/v+NYfz+imL36o5i/v+OY/7/jmL//45i//+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v/Itvj/////////////////////////////////////////////////5t/8/6eH+v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/4pi9+qKYvbNjmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/49i/v+OYv//jmL+/8m2+P///v/////////////+////////////////////9fL9/7uj+/+QZf7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/imP3zYti+Z6OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/yLb4/////////////////////////v///f3+/9HA/P+Wbv3/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmP+/45i//+OYv7/jmL+/49i//+LYvmeh2PuW45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv//j2L+/45i/v/Itvj//////////////////////+Pa/f+igPv/jmL+/45i/v+OYv7/jmL+/45i//+OYv7/jmL+/45i/v+OYv//jmL//45i/v+OY/7/jmL+/4di7luAY+MSjGL69I5i/v+OY/7/jmL+/45i/v+OYv//jmP+/45i/v+OYv7/jmP+/8ey+f////////////Pv/f+3nPz/jmP+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45j/v+OY/7/jmL+/45i/v+OYv7/jmL+/45i/v+MYvr0gGPjEgAAAACJY/WejmL//45i/v+OYv7/jmL+/45i/v+OYv7/j2L+/45i/v+OYv7/n3n9/9/T/v/ItPz/k2r8/45i/v+OYv7/j2L+/45i/v+OYv7/jmL+/45j/v+OYv7/j2P+/45j/v+OYv7/jmL+/49i/v+OYv7/jmL+/4li9Z4AAAEAAAAAAIBg7CiMY/z4jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/j2L+/45i/v+OYv7/jmL+/45i/v+OYv//jmL+/45i/v+OYv7/j2L+/45i/v+OYv7/jmL+/45i//+OYv7/jmP+/45j/v+OYv7/jmL+/45i/v+MYvz4gGDsKAAAAAAAAAAAAAEAAIhf9I6OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45j/v+OYv7/jmL+/45j/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/4hf9Y4AAAAAAAAAAAAAAAAAAAAAgGrVDIph+NOOYv7/jmL//45i/v+OYv7/jmL+/45i//+OYv7/jmL+/45i/v+OYv7/jmL+/45j/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OY/7/j2L+/45i/v+OYv//jmL+/45i/v+KYfjTgGrUDAAAAAAAAQEAAAAAAAAAAQAAAAAAg2TsKYxh+umOYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45j/v+OYv7/jmL+/49i/v+OYv7/jmL+/45i/v+PYv//jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jGH66YNl7CkAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgmTrM4xh+umOYv7/j2L+/45i/v+OYv//jmP+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL//49j//+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+PYv7/j2L+/41h+umDZOozAAAAAAAAAAAAAAAAAAAAAAAAAQABAAAAAAAAAAAAAQAAAQAAg2TsKYph+NOOYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i/v+OYv//jmL+/45i/v+OYv7/jmL+/49i/v+OYv7/jmL+/45i/v+KYfjTg2TsKQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgGrUDIhf9I6MY/z4jmL+/45i/v+OYv7/jmL+/45j/v+OYv7/jmL+/45i/v+OYv7/j2L+/45i/v+OYv7/jmL+/45i/v+MYvz4iF70joBq1AwAAAAAAAAAAAAAAAAAAAAAAAEAAAABAAAAAAAAAQAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAIBg7CiJYvWejGL69I5i/v+OYv7/jmL+/45i/v+OYv7/jmL+/45i//+OYv7/jmL+/45i/v+MY/r0iWP1noBg7SgBAAAAAAAAAAABAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACAY+MSh2LuW4ti+Z6KYvbNimL36o1h/P6MYfz+imL36opi9s2LYvmeh2LuW4Bj4xIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEBAAAAAAAAAAAA'
    ACCEPT_COOKIES = [r'(.*\.)?(missav)\.(com)']

    @try_n(2)
    def read(self):
        video = Video(self.url, self.cw)
        self.urls.append(video.url)
        self.title = video.filename
