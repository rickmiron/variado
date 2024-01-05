import requests
import constants
from utils import Session, Soup

class InDig(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert Link Search")

        self.infd = QLineEdit(self)
        self.okbu = QPushButton("OK", self)
        self.cabu = QPushButton("Cancel", self)

        lay = QVBoxLayout(self)
        lay.addWidget(self.infd)
        lay.addWidget(self.okbu)
        lay.addWidget(self.cabu)

        pal = self.infd.palette()
        pal.setColor(QPalette.ColorRole.Text, QColor("red"))
        pal.setColor(QPalette.ColorRole.ButtonText, QColor("red"))
        self.infd.setPalette(pal)
        self.okbu.setPalette(pal)
        self.cabu.setPalette(pal)

        self.okbu.clicked.connect(self.accept)
        self.cabu.clicked.connect(self.reject)

    def getex(self):
        return self.infd.text()

def showInDig():
    dig = InDig(None)
    if dig.exec() == 1:
        arr = f_serch(dig.getex())
        ui.edit.setText(arr)
        ui.downButton.click()

def getcuki():
    return {cookie.name: cookie.value for cookie in Session().cookies if '.exhentai.org' in cookie.domain}

def f_serch(url):
    url = url.replace('/e-hentai.org/','/exhentai.org/')
    codigos = []
    for _ in range(100):
        resp = requests.get(url, cookies=getcuki(), headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        soup = Soup(resp.text)
        for elem in soup.findAll(class_='gl3t'):
            codigos.append(elem.find('a')['href'])
        dnext = soup.find(id='dnext')
        if not dnext:
            messageBox('Your IP is probably banned')
            break
        url = dnext.get('href')
        if not url:
            break
    return ', '.join(codigos)

ficon = QtGui.QIcon()
ficon.addPixmap(
    QtGui.QPixmap("imgs/icons/disk.png")
)

ui.action_fread5 = QtGui.QAction(constants.mainWindow)
ui.action_fread5.setIcon(ficon)
ui.action_fread5.setObjectName("action_fread5")
ui.action_fread5.triggered.connect(showInDig)
ui.action_fread5.setText("Ehentai search")
ui.menu_2.addAction(ui.action_fread5)
