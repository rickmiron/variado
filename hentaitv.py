#coding: utf-8
#title_en: Hentai TV
#https://hentai.tv/
import downloader
from utils import Downloader, LazyUrl, Session, try_n, format_filename
from io import BytesIO
import clf2



class Downloader_hentaitv(Downloader):
    type = 'hentai.tv'
    URLS = ['hentai.tv'] #4835
    icon = 'base64:AAABAAEAICAAAAEAIAAoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAABAQAAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAAABAAAAAAAAAQAAAAAAAAABAAAAAAAAHZ3/Ghee+jcYof9BGJ3/QRif/0AYn/9AGJ//QBif/0AYn/9AGJ//QBif/0AYn/9AGJ//QBif/0AYn/9AGJ//QBmf/0AYn/9AGJ/+QBif/0AYn/9AGJ//QBie/0AYn/9AGJ//QBih/0Ebof85Gp7/HQAAAAAAAAEAAAAAARmf+0gaofy+GKn85Rqp/eYap/3mGqf95hqn/eYap/3mGqf95xup/egapv3nGqf95hqn/eYap/3mGqf95hun/eYap/3mG6f95hqn/Ocbqf3oGqf95xqn/eYap/3mG6f95hqm/eYap/3mG6b95xqp/OYYovvGGaP8UgD+/wIZov80GKP90Ryu//8brf//G6z//xqs//8brP7/G6z//xus/v8brv//G6///x2y//8cr///G6z//xus/v8brP//G6z//xus//8brP//G63//xuu//8csf//HLH//xut//8brP//G6z//xut/v8brf//G63//xuw//8ZpvvaGaP/QBuh/YUbp/7/HKr//xui//8aov//GqP+/xqi//8apP//F6L89xqh/L0YoPqnGaL7yhik/PcapP//GqP//xqi//8aov//GqT//xmh/PwWoPrVGZ/7rBif/LgaovvrG6T//xqj//8ao///GqP//xui//8ao///G6n//xqq//8ao/yWGKL6qBqo//8ap///GqP//xqj//8ao///GqL//xus//8ap/zmGqH/RBKk/w4ZovgpF6H8rhqj/f4apv//GqP//xqj//8bqP//GKP89hei/YMXov8WF6b/Fxij/XMapf3xG6n//xqi//8ao///GqP//xqj//8apP//Gqn//xif+bgYofqpGqf//xqn//8ao///GqP//xqj/v8aov//G63//xmn/eMaof8xAAAAAAAAAAAaof1sGqT88xup//8ao///GqL//xup//8bpPz1GKD/dgAAAQAAAAEAGaL/KRqo/d8brv//GqP//xqj//8ao///G6P//xql//8aqv//Fp/5uRig+qcZpv//Gqb//xqj//8ao/7/GqP//xqi//8brf//Gab85Bqg+zsAAAAAAP//ARqg/GYZpvzvG6r//xqj//8ao///G6j//xql/PUYof19IJ//CAABAAAanf8nG6j83Ruu//8aov//GqP//xqj//8ao///GqX+/xqp//8Yovy3GKD6pxmm/v8apv//G6P//xuj//8ao///GqL//xqt//8ZpvzkGqP/OgEAAAAAgP8CG6D9aRuk/PAbq///GqP//xqj//8bqP//GqX89Rig/X0gnv8IAAAAABmj/ikap/zeGq7//xqi//8ao///GqP//xui//8apf//Gqn//xii/LcYoPqnGab//xqm//8ao///GqP//xqj//8aov//G63//xmm/OQao/86AAAAAACA/gIbo/1oGqT88Bup//8aov7/GqL//xun//8XpPz1F6L9fCCf/wgAAQAAGaL/KRqn/N4brv//GqL//xqj//8ao///GqP//xql//8bqf//GKP8txig+qcZpv//Gqf//xqj//8ao///GqP//xqi//8brf//Gab85Bqj/zoAAAEAAVX/Axme/HAbqPz6HbT//xut//8brf//HLL//xuo//8XoP2EIJ//CAAAAAAZov8pGqf83huu//8aov//GqP//xuj//8aov//GqX//xqp//8Yovy3GKH6pxmm//8apv//GqP//xqj//8ao///GqL//xut//8ZpvzkGqP/OgAAAAAAVf8DG6L/YBim+tgYq/zlGaf84xmn/OMZrPzkGqj83Rmh/3IAtv8HAAAAABmi/ykbp/zeG67//xqi//8ao///GqP//xqj/v8apf//Gqn//xmi/LcYoPqnGab//xqm//8ao///GqP//xqj/v8aov7/G63//xmm/OQaov86AAAAAAABAAAXov4WGKT+NRqe/zobn/84G5//OBqe+zocoP82HaH/GwCA/wIAAAAAGaL/KRqn/N4brv//GqL//xqj//8ao///G6P//xql//8aqf//GaL8txig+qcZpv//Gqb//xqj//8aov//GqP//xqi//8brf//Gab85Bqj/zoAAQAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAAAAZov8pGqb83huu//8aov//GqP//xqj//8ao/7/G6X//xqp/v8Yo/y3GKD6pxmm//8apv//GqP//xqi//8ao///GqL//xut//8Zp/zkGqP/OgAAAAAAAAAAGpn/CiCf/xgdnf4aH6P1GR+j9RkdnfUaFar/GBWV/wwA/v8BAAABABmi/ykap/zeG67//xqi//8ao///GqP+/xqj//8apf//Gqn//xii/LcZoPqnGKb//xqm/v8ao///GqP//xqj//8aov//G63//xmm/OQaov86AQAAAACA/wIao/9NGqL8sxqg/MIYoPq8GKD6vBqj+8Eao/y3GqL+Wiqq/wYAAAAAGaL/KRqn/N4br///GqL//xqj//8ao///GqP//xqk//8aqf//GKL8txmg+qcZpv//Gqb//xqi//8ao///GqP+/xqi//8brf//Gab85Bqj/zoAAAAAAID/Ahuh/2wYpfv4HK///xqm//8ap///HK3//xql/P0Yof+AIJ//CAAAAAAZov8pG6b83huv//8aov//GqP//xqi//8ao///GqT//xqp//8Yovy3GKD6pxmm//8apv//GqP//xqj//8ao///GqP//xut//8ZpvzkG6P/OgAAAAAAgP8CGqH9ahqn/PEbrP//G6T//xqk//8bqv//GKb89xii/X4gn/8IAAAAABmi/ykap/zeG67//xui//8ao///GqP//xqj//8apf//Gqn//xii/LcYoPqnGaf//xqm//8ao///GqL//xqj/v8aov//G63//xmm/OQbn/84AAAAAACA/wIboP1pGqT98Bqq//8aov//GqP//xuo//8apfz0GaH9eiSS/wcAAQAAGaL/KRqn/N4brv//GqL//xqj//8ao///GqP//xql//8aqf//GKL8txmi+qgap///Gqb+/xqj//8bo///GqP//xqi//8brf//Gab85B2f/zUAAQAAAAAAABqg/GMZpvzvG6r//xqj//8ao///G6j//xik/PcZov17AAH+AQAAAAAco/8kGqn93Bqu//8aov7/G6P//xqi//8ao///GqX//xuq/v8Yovy4GKH6qRqo//8apv//GqP//xqj//8ao///GqL//xur//8apPzwF5/9bRGq/w8as/8KGqH9bRqk/PAbqv//GqP+/xqj//8ap///GqP8/hmh/K0Vo/8kM5n/BRul/zAapfzfG63+/xuj//8ao///GqP+/xqj//8apf//G6n//xif/LgZo/2OGqj//xup//8aov//GqP//xuj//8ao///GqP//xql//8YpPzjF6H8mhui+4YaoPy6GKP8+Bqm//8bov//GqP//xqj//8apv//GqT79Bmh/LYaov2CG6L8mRqi/PAbp///GqL//xqj/v8ao///GqL//xun//8aq///GqD9nxug+0Mao/zeHLH//xys//8bqv//G6r//xuq/v8bqf//Gqb//xuo/v8Zovv+GaP6+Bql+/0bqf//G6r//xuq/v8bqv//G6r//xup//8bqf//Gqb//xmj+/kZo/35GqT+/xup//8bqv//G6r//xuq//8bq///HLL//xqm/eYYpP9RAJn/BRii/2AZov3SGKf87Rem/O8XpfzvGKX87Rml/O8aoPz8GqP+/xqo//8crv//HKr//xqm/PQYpvzuGKb87him/O4YpvzuGqP88xqm//8arP//G6n//xqo//8ao/z9GqP78Bik/O0WpfzvF6X87xip/O4Xp/vXGqD9bRyO/wkAAAAAAKr/AxqZ/ygXofxXGaD8Zhih/GQaoPxZGKL9cxqk++Ybq///G6j//xqk/PAaovm0GqH9dRqg/GEaofxiGqH8Yhqg/GEZof5yGKL8rRil/OwaqP//G6r//xqj/OsZoft6GqL/WBme/GQZoPxmGqD/WRec/ywAmf8FAAAAAAAAAAABAAAAAAAAAAAAAAAAgP8CAP7/AQAAAAAWoP8jGKf92x20//8bo/zrGaP/bxam/xczmf8FAAAAAAAA/wEAAP8BAAD/AQCZzAUapv8UGqL8Yxih++Ubs///GKj84hef/i0AAAAAAP//AQCA/wIAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAABAAAAAQAAAAAAAAAAABiX/yAap/zeG63//xug/Ywas/8KAAAAAAEAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAEAAAAzmf8FF6D9exqr/P0aq/3lGZv5KQAAAAAAAAAAAAABAAAAAAAAAAEAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFZ//GBmi/MkaovvrGaD6MwAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAanfgnGKL64hil+9gZnP8fAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAgn/8IGaL8exmh/LUZn/cgAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB+j/xkaovyqGqD7ihWd/w0AAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAEAAAAgn/8gGKT+Xxam/xcAAAAAAAEAAAAAAQAAAAAAAAAAAAEAAAAAAAAAAAAAAAEAAAAAAAAAGqb+FBqi/Fodpf8lAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAABAAAAAAAamP8KAKr/AwEAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAQAAAAAAAABVq/8DGpn/CgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAABAAAAAAABAAAAAAAAAAAAAAAAAAEBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
    single = True
    display_name = 'Hentai TV'
    ACCEPT_COOKIES = [r'(.*\.)?(hentai)\.(tv)']

    def read(self):
        self.session = Session()#get_session(self.url, cw=self.cw)
        video = get_video(self.url, self.session, self.cw)
        self.urls.append(video.url)
        self.setIcon(video.thumb)
        self.enableSegment(1024*1024//2)
        self.title = video.title


@try_n(2)
def get_video(url, session, cw):
    #print_ = get_print(cw)
    soup = downloader.read_soup(url, session=session)
    src_best = soup.find('iframe').attrs['src']
    title = soup.find('h1').text.strip()
    id = ''
    url_thumb = soup.find('meta', {'property': 'og:image'}).attrs['content']
    video = Video(src_best, url_thumb, url, title, id, session)
    return video


class Video:
    def __init__(self, url, url_thumb, referer, title, id, session):
        self.title = title
        self.filename = format_filename(title, id, '.mp4')
        url = self.get_urlx(url, session)
        self.url = LazyUrl(referer, lambda x: url, self)
        self.thumb = BytesIO()
        self.url_thumb = url_thumb
        downloader.download(url_thumb, buffer=self.thumb, session=session)
    
    def get_urlx(self, view, sessiona):
        soup = downloader.read_soup(view, session=sessiona)
        view = 'https://nhplayer.com/' + soup.find('li').attrs['data-id']
        soup = downloader.read_soup(view, session=sessiona)
        view = soup.find('body').find('script').text.strip()
        iid = view.find('file:')
        view = view[iid + 7:]
        idd = view.find('"')
        return view[:idd]


@try_n(2)
def get_session(url, cw=None):
    session = Session()
    clf2.solve(url, session=session, cw=cw)
    return session