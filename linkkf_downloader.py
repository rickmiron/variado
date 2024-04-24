#coding:utf8
#title_en: Linkkf
#comment: https://kr.linkkf.net/
import downloader
from utils import Downloader,try_n,LazyUrl,get_print,Soup,clean_title
from m3u8_tools import M3u8_stream
from os import makedirs, path
UAT='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

class Video:
    def __init__(self,url,cwz,dx):
        self.sub=None
        self.cw=cwz
        print_=(get_print)(cwz)
        print_('Get ofuscado')
        urlv=self.ofuscado(url)
        try:
            m=lambda: M3u8_stream(urlv,referer=self.urlr,deco=self.cortabyte,n_thread=4)
            m=m()
        except Exception as e:
            ex=e
            raise Exception(ex)
        if getattr(m,'live',None) is not None:
            m=m.live
        self.url=LazyUrl(self.urlr,lambda _: m,self)
        downloader.download(self.sub,outdir=dx,header={'referer':self.urlr},fileName=self.filename[:-3]+'vtt')
        
    def cortabyte(self,dato):
        return dato[8:]

    def ofuscado(self,url):
        try:
            soup=Soup(downloader.read_html(url,user_agent=UAT))
        except Exception as e:
            get_print(self.cw)(e)
        self.filename=clean_title(soup.find(class_='myui-panel__head').text)+'.mp4'
        cod=soup.find(id='player-left').find('script',recursive=False).text
        un=cod.find('player_post',cod.find('.click'))+13
        pagvid=cod[un:cod.find(',',un)-1]
        soup=Soup(downloader.read_html(pagvid,referer='https://kr.linkkf.net/',user_agent=UAT))
        self.urlr='https://'+pagvid.split('/')[2]
        sub=soup.find('track')['src']
        self.sub=sub if 'https:' in sub else self.urlr+sub
        return soup.find('source')['src']

class Downloader_linkkf(Downloader):
    type='linkkf'
    single=True
    strip_header=False
    URLS=['//kr.linkkf.net/']
    display_name='Linkkf'
    MAX_PARALLEL=2
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAAFcklEQVRYhYWXy28bVRTGf+fO2E7sJE5TEuhLakN3LVIRLGBJxQIBEhvYsGDBH8YCJDasKUu6QKKLCgWSZdQK2qI0LbFjx7Ede+5hcR9zx3bTRJbsuTPn8Z3zfeeMfHH/QIl/FqyCKGoUVUVUwbhrqALut6qiWATcmSioBXG/VS2KunNj/bPlveE8d1f9oVadB2eQOBcl/DuDNnnW2XLB+XOj0Tyi1XMJASgLjYvMZC6KCjE4icEF4xZ3xZbPq/+YkLlDDlHEBWDnnVtvfM55iYzMZh6e97/FB+FQdKUJsAckUMiDA2fcI2VIYGeB82rJ3NcZ5BJUK+eSION6IKm5Lsg8NJw6iMvg0obzsAsOmdS52ErNJQTubedpwy2EPfaEzmWm3ljMjJnMY83LMs0ik8cGlbJk7oL7WFUkOI9lshSqjAuLFctSJmSukC6I0LxYLIrITFlM8GXJxdpX81ytu9cbnFilYYRb7RbrueH6SgMQHg+GHE8n7PVOGKulFhpOFZMlTEhorer6KqfScIt5rsCksNxZb3K7vcz+YMhub8CD7jGgtDLD9soSX17ZYq/XZ6fXI5dEQwK0HoW0rPnree6cv7fRYrOe89OzlwyLKfVMYjePi4KDoxF/dI+5u7lBZlZ52O1SN6HhmGnYkqoGTXTAS2TJc2ViC+6sL7NZz/nl+X8UWpAbmNqibDBjaWSCxfLz80M2GzXutFeZFMG2TdjgS+51wpzHc1VX89vtJvdfdMmNoCjXluu8f2GVUVHM8byeCb++eMk7q2s0MkHjechcXUt5v8bVOOV56AN3/Va7yf7JkFM79UyArXqdDy62+fb6JS7UciYeDcdzZWgL9k9PuL226rlhUXGZS9AQL8dGZZbnGhXOYlmvZTwaDF3N8UGK8uCow49P/uWTNy/y8dZFsgymXmrrBh6dntCu1ShS+Y00LFlnKrAHjfafsbVcbzUY2CIZTA66TISJWn548oyDszHfXL3CtaUlCnVqOSim3FhuMtIiKqBEQSIyI68IRzJYCA2DE55ZHgcyifidIdELH6V3YYOiVTJXFBVLft48bxgnMq3MMA4o+KCmqtQMfH31Cs9GI75/+g9nOiUTQVVp1nIeD09YMqYaeHTu/OUIseaz8zwzyvFkwnZrmYPOiIaRaODDjXVura5w7/CAw7MxNSPkxrFhrAXbzXWOp+OKkuKHmprABsVE54GK6VQD9vp93m4ts2wkzvODsxG/H3X47snfdCZn1Iy7P/B82Rhutlrs9jtI7Hyf+YzsG7zglCOXqAOCMlbLXr/HR5sbjK1jwNPhkIfdjkMk7gauK8ZacPeNLXb7XX+/Lyug/rtoObQMEtrJZ26ShhOlZpSd4x6H4zGfvrVJJo5uuXGLi/imG2lBZuDzrUscng3Z6R1RywCPmhqnhhJYJk4H8iA4583z3MDDXpd3dY2vLl9mf9Dn0emAQTEBDM1axnazzc3mCrsnHXb6R9SSftG4gtmSLd6XfPbbXxoWxDgVk3leaDnPJ7Zw0ry2SjuvcaPZBJTHwwHdyRl7/Q5jiugcVayxseGg3KJCMF4H0r09WSBn5nlNoMDyZ69LoZZ7LwtAWTJuIcG4e0rYfbfbNCnHOpW4DwTYiTeUU25+notvKSPQMn6WeV2f57kiye4YKB/lP9IwpWJsSK1sr5XVO/RMdFAqYNh0StirShsU0OXrt+Lz9vaFC6bxgQV5PYfnVditN1nKev66vb08r87zcqp54zM8J00EqExdypLn6Yvior19IawpU9LMK87tTHDu3vJl1g2pvHQe6JHAXkEmOVs0WF7Bc3cekipZFuZyPg87cw7CpjPbUMwMFiqJ+AT8Ylq+5kf8Afgfh9I5AvOT7Y4AAAAASUVORK5CYII='
    ACCEPT_COOKIES=[r'(.*\.)?(linkkf)\.(net)']

    @try_n(2)
    def read(self):
        if not path.exists(self.dir):
            makedirs(self.dir)
        video=Video(self.url,self.cw,self.dir)
        self.urls.append(video.url)
        self.title=video.filename