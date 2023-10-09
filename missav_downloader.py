#coding: utf-8
#title_en: Lectortmo
#https://lectortmo.com/
from utils import LazyUrl, clean_title, try_n,Session, Downloader, check_alive
from translator import tr_
import requests
from bs4 import BeautifulSoup

USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
REFER = 'https://lectortmo.com/'
class Downloader_lectortmo(Downloader):
    type = 'lectortmo'
    URLS = ['img1.japanreader.com']#['lectortmo.com']
    icon = 'base64:AAABAAEAICAAAAEAIAAoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAQAAAAEAAACAgQACvFcrNbldLJa5WCrduVQn/LlVJv+6Vij/ulcp/7pXKf+6Vyn/u1cp/7pXKf+6Vyn/ulcp/7pXKf+7Vyn/ulcp/7pXKP+6Vyn/ulcp/7pXKf+6Vyn8ulco4LhYKZq8VSg5qlUAAwAAAAAAAAAAAAAAAAAAAAABAAAAv1UqDLlXKHW6VijjwXBK/9Kql//Qoo3/xH1c/7teM/+7VSf/ulcp/7pXKf+6Vyn/ulcp/7pXKf+6Vyn/ulcp/7pXKf+7Vyn/ulcp/7pXKf+6Vyn/ulcp/7pXKf+6Vin/ulco/7pWKOa5Vil8tlskDgAAAAAAAAAAAAAAALldLgu5VyiSuVYp+rpXKf+7WSz/0pR4//bx7v/x7+7/3cS4/8aDZP+6Wi3/ulYn/7pXKf+6Vyn/ulcp/7pXKf+6Vyn/ulcp/7pXKf+7Vyn/ulco/7pXKf+6Vin/ulcp/7pXKf+6Vyn/ulcp/7pXKfy5WCmatlskDgAAAAAAAAAAulYoc7lWKfq6Vin/ulcp/7pXKf+7Vyj/15+E//36+P/+////8e3r/9Wwn/+/aUH/uVQm/7pWKP+6VSf/uVUm/7lVJv+5VSf/ulQn/7pXJ/+6Vij/u1cp/7pXKf+7Vyn/ulcp/7pXKf+6Vyn/ulcp/7pXKfy5Vil8gIAAArpYKjG6Vinfulcp/7pXKf+6Vyn/ulcp/7tWKP+8Wy//5L+s////////////+vv7/+HPxv/EfVz/vWQ6/8BvSv/Delf/xX9f/8R9XP/DdVH/v2tE/7xgNf+6WSr/uVUm/7pWKP+6Vyn/ulcp/7pXKf+6Vyn/ulcp/7lWKeS5WCk6u1YpjrpXKf+6Vyn/ulco/7pXKf+6Vyn/ulco/7lVJ//Eb0j/9eTe/////////////f7+/+3n5f/n2dL/7ufk//Lv7v/08vH/9PHw//Hs6v/r4t3/4tDH/9ayof/Ii2//vmc//7pWKP+6Vij/ulYp/7pXKf+6Vyn/ulcp/7hYKZq6VyjVulcp/7pXKf+6Vyn/ulco/7pXKP+7Vyn/uVUn/7xiOP/lxrn////////+//////////7//////////////////////v/////////////+/////////f7///X19f/l19H/zp+J/75nP/+6VSf/ulYp/7pXKf+6Vyj/ulYp37lXKPa6Vyn/ulcp/7pWKf+6Vyn/ulYm/7taLf/JiGv/5NDG//r49////////////////v///////////////v///////////////////////////////////////v/////////4+fn/4tHI/8WAYP+6Vyn/ulcp/7pXKf+6Vyn8ulcp/7pXKf+7Vyn/ulco/7lVJ/+9ZTz/2LGe//bz8f///////////////////////////////////////v/////+///////////+/////////////////////v/////////////////+////7ebj/8qQdP+6WCr/ulcp/7pWKf+6Vyn/ulcp/7pXKf+5VSf/wG5H/+PKvv/9/f3//////////////v//////////////////////////////////////////////////////////////////////////////////////////////////8Ovo/8iKbv+6Vij/u1cp/7pXKf+6Vyj/uVUn/8BtR//n0sn//v7+///+/v////7///////7////+/f3//v38//79/f////////7///v6+f/+/f3////////////+/f3//v38//79/f/////////+//z49v/68u7//fn3////////////6d7Y/8BvSv+7VSf/ulcp/7pWKP+9Yzn/5Mm9//35+f/Zoon/47yo////////////+/Xy/9efhP/OiWj/37Cb/////v/37Of/0pR3/9abgP/68u///vr7/9qokf/OiWj/2qaN//rz8P/juqf/yn9c/8Z1UP/Mg2H/47qn//z39P/9/v7/1q+d/7pYK/+6Vyn/ulco/9eplP/9/v7/+/bz/8Z1UP/Wm3////////7////58Oz/xHBJ/7dQH//Pi2z//////+bCsv+6Vyj/u1ot/+rPwv/9+/r/yn9c/7dPH//Je1f/3q+Z/8BmPP/bpIv/58a2/9yqkv/DbEX/15uA//z49//u5eD/wXJN/7lVJv/FeFT/9e3p///////79vP/x3hT/9adgv////////////nx7f/Eckz/uFMj/9GPbv/9+/n/0pJ0/7lUJf+5VCb/2J+E//z5+P/Lgl//uFIk/8NuRv/CbET/2aKI///+/v///////////+zSxf/BaUD/47qn//r7+//OmYD/ulgq/962pP////////////v28//HeFP/1p2C////////////+fHt/8VyTP+4UiP/05V3//Xm3//Ca0L/vVwv/7paLf/GdE7/9+vl/82HZf+5VSX/u1ou/7xdMP/rzsD///////7//////////////9ighv/IeVT/+fPw/9u5qf/Cbkf/8+fg////////////+vbz/8d4U//WnYL////////////48e3/xXJN/7hSIv/WnIH/5b+t/7lWJ//QjGz/zIRi/7tYLP/pybv/0Y5v/7lUJf+6Vij/vF0x/+7VyP////////7//////////v7/7NHF/8BkOv/u18z/48q+/9CRdP/8+vj////////////79vP/x3hT/9adgv////////////nx7f/Fckz/uFMk/9edgv/Rj3H/uVUn/+bCsf/htqL/uVQl/9Wafv/SkXP/uVQl/7xcMP+8XDH/6cq8//////////7////////////26OL/wmlB/+S9q//ky77/3a+Z//////////////////r28//HeFP/152C////////////+fHt/8VyTP+5VCb/0I1t/8BpQP/BaUD/9uji//Lf1v++Yjb/xHBJ/82GZf+5VCX/wmtD/8BnPf/fsJv///////////////7///////ry7//Fc0z/3KyV/9y6qf/kvqz//v/+////////////+/bz/8d4U//XnYL///////7////58e3/xXJM/7lXJ//Ca0L/ulcp/9CNbv/+/Pv//Pj2/8yCYP+7WSz/wmhB/7lVJv/Ielb/zohn/82FZP/8+Pf/////////////////+vPv/8Z0Tf/ap5D/0Jh//+S9q//+///////+/////v/79vP/x3hT/9edgv////////////nx7f/Fckz/uVUn/7pXKf+6Vyn/47up////////////3q6Y/7hVJ/+6Vyn/uFUm/8t+W//nxbX/wGY9/+jGuP////////7////////y39f/wWg//9utl//EdE7/26iR//v28//16OH/9uji//Lg1//Ec0z/0pN1//bp4//26eL/8NvR/8NvR/+5VSb/uVUn/8FnPf/0493//v/////////w2c//vmE1/7lWJ/+5VCX/yXxY//rz7//ZoYf/w2xE/+S+rf/26eL/8+HZ/9CObv/Hd1L/2KeP/7tZLP/Oh2b/5sOx/8RzTP/Fckv/xHFK/79jOf/BZj//xXJL/8VyS//EcUn/v2M4/71gNP+9XTH/0Y5v//36+P////////////v28//Mg2L/vV8x/71eMf/Mg2H//Pj2//v28//cqpL/xHBJ/8RvR//CbEL/yHpW/+TBsf/GeVX/uVUm/8BlO//qzL7/8dzS//DZz//w2s//8drQ//Da0P/w2c//8NnP//Daz//w2tD/8NvR//Da0f/26uX//v////////////7///////Xn4P/w2tH/8NrQ//Pj2//+/f3////////9/f/26eP/7dLG/+7Wy//48Ov/2qiR/7pXKf+6Vyn/uFUm/teehP/+/v3///////////////////////////////7//v///////////v////////////////////////7//v/////////////////////////////////////////////////+/////////+fFtf+9YDX/ulYo/7pXKf+6Vif1v2M4/+zRxP////7//v/////////////////////+//////////////////////////////////////////7//////////////////////////////v///////////v/////////////qz8L/wWlA/7lVJ/+6Vyn/uVco+7lXKNK5VSf/xndS//Pj2/////////7///////////7////////////////////////////////////////+//////////////////////////7//////////////////////////fz/58W1/8FpQP+4VSb/ulcp/7pXKf+5Vincu1coirlXKf65VSf/yXtW//Dc0//////////////////+//7//////////////////////////v/////////+/////////////v/////////////////////////+////+fDs/9unj/++YDT/uFUn/7pXKf+6Vyn/ulcp/7tXKZW8WScuuVYp3LpXKf+5VSf/wmxD/+O7qP/79fL////+/////v/////////+/////////////////////////////////////////////////////////////Pf1/+jHuP/KfVr/ulco/7pWKP+6Vyn/ulYp/7pXKf+5VyjhvFcrNQAAAAC7Vyhsulco+bpXKf+5Vif/u1ot/8yCYP/mwrL/+O/r///+/////v////////7//////////////////////////////////v/+/Pv/9+nj/+S+rf/MhGL/vFwv/7lVJv+6Vyn/ulcp/7pXKf+6Vyn/uVco+7lXKXX/AAABAAAAAMZVHAm7VimKu1co+bpXKP+6Vyn/uVUm/7taLP/Gc03/1pyA/+XAr//v2M//9ebf//fr5v/37Of/9ejh//He1f/qzL7/37Kd/9GPcP/DbET/ulgr/7lVJv+6Vyj/ulcp/7pXKf+6Vyn/ulcp/7lWKPq5VyiSv1UrDAAAAAAAAAAAAAAAAMZVHAm7VyhsuVcq3blXKP66Vyn/u1co/7lVJ/+5VCb/ulgq/71fM//AZz3/w2xD/8NtRf/BaD7/vmI2/7taLf+5VCf/uVQm/7lWJ/+6Vyn/ulcp/7pWKP+6Vin/ulcp/7lXKP66Vyjgulcocr9VKgwAAAAAAAAAAAAAAAAAAAAAAAAAAP4AAAG7VSgtu1cpirpXKdO7Vyj1ulcp/7pXKf+6Vyn/ulco/7pWKP+5VSf/uVQn/7lWJ/+6Vij/ulcp/7pXKf+6Vyn/ulcp/7pXKf+6Vyn/ulYo/7lXKfa5VinWu1YpjrtYKjGAgAACAAAAAAAAAAAAAAAA'
    MAX_CORE = 3
    display_name = 'Lectortmo'
    ACCEPT_COOKIES = [r'(.*\.)?lectortmo?\.com']
    user_agent = USERAGENT
    referer = REFER

    def read(self):
        imgs = get_imgs_single(Page(self.url, ''))
        imgs = get_imgs_all(self.url, cw=self.cw)
        Session()
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
        ext = url[point:] if point > 27 else '.webp'
        self.filename = '{}/{:04}{}'.format(page.title, p, ext)
        self.url = LazyUrl(page.url, lambda _: url, self)

