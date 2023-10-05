#coding: utf-8
#title_en: Chochox
#https://chochox.com/
import downloader
from utils import Downloader, Session, Soup, clean_title


@Downloader.register
class Downloader_chochox(Downloader):
    type = 'chochox'
    URLS = ['chochox.com']
    icon = 'base64:AAABAAEAICAAAAEAIAAoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAAAAAAAMPSlhG9z5jukbxN7om3N+6Ktzjui7c57ou4Ou6LuDrui7c57ou3Oe6LuDnui7g57ou4Oe6LuDnui7k57ou4Oe6LuTjui7k57ou3Oe6Ltznui7c57ou3Oe6Ltznuirc57oq3OO6XvlDuvdWT7sPSlhEAAAAAAQAAAAAAAADC0pYRr8ln/4+5LP+SwDD/kLwz/4+8Mv+MvC//ibop/4q8LP+NvC//jL0t/42+Lf+Nvi3/jb4t/46+Lv+Ovi7/jb4t/42+Lf+Nvi3/jL0t/4y8Lv+LvC7/i70u/4u8Lv+LvC7/jL0u/4u/Kv+HvSP/oMpW/8PSlhEAAAAAw9KWEbjQf/+RvDv/lLtB/5S5Pf+RuDr/kLc1/5O6Ov+Uuj7/iLUu/4m4Lf+KuS7/jLov/426L/+Mui//j7sw/427L/+Kuy3/jLou/4y6L/+KuS7/irku/4i3Lv+Jty7/iLcu/4i3Lv+Ity7/iLYu/4e2Lv+DuR7/nspU/8PSlhHP27Ltq81j/6zNbf+rzGr/qMpm/6LGX/+hxFj/jrg4/5a6PP+bvUX/i7gv/427L/+OujD/j7sw/467MP+Nuyv/kLsx/5O8OP+QuzL/jLow/4u6Lv+LuS3/ibkt/4m4Lf+JuC//iLcu/4i3Lv+Ity7/iLcu/4e2Lf+IvyT/tM2L7rbOhO2t0Wb/qMpn/6nKZ/+qy2j/q81r/67Obv+oymf/i7Y1/5y+QP+avEL/jbkv/5C9Mf+TvDH/lL0y/5S9OP+VvDr/m7w9/5m9Ov+YvDz/l7s7/5W6OP+Rujf/jbky/4u5Lv+JuC7/iLcu/4i3Lv+Ity7/iLcu/4u9LP+OvELuoshk7bHTcP+py2f/qctn/6nLZ/+py2f/qMtm/7DPbP+pymP/kLkz/6LBRv+ZvEH/kbww/5O9Lv+bwDv/tdJv/7DOaP+qy1z/pMZT/6DCTP+dv0T/m78//5u+Qf+cvUP/jLkw/4q7Lv+JuC//iLcu/4i3Lv+Ity7/jL0v/4S1L+6GtDPtpMtZ/67Ob/+py2f/qctn/6nLZv+szWj/rs5o/7PTb/+myV7/k7sz/6bDSf+ZvT7/k7st/6PGSv+51XP/t9Ru/7fVcf+21HD/ttRw/7TTbv+vzmv/mr5B/5m9Pv+Nui//jrsw/4u6L/+JuC7/iLcu/4i3L/+MvC//hbYx7oa0M+2Juyn/oMZZ/67Ob/+oy2f/rM1m/67Oaf+uz2j/sdBp/7bUc/+kx1f/mr40/6vES/+ZvTj/qspS/7vWcf+41Gz/uNRs/7fVbP+1023/tNNt/7DQav+ewUP/m74+/4+7L/+OuzD/jrsw/4q5Lv+JuC7/iLcu/428L/+FtjHuibU27Yu7K/+FtCr/o8hY/7zccP++3m3/uNps/6/Paf+y0Wr/s9Nr/7rVdP+kxk//osE8/6nCQ/+yzl7/vdZx/7rVbf+71W3/udVt/7jVbP+61nD/sM9j/6DBP/+bvzv/k70x/5K6Mf+PuzD/jbov/4u4Lv+Jty7/jLwv/4W2Me6JtDbtjrku/4y7LP+HsyX/Zm1C/1xdQP+PoVT/weJw/8Heb//C3m//xeNy/8HYdf+qzE3/osM1/7rUbP/A1nL/vtVv/7zVbv+81W7/u9Vt/7zWc/+wzFr/psFA/5y/Of+WvjP/lLwy/5K6Mf+PuTH/jLYv/4q1Lv+Oui//iLUx7oq1Nu2Pui//krgk/2l+Uf91lL7/dJS8/0FFVv+CjUz/cHhM/0tKQf9+hk3/yeJ1/7TMZf+20VD/yuFx/8jec//C2HD/xdpy/8DWcP++1G//vtZ0/6rIU/+nw0L/nL82/5q+NP+YvTT/lLkx/5K4Mf+QuDH/j7Qw/5G5MP+KsTLuirM57ZS+Lv+DnCH/iKS6/6jZ/P+cx+r/h6jF/0JHTf+DqMr/ibHU/0xUaf9aXEL/UVZS/2BjS/+QnVr/mKZg/9Lqc//D1Wv/yt9z/9Dmdv/L5Hb/qsVJ/6nCQv+fwDX/nb81/5m8NP+XtzP/lbky/5K3Mf+PtDD/k7kx/4yxMu6RsDrtmb8t/3uXKP+jw9r/j6vC/2d0Nf92gzn/h6Oo/6fZ/f+Vvdv/o9Pz/z5CUf+GrM3/Z3uT/0hIQ/9bYE7/doFX/0ZJS/+HkFj/nKFV/46aVP+ux0j/tMxB/6rIMP+ryzX/ocA1/6PCNf+avDL/k7Qx/5KyMP+VuDH/jK8z7pKuOu2avC//gJco/7bO2P+UpsH/cYEj/6K7G/+mv8X/l7XN/1ZZR/+x3Pf/dYiZ/42uwf+IpbT/a3+Q/15vgf9me5L/hKrM/0FDTf9edJf/S1NR/7HAOP9xdzz/TUw3/2t0Lv+Spy7/hZEp/5evMP+fvjH/k68x/5e2Mv+OrDPukq467Zu2Mv+JmyD/s8O5/7/R5/9SVTL/kJ8W/6u8uP+yyN7/V1Y0/7nR0f+es8L/hpmp/6bA1P+buMv/n7zP/3+Upv+fx+L/V2Js/7Lp//9rfHj/b3I9/36gx/+OuOD/WGaB/1BZY/9TXXP/Pz4//32MLP+hvDL/mLIz/5CsNO6UrjvtnLEz/5WrIf+SmW3/8/7+/29zd/81NS//foaM/+L3//9ERDP/orKj/7fK3P96g43/zun9/7/c8f/G5fv/qMbb/7DN4v9bY2n/uN34/2x6hP9ldoj/tOb//5a60P+Ns9X/fpzA/67h//+Gqc//QkJH/5GjLv+gtzP/kqs17pasO+2drzP/na8v/4iVKP/Bxcb/+////+Xp9/96fYz/6/H1/4CDhv+iqqz/z9vg/2Rlaf/i9Pv/x9no/6Cvv//R7P3/yuXy/1tiaP+51ef/g5Oh/4KWqP+ryOP/YmUu/42YPP+BiT//gZaD/6/e/f9yiq3/cXgp/6a6Mv+TqjXunKU77Z+tM/+eqTX/o64r/42XNf+0uJ//wcG5/32ET/+orZb/+vz///////+qr7r/a21Q/+v0/f/L1+D/XmJU/9Tj6//r+///ZWhs/7jIzP+ltbz/jJql/7jN5v9hZTr/w88x/7zGKf99hx3/psjm/5Gqx/96gCb/prYy/5mjNe6dpDvtoasy/5+oNP+gqTb/pq4w/5egJP+Tlyf/sLgr/5+pM/+gqHn/rLah/5ebY/+0tl//wMfL/6yzwv+Hikf/s7if//7//v98f4P/pa2t/83Z4f98f4b/5vj//1RXVP+NjS//jpUl/4ybi//V8P//dX91/5ieJ/+jrDP/m6I17p6iO+2lqDT/oaQ0/6KnNf+lqzb/qqs3/6+yOP+ssjj/tbg5/66yLf+jqSn/yspf/9bVef+3uW7/i4xp/8TFav+9vWj/vsK+/4yQmP9xdoH/9/z//11dY//o7fH/paiw/0lHTP9HRkX/4fD4/6ayvv9xcyT/q7E0/6SoNP+coTXuoKI87aWkM/+hozX/oqQ0/6enN/+rqTj/qqk4/66uOf+ysDz/s7E7/7SzPv/JxG//zsx4/9LRdP/U03L/09J4/9LRc/+/wGb/pKVn/4iEXf+8wKr/XGFY/5OWif/8/f//+P3//5+jtf/q8v//q7C3/0FBN/+UmTf/q6o0/56eNe6lnT3tqaM1/6WfNP+lnzX/qqM3/6qmOP+rqDn/r6k5/7KsOv+xrTr/urFJ/83Idv/MyHT/zMl0/83Kdf/My3X/zct1/9PQdv/W03j/2dR0/8XCZP++vW3/s7Jj/6quj/+6wbf/gode/6Gmkf/5+///g4ma/4KBKf+wqjb/oZo17qWcPe2poDT/pZ00/6WeNf+poDf/qqI2/6qlN/+wpTn/sKo4/7CqN/+8tU7/zsh3/8vFc//Mx3T/y8Zz/8zIdP/NyXb/yMNu/8bAaP/OyHr/zMVz/8/Hdf/PxnL/w75n/7axYP/Cu13/mpI1/5WWaf+Ag2P/nZMw/6yjNP+imTbupZk87aqcNf+mmTT/qZs1/6udN/+rnjf/rKA3/7CjOv+xpTr/r6I0/8G1Xf/LxXb/y8Jy/8rEcv/KxHL/ysVz/83Gd//Gv2n/tKY9/8rDbv/Kw3b/x79w/8a/cf/HvnH/yL1w/8m8df/FuGv/o5ot/7KlPv+1okr/qpo2/6KXNe6nlz7trZw1/6mZNf+pmTX/qpo2/6udN/+tnTj/sJ84/7GhOf+xojj/xbtp/8y+df/Lv3L/y8By/8vAcv/KwHL/zMN3/8W5Yv+2pD7/uKtG/8rBdf/JvnP/x7xw/8W6b//Eum//w7du/8a5c//BtG3/qZc6/7OdQv+4pEn/opc27q6UP+2xmTb/rJQ2/62WNv+ulTb/r5g2/66ZN/+ynDn/sJs3/7SgQv/KuXH/yrty/8q7cf/KvHH/y7xx/8u8cf/Mv3X/wLBa/7upSP+zoTn/u61P/8y+eP/JuXD/x7dv/8S3b//EtW7/xLNt/8i2cv/CsGv/qpQ6/7ihQv+xoEnur5M+7bOYNv+ukzb/rpM2/66UNv+ulDb/rpU2/7OYOf+xlzX/uqRP/828e//Lu3b/y7x2/8q7df/Lu3T/yrty/8y9d/+9qVX/u6dH/7WePv+xmTX/wqxf/8u6d//HtG7/xrNu/8Wybf/Fsm3/xbBs/8iycf/Brmr/rpk7/7GYQO64n1rtspMz/7GSN/+vkjf/r5E3/66RN/+vkjf/spU4/7OVNv+3nET/vaZV/8CpWP/ErWP/x7Bo/8eybP/ItnD/zLl5/72hTf+zmDj/tJs8/7OXOP+yljf/xq5p/8m1df/GsW7/xbBu/8Wubf/Fr2z/xa9s/8iycf/GsWn/spxS7tHBne2wiiz/sZA3/7GQN/+xkDf/sZA3/7GQN/+wkTf/spM4/7OSN/+ykjL/spEz/7KSNf+zlDb/tJY6/7aYPv+5m0X/tpg+/7KVNv+zlTn/tJU4/7KRNP+3lj7/x69r/8ewb//HsW//yLNz/8iycv/IsnP/x7Jx/8u0b//Uyajuw9OWEcOnZv+thCb/s402/7ONN/+zjTf/so43/7KON/+zjjb/so43/7SQOf+1kTn/tZI5/7WSOf+0kTj/tJA2/7OQNf+0kjj/tZI5/7WSOP+1kTn/tZA5/7KONv+zjjf/tZI7/7eVQf+6mEb/u5xM/72fU/+9n07/z7qB/8LSlhEAAQAAw9KWEcOlZP+zhyz/t40z/7mQOP+5kDj/uZA4/7mQOP+5kDj/uZA4/7qSOf+6kzr/upM7/7qTO/+6kzr/upM6/7qSOv+6kzv/upM6/7qSOP+5kTj/uZA4/7iPN/+4jzX/uI41/7eNNP+1ii//sYUm/8ChWf/D0pYRAAEBAAAAAAAAAAAAwtKWEdHBnO26mVjtsoo/7bOKPe2zij/ts4o+7bOKPu2zij7ts4o+7bOKPu2zij7ts4o+7bOKPu2zij7ts4o+7bOKPu2zij7ts4s+7bOKPu2zij7ts4o+7bOKP+2zij7tsos+7bqZWe3RwJztw9KWEQEAAAAAAQAA'
    display_name = 'Chochox'
    MAX_CORE = 4
    ACCEPT_COOKIES = [r'(.*\.)?(chochox\.com)']

    def read(self):
        self.session = Session()
        info = get_imgs_www(self.url, self.session)
        for img in info['imgs']:
            self.urls.append(img)
        self.title = clean_title(info['title'])

def get_imgs_www(url,session):
    soup = Soup(downloader.read_html(url, session=session))
    #soup = Soup(downloader.read_soup(url,session=session))
    info = {}
    imgs = []
    info['title'] = soup.find('h1').text.strip()
    view = soup.find('div', class_='wp-content').findAll('img')
    for imgv in view:
        img = imgv.attrs['src']
        if not img:
            continue
        imgs.append(img)
    info['imgs'] = imgs
    return info