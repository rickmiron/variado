#coding: utf8
#title_en: Buondua
#comment: https://buondua.com/
import downloader
from utils import Downloader, clean_title
from translator import tr_
REFERBOUN = 'https://buondua.com/'

@Downloader.register
class Downloader_buondua(Downloader):
    type = 'buondua'
    URLS = ['buondua.com']
    icon = 'base64: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'
    display_name = 'Buondua'
    MAX_PARALLEL = 2
    MAX_CORE = 6
    ACCEPT_COOKIES = [r'(.*\.)?(buondua\.com)']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    
    def read(self):
        if '/tag/' in self.url:
            self.urls, self.filenames, self.title = get_gall(self.url,REFERBOUN,self.user_agent,self.cw)
        else:
            self.urls, self.filenames, self.title = get_imgs(self.url,REFERBOUN,self.user_agent,'')

def get_imgs(url,refere,user_agen,unico):
    soup = downloader.read_soup(url,referer=refere,user_agent=user_agen)
    title = soup.find('h1').text.strip()
    idz = soup.find('div', class_='article content').attrs.get('data-id')
    title = clean_title(f'{title}({idz})')
    last = len(soup.find('div', class_='pagination-list').findAll('a')) + 1
    imgs = []
    filenames = {}
    num = -1
    if unico:
        unico = title+unico
    for i in range(1,last):
        if i > 1:
            soup = downloader.read_soup(f'{url}?page={i}',referer=refere,user_agent=user_agen)
        views = soup.findAll('p')
        for p in views:
            src = p.find('img').attrs['src']
            ext = src[src.rfind('.'):]
            if ext == '.jpeg':
                ext = '.jpg'
            src = src.replace('i1.wp.com/','',1)
            #imgs.append('https://'+src[src.find('.com/')+5:])
            imgs.append(src)
            num += 1
            filenames[src] = unico+str(num) + ext
    return imgs, filenames, title

def get_gall(url,refere,user_agen,cw):
    soup = downloader.read_soup(url,referer=refere,user_agent=user_agen)
    titu = clean_title(soup.find('h1').text.strip())
    galerias = []
    nga = 0
    elementos = soup.findAll('h2')
    for h2 in elementos:
        galerias.append(h2.find('a').attrs['href'])
    Next = soup.find('a', class_='pagination-next')
    Next = Next.attrs['href'] if Next else "j"
    cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), titu, nga))
    while '/' in Next:
        Next = 'https://buondua.com'+Next
        soup = downloader.read_soup(Next,referer=refere,user_agent=user_agen)
        elementos = soup.findAll('h2')
        for h2 in elementos:
            galerias.append(h2.find('a').attrs['href'])
        Next = soup.find('a', class_='pagination-next').attrs['href']
    files = []
    namefiles = {}
    for gale in galerias:
        urls, filenames, _ = get_imgs('https://buondua.com'+gale,refere,user_agen,'/')
        files += urls
        namefiles.update(filenames)
        nga += 1
        cw.setTitle('{}  {} - {}'.format(tr_('읽는 중...'), titu, nga))
    return files, namefiles, titu[:titu.rfind('(')-1]
