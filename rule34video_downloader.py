#coding:utf8
#title_en:Rule34Video
#comment:https://rule34video.com/
import downloader
from utils import Downloader,Soup,try_n,get_print,clean_title,get_resolution,File
import subprocess
from timee import sleep
import os
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import DEFAULT_CIPHERS
UAG='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
REF='https://rule34video.com/'
def pythonexter(url):
    comans=[
        "python",
        "import requests",
        f"u = '{url}'",
        "r = requests.head(u,headers={'referer':'"+REF+"','User-Agent': '"+UAG+"'})",
        "if r.status_code == 302:",
        "   print(r.headers['Location'])",
        "elif r.status_code < 300:",
        "   print(u)",
        "else:",
        "   print(r.status_code)",
        ""
    ]
    proceso=subprocess.Popen(["cmd"],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    for line in comans:
        proceso.stdin.write((line+"\n").encode("utf-8"))
    proceso.stdin.close()
    output,_=proceso.communicate()
    output=output.decode("utf-8",errors="ignore")
    return output.splitlines()[-3]

def texto(f):
    return f.text.strip()

class File_rule34video(File):
    type='rule34video'

    def get(self):
        if not self['filex']:
            self.getx(self['urlx'])
        sleep(6)
        urlse=pythonexter(self['filex'])
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
            if label=='Artist:':
                names=inf.findAll('span',class_='name')
                if len(names)<4:
                    artis='-'.join(map(texto,names))
                    break
            elif label=='Uploaded By:':
                artis=inf.find('a', class_='name').text.strip()
        m1=url.find('/',url.find('.')+6)+1
        self['filename']=clean_title(artis+')'+title,n=191)+'('+url[m1:url.find('/',m1)]+'.mp4'
        reso=get_resolution()
        for a in soup.find('div',class_='video_tools').find('div',class_='wrap').findAll('a'):
            if int(a.text.replace('MP4','').replace('p',''))<=reso:
                file=a.attrs['href']
                break
        print_('getfile '+file)
        self['filex']=file

class Downloader_rule34video(Downloader):
    type='rule34video'
    strip_header=False
    URLS=['//rule34video.com']
    MAX_CORE=2
    single=True
    display_name='Rule34Video'
    icon='base64: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'
    ACCEPT_COOKIES=[r'(.*\.)?(rule34video)\.(com)']
    user_agent=UAG

    def read(self):
        self.print_('1.06')
        self.single,self.title,self.urls=get_videos(self.url,self.dir,self.cw)
        self.enableSegment()

@try_n(4)
def get_videos(url,dirx,cw):
    local={dx[dx.rfind('(')+1:dx.rfind('.')]:raiz+'/'+dx for raiz,_,archivos in os.walk(dirx) for dx in archivos}
    vids=[]
    singlex='.com/v' in url
    if singlex:
        vidx=File_rule34video({'referer':REF})
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
                vids.append(local[tte] if tte in local else File_rule34video({'urlx':href,'filex':''}))
                url_vids.add(href)
    return singlex,title,vids
