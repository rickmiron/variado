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
    icon = 'base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAABLFBMVEUAAAD/RVSZ3H3/RFT/RVX+RVSD1GH8JzfzVVX8Jjf+RFSZ3HyC1GH5VVVbW1uD1WGS2XWF1WT8KDiX3HuX23r+QlGE1GKjUVipUFfaSlXPflnVb1ThSVX/O0vaZ1GlxnX7RVSM12ye1XplWVqD1GKA32GD02GFVVn+QFCV2nj4LzqR2HKJ2GKE1GOJ12mwUFeD1GKV2nb8KjpvWFrzLjqU3HmAgICC1GCD1GPEj16H01r1NDyD02JrWFqA/4CxsWyb3X6Y3HyZ3H6F1GKZ3XeY3XqJ02p3V1r3UVfBTVf0NT2Z3H3la1/JlGvlUkn9MkKD1GKwunTDnmzwP0B2Vlua3XzxWlr8LT3KhFya3YD+OEf9LDyH1mX1PEOa3Hmb2H1qWFqE1mL+Pk2Z3HzkXfH+AAAAZHRSTlMA/////////yr/////Kv/9////////ff/////////////////iEIb//////g1N//+J////LCYC+c7/Ef9G/wL/yfdBXg9ZKf/////h/////2v/////TP///yb//9//Jv//Uf/7620OyAAAAcJJREFUeJx9kmdb2zAUhatzJRlbxhkkbFpWC5QWCnTvvffeLfD//wPnKs4DwTEnkT7o1R3nyqdq9ReP6yH1A8BJfOQ5EF7V81Ejr4Gxh/Wc+lBfJHIjCPgynDtjnTXmY8CDof2RGWvEuIBwdQgX55Y29ZJbBJ5UOaMnihVhD+4NcL8ab4RywhvmK7Bfra/EON2sqxgdUUyYWcdENIpwjDsNlcn/87wpphswVvHHxG6nmHJCp3NAZ7B/9a8/TcP1B1gf5CwdWaZ7ZmeA30frqwOuWc5QE8jqGWD86HxiBTNbfDY20yQJ0LxQ8lHhgUis/uyFjVb3TgP+8H2zCbLJHY3UAlxpwNa5fn5rlwoe3imcTkIzuO3p0E+g30e2ucJ9fkrjadSab+eBjUuRXxar9jRSXTprrZhtdrjeiPzKrWSufJ04HRqVbpL8w5o/q/wp8DZpr8YZcr7xpX8lzN/0F2OCvBVwL02Sd116ZG/ys52k08CCf9/r8Kb3TeAGr/CvSlP67/gyXrXs/Raw+P1TO03TlzOcb6flG7F+qdt57jfW+PVEdRa89z1/h9q95n3O85buuS/nN6C7j643Ilwe779PTweMMR8RIfXThQAAAABJRU5ErkJggg=='
    display_name = 'Buondua'
    MAX_PARALLEL = 2
    MAX_CORE = 6
    ACCEPT_COOKIES = [r'(.*\.)?(buondua\.com)']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    
    def read(self):
        self.print_('1.0')
        goo='/tag/' in self.url
        self.urls, self.filenames, self.title=(get_gall if goo else get_imgs)(self.url,REFERBOUN,self.user_agent,self.cw if goo else '')

def get_imgs(url,refere,user_agen,unico):
    soup = downloader.read_soup(url,referer=refere,user_agent=user_agen)
    title = soup.find('h1').text.strip()
    idz = soup.find('div', class_='article content').attrs.get('data-id')
    title = clean_title(f'{title}({idz})',n=170)
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
            ext = src[src.rfind('.'):].split('?')[0]
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
    titu = clean_title(soup.find('h1').text.strip(),n=170)
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
