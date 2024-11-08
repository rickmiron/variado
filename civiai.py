#coding:utf8
#title_en:Civitai
#comment:https://civitai.com/
import downloader
from utils import Downloader,clean_title,Soup,LazyUrl,Session
import os
import json
import requests
UAG='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
@Downloader.register
class Downloader_civitai(Downloader):
    type = 'civitai'
    URLS=['civitai.com']
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAACtVBMVEUAAAD///8TDWYQbOwSDmwQb+4MM9ILLc8QZugMOdURdvAQaesMN9MXCVULMNAUDGIREHALKs0OEXkPEHQMPdYNR9sVC1wNQdgRcu8RePPf3uoXClcYCVIOUuAPYOYNEXsOVuISD2gOUN4PXeUQY+gQEXYPWeMZCE8VDWH29vkKJswNEn4WD2b6+fwPTNwAAP8NQtgRffQNSdwNLsUQdO8QWtgQfPMMFoIYDF0QaugMNdIPJJQMOdMSHYkpHGMPN7kKJcsVE28PQ8AQPbwNWuIWGYCPjLiqp8YVFHQaC1YRd/EQII0MOdAPPrYKIsgQGIULLM0MU96fmroPVtERcu/T0+RoZ6cVbuoNStkPYuUNQ9YLLM4Sf/IQbOwaFGgOMb4MPtRaV5UPV+B1dbAKIcfv7/QRefALJMqurtAJLdMPYuYLTtzBv9YMN9JdVY4OK5sQfPQQePDRz9/r6/MPMrEPQMAQQ7oPXOMKKMsOUN0PR8MqLIcQN7UMRdcQJacWEWjy8/cRbOt9eakAVapUTYfk5O8OKa0QZui2tdMMK8sHIcoA//8PePAAAIARce4MJ8suIWYKL8sAGswAVf8MYecxM4oAAKoPPLGiosuWjrHKyNkcceMJKcQPbesIHskAbf8PdekAVNUmJ4MAIrsAM8xGRI4Pc+4PS8gPOccNbfMMN9MLMcwRI6ERbOoNM9AOSMYUO8QSJMgSf/URe+8NNc8MOtEAL9EaZuYLb+6GgasRde9iW5EAgP8MLMcMPtWWlcEQXt0Qa+sKMdAAZv8Qbu0hgN8LMM8NM9ANJs0YC1cOLZ4QPLALMdAOLsyIhrUSaOcObecQMM4LKMgSZOQRauofEVefnMEUevUMMtFeW5oSe+0NM8wPUs0Rc+/LzOBoYJIKLs0Qc+xLSZFWUY0Uf/QNSNkONsHapPOtAAAA53RSTlMA/////////////////////////////////////////////////////////////wH/+f////////////+q////+////4b//////+b///+E//CG///2//8YqoaG6mDj//+G/6r/df+p1/8gqob/6///b5v//////6q1qv///6r///9a/wP///+j/6wnATMCxMP/YgoDFf8D/////wk4myEHIwb/Dwr/aP//FaFz/0m0/w0Oyh86hQsKLv/f/wIpqv//j9YFrAjQwz3////5bv+ANh9GHJv//xlC/zoo/8z//3pd///Rhv94o80jAAACgUlEQVR4nGNABddjCjbro4khgcMxmwwNnxQcxSE9v6fQ0AwIDNNubccmH17oJQkFXmkL0GW7Vz7cxQUCJiZgymtZ+B4UBWv7QiQkJEwkmMt8LYEMCYmQu40I2YU75rKCgWVwvrm29R1LCO/IhdkQ+SkHY5nBwPSUvzYQmOcHQ/ixVy6DFZznBgHLA77m8vLyrq5Awny6KViMux2sIJIDBMq8hYCgekbGVBBte1oFJJgFUaCiomJqLSwsrLoorJWRMTW5WhXI8TYFCkMUuMjJyS0XEhDwCLunyQgEuqHJHsICqlVA4XKIAmVl5fWqAgL7dYGyxcUgJRkCAqpOQGGoAjU1tSpVFhYpoFTOo6UdIFNYWARKgcJJYAWBCgoKTmAFuudYgOCmm5sbUIEzUBiqQFZWtlSAiUmKUTORCQ4UnYHClWAF2UpKsqUsCAU6QABU4KukpARVoKen56zIzw90w7U4fv64Jnd3d35+phqgcARYwVMjIyN7RQ0NkCND8x4XgRzJr8FfAxSGKIgSFRW11xET29kAlGlIBXkzSExMowQoXAtRYGBgYK8hJmbRkgNSwqg5a7cFkFcCFIYoSBAXF1/hKA0EdnlA86Xu24HY9c+AwvsgCkSAwMe6nhcI7GYGTQDROrY+IFGIgq2cIMAT7y0tIyNz9SqQOGkbzwMWtAEruLgqlwcM2hxPqqury/A61lmB+bk2tyFJasmWdWxgYFyno65uscYYwjt+YwM8VepPPHaGDwSM/V2NwYwzh1Y3I6dq/cyz0exgIAgmAx5kTkbPGns7owWhIKBiDrYMuu1EhYMWCPRfWoxFGgQmpaQ7OKT7bcQhDQS981L8uqahCAEA87moVdISw3QAAAAASUVORK5CYII='
    display_name='Civitai'
    MAX_PARALLEL=2
    MAX_CORE=4
    ACCEPT_COOKIES=[r'(.*\.)?(civitai\.com)']
    user_agent=UAG

    def read(self):
        self.single=True
        self.title,self.urls=(model if'm/models/'in self.url else imgs)(self.url,self.dir)
        self.single=False

