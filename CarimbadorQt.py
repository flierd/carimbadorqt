import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image, ImageQt


class CarimbadorQt(QWidget):

    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.btnAbrir = QPushButton('Abrir')
        self.btnCapturar = QPushButton('Capturar')

        layout = QGridLayout()
        layout.addWidget(self.btnAbrir, 0, 0, 5, 10)
        layout.addWidget(self.btnCapturar, 0, 0, 10, 10)

        self.setGeometry(100, 50, 200, 200)

        self.setLayout(layout)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = CarimbadorQt()
    sys.exit(app.exec_())
