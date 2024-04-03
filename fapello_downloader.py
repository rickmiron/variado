#coding: utf-8
#title_en: Fapello
#comment: https://fapello.com/
import downloader
from utils import Downloader,Soup,clean_title
from translator import tr_
UAG='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
FAP='https://fapello.com/'

class Downloader_fapello(Downloader):
    type='fapello'
    URLS=['fapello.com']
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAABXRJREFUWEeVV1tslEUU/maLgMVwqa0YAlpaet3dbtttty0FqUiBKL6AIjHhQZSYEAw+aEjgQU3EhDeITxLvMSSCMdGCIVpClVJ2u9vdbXe3u71xEQWUoJaLtNDdMTPz//Nfd1v/h/bfc86c+c4355w5PwFAoXsIE/A/TChfpAWTMDkllNtYTAkBqMGl3r3lna8vraoxwbBAsnEitmZbCVDZHp2dKZ6x1AA43hWVNWK1IXzV2rTKSBGEh5lHrIc5koqBEAJaWukWDOQORVmbw1CvYsfD/TGW7B2PMgDMorzKY8+f6lDn2JoV5qVWgHmEILHufRA4kKZpVHXuBwHBcLKf/6dlNgBs4+SJZx+NeghmrYMAqWcOWPK5vHM/RgZ5DhBaXp2FATteDBQoP0zpIsET4GT9qyhd+KS5zvBa6GN8cv575QicdTnzWFXyfRTvEsc0uVP2cAFONO+2MnDmPYwmogJAhUsBoEvoGeWj0i4MtjZFk2zbpwtQIK7s+gBD8YgKoH5GDExT6rZqVgNDbXu1UqXAhsBHuDx5C0PxMANAaJVbA2CqJFlAWkGwojLyw3VyoZaOqmj9oidwyL2Zl7qr+zAyGVajFEkBALS6xmtAr7qX7SVH7SVWvQFn94c5GSyaNRddzTu5zYHhn3D0zxR/HxzoUwE0WABomyu72zS7jtotKJlXyDPBee6I5oMALxaW4N3ydi5jiUtUiqYm4Qx8rgAICQDO2ka7e8cAyi7Z4807ZPf0+r/AJE3LNfGWHbasZCZuoyZynOsS0aAA4KpjDPyPvGfNiACxxu0A6zTK4w58Kd8HfNtBmM7E3MELPfjqxii3i0cYAALq9vjs95+mxgd82wxRpmkGdcFjXOadV4DPnOstd0xd8GtMZSi/J2LRXsGA29ukdRjZdbK3XdVkoGGzhea3hnvw463rkDpTAteEvlVKBoj1KQBqvC2MCCNb+n6q00TrN3HUzr4OJLzPCwAmpjzhE+iv32QERynPEV/0lHZMfX7BgMfbzI8gG+NMHvG0w+HIs0ksU4gUcId/QMz7rJyoPJFT6K/biO+uj+GdayMSdL8E0LDSWgXK4LF1YRH2FbsFbRQYf3AfCx6abZvhdsLum1ex+0oK0dq1aOnvwj2akXv1h3oEA7WNrTbTH+B3NmN23iy+d9ugH+PpKb7H0RIXqh5ZmBWEnsmtqRBG7k8g7FoJT/wc8nTVFg2eE/vW+VqFM4XNvmofiMPBRU2JAB5Qlh+inkQbpji8pAyrHy3MMUsK1dsXkzh9dxzHSl04fuMavrl9UzkCikjveRXAKhlN2KW15ZdGEhiZnLCNlJVRn9PYwu2yyP/3Tez6/RK2LFiEnYuXYuNwTPqL9HYrR9C0GnsLH8O2osXqIMfLsiGpGZsTNMQmad6DKLyDMbxeUIidjy9RCNase//5C7uu/gbGZ8eKSjw3Ku4Bti4cUADseXoDDhUvl2cQv3MXznn58KUGbaMPVlYLWwVAY1Kxo0Cw2mlY05QcREY5wFClEw2phMyCkP+sYOCVNe34dHmxXHj21jha589HU2pYSw0CrM3Px8Fly6RdfWoI4YoKNA4NSTv28mZBAV5eXIQ9l39Fz7/3lHiBUEUZf980dgF/TGUQCvwsADS2rEEGwGxCkM7QbHMnPHPm4EjxUp6IE+k0nhq9iM7SYqwbuyRrW51ZFXKyt3gAQb8OwDRtn28w10HwywrB1KU79/DC1es4XbIM7ReuZC3JXN8bwfMKAN/KNnErma+u7G6tGn1DtJkLbcYJ9PZ0iSNgAKZ/rBDtQWcbn6zyoATQ2qZ0WuFyps9Mjk31ZbUlCPScEd+GWb8tdaDt4hIyTZN9dFQt1fC0IP8DdDkiKdFGTnYAAAAASUVORK5CYII='
    display_name='Fapello'
    MAX_PARALLEL=2
    MAX_CORE=2
    user_agent=UAG

    def read(self):
        self.title,self.urls=getfx(self.url,self.cw)

class Failx:
    def __init__(self,idc,url,idd,sg):
        self.referer=idc
        self.filename=idd
        self.segment=sg
        self.url=url

def getfx(url,cw):
    imgs=[]
    p=1
    while True:
        soup=Soup(downloader.read_html(url,user_agent=UAG))
        if p==1:
            title=clean_title(soup.find('h2').text.strip())
            show=soup.find(id='showmore')
            last=int(show.attrs.get('data-max'))-1 if show else 0
            mod=soup.find('link',{'rel':'canonical'}).attrs['href'][20:-1]
            soup=soup.find(id='content')
        for a in soup.findAll('a'):
            href=a.attrs.get('href')
            idd=href[href.find('/',20)+1: -1]
            url=a.find('img').attrs.get('src')
            url=url[:url.rfind('_')]
            imgs.append(Failx(href,url+'.jpg',idd+'.jpg',False).url)
            if a.find('img',class_='w-16 h-16'):
                ext='.mp4'
                resu=downloader.requests.head(url+ext,headers={'Referer':FAP})
                if resu.status_code==404:
                    ext='.m4v'
                imgs.append(Failx(FAP,url+ext,idd+ext,True).url)
        if last<p:
            break
        cw.setTitle(f'{tr_("읽는 중...")} {title} - {p*32}')
        p+=1
        url=f'{FAP}ajax/model/{mod}/page-{p}/'
    return title,imgs
