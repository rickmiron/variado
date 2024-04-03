#coding: utf8
#title_en: Kemono.Su
#comment: https://kemono.su/
import downloader
from utils import Downloader,Soup,urljoin,get_ext,clean_title,get_print,LazyUrl
from translator import tr_
import os
KEM='https://kemono.su'
TXT='/content.txt'
@Downloader.register
class Downloader_kemonosu(Downloader):
	type='kemono.party'
	URLS=['kemono.party','kemono.su']
	icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAAAIGNIUk0AAHomAACAhAAA+gAAAIDoAAB1MAAA6mAAADqYAAAXcJy6UTwAAABpUExURQAAAAAAAAAAAAAAAAAAAAgDAQUCAQoFAioUCDQZCgAAAGIvFBEIA0MgDQQCAA0GAhIIAz0eDItEHHo7GA8HA04lEKhSIrNXJJlKH91rLcBdJ89lKl4tE3E3F+lxL+ZwLyQRBwEAAP///x3CqNsAAAAVdFJOUwAoCRVAd66L77pR5p7WY8Xb+f72/e5VQwgAAAABYktHRCJdZVysAAAAB3RJTUUH6AQBEQoHApBGhAAAAcFJREFUOMt1U9uCqyAMRARRRBEsICgX//8nN2q39exp5wVjhsmFBFUYfUdNMKK0/u5vGEKk7cj7F69r/jKqzoCBO9s/RWqOBeUNJpdJBtdXcI6LXy6RWjIxSTnK6hTrw9odCVZ9sO4SGdt2M6oV8Ilp75ylp5QISwz6EKkG7cBgGNVsdnGdr+y4TlrZoISYdAaEuaPd4pT1wzO3wWddtN733Vifcsrr4myZUxDPcphLaylhKfv+MA4IOaW467SMpxvzEchF5xQMiDy2AJTkzZb76grBpnYNR/TkdTkoMazBxrJNQkCZFSESLl24RPZHeZyHJBijqpna6PMvw8f9CWDJpjmKb5TNL0C6lz9CR4wEP5Xt5vIN2+k3PiVnJOOQA2utv0nYI34JUKxVDRAQn5RxN4aPqhQN/jWqBp4NjyNVRi+3IN6vcMFFJRp2PCduGqGmQzPfI0XZMnx2qqY1laT3/xDWYaJEvKZx5Igud4mkR0rRe1ohUt2tb0aCWcJ/h5nPN4WZo/+AhfuVgEn4tC3V8MqzJ+gTRn1JJMe+LFJ3NcOf6/AJpD/amJ7T/glsM0Vtw/dtrabjqUf0HZyxP+v+AyXlNz7GmJY3AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDI0LTA0LTAxVDE3OjEwOjA2KzAwOjAwVR9kVQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyNC0wNC0wMVQxNzoxMDowNiswMDowMCRC3OkAAAAodEVYdGRhdGU6dGltZXN0YW1wADIwMjQtMDQtMDFUMTc6MTA6MDcrMDA6MDDVIPaCAAAAAElFTkSuQmCC'
	display_name='Kemono.Su'
	MAX_PARALLEL=1
	MAX_CORE=4
	single=True

	def read(self):
		dix=self.dir
		self.single=False
		px='/post/' in self.url
		self.title,self.urls,self.filenames=(rid_post if px else rid_user)(self.url,self.cw,dix)
		if px:
			titu=self.filenames[self.urls[0]]
			self.cw.setTitle(titu[:titu.find('/')])

def rid_user(url,cw,dix):
	fis=[]
	nafi={}
	nga=0
	while url:
		soup=Soup(downloader.read_html(url))
		if nga<1:
			titu=clean_title(soup.find('meta',{'name':'artist_name'})['content'])
		for a in soup.find('div',class_='card-list__items').findAll('a'):
			_,us,fn=rid_post(KEM+a['href'],cw,dix)
			fis+=us
			nafi.update(fn)
			nga+=1
			cw.setTitle(f'{tr_("읽는 중...")} {titu} - {nga}')
		Next=soup.find('a',class_='next')
		url=KEM+Next['href'] if Next else None
	return titu,fis,nafi

def rid_post(url,cw,dix):
	print_=get_print(cw)
	soup=Soup(downloader.read_html(url))
	idp=soup.find('meta',{'name':'id'})['content']
	usu=clean_title(soup.find('a',class_='post__user-name').text.strip())
	info=clean_title(f'{idp}-{soup.find("h1").text}-{usu}')
	imgs=[]
	tex=[]
	fns={}
	# Downloads
	for ite in soup.findAll('li',class_='post__attachment'):
		href=urljoin(url,ite.find('a')['href'])
		ext=get_ext(href)
		fns[href]=f'{info}/{len(imgs):04}{ext if ext!=".bin" else href[href.rfind("."):]}'
		imgs.append(href)
	# Files
	fis=soup.find('div',class_='post__files')
	if fis:
		for ite in fis.findChildren(recursive=False):
			a=ite if 'href' in ite.attrs else ite.find('a')
			href=urljoin(url,a['href'])
			# Imgur
			if 'imgur.com/' in href:
				print_(f'Imgur: {href}')
				try:
					from extractor import imgur_downloader
					for img in imgur_downloader.get_imgs(href):
						ext=get_ext(img) or downloader.get_ext(img)
						fns[img]=f'{info}/{len(imgs):04}{ext}'
						imgs.append(img)
				except Exception as e:
					print_(e)
				continue
			if '.kemono.' not in href:
				tex.append(href)
				continue
			fns[href]=f'{info}/{len(imgs):04}{get_ext(href)}'
			imgs.append(href)
	# Content
	cont=soup.find('div',class_='post__content')
	if cont:
		for img in cont.findAll('img'):
			src=img.get('src')
			if not src:
				continue
			src=urljoin(url,src)
			fns[src]=f'{info}/{len(imgs):04}{get_ext(src)}'
			imgs.append(src)
		for a in cont.findAll('br'):
			a.replace_with('\n')
		for a in cont.findAll(recursive=False):
			tex.append(a.text)
		for a in cont.findAll('a'):
			src=a.get('href')
			if src:
				tex.append(src if 'http' in src else KEM+src)
	if tex:
		imgs.append(Text(dix+'/'+usu+'/'+info,info,'\n'.join(tex)).url)
	return usu,imgs,fns

class Text:
	def __init__(self,dix,nam,ct):
		self.filename=nam+TXT
		self.ct=ct
		self.url=LazyUrl(dix,self.ruait,self)
	
	def ruait(self,dix):
		try:
			os.makedirs(dix)
		except:
			pass
		with open(dix+TXT,"wb") as f:
			f.write(self.ct.encode())
		return dix+TXT