def model(url,dix):
    cok=Session().cookies.get('__Secure-civitai-token')
    urls=[]
    soup=Soup(downloader.read_html(url,user_agent=UAG))
    idx=url.split('/models/')[1].split('/')[0].split('?')[0]
    titulo=clean_title(soup.find('h1').text,n=170)+'('+idx
    content=soup.find(class_='mantine-1iztkyj').find(class_='mantine-1uhluxa').find('div')
    [a.unwrap() for a in content.findAll('ul')]
    tex=[a.text for a in content.findAll(recursive=False)]
    tex+=[a['href'] for a in content.findAll('a')]
    tejson=json.loads(soup.find(id='__NEXT_DATA__').text)
    for m in tejson['props']['pageProps']['trpcState']['json']['queries'][5]['state']['data']['modelVersions']:
        idm=str(m['id'])
        if not urls:
            urls.append(Text(dix+'/'+titulo,idx,'\n'.join(tex)).url)
            ara=m['files'][0]['url'].split('storage.com/')[1].split('/')
            user=ara[1] if ara[0]=='model' else ara[0]
        rex=requests.get(f'https://civitai.com/api/trpc/image.getInfinite?input=%7B%22json%22%3A%7B%22modelVersionId%22%3A{idm}%2C%22prioritizedUserIds%22%3A%5B{user}%5D%2C%22period%22%3A%22AllTime%22%2C%22sort%22%3A%22Most%20Reactions%22%2C%22limit%22%3A20%2C%22pending%22%3Atrue%2C%22cursor%22%3Anull%2C%22authed%22%3Atrue%7D%2C%22meta%22%3A%7B%22values%22%3A%7B%22cursor%22%3A%5B%22undefined%22%5D%7D%7D%7D')
        pjs=rex.json()
        for j in pjs['result']['data']['json']['items']:
            urls.append(Image(j['url'],idm+'/'+str(j['id'])+'.'+j['mimeType'].split('/')[1]).url)
        hss=[h['type']+':'+h['hash'] for h in m['files'][0]['hashes']]
        soup=Soup((m['description']or'').replace('<ul>','').replace('</ul>',''))
        tex=[a.text for a in soup.findAll(recursive=False)]
        tex+=[a['href'] for a in soup.findAll('a')]
        texx='ID\n'+idm+'\n\nNAME\n'+m['name']+'\n\nBASEMODEL\n'+m['baseModel']+'\n\nHASHES\n'+'\n'.join(hss)+'\n\nDESCRIPTION\n'+'\n'.join(tex)
        for f in m['files']:
            urls.append(File('https://civitai.com/api/download/models/'+idm+'?type='+f['type']+'&format='+f['metadata']['format'],idm+'/'+f['name'],cok).url)
        urls.append(Text(dix+'/'+titulo+'/'+idm,idm,texx).url)
    return titulo,urls
def imgs(url,_):
    urls=[]
    usna=url.split('/user/')[1].split('/')[0]
    nex,ne2='null','undefined'
    while True:
        rex=requests.get(f'https://civitai.com/api/trpc/post.getInfinite?input=%7B%22json%22%3A%7B%22browsingLevel%22%3A31%2C%22period%22%3A%22AllTime%22%2C%22periodMode%22%3A%22published%22%2C%22sort%22%3A%22Newest%22%2C%22username%22%3A%22{usna}%22%2C%22followed%22%3Afalse%2C%22draftOnly%22%3Afalse%2C%22pending%22%3Atrue%2C%22include%22%3A%5B%22cosmetics%22%5D%2C%22cursor%22%3A{nex}%2C%22authed%22%3Atrue%7D%2C%22meta%22%3A%7B%22values%22%3A%7B%22cursor%22%3A%5B%22{ne2}%22%5D%7D%7D%7D')
        rjn=rex.json()
        for t in rjn['result']['data']['json']['items']:
            for i in t['images']:
                urls.append(Image(i['url'],str(i['id'])+'.png'if i['type']=='image'else'.mp4').url)
        nex=rjn['result']['data']['json']['nextCursor']
        if not nex:
            break
        nex,ne2='%22'+nex+'%22','Date'
    return usna,urls
class Image:
    def __init__(self,urx,idx):
        urx=f"https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/{urx}/original=true/"
        self.filename=idx
        self.url=LazyUrl(urx,lambda _:urx,self)
class File:
    def __init__(self,urx,idx,cok):
        self.c=cok
        self.filename=idx
        self.url=LazyUrl(urx,self.get,self)

    def get(self,url):
        res=requests.head(url,cookies={'__Secure-civitai-token':self.c})
        if res.status_code==307:
            return res.headers['location']
        return url
class Text:
    def __init__(self,dix,name,cont):
        self.filename=name+'/content.txt'
        self.cont=cont
        self.url=LazyUrl(dix,self.ruait,self)

    def ruait(self,dix):
        try:
            os.makedirs(dix)
        except:
            pass
        with open(dix+'/content.txt',"wb")as f:
            f.write(self.cont.encode())
        return dix+'/content.txt'
