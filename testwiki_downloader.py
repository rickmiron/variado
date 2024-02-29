#coding: utf-8
#title_en: Test
#comment: Test https://www.wikipedia.org/
import downloader
from utils import Downloader, Soup, clean_title, LazyUrl
from io import BytesIO
USERAGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

class Downloader_wikipedia(Downloader):
    type = 'wikipedia' #default root folder name and if you are going to change it you must restart the program for the changes to work
    URLS = ['https://www.wikipedia.org/'] #is the type of url that will be accepted
    display_name = 'Test'
    #icon = 'base64:codigo_base64' #If you want to show the page icon you can place it in a base64 format string
    PARALLEL = 2 #number of tasks of the same type to download in parallel
    MAX_CORE = 3 #number of files to download in parallel
    ACCEPT_COOKIES = [r'(.*\.)?(wikipedia\.org)']
    user_agent = USERAGENT

    def read(self):
        # Required data
        self.title = 'The title' #self.title It is of type string: it is the title that the task will carry
        self.urls=['www.test.com/archivo.jpg'] #self.urls It is of type list: they are the urls of the files that you are going to download

        #optional data
        # If they are not set, their default value will be set.
        self.filenames[self.url] = 'nombre_archivo.jpg'  # self.filenames It is of type dictionary: they are the names of the files that you are going to download
        self.enableSegment(chunk=2**20,n_threads=4) #It is to indicate if you want your file to be downloaded in parts
        #chunk is the size in bytes that your file will be downloaded in each thread
        #n_threads is the number of threads that will be used
        self.disableSegment()
        self.single=False # By default it is False
        #you indicate whether it is one file (True) or several (False), if false the files will be downloaded to a folder
        self.urls, self.filenames, thumb = get_imgs(self.url)
        self.setIcon(thumb) #self.setIcon(thumb) is the image that will be shown in the task
        
class Image:
    def __init__(self, urlrefer, nombre):
        self.filename = clean_title(nombre)
        self.urx = urlrefer 
        self.url = LazyUrl(urlrefer, self.get, self)
        # LazyUrl It is activated at the time of file download
        # Normally the get function is to download another page that contains the file
        # but since the file in this example is on the same page it only returns the same value

    def get(self,_):
        return self.urx

def get_imgs(url):
    html = downloader.read_html(url,user_agent=USERAGENT) #downloader.read_html() It is used to download the html file from the url you provide
    # some pages require user_agent and referer: downloader.read_html(url,user_agent=USERAGENT,referer='www.referer.com')
    soup = Soup(html) # Soup() It is used to analyze the html file and obtain the data that is needed
    archivo = 'https://www.wikipedia.org/' + soup.find('img', class_='central-featured-logo')['src']
    #to search for tag, class or id you can use find o findAll
    #find: returns the first element it finds
    #findAll: can search all elements and returns them as a list
    #for search 'tag' use find('div')
    #for 'class' use find(class_='menu')
    #for 'id' use find(id='showmore')

    #Now find an image to show in the task.
    urlthumb = 'https://www.wikipedia.org/' + soup.find('link', {'rel': 'apple-touch-icon'})['href']
    # get the url of the image
    thumb = BytesIO()
    # create a variable of type ByteIO()
    downloader.download(urlthumb, buffer=thumb)
    # use the downloader.download() function to obtain the bytes of the image
    # urlthumb: is the url of the image
    # buffer: It is where the downloaded bytes of the image will be placed
    nombre = clean_title(soup.find('title').text)
    # If you want to give the file a name, it must be valid.
    # You can use the 'clean_title' function to prevent the name from having invalid characters.
    listaarchivos=[]
    listaarchivos.append(archivo)
    #You can also use the LazyUrl function to analyze the file when it comes its turn to download.
    urllazy = soup.find('meta', {'property': 'og:image'})['content']
    listaarchivos.append(Image(urllazy,'LazyImage.png').url)
    return listaarchivos, {archivo: nombre+'Image.png'}, thumb