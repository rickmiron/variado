#coding:utf8
#title_en:Rule34Video
#comment:https://rule34video.com/
import downloader
from utils import Downloader,Soup,try_n,get_print,clean_title,get_resolution,File
from timee import sleep
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import DEFAULT_CIPHERS
UAG='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF='https://rule34video.com/'
def pythonexter(url,kuk):
    r=requests.head(url,headers={'Cookie':'PHPSESSID='+kuk,'User-Agent':UAG})
    if r.status_code == 302:
        res=r.headers['Location']
    elif r.status_code < 300:
        res=url
    else:
        raise Exception(r.headers)
    return res

def texto(f):
    return f.text.strip()

class File_rule34video(File):
    type='rule34video'

    def get(self):
        if not self['filex']:
            self.getx(self['urlx'])
        sleep(6)
        urlse=pythonexter(self['filex'],self['k'])
        get_print(self.cw)('getx fin '+urlse)
        sesion=requests.session()
        sesion.mount('https://',HTTPAdapter(max_retries=3))
        sesion.verify=True
        sesion.headers['User-Agent']=UAG
        ciphers=':'.join(DEFAULT_CIPHERS.split(':!SSLv3'))
        sesion.hooks['response']=[lambda r, *args, **kwargs: setattr(r.connection, 'default_socket_options', [('SSL_CTX_set_cipher_list', ciphers)])]
        sesion.hooks['response']+=[lambda r, *args, **kwargs: setattr(r.connection, 'default_socket_options', [('SSL_CTX_set_options', 'TLSv1.3')])]
        sesion.head(urlse)
        return {'url':urlse,'name':self['filename'],'session':sesion}

    def getx(self,url):
        print_=get_print(self.cw)
        try:
            soup=Soup(downloader.read_html(url,user_agent=UAG))
        except Exception as e:
            print_(e)
        title=soup.find('h1',class_='title_video').text.strip()
        artis=''
        for inf in soup.find('div',class_='cols').findAll('div',class_='col'):
            label=inf.find('div',class_='label').text.strip()
            if label=='Artist':
                names=inf.findAll('span',class_='name')
                if len(names)<4:
                    artis='-'.join(map(texto,names))
                    break
            elif label=='Uploaded by':
                artis=inf.find('a', class_='name').text.strip()
        m1=url.find('/',url.find('.')+6)+1
        self['filename']=clean_title(artis+')'+title,n=191)+'('+url[m1:url.find('/',m1)]+'.mp4'
        reso=get_resolution()
        for a in soup.find('div',class_='video_tools').findAll('div',class_='wrap')[-1].findAll('a'):
            if int(a.text.replace('MP4','').replace('p',''))<=reso:
                file=a.attrs['href']
                break
        print_('getfile '+file)
        self['filex']=file
@Downloader.register
class Downloader_rule34video(Downloader):
    type='rule34video'
    strip_header=False
    URLS=['//rule34video.com']
    MAX_CORE=2
    MAX_PARALLEL=2
    single=True
    display_name='Rule34Video'
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAABHVBMVEUAAADXMz7kOETtOkX6QUzqO0bmOEX+Qk7oOUXvPEj3P0v8QU3aND/pOUbdNUD0Pkr9QU3+Qk39QE3bNEDfNkHiN0LlOETwPUjgNkHjN0TfOED5QEzhN0PtO0fZND/hNkLyPUn7P0zyPEndNUH/Qk7mMzP1Pkj9QU3zPkn7QE3aND/XMz7cNUDgNUHnOEjvQEjyPEr0P0vYMz/vO0j9Qk3+Qk7cNT//Qkr9QkzxPkjZMz/1QEv/AADuOkf/AIC/QED1PkrqQFXdMjv4PkvwPUnmM0z1PUf/QEDYND/dNT/zPEr0P0rwPUj/O07uPEjgNkLYND/1P0jtQEnbMT3+QE3ZND/jOUfnOEDXMED5P03/QVDYNj7wPkz1QEraNT+JQkjFAAAAX3RSTlMA//9G/////////////////+3//////////yD////////y////Ck7t//Lh32pqICAmaqXfp+ThH+hq32kB+QIE+AwevGUKGQjFhibXeQ1q73Y1HCqy+xIgIGogISEYp74cdI8AAAGkSURBVHicxdJpV4JAFAbgC4KAqEyIIrlAWGnmkpmZ2r7v+779/5/RnQFt1O91P8DhzHPmvtwZ+Ivaf50N6qXRaHzBfbPZPA6Xuu9dgO94Kpm0sm5azEQTcmGvbfsV446tHxBF6UA/jsLK5hGoqixH2ppXMRYZWCLK/Az0iwgWaD1H1YQcOdJsfwh0Ck6r1ep60DJDAXDAVJQZPi4NgUDzvGELMglUBuzKEOjYgisRQzDgX9DPTck0wx1SpZLlph0xk0BQ0GzPMGKxXE7SCQkBnQT+qEh3KGCICoIYBz5qtVq9XncwRATg8LrXa7VagzdJ182xDI6oUjCqOWkKsB1+QU43yzxITwLJJGVYFoRiPARONDrRIgT0OPBH8xhiHEg6BUUGkpbr4iTGM0iYYVugPUZ3gs90gpO4Gn25N+wlb/GEr7OHABSmVoRVqKYArDxkcNQIVnwPJw0gEbwwHHDBwQQU2JdgULABawwIQAdhZSEvIpAR+HiaCDoBAOG2uANQyuIkARIynGsD2A12eFQYEJ7wWbLoqPHSwSc7boAcMQkD/14/N7Us67y1Ju4AAAAASUVORK5CYII='
    ACCEPT_COOKIES=[r'(.*\.)?(rule34video)\.(com)']
    user_agent=UAG

    def read(self):
        self.print_('1.09')
        self.single,self.title,self.urls=get_videos(self.url,self.dir,self.cw)
        self.enableSegment()

