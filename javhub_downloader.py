#coding:utf8
#title_en:Javhub
#comment:https://javhub.net/
#author:Rickelpapu
import downloader
from utils import Downloader,try_n,LazyUrl,Soup,clean_title,get_resolution
from io import BytesIO
import clf2
S1X='efghijkmnopqrstuvwxyz1789ABCDEFGHJKLNMPQRSTUVWX23456YZabcd'
class Video:
    def __init__(self,dat,nam,ses):
        self.ses=ses
        self.dat=dat
        self.filename=nam
        self.url=LazyUrl('https://javhub.net/',self.get,self)

    def get(self,_):
        dd={ch:idx for idx,ch in enumerate(S1X)}
        dataapi=fp2(self.dat,dd)
        res=self.ses.post('https://javhub.net/playapi',data='data='+dataapi)
        djson=res.json()
        return fp1(djson['playurl'],dd)

class Downloader_javhub(Downloader):
    type = 'javhub'
    single=True
    strip_header=False
    URLS=['javhub.net']
    display_name='Javhub'
    MAX_PARALLEL=1
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAABHVBMVEV3XNwAAAB3Xdx2XNx3XN12W9z///93Xd13W9x2XN13XNx3XNygjuZ3XN1tW9t2XNy0puvFuvB2XNx3Xd6Cad94XNz+AP93Xd2yo+t3XNx3Xdx4Xtx3XNx3Xdx3XN13XN12XNt4XN15X911W9ptSdtgYN93XduPeOJ3XNt2YtjIvfGJceC1pux3WtqAAICBVdVtbduAVep2Tth8Yt359/3Ty/SahuWSfePMwfN1W92+se2Kc+F+Zd52Xd13XNns6Pp4XtvEuPD8/f50W912W9wAAP/Ctu7p5fmAgIDOxPL6+v7a0/Xw7vq6re2kkueVgONsVduGb+B2YutzWdmun+rf2PeAW9t5XtepmOl3XN6Fbd/i3fd0XdzRx/N5Xd0JxAE6AAAAX3RSTlP/AP///////////uj//Q5Q//+uTf+/AZn/z/z/+5zCYk7R/zEHCE3/qw3///9gAgwHDA3///////9M////Si//Mf//UV8B//8C/////////xX/DRT//w4T/y///xb/Si8Ahi8AAAIOSURBVHichZOFbiNBDIbdgcUGN8zUcK+MV26Pmfne/zHutzdpG12kWlppZv0Z5h8PrTxgC8DGWbR+E51tLQd6/WEYkGvcRDjs9/4DCqflgIg0PiIVlE8Li8BWsUZkXPiqAHzSteLoPvAtT0Zive8T5fu88fOf7oDtvHhhJ6/350vKf5wDT4pcF3GKDpxDSxqdGNQrch8M/K0Z19fIq+ndy92JLBQaqRzFQK/MCbl/TXu/nIyFl7TCrrwpQD/w8UsO6O1dOecdjgdDFLQEGEpR1zDy89x51iElbliWgY1wtgOgaP+qZFkIrEGFIwA/AoW2+GPb+cxKieFnogug5QKFFzJyFs9oxHKbnDAF4OY2PXnW86y1nsRLxiaAdVLs1kp3StN0ulSaTg9ur42BiHcaAaY6yTiHk8dvd4/Rp5RVXKKLa+YcXGPVubTa+/OUAXSiExcAtkO444oAWMdcjg/Fv8IkC5WVaJF31XkxGAx2sGZCGRFqJQrii5ASX9LpdI514nMHKQE22wKgEDJc4qgzzYjaa/F1H2HcWDfFPYgIXNBQBXclQKHOGUCcvHFe5arIJyKo+qP5yI0aImXneDweZz4Y1h7W+Ho3tO8bGDciyGztvIHG7/tjn6xzH3F1DKdLlXpy8eE8j9qzqRJR2i2uv/j01lLZMOC3kwizKZxv2eNNXlw3m9fdWfIlwDL7ByxxJU+SbbyUAAAAAElFTkSuQmCC'
    ACCEPT_COOKIES=[r'(.*\.)?(javhub)\.(net)']

    @try_n(2)
    def read(self):
        self.urls,uth,self.title=getvid(self.url,self.cw)
        thumb=BytesIO()
        downloader.download(uth,buffer=thumb)
        self.setIcon(thumb)
        self.enableSegment()

def fp1(a1,dc):
    arr1=[0]
    for aa in a1:
        arr1=[x*58 for x in arr1]
        arr1[0]+=dc[aa]
        qq=0
        for i in range(len(arr1)):
            arr1[i]+=qq
            qq=arr1[i] >> 8
            arr1[i] &= 255
        while qq:
            arr1.append(qq & 255)
            qq >>= 8
    return ''.join(map(chr,arr1[::-1]))

def fp2(a1,dc):
    s2='JKLNMPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz123456789ABCDEFGH'
    return ''.join([s2[dc[x]] for x in a1])

def getvid(url,cw):
    res = clf2.solve('https://javhub.net/',cw=cw,timeout=5.0,delay=0.0,check_body=False)
    sesion=res['session']
    resp=sesion.get(url)
    soup=Soup(resp.text)
    sesion.headers.update({"content-type": "application/x-www-form-urlencoded; charset=UTF-8"})
    uth=soup.find(class_='big_cover')['src']
    if 'http' not in uth:
        uth='https:'+uth
    title=clean_title(Soup(f'<p>{soup.find(class_="d-inline").text.strip()}</p>').string,n=190).replace('...','')
    shd=480<get_resolution()
    may=[]
    men=[]
    for di in soup.findAll(class_='playbtn'):
        (may if di.find('span') else men).append(di['data-src'])
    datas=(may if shd else men) if (men and may) else (may+men)
    hd='HD' if datas==may else 'SD'
    videos=[]
    for pp,da in enumerate(datas):
        videos.append(Video(da,title+str(pp)+hd+'.mp4',sesion).url)
    return videos,uth,title