def get_imgs_single(page):
    soup = get_soup(page.url)
    views = soup.find('ol').find_all('li')
    info = {}
    info['title'] = views[2].text.strip()
    page.title = clean_title(soup.find('h1').text.strip())
    view = soup.find_all('img', class_='wp-manga-chapter-img')
    imgs = []
    for img in view:
        src = img['data-src']
        img = Image(src, page, len(imgs))
        imgs.append(img)
    info['data'] = imgs
    return info

def get_soup(url):
    response = requests.get(url, headers={'User-Agent':USERAGENT})
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

@try_n(2)
def get_imgs(page):
    for _ in range(16):
        try:
            response = requests.head(page.url, headers={'Referer':REFER,'User-Agent':USERAGENT})
            if response.status_code == 302:
                page.url = response.headers['Location'].replace('paginated','cascade')
                break
        except Exception as e:
            e_ = e
            print(e)
    else:
        raise e_
    soup = get_soup(page.url)
    view = soup.find_all('img')
    imgs = []
    for img in view:
        src = img['data-src']
        img = Image(src, page, len(imgs))
        imgs.append(img)
    return imgs

def get_pages(url):
    print(url)
    for _ in range(4):
        try:
            soup = get_soup(url)
            view = soup.find_all('li', class_='upload-link')
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
    h1 = soup.find('h1', class_='element-title')
    if h1.small:
        h1.small.extract()
    info['title'] = clean_title(h1.text.strip())
    pages = []
    for li in view:
        href = li.find_all('div', class_='row')[1].find('div', class_='text-right').find('a')['href']
        if href in urls:
            continue
        urls.add(href)
        title = clean_title(li.find('div', class_='row').find('a').text.strip())
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
