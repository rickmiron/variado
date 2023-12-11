#coding:utf8
#title_en:Topgirl
#comment:https://kr#.topgirl.co/

import downloader
from utils import Downloader


@Downloader.register
class Downloader_Topgirl(Downloader):
    type = 'topgirl'
    URLS = ['.topgirl.co']
    single = True
    icon = 'base64:AAABAAEAEBAAAAEAIAAoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAtIx7cLiQf7S0iGu0vFg3tKzEr7SBoee0Wh6jtFZTC7RSQwe0afaXtJk1q7S8hJO0vGAztLSQd7S4lH+0tIh7cLSIf8zAiHP8wHhP/Hmly/wy24/8Gzf//Bc///wXM//8Ez///B8///wnG//8Yntr/LUFc/zAaEf8vJh7/LSIe8y4gGu0vHxP/FoKU/wTO//8Fxv//BsL//wfA/v8Hwf//B8D//wbB//8Gwv7/A83//w69/v8rTHz/MRsQ/y0kHe0vGAvtGnZ8/wTP//8Hwv//BsL//wfG//8Ey/7/B8X+/wbA//8Hwf//B8H//wfA/v8Dyf//ELv//y4+Yf8uGgztJEY67QnF8/8Gxf//BcT//xGw9/8pSmT/GXuM/wfC9/8EzP7/B8L//wbA//8Hwf7/B8D//wXP//8cl+P/Lx8m7ROIk+0Fz///B8H//wTI/v8Woun/Mx4g/zAWBv8nQ0D/E5e2/wbJ/v8Eyf//B8D+/wfB//8Fw/7/DsX//ytJd+0JstDtB8n//wfB//8EyP//FaTq/zApLv8sIRj/LxsS/y8eE/8iV1z/DqrR/wXK//8Gwf7/B8D+/wbN//8kdavtCb3o7QfG//8Hwf7/BMj//xWk6/8wKC7/LSEY/y0kHv8tIx3/LxkP/y4jF/8ZeIH/BMf//wfA//8Hz/7/IIHO7Qi96+0Hx///B8H//wTI//8UpOv/MCgu/y0gGf8tJB7/LSMe/y8aEf8vHBH/G3N6/wXI//8Hwf//B87+/yGC0u0JtdrtB8j//wfB//8Fyf7/FaTq/zAoLv8sIBn/Lh0X/zEZDf8kS0r/EKPD/wXJ//8Gwf//BsH//wfO/v8ieLTtEZSi7QXN//8Gwf7/BMj//xSj6f8xIib/MBQG/yozLf8XhZr/B8T7/wTK//8Hwf//B8H//wbD//8LyP//J1GE7SFTTe0Gyv7/B8P//wXG//8UrPH/LzVC/x9gZ/8Kt+L/BM3//wbC//8Gwf//B8H//wfB//8Ey///GKXw/y8lMO0uHRDtFY6a/wTO//8Hwf//CMD//w208f8Hx///Bcf//wfB//8Gwf//B8H//wfB//8Fxf//Csn//ypRgP8vFwvtLh4W7S0uHv8QoLv/BM///wfF//8Fxf7/B8L//wfB/v8Hwf7/BsH+/wfB//8Fyf//Ccr//yVqnv8xGxX/LSIZ7S0iH/MxHxn/LSwh/xeInv8Ix/3/Bc///wbK//8Gyf//B8j//wXM//8Gz///Ebb1/yhdiP8xHBX/LyQb/y0iHvMtIh/cLyUg7S4eFu0uGRDtJUxM7ReGo+0Rq9vtDLX07Q+08+0UndbtIHKZ7S0xQe0vFwztLSMZ7S4kH+0tIh7c'

    def read(self):
        soup = downloader.read_soup(self.url,user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        title = soup.find('div', class_='main_title').text.strip()
        src = soup.find('source')['src']
        self.urls.append(src)
        self.filenames[src] = clean_title(title)+'.mp4'
        self.referer = self.url
        self.title = title
        self.enableSegment(chunk=2**20,n_threads=2)

messageBox('If you are not in South Korea, you need VPN')
