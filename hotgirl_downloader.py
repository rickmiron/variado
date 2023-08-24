#coding: utf-8
#title_en: Hotgirl
#https://hotgirl.asia/
import downloader
from utils import Downloader, Soup, lazy, Session, clean_title


@Downloader.register
class Downloader_tmohentai(Downloader):
    type = 'hotgirl'
    URLS = ['hotgirl.asia']
    icon = 'base64:AAABAAEAICAAAAEAIAAoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD9/f3e6urr7pGRkO5lZGTuXFxb7lZVVO5VVFLuVVRS7lVVU+5dXFvubm1s7oKBgO6enpzupqaj7pybm+6srKzusK+v7rm4uO7Q0NDu/f397v39/e79/f3uycjI7mZkZe56eXnu6enp7vz8/O78/Pzu/Pz87vz8/O78/Pzu/Pz83tLS0vQrKyr/AQAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8pKSj/PTw9/7u6uv/x8fH/wcHA/8LCwv8EBAT/hIOD//////////////////7///////////7////////8/Pz0RERC7gAAAP8IBgX/CggH/wcFA/8EAwL/BQMC/wgGBP8PDQz/FRQS/xcVFP8QDw3/CQcG/wcFBP8BAAD/W1pZ//7+///+//////////39/f+oqKj/JSUk/wAAAP/R0dD////////////////////////+//////////////z8/O4kJiPuAQAA/wYFBP8ODg3/FxUU/xUVEv8ZFxX/Hhwb/xoZF/8TEhD/EQ8O/xIQD/8RDw7/BgUE/wUEA/9tbGz/6ejo//////////////////z9/P8gIB//AAAA/8bGx//+/////////////////////////////////////Pz87jU1Ne4BAAD/CAYE/wcFBP8KCAf/EQ8N/xAPDP8IBgT/BAMB/wUDAv8GBAP/BgQD/wcEBP8IBgX/CAYF/wAAAP8dHBz/3t3d//////////////7//3Z2df8AAAD/ycnI///////////////////////////////////////8/Pzup6am7gAAAP8DAQD/CQYF/wgGBP8HBAP/BgUD/wgGBf8IBgX/CAYF/wgGBf8IBgX/CAYF/wgGBf8JBgX/CAcF/wAAAP9qaWn///7/////////////qKen/wAAAP/Gxsb//////////////////////////v////////////z8/e78/f3ukZGQ/wAAAf8AAAD/AwEA/wgGBf8IBgX/CAYF/wgGBf8IBgT/CAcF/wgGBf8IBgX/CAYF/wgGBf8IBgX/AAAA/z49O//////////////+//+np6b/AAAA/7a2tv//////6+vr/+vr6v///////////////////////fz97v39/e7/////xcXE/1pZWf8PDw7/AAAA/wABAP8FAwH/CAcF/wgGBf8IBwX/CAYF/wgGBf8IBgX/CQYF/wgGBf8BAAD/Ozo4/////////////////5aWlf8AAAH/pqel///////z8/P/rKyr//f39//09fX////+///////8/Pzu/P387v///v///////////+Lj4v+RkpL/Pz49/wYGBf8AAAD/AQAB/wMBAP8IBgX/CAYF/wgGBf8IBgX/CAYF/wAAAP9RUU////////////////7/iYiH/wAAAP+cm5v//v////v7+/+en5//29vb/+Hh4v////7///////r6+u78/Pzu/////////v///////v//////////////1dbV/5GRkP9RUE//CgoJ/wMAAP8JBgX/CAYF/wgGBf8IBgT/AAAA/4uKif/////////////+//95eHf/AAAA/46NjP/4+Pj/srKw/2BfX/++vr7/fn5+//Dw8P+3t7f/+fj47v38/O7///////////////////7////////////+///////////////S09L/GRoY/wMCAv8IBgX/CAYF/wQCAv8IBwb/3Nzc/////////////////2lpaP8AAAD/dXV0/8bGxv9iYV//hIOD/7Kys/94eHf/hIWE/7Ozs//9/P3u/Pz87v7//////////v7///////////////////////////////////////9AQD7/AAAA/wgGBf8IBgX/AAAA/z48PP///////v/+////////////YWFe/wAAAP9mZmX/vb28/3Z2df/Z2dr/iYmJ/5ycnf9sbGr/y8zL//39/e78/P3u/////////v///////////////////////////////////////////1dXVv8AAAD/BwUE/wgGBf8AAAD/k5KR//////////////////7///9UVVT/AAAA/3p5ef90dXX/b29u/5mamf84ODf/x8fG/2traf9xcHD//f397vz8/e7////////////////+////////////////////////////////////eHh3/wQCAP8FAwL/BgQD/wAAAP/Lysj/////////////////+/r6/ysrKf8AAAD/srKx/6SkpP9SUlH/Tk5M/1xdXP/39/f/kpGQ/zg4Nv/p6eju/Pz87v////////////////////////////////////////////////7///+jo6P/AwEB/wYEA/8HBQT/AAAA/7u7uv/////////////////k5eT/DQ0L/wAAAf+UlJP/k5KS/0BBP/8gIB//W1xa/7CwsP+SkpL/T01M/5CQkO78/Pzu//7//////v/////////////////+//////////////////////7//728vP8AAAD/BgUE/wgGBf8AAAD/X15d/////v///////////+Lj4v8ODQr/AAAA/4F/fv9TU1H/FBIR/wEAAP8EAwL/KSgm/yUlJP9IR0f/dHV17vz8/e7/////////////////////////////////////////////////////6urq/xIQD/8CAAH/CAYF/wYEA/8BAQD/uLi4/////////v//7e3t/xgXFf8AAAD/Z2Zl/xQTEP8HBQT/CAYF/wcFBP8AAAD/AAAA/ywrKv9iYmLu/Pz87v///v///////////////////////////////v/+////////////////////TkxL/wAAAP8IBgX/CAYF/wEAAP8VFBP/1tbW///+///4+fj/IyMi/wAAAP9hYF7/IB8d/wIAAP8IBgX/CAYF/wgGBf8IBgX/AAAA/2ZkY+78/Pzu/////////////v////////////////////7///////////////////////+RkJD/AAAA/wkGBf8IBgX/CAYF/wAAAP8dGxv/zMzN//////8wMC7/AAAA/1NTUf+Pj47/CAcH/wcEBP8IBgX/CAYF/wgGBf8AAAD/qamn7v38/O7///////////////////////////////////////7//////////////////7GxsP8AAAD/CAYF/wgGBP8IBwX/CQYF/wAAAP8LCwr/trW1/09OTf8BAAD/PDs6/4ODgv8hHx7/AgEA/wgGBf8IBgX/BgUE/wEAAP+srKzu/Pz87v////////7///////////////7/////////////////////////////////zc3M/wEAAP8GBAP/CQYF/wgHBf8IBgX/CAYF/wAAAP8ODAr/IiEf/wAAAf9FREP/X15d/wEBAf8JBgX/CAYF/wgGBf8IBgT/AAAA/42NjO78/Pzu//////////////////////////////////////////////7////////////29/b/Hh4c/wABAP8IBgX/CQYF/wgGBf8JBgX/CQYF/wMCAP8CAAD/AgEA/yYlI/87OTn/AAAA/wgGBf8IBgX/CAYF/wgGBf8AAAD/ZmVj7vz8/e7///////////////////////7///7///////////////////////////////////+Dg4L/AAAA/wcFBP8IBgT/CQYF/wgGBf8IBgX/CAYF/wgGBf8GBAP/EQ8O/yQkIv8DAQD/CAYF/wgGBf8IBgX/CAYF/wEAAP84NzXu/Pz97v///////////////////v/////////////////////////////////+/v////////v7+/9MTEv/BwcE/x0bGv8KCAf/BwUF/wgGBf8IBgX/CAYE/wgGBf8JBwX/HBoY/wcFBP8IBwX/CAYF/wgGBf8IBgX/AwEA/yAeG+78/Pzu/////////////v///v7//////////v///v/////+///////////////+/////////////+Hh4f8MCwj/BAIC/wcFBP8IBgX/CAYF/wgGBf8IBgX/CQYF/wgFBP8GBAL/CQcF/wgGBf8IBgX/CQYF/wgGBP8AAAD/NTU17vz8/O7/////////////////////////////////////////////////////////////////////sbCw/wAAAP8GBQT/CQYF/wgGBf8IBgX/CAYF/wgGBf8IBgX/CAYF/xMREP8HBAT/CQYF/wgGBf8IBgX/CAYF/wAAAP+BgYDu/Pz97v/////////////////////////////////+/////v////7////////////////+//////+sra3/AAAA/wgGBP8JBgX/CAYE/wgGBf8IBgX/CAYF/wcFBP8NCgj/GxgX/wUDAv8IBgT/CAYF/wgGBf8AAAH/Kyop/+np6e78/P3u//////////////////////7+/v/////////+//////////////////7///////////7+/+vr6/8TExH/AAAA/wAAAP8AAAD/AAAA/wAAAf8CAAD/BgQD/xkYFv8PDg3/BgQD/wgGBf8IBgX/AwIB/xQTEv/k5OT//f397vz8/O7//////////////////v///////////////v///////////v/////////////+/v///////////7m4uP9qa2v/jIyL/6Sjo/+SkZD/Tk5N/xMSEf8AAAD/CQYG/wcFBP8IBgX/CAYF/wgHBf8BAAD/hYWE///////8/Pzu/Pz87v///////v///////////////v/////////////+//////////7////////////////////////////////////////////////////+////5eTl/2BgX/8AAAH/AAAA/wEAAP8IBgX/AAAA/wwLCv/a2tr////+//z8/O78/Pz0//////////////////7////////////////////////////////////////////////////+/v///////////////////v/////+/////////////v7//7u7u/+IiIj/UlFR/wAAAP8VFBT/jIuL//7//////v///Pz89Pz8/N78/Pzu/Pz87v38/O78/Pzu/Pz87vz8/O78/Pzu/P387vz8/O78/Pzu/Pz87vz8/O78/Pzu/Pz87vz8/O78/Pzu/Pz97vz9/O78/Pzu/Pz87v38/O79/f3u/f397v39/e79/P3uXV1c7r+/v+79/f3u/Pz87vz9/O78/Pze'
    display_name = 'Hotgirl'
    MAX_CORE = 4
    ACCEPT_COOKIES = [r'(.*\.)?(hotgirl\.asia)']

    def init(self):
        self.session = Session()
        if '/?stype=slideshow' not in self.url :
            self.url += '/?stype=slideshow'
        html = downloader.read_html(self.url, session=self.session)
        self.soup = Soup(html)

    @lazy
    def id(self):
        return clean_title(self.soup.find('h3').text.strip())

    @property
    def name(self):
        return self.id

    def read(self):
        imgs = get_imgs_www(self.soup)
        num = 0
        for img in imgs:
            num += 1
            self.urls.append(img)
            self.filenames[img]=str(num) + '.jpg'
        self.title = self.name

def get_imgs_www(soup):
    imgs = []
    views = soup.findAll('img', class_='center-block w-100')
    for imgv in views:
        imgs.append(imgv['src'].rstrip())
    return imgs