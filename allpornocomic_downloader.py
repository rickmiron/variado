#coding: utf-8
#title_en: Allporncomic
#https://allporncomic.com/
from utils import LazyUrl, clean_title, try_n, Downloader, check_alive
from translator import tr_
import requests
from bs4 import BeautifulSoup


class Downloader_allporncomic(Downloader):
    type = 'allporncomic'
    URLS = ['allporncomic.com']
    icon = 'base64:AAABAAEAICAAAAEAIAAoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAEBAAEAAAAAAAEAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAQAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAP///v/Pz8//dHV0/y4vL/8EBAT/AAAA/wAAAP8BAAD/AAAA/wgJCP82Njb/fn5//9vb2/8AAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAADJyMn/QkNC/wICAv8oKCj/dXR0/6+vr//S0tP/5eTl/+Xl5f/Q0dH/qamp/2xsbP8eHh//BAQE/1NSUv/X19f/AAAAAAABAQAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAABAAAAAQD39/b/cXBw/wQEBP9BQED/v7+///z9/f///v///v7///////////7///////7+/////v/////+//v7+/+wsbH/MDAw/wgICf+Hh4b/AAAAAAEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQAAAAAAAAAAAAAAAAAAAAAA7O3t/zo6Ov8AAAD/MDAw/4WEhf+FhYX/hYWF/4WFhf+FhYX/hYWF/4WEhf+FhYX/hYSE/4WFhf+FhYX/hYSF/4WFhf+BgYH/IiIi/wEAAP9SUlL/AAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAO/v7/8wMDD/Hh4e/1xcXP9cXFz/HB0c/wAAAP8BAAH/AAAA/wAAAP8BAQD/AAAB/wEAAP8AAAD/AAAA/zMzM/9cXFz/XFxc/1xcXP9cXF3/XFxc/xAREP9GRkb/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD7+/v/RkZG/xwdHf/h4OD//v/+///+/v9LS0v/AAAA/wAAAf8AAAD/AAAA/wABAP8AAQD/AAAA/wEBAP9AQED/9PX0//7+/v/+/v7//v/+//7+/v/+//7/ysrK/w4ODv9iYmL/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAImJiP8ICAj/zczM//7+///+/v7//v7+/0tLSv8AAQH/AAAA/wAAAP8AAAD/AAAB/wABAP8BAAD/Ozs7//Hx8P/+/v7//v7+///+///+//7////+//7//v/+////sbGw/wEBAf+pqan/AAAAAAAAAAAAAAAAAAAAAAABAADh4OH/CwoK/4eHh//+/v///v////7+/////v7/S0tL/wAAAf8AAAD/AQAA/wAAAf8AAAD/AQEA/zY3Nv/v7+///v/+//7+/v/+/v7//v7+//7+/v///v7//////////v///v7/Z2dn/xoaGv8AAAAAAAAAAAAAAAAAAAEAAAAAAGZmZv8AAAH/0dHR///+/v/+/v7//v7+//7+//9KSkv/AQAB/wABAP8AAAD/AAAA/wAAAP8AAAD/oqKi//7+/v/+/v////////7+/v///v//9PT0//7+///+/v7//v7+//7+/v/r6+v/EBAQ/4eHh/8AAAAAAAABAAAAAADs7O3/CgoK/wABAP/T0tL//v7+//7+/v/+/v7//v7+/0tLS/8BAQH/AAAA/wAAAP8BAAD/AAAA/wAAAP+ioqL//v7+//7+/v/+/v7//v7+//7+/v8fHx///P39//7//////v///v7+//7///9MTEz/Hx4e/wEAAAAAAAAAAAAAAJ+fnv8BAAD/AQAB/9LS0//+/v7//v/+//7+/v/+//7/SktL/wAAAP8AAAH/AAAA/wAAAP8AAAD/AAAA/6Kiov/+/v7//v7+//7+/v/+/v///v7+/x8fH//+/////v7+//7+/v///v7//v7+/05PT/8AAAD/v7+//wAAAAAAAAEAWFlY/woKCv8AAAD/0tLS//7+///+/v7//v7+//7+/v9YWFj/EhIS/xISE/8FBAT/AAAA/wAAAP8AAAD/oqKi//7+/v////7//v7+//7+/v/+/v7/Hh8f//7+/v/+//7//v/+//7+/v/+/v7/Tk9P/wAAAP94eXj/AAAAAAAAAAAiIiL/Ojo6/wAAAP/S0tL//v7+//7+/v///v///v7+//39/f/9/fz//f39/8PDwv8MDQz/AAAA/wAAAP+io6P//v7+//7+/v/+/v7//v7///7//v8fHx///v7///7+/v/+/v///v7+///+/v9OTk//AQEB/0RERf8AAAAAAAAAAAYGBv9iY2P/AAAB/9LS0//+/v////7+//7+/v/+/v7//v7+/////v/+/v////7+/7y8vP8ICQn/AQAA/6Kiov/+/v7//v/+//7////+/v7//v7//x4eHv/p6en/6enp/+np6f/p6en/6enp/0hISP8BAAD/ICAg/wABAAAAAAAAAAAA/3Z2d/8AAAD/09PS//7+/v/+/v7//v7////+/v/+/v7//v7///7+/v////7///7+/7a2tv8HBwf/oqKi///////+/v7//v7+//7//v/+/v//CQgJ/wAAAP8AAAD/AQAB/wAAAP8BAAD/AQAA/wABAP8NDQz/AAAAAAAAAAABAAH/fHx8/wAAAP/S09P//v7+//7+/v/+/v7//v7+///+/v/+/v7///7+//7+/v/+/v7///7//3t6ev+jo6P//v7+//7+/v/+/v7//v7////+/v8ICAj/AQAA/wAAAP8AAQD/AAAA/wEBAP8BAQD/AQAA/wgICP8AAAAAAAAAAAICAv9ubm//AAAA/9LS0v/+/v7///7+//7//v/+/v//ZWVl/83NzP/+/v7//v7+///+/v/+/v7/hYWF/6Kiov/+/v7//v7+//7+/v///v7//v7+/wgICf8AAQD/AAAA/wAAAP8AAAD/AAAB/wAAAf8AAQD/EhIS/wAAAAAAAAAAEBAQ/1BQUf8AAQD/0tLS//7+/v/+/v7//v7+//7+/v9LS0v/w8PD//7+/v/+//7//v7+///+//+FhYX/oqKi//7+/v/+/v7//v7+//7+/v/+/v7/Dg4O/zg4OP84ODj/ODg4/zg5OP84ODj/ERER/wAAAP8uLi7/AQEAAAAAAAA7Ozr/ICEh/wAAAf/S0tP//v7+//7+/v/+/v7//v/+/0xMTP/Dw8P//v7+///+/v/+/v7//v7+/4WFhf+ioqP//v7+//7+/v/+//7//v7+//7//v8eHx/////+//7+//////7//v/+///+/v9OTk7/AAAA/1xdXP8AAAAAAAAAAHh4eP8AAAD/AAAA/9LT0//+/v7//v7+//7+/v/+/v7/SktK/8PDw//+/v7//v/+//7+/v/+/v7/hISE/6Kiov/+//7///7////+/v/+/v7///7+/x8fHv/8/Pz//v/+//7+///+/v7//v/+/05PT/8BAAD/mZmZ/wAAAAAAAAAAycnJ/wAAAP8BAQD/0tLS//7+///+/v7//v7////+/v9MTEz/w8PD//7//v/+/v7//v7+//7+/v+EhYX/oqKi///+/v/+/v///v7+//7//v///v//Hh8f///+///+/v7///7+//7//v/+/v7/T05O/wUEBP/l5OX/AAEBAAEAAAAAAQAALi4u/wEAAP/T0tL//v7+///+/v/+/v7//v7//11dXf/Iycn//v7+//7+/v/+/v7//v7+/4WFhP+io6P//v7+//7+/v/+/v7//v7+//7+/v9BQED//v/+//7+///+/v///v7///7//v82Njb/TExN/wAAAAAAAAAAAAAAAAAAAAClpaX/AAEB/8DAwP/+/v////7+///+/v/+/v///v7+///+/v/+/v///v/+//7//v/+/v//goKC/6ChoP///v///v7+///+/v/+/v7//v7+//7+/v/+/v7//v7+//7////+//7/tbS1/wICAv/Cw8L/AQAAAAAAAAAAAAAAAAAAAAAAAAA5ODn/OTk4//v6+v///v7//v7+//7+/v/+/v7//v7+//7////+//7//v7//9DR0f8UFRX/IyMj/+Hh4f/+/v7//v7+//7+/v/+//7//v/+//7+///+/v7//v7///Dw8P8jIiL/VFRV/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANXV1f8KCgr/cHFx//7+///+/v7//v7+//7+///+/v7//v////7+///V1dX/GBkY/wEAAP8AAAD/JyYm/+Xl5f/+/v///v7///7+/v/+//7//v/+//7+///8/fz/U1NT/xgZGP/n5+f/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEA/////6emp/8CAgP/hYWF//7+/v/+/v7////+//7+/v/+/v7/2dnZ/xoaGv8AAQD/AQEA/wAAAP8AAAD/Kyor/+fn5//+/v7//v/+//7+/v//////+/v6/2dmZ/8ICAj/wcHB/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJmZmP8CAwL/MTEx/zs6O/86Ojr/Ozo6/zo6Ov8VFBT/AQEA/wAAAP8AAAD/AAAB/wABAP8AAAD/Gxsb/zo6Ov86Ojr/Ojo6/zo7Ov8rKiv/CQkJ/7Gwsf8AAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAABAAAAAQAAAAAAAK2trP8QEBD/AQAA/0JCQv9+fn7/fn5+/35+fv9/fn7/fn5+/39+fv9+fn7/fn5+/35+fv9+f37/fn5+/35+f/8yMjP/AQEA/xoaGv/BwcH/AAAAAAAAAAAAAAAAAAEAAAEAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAQAAANzd3f9KSkr/AgIC/0NCQv+pqan/8fDx/////////////v/////+///////////+/+vr6/+dnJz/NTQ0/wICAv9cXV3/6enp/wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAC/vr//Tk5O/wYGBv8GBgf/MjIz/1lYWP9oaGj/aGho/1VUVP8sLCz/BAQE/woKCv9aWlr/zMzN/wAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAA6uvq/6urq/92dnb/VFVU/0RERP9ERET/WFhZ/3x8fP+zs7P/8fHx/wAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    MAX_CORE = 3
    display_name = 'Allporncomic'
    ACCEPT_COOKIES = [r'(.*\.)?allporncomic?\.com']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'

    def read(self):
        no = self.url[self.url.find('a'):].split('/')
        num = len(no) - 1
        if no[num]:
            num += 1
        if num > 3:
            imgs = get_imgs_single(Page(self.url, ''))
        else:
            imgs = get_imgs_all(self.url, cw=self.cw)
        if isinstance(imgs['data'][0], Video):
            self.enableSegment()#n_threads=4
        for img in imgs['data']:
            self.urls.append(img.url)
        self.title = imgs['title']
        
