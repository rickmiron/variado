#coding:utf8
#title_en:Highporn
#comment:https://highporn.net/
#author:Rickelpapu
import downloader
from utils import Downloader,try_n,LazyUrl,Soup,clean_title
from io import BytesIO
import clf2
from time import time
class Video:
    def __init__(self,dat,nam,ses):
        self.ses=ses
        self.dat=dat
        self.filename=nam
        self.url=LazyUrl('https://highporn.net/',self.get,self)

    def get(self,_):
        if len(self.dat)>20:
            url=self.dat
        else:
            res=self.ses.post('https://play.openhub.tv/playurl?random='+str(int(time()*1000)),data=f'v={self.dat}&s=highporn')
            url=res.text
        return fp1(url)

class Downloader_highporn(Downloader):
    type = 'highporn'
    single=True
    strip_header=False
    URLS=['highporn.net']
    display_name='Highporn'
    MAX_PARALLEL=1
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAY1BMVEXaJ1j////aJ1naJljbJ1j+/////v/bJlj///7aJlnbJ1ntmK/yscP99fj/+vzcMWDxrsDfQm3jWX7cL1/++Pjskqr41d7hU3rbLFzhUXjqhKHbKVr2yNXxrcDhTnb3z9rjXIBSDL0oAAABuElEQVR4nE1Th5aDMAyLMyDQUrqvt+//v/IkOaE1D7LsSJZNCCHhgeUQIseQMMMqxjD5Tsp55J68dKoIninSLY0hYcsdsR85w8hhwjsnTLHAR0fNjTF8aZwSYyanlBAVHQhcuI9B+Ih3jjRQ4/UI5W39npcBDphFz1MO30ut9vvTyXc28MlTmterWTGrZnbSYROo2xsOaBVOds6d/IZ3wvZQBncqtoaR/KkIrwHXwYZq5XA8HuhVr+KX9GEO4SxsT7zYYOVBhiDHzAlyJ8LF0S6Y2r7nDeVQrQiEoQBXtSSNZUpYSkxKm0HQ9p30XnASccuFQXBAUXNIO9AsG3oAQEhSAOWQPDvq5dFKhnYHRiFJrncgiYxG1tSdMtKktcx2FPypYgb3kCVgPRxvH7E5QJHXUpyGWgpgkO9MkjazmdgtkcxULOhHqvbeIEZRcEVpq1fB6voHx4WSCV0Vo4IxfO4XXHHL4cuuD6q6EfAFANWh2UHH3n/q9md70ZcqogQuA78I6SlBaflu7YvbpQOjHAm/wISGcwL+O7WQ9qdlNRk3uw8xJUsTHj2+JaBRB3Oe5RETWqgR4Ok//AwJ+haTbAsAAAAASUVORK5CYII='
    ACCEPT_COOKIES=[r'(.*\.)?(highporn)\.(net)']

    @try_n(2)
    def read(self):
        self.urls,uth,self.title=getvid(self.url,self.cw)
        thumb=BytesIO()
        downloader.download(uth,buffer=thumb)
        self.setIcon(thumb)
        self.enableSegment()

def fp1(a1):
    dc={ch:idx for idx,ch in enumerate('789ABCDEFGHJKLNMPQRSTUVWX23456YZabcdefghijkmnopqrstuvwxyz1')}
    arr=[0]
    for a in a1:
        arr=[x*58 for x in arr]
        arr[0]+=dc[a]
        q=0
        for i in range(len(arr)):
            arr[i]+=q
            q,arr[i]=divmod(arr[i],256)
        while q:
            arr.append(q&255)
            q>>=8
    return ''.join(map(chr,arr[::-1]))

def getvid(url,cw):
    res = clf2.solve('https://highporn.net/',cw=cw,timeout=5.0,delay=0.0,check_body=False)
    sesion=res['session']
    resp=sesion.get(url)
    soup=Soup(resp.text)
    sesion.headers.update({"content-type": "application/x-www-form-urlencoded; charset=UTF-8",'referer':'https://highporn.net/'})
    uth=soup.find('meta',{'property':'og:image'}).attrs['content']
    title=clean_title(soup.find("h3").text.strip(),n=190)
    datas=[di['data-src'] for di in soup.findAll(class_='playlist_scene') if di.has_attr('data-src')]
    videos=[Video(da,title+str(pp)+'.mp4',sesion).url for pp,da in enumerate(datas)]
    return videos,uth,title