#coding:utf8
#title_en: NjavTV
#comment:https://njav.tv/
from utils import Downloader,try_n,LazyUrl,get_print,Soup,clean_title
from error_printer import print_error
from m3u8_tools import M3u8_stream
from downloader import read_html as get,download
from io import BytesIO

class Video:
    def __init__(self,url,cwz):
        self.cw=cwz
        urlv=self.getx(url)
        get_print(cwz)(urlv)
        m=lambda: M3u8_stream(urlv,referer='https://javplayer.me/',deco=self.cbyte,n_thread=4)
        try:
            m=m()
        except Exception as e:
            raise e
        if getattr(m,'live',None) is not None:
            m=m.live
        self.th=BytesIO()
        download(self.uth,buffer=self.th)
        self.url=LazyUrl(url,lambda _: m,self)
    def cbyte(self,dato):
        return dato[8:]
    @try_n(2)
    def getx(self,url):
        print_=get_print(self.cw)
        try:
            soup=Soup(get(url))
        except Exception as e:
            print_(print_error(e))

        self.uth=soup.find(id='player')['data-poster']
        self.filename=clean_title(soup.find('h1').text.strip()+'.mp4')
        if len(self.filename)>209:
            self.filename=self.filename[:205]+'.mp4'
        idv=soup.find(id='page-video')['v-scope']
        un=idv.find('id: ')+4
        idv='https://njav.tv/en/ajax/v/'+idv[un:idv.find(',')]+'/videos'

        try:
            idv=get(idv)
        except Exception as e:
            print_(print_error(e))

        un=idv.find('url')+6
        idv=idv[un:idv.find('"',un)].replace('\\','')
        try:
            soup=Soup(get(idv))
        except Exception as e:
            print_(print_error(e))

        idv=soup.find(id='player')['v-scope']
        soup=Soup(f'<p>{idv}</p>')
        idv=soup.string
        un=idv.find('https')
        return idv[un:idv.find('"',un)].replace('\\','')

class Downloader_njavtv(Downloader):
    type = 'njavtv'
    single=True
    strip_header=False
    URLS=['njav.tv']
    display_name='NjavTV'
    MAX_PARALLEL=2
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAAXNSR0IArs4c6QAABPBJREFUWEeVV11sFFUUPudOK9SICv3Z2W0gARuwRvEnUaSwU41P+GJITI2+QeTBF2I7s9vYGAMxRqTTgokmjYT44oNgfDHxxcQwO1uIEhP/kJQgBFNiZ6U2Gtq0AjPH3PnZuTN7Z7vsw3Z759xvv/t955x7FmGVFwIANYkJnvN3/moWmQSJcDHxBfVVAKQAzhkY76E23IOAowDULyMUb8OPiXlTqlW6IOOctRcWBo5vutXuVgHoqloxnuebb+z6YJ2rKNMAsD0Gyz5pCnweEE+oFX0sVkiujo84VzRnEGEb/+wx2Kt4mCOgKV9Zvg9jRXiMv8y1IwloksmSh96eQqVc9Q8hkcAnUNNMovjh7wDQh4BALbifBBa+QSAPBKdV23hFjI3wfQKOZiaOkpl40oRpdDsj7JxqG7uiaJFfoEBGpsdgCITe3wS0l93GSzcfWPNv3/KCu7C84d7/Om4VFBf2EUI5DRPYVX87otrGW0GMUD9pBTK8upCrGo/Frsh1qmnm2wT4bqI4hVDFdXu7z43+GeFILZDK5NGzuenS9z73jPyL9t0oHst76F4kgAfjpK23ia9U23gpWm8kQHAAEE6IMvHPLuBTvbb+Y309ahQZ1vnVpY3PI2BnWqt81cDI85hAGMUYFF3w+tBjnwrYS8tssWuLdWglnSuZCcsPvHOyw2nzriODDYmCWkv3qd+UliIVwBk0/YrzwRTcqZ7Rv3MGJ18Dovd5LboIxV5bn5V3suxy5fGzz3zU2bZ2ZV5sZuS5Q4Wz5S+4CgkL+D8KsR1d1ZHzye63So8PmUW5Uf8b2u4UJz4BpAMRJgFM5W3jjVgBoQ94jD1dsEZ+kFnbTO504or7ay8cz9GdO05kAxFM56tGscECvsCY92SPVf5JWs+ZCSd2i6h7J61xtIk/AGhTGPmLapce90uVL8wlOiHbrtojvzZJ7nSBBG0l82oIiDiaeRYABkLcy6ptbJVboLBHC2dGfhOaVYpL3MGSmZE0KG2Xo018DUAvhuyvqba+uU5AbMVtDPq7LGNmVQUyPEqYIfSKmmaeIoAhKQGxFd8Gb+tGu3w5qI8mLY9f0TzLpQUSlUVQBvzmc7TxkICPeUWtGn3Bk/Rt6CkP5aeHr7Y0XGVcezL1nEHzFBAM8S0ewEzeNvqlOUBM2Zy3hq+1kPAtuBQznNPMk4iwPxxwflYrxhNSAu3M3dhpjV5vAV0cmOIrN+OO8AkA7A9xz6u2sUNKgDEv32OVHZFA4JRkPqofMJjZmt1PSQJYUW39uYAAAjjFiXAGBsD2NjX37Zu1xplAUmapWTGhWio/HO3ohwB4MBwwP1crpVfrM4NYBcSgO28Z8/KL524m/6SJnAAiO+hfQB5O5qZ1XWrBGqasX28N/9PQiGSnvZsq0MZDBXzZSzlbN6UEFNe9v/vs6E1pEvpf2GgFj5XOCUJobfDoESI2GuDS66pdOtlIAAEYLq7rsQ4vti52sun4oJL+5RTN9wBxzPed8OVcVf9S2opzrLMDrX0rzcswOlorF3SAFBCAMf6ZIdN6KiP+j5VkJ0SgXEVXELFec+IPFD843JU5x6eZhxxrRfMwIbzDH4t55mPO7TZnkME2BJjL2UYhmYCtn1Lg15ATtd3HthBzrxDBpUK19HB0Qp8APXL6nr+6Zj9ziQ4VqqWLmf5ncGlclgRm7P0fnCtBQfdRM4sAAAAASUVORK5CYII='
    ACCEPT_COOKIES=[r'(.*\.)?(njav)\.(tv)']
    @try_n(2)
    def read(self):
        video=Video(self.url,self.cw)
        self.urls.append(video.url)
        self.title=video.filename
        self.setIcon(video.th)
