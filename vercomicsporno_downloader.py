#coding:utf-8
#title_en:Vercomicsporno
#comment:https://vercomicsporno.com/
import downloader
from utils import Downloader,Session,clean_title
@Downloader.register
class Downloader_chochox(Downloader):
    type = 'vercomicsporno'
    URLS=['vercomicsporno.com']
    icon='base64:iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAACtVBMVEUAAADr3lBGREJGRUPq41H+AABDQT//1McuLCpAPTz+3ND+4dWkgGvq3VD9w7U6OTczMTD/0MS2l4T/AAD/AAGAVT+wjXiNYUv1u6ZHRULyx7r+yLyeeWREQT3n103vz8P7DAb/AQBANCaSaFP7wbL5Phf1zb/sx0erhnH60sX9AwDylzaui3b+2Mv/AAD0w7L/AQD/AADvsZ6yhWtCPTc7LBpBMRHtwUXixLj+AgDRsaEpJSX4TBve0kw+JwnwqZr8FgnCmopEPDT/AQD/AQBAODH31cjkp5S2kX5COzNBPDW+no7JlGgzGgDxizNDOzLzcig1Kh+AVSv/AAG/YDDapZP/AABBOTXexGHwozvos6KCeD/Mm4vYAADzva35AgA2LywzKyPwsp7QpIP8EwndmYnwv5JIMAD/AwHvtEG7gHuogGvyAACKd3DHMSv/AgBDQT//BABANS37Jw6CXEXDp2T/BgCRdGiedWD+AQGrAABUHx7dsZlZUTWYEhC9GhUuKSOukaSHbF7fknytbFy6q0ftrpAvKiTqQSA1KxyLYE3/AADlIhyLXUGUb1jhYy+JTTjrn4eCQzajb1rGkXuvLyLVknDDPzXzYE67oVjqxIP+DAR7conWEA3HeEjmAAD0KxRBOjIzMwDut6VVQBXorpNURTzZp4nMpJSWh4DtwbDKimrRp3nwdGv1ZiTWLBLQxUj7Ig04NjI0MS7ZtKSTgnyJX0lVLRdZTUkuKidCPDQzLSbMsVz9IAvpwKfss6K0g1G7n3VBNyXxyLJ9ZTjimoW4opg5MiziooC4mHQ+NCvLn3DQu6+HfpU+JiDawLX5JRumkYfqnonRlm08KxtYRhpAQACPfDns0EryyabnxmxAIAGLXS7Bq59YTzA8NC7Zm4piV1FDNSK+lYDluqZDOy36rpyyZYfsAAAA53RSTlMA///////+////////////////Avf//////////+7///8WV//+/v////9B////CP+1NP//2zkf//+C/////x3///2oq+D/////m7f/Tgr/bf9jBpYQ/+aT//////8H/2H/nOdc6P//EMn///4d//5v+E5y////K/7/7wP/gP/9wsL//2my/8zJ/33gXf9u////lz3//69U/////9L/6iAKiawF0gyn/7r//+0wPf///f/v8/P///8t/+fJqf/qo4kp/2bI/33/i2D/lGL++7X//v+2PS8dBP////8IC///sf//Nf+Tff5bt8/EAAADA0lEQVR4nH1TZVcbQRTdnVnfbIyEKASaBCkJKV5ci5S6Gw7FKS51d3d3d3d3p+5uv6OzJEgP5/R+eu/dO2+ezGBY8Y6H2H8xEI7sHnTz9vbOctkj4ddufM9Ca4z1xKbkRaKTAdkFGFYRVJMTOTS5pGebIDKAQBAivCYgpwcEsryJJTEDRpf6vgtQNYqCXr64CKJuhBvykgBgLuVYCTHk6TUURQKv4LggCMgjK5AbpgOU/GmLLy7gAmEVzzTGeAqi3JdUeSPB7tCLSTr51EHoFI4PIIPerJwdYgy5MUrAR5MpbSXtxMKrYe4xAqVFh6YtlBjLbZlRylhiENmrva++gJoUgZIKRN069/T9p20Sm/IyYSUj2wViK2/b7ji62NjK85L0pcoGIoGsaRcUV+tA7nHUGF5KNifyrUZJs60hgiTFGp3I0AH2Cz5nbKzgJXliMm2e6Wd+EECmiGNw4rUHAPIpFBhLLEvUK/QzxrmrJfPJ5C7j7wEAqwOQjd1Qrtf7K9LM5voqUpx0B25SAACKvV2uKSvrrddoJOrlZFAX/mNfCAHLgj7pzX7DtavNSqOmfktgJz8kSQd0FAMgk+njH6VY5af006jXdEmQASFkmVwIZZW0j49D4650V/9cgg3r5+J/Qx0lZxg5BFSfbDtNm21IkPioYJ9LILZw4RSQyyAA0Y8d8dIQSWaU2pR68KWTD/cAsulxHpBBAsic0Qcbhp81FVVxV7d2rIqd1z8OUNEsEsjO83ZL2rjeR+JvdW4KMuewOEoWTQHU6l5HcPAoOlXPHXbx/UNR3oHY9btNTWhW1Pcx/pYPnj4mfm57glpUOjMYK+Dt2ueVBz7ztEPrKbznLdtdfLgHpJi8Idhkjv6WynMcz2nHC/jG7GfOH4D9QGs8+QoZv2hHkT9N2zkkwPEAr5ZtTkEoGt5g0bhmkKYpDAqas1vWJySQHc8xrPZeWJuxViENlkoNCs6gLVSpVCmuGzrxaZf0TzwSKCz33bICAzvfUgeG3Vkx60V+/p5D/0T/Ag8/nclbQPdgAAAAAElFTkSuQmCC'
    display_name='Vercomicsporno'
    MAX_CORE=4
    ACCEPT_COOKIES=[r'(.*\.)?(vercomicsporno\.com)']

    def read(self):
        self.session=Session()
        self.referer=self.url
        self.title,self.urls,self.filenames=get_imgs(self.url,self.session)

def get_imgs(url,ses):
    soup=downloader.read_soup(url,referer=url,session=ses)
    imgs=[]
    fn={}
    title=soup.find('h1').text.strip()
    p=0
    for imgv in soup.find('div',class_='wp-content').findAll('noscript'):
        img=imgv.find('img').attrs['src']
        if not img or not img.startswith('http'):
            continue
        imgs.append(img)
        fn[img]=str(p)+img[img.rfind('.'):]
        p+=1
    if '/girlD.png' in imgs[-1] or '/descargavcp.png' in imgs[-1]:
        imgs.pop()
    return clean_title(title),imgs,fn
