import requests
import struct
import constants

class InDig(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Insert Link Artist")

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
        tup = f_noserch(dig.getex())
        ui.edit.setText(str(tup)[1:-1])
        ui.downButton.click()

def f_noserch(url):
    url = url.replace("//hitomi.", "//ltn.hitomi.")
    url = url[:url.rfind(".html")] + ".nozomi"
    res = requests.get(url)
    if res.status_code in [200, 206]:
        arbuf = res.content
        if arbuf:
            data = memoryview(arbuf)
            return struct.unpack_from(">"+"i"*(len(data) // 4), data)

ficon = QtGui.QIcon()
ficon.addPixmap(
    QtGui.QPixmap("imgs/icons/disk.png")
)

ui.action_fread4 = QtGui.QAction(constants.mainWindow)
ui.action_fread4.setIcon(ficon)
ui.action_fread4.setObjectName("action_fread4")
ui.action_fread4.triggered.connect(showInDig)
ui.action_fread4.setText("Hitomi artist")
ui.menu_2.addAction(ui.action_fread4)