@try_n(4)
def get_videos(url,dirx,cw):
    local={dx[dx.rfind('(')+1:dx.rfind('.')]:raiz+'/'+dx for raiz,_,archivos in os.walk(dirx) for dx in archivos}
    vids=[]
    singlex='.com/v' in url
    res=requests.head(REF)
    kuk=res.cookies.get('PHPSESSID')
    if singlex:
        vidx=File_rule34video({'k':kuk})
        vidx.getx(url)
        title=vidx['filename']
        vids.append(vidx)
    else:
        if '.com/me' in url and '/favourites/' not in url and 's' not in url[-2:]:
            url+='videos/' if '/'==url[-1:] else '/videos/'
        print_=get_print(cw)
        soup=Soup(downloader.read_html(url,user_agent=UAG))
        url_vids=set()
        tte='?mode=async&function=get_block&block_id='
        if '.com/mo' in url:
            header='Artist'
            title=soup.find('h1').find('span').text.strip()
            url+=tte+'custom_list_videos_common_videos&sort_by=post_date&from='
        elif '.com/m' in url:
            header='Member'
            title=soup.find('div',class_='channel_info').find('h2').text.strip()
            if '/favourites/' in url:
                header+=' Favourite'
                a='favourite'
                b='_fav'
            else:
                a='uploaded'
                b=''
            url+=tte+f'list_videos_{a}_videos&sort_by=&from{b}_videos='
        elif '.com/c' in url:
            header='Category'
            title=soup.find('h1').find('span').text.strip()
            url+=tte+'custom_list_videos_common_videos&sort_by=post_date&from='
        elif '.com/t' in url:
            header='Tag'
            title=soup.find('h1').text.strip()
            title=title[title.find('h')+2:]
            url+=tte+'custom_list_videos_common_videos&sort_by=post_date&from='
        elif '.com/s' in url:
            header='Search'
            title=soup.find('h1').text.strip()[12:]
            url+=tte+'custom_list_videos_videos_list_search&sort_by=&from_videos='
        elif '.com/p' in url:
            header='Playlists'
            title=soup.find('h1').text.strip()
            url+=tte+'playlist_view_playlist_view&sort_by=added2fav_date&from='
        if not title:
            raise Exception('No title')
        print_(title)
        title=f'{header}]{title}'
        view=soup.find('div',class_='pagination')
        ultimo=2
        if view:
            last=view.findAll('a')[-3].attrs['data-parameters']
            ultimo=int(last[last.rfind(':')+1:])+1
        for p in range(1,ultimo):
            if p>1:
                try:
                    soup=Soup(downloader.read_html(url+str(p),user_agent=UAG))
                except Exception as e:
                    print_(e)
            for wvid in soup.findAll('a',class_='th'):
                href=wvid.attrs['href']
                if href in url_vids:
                    continue
                m1=href.find('/',href.find('.')+6)+1
                tte=href[m1:href.find('/',m1)]
                vids.append(local[tte] if tte in local else File_rule34video({'urlx':href,'filex':'','k':kuk}))
                url_vids.add(href)
    return singlex,title,vids