class Page:
    def __init__(self, url, title):
        self.url = url
        self.title = title

class Image:
    def __init__(self, url, page, p):
        point = url.rfind('.')
        ext = url[point:] if point > 25 else '.gif'
        self.filename = '{}/{:04}{}'.format(page.title, p, ext)
        self.url = LazyUrl(page.url, lambda _: url, self)

class Video:
    def __init__(self, url, page):
        self.filename = page.title  + '.mp4'
        self.url = LazyUrl(page.url, lambda _: url, self)

def get_imgs_single(page):
    soup = get_soup(page.url)
    views = soup.find('ol').find_all('li')
    info = {}
    info['title'] = views[2].text.strip()
    page.title = views[3].text.strip()
    view = soup.find_all('img', class_='wp-manga-chapter-img')
    imgs = []
    if view:
        for img in view:
            src = img['data-src']
            img = Image(src, page, len(imgs))
            imgs.append(img)
    else:
        view = soup.find('source')
        src = view['src']
        vid = Video(src, page)
        imgs.append(vid)
    info['data'] = imgs
    return info


def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

@try_n(2)
def get_imgs(page):
    soup = get_soup(page.url)
    view = soup.find_all('img', class_='wp-manga-chapter-img')
    imgs = []
    if view:
        for img in view:
            src = img['data-src']
            img = Image(src, page, len(imgs))
            imgs.append(img)
    else:
        view = soup.find('source')
        src = view['src']
        vid = Video(src, page)
        imgs.append(vid)
    return imgs

def get_pages(url):
    print(url)
    for _ in range(4):
        try:
            soup = get_soup(url)
            view = soup.find_all('li', class_='wp-manga-chapter')
            if not view:
                raise Exception('no view')
            break
        except Exception as e:
            e_ = e
            print(e)
    else:
        raise e_
    urls = set()
    info = {}
    info['title'] = clean_title(soup.find('h1').text.strip())
    pages = []
    for li in view:
        li = li.find('a')
        href = li['href']
        if href in urls:
            continue
        title = clean_title(li.text.strip())
        urls.add(href)
        page = Page(href, title)
        pages.append(page)
    info['data'] = pages[::-1]
    return info

def get_imgs_all(url, cw=None):
    pages = get_pages(url)
    imgs = []
    p = 1
    for page in pages['data']:
        check_alive(cw)
        imgs += get_imgs(page)
        msg = tr_('읽는 중... {} ({}/{})').format(pages['title'], p, len(pages['data']))
        p += 1
        if cw is not None:
            cw.setTitle(msg)
        else:
            print(msg)
    pages['data'] = imgs
    return pages
