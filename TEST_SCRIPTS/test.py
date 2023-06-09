from QTNOME import QTNOME
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel

import sys

class WIN(QTNOME.WINDOW) :
    def __init__(self, parent, xi, yi, width, height) :
        super().__init__(parent)
        self.setGeometry(xi, yi, width, height)
        self.L = QLabel("QWEASDZXC",  self)
        #self.L.resize(50, 50)

    def resizeEvent(self, event) :
        print("@", self.L.height(), self.L.width())
        print("$", self.height(), self.width())
        self.L.setGeometry(self.width()//4, self.height()//4, self.width()//2, self.height()//2)

if __name__ == "__main__" :
    from random import randint

    QTNOME.INIT_UI()

    for _ in range(1) :
        randcolors = [randint(0, 255), randint(0, 255), randint(0, 255)]
        WI = QTNOME.CREATE_WINDOW([WIN, {"xi": randint(0, QtWidgets.QDesktopWidget().screenGeometry(-1).width() - 500),
                                  "yi": randint(0, QtWidgets.QDesktopWidget().screenGeometry(-1).height() - 300),
                                  "width": randint(0, 400), "height": randint(0, 250)}],
                                  name = str(_),
                                  window_bar_color="rgb({0}, {1}, {2})".format(*randcolors),
                                  window_border_color="solid rgb({0}, {1}, {2})".format(*randcolors),
                                  text_color="rgba(255, 255, 255, 1)",
                                  window_border_width=1,
                                  text_style="Z003")

    QTNOME.INTERFACE_ENVIREMENT.show()
    sys.exit(QTNOME.APP.exec())
