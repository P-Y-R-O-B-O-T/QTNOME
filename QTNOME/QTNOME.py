from PyQt5.QtWidgets import QDesktopWidget, QMainWindow, QFrame, QLabel, QGraphicsBlurEffect
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPainterPath, QRegion
from PyQt5.QtCore import Qt, QPoint, QRectF, QObject, QThread, pyqtSignal
from PyQt5 import QtWidgets

import threading
import time
import sys
import gc
import sip

from PyQt5.QtWidgets import QApplication

#$$$$$$$$$$#

class COLORS() :
    def __init__(self) :
        self.MAIN_WINDOW = {"BACKGROUND": "border: 7px solid rgb(28, 29, 50);\
                                           background-color: rgb(28, 29, 38)"}
        self.CLOSE_BUTTON = {"BACKGROUND": "background-color: #FF3942;\
                                            border: 0px; border-radius: {radius}px",
                             "TEXT_LABEL": "color: #FB2576"}
        self.WINDOW = {"WINDOW_STYLE": "border: {border_width}px {border_color};\
                                        background-color: rgba(0, 0, 0, 0);\
                                        border-radius: {border_radius}px",
                       "BAR": "color: {text_color};\
                               background-color: {bar_color};\
                               border-top-left-radius: {tlr}px;\
                               border-top-right-radius: {trr}px;\
                               border-bottom-left-radius: {blr}px;\
                               border-bottom-right-radius: {brr}px;\
                               padding-right: {rpadding}px",
                       "BODY": "background-color: {body_color}"}

#$$$$$$$$$$#

class CLOSE_BUTTON(QFrame) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.PARENT = parent
        
        self.PIXEL_MARGIN = 10
        self.HEIGHT = self.PARENT.height()//40
        self.WIDTH = self.HEIGHT

        self.INITIAL_X = self.PARENT.width() - self.WIDTH - self.PIXEL_MARGIN
        self.INITIAL_Y = self.PIXEL_MARGIN

    def init_ui(self) :
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(self.INITIAL_X, self.INITIAL_Y,
                         self.WIDTH, self.HEIGHT)
        self.setStyleSheet(COLORS_OBJ.CLOSE_BUTTON["BACKGROUND"].
                           format(radius=self.HEIGHT//2))

    def mousePressEvent(self, event) :
        sys.exit(0)

#$$$$$$$$$$#

class WINDOW_CLOSE_BUTTON(CLOSE_BUTTON) :
    def __init__(self, parent) :
        super().__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.PIXEL_MARGIN = self.PARENT.PARENT.height()//100
        self.HEIGHT = self.WIDTH = self.PARENT.PARENT.height()//80
        self.INITIAL_X = self.PARENT.width() - self.WIDTH - self.PIXEL_MARGIN
        self.INITIAL_Y = self.PIXEL_MARGIN

    def mousePressEvent(self, event) :
        self.PARENT.hide()
        self.PARENT.setParent(None)
        self.PARENT.PARENT.add_window_to_delete(self.PARENT)

    def mouseMoveEvent(self, event) :
        pass

#$$$$$$$$$$#

class WINDOW_RESIZE_EVENT_ELEMENT(QFrame) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.PARENT = parent

        self.HEIGHT = self.WIDTH = self.PARENT.PARENT.height()//75

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0); border: 0px")
        self.setGeometry(self.PARENT.width() - self.PARENT.PARENT.height()//75,
                         self.PARENT.height() - self.PARENT.PARENT.height()//75,
                         self.PARENT.PARENT.height()//75,
                         self.PARENT.PARENT.height()//75)

    def mousePressEvent(self, event) :
        self.PARENT.raise_()
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event) :
        delta = QPoint(event.globalPos() - self.old_pos)
        curr_pos = QPoint(event.globalPos())
        if self.PARENT.BODY.RESIZABLE :
            self.PARENT.resize(curr_pos.x() - self.PARENT.x(),
                                   curr_pos.y() - self.PARENT.y())

#$$$$$$$$$$#

class WINDOW_MANAGER(QFrame) :
    def __init__(self, name, resizable=True,
                 window_border_width=2,
                 window_bar_color="rgba(0, 0, 0, 1)",
                 window_border_color="rgba(0, 0, 0, 1)",
                 window_body_color="rgba(0, 0, 0, 0)",
                 text_style="",
                 text_color="rgba(255, 255, 255, 1)") :
        global INTERFACE_ENVIREMENT
        super().__init__(INTERFACE_ENVIREMENT)
        self.PARENT = INTERFACE_ENVIREMENT

        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.setMinimumSize(self.PARENT.width()//16,
                            self.PARENT.height()//16)

        self.NAME = name
        self.RESIZABLE = resizable
        self.WINDOW_BORDER_WIDTH = window_border_width

        self.setStyleSheet(COLORS_OBJ.WINDOW["WINDOW_STYLE"].
                           format(border_width=self.WINDOW_BORDER_WIDTH,
                                  border_color=window_border_color,
                                  border_radius=self.PARENT.height()//42))

        self.BAR = QLabel(self)
        self.BAR.setFont(QFont(text_style))
        self.BAR.setText(" "+self.NAME)
        self.BAR.setGeometry(0, 0, 0, self.PARENT.height()//40)
        self.BAR.setStyleSheet(COLORS_OBJ.WINDOW["BAR"].
                               format(bar_color=window_bar_color,
                                      tlr=self.PARENT.height()//42,
                                      trr=self.PARENT.height()//42,
                                      text_color=text_color,
                                      blr=0, brr=0,
                                      rpadding=(self.PARENT.height()//75)*2))
        self.BAR.show()

        self.CLOSE_BUTTON = WINDOW_CLOSE_BUTTON(self)
        self.CLOSE_BUTTON.init_ui()
        self.CLOSE_BUTTON.show()
        self.RESIZE_EVENT_ELEMENT = WINDOW_RESIZE_EVENT_ELEMENT(self)

    def new_resize(self, x, y) :
        self.resize(x + self.WINDOW_BORDER_WIDTH*2,
                    y + self.BAR.height() + self.WINDOW_BORDER_WIDTH)
        self.BODY.resize_ref(x, y)

    def new_setGeometry(self, xi=None, yi=None, x=0, y=0) :
        self.setGeometry(xi, yi,
                         x + self.WINDOW_BORDER_WIDTH*2,
                         y + self.BAR.height() + self.WINDOW_BORDER_WIDTH)
        self.BODY.setGeometry_ref(self.WINDOW_BORDER_WIDTH, self.BAR.height(),
                                  x - self.WINDOW_BORDER_WIDTH, y)

    def new_setMinimumSize(self, x, y) :
        self.setMinimumSize(max(x + self.WINDOW_BORDER_WIDTH*2,
                                self.PARENT.width()//16),
                            max(y + self.BAR.height() + self.WINDOW_BORDER_WIDTH,
                                self.PARENT.height()//16))
        self.BODY.setMinimumSize_ref(self.PARENT.width()//16 - self.WINDOW_BORDER_WIDTH*2,
                                     self.PARENT.height()//16 - self.BAR.height() - self.WINDOW_BORDER_WIDTH)
        self.resize(x, y)

    def new_setMinimumWidth(self, x) :
        self.setMinimumWidth(max(x + self.WINDOW_BORDER_WIDTH*2,
                                 self.PARENT.width()//16))
        self.BODY.setMinimumWidth_ref(max(x, self.PARENT.width()//16 - self.WINDOW_BORDER_WIDTH*2))
        self.resize(x, self.PARENT.height()//16)

    def new_setMinimumHeight(self, y) :
        self.setMinimumHeight(max(y + self.BAR.height() + self.WINDOW_BORDER_WIDTH,
                                  self.PARENT.height()//16))
        self.BODY.setMinimumWidth_ref(max(y, self.BAR.height() - self.WINDOW_BORDER_WIDTH))
        self.resize(self.PARENT.width()//16, y)

    def new_move(self, x, y) :
        self.move_ref(x, y)

    def mousePressEvent(self, event) :
        self.raise_()
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event) :
        delta = QPoint(event.globalPos()-self.old_pos)
        self.move(self.x()+delta.x(), self.y()+delta.y())
        self.old_pos = event.globalPos()

    def resizeEvent(self, event) :
        self.BAR.resize(self.width(), self.BAR.height())
        self.CLOSE_BUTTON.move(self.width() - self.CLOSE_BUTTON.WIDTH - self.CLOSE_BUTTON.PIXEL_MARGIN,
                               self.CLOSE_BUTTON.INITIAL_Y)
        self.RESIZE_EVENT_ELEMENT.move(self.width() - self.RESIZE_EVENT_ELEMENT.WIDTH,
                                       self.height() - self.RESIZE_EVENT_ELEMENT.HEIGHT)
        self.BODY.resize_ref(self.width() - self.WINDOW_BORDER_WIDTH*2,
                             self.height() - self.WINDOW_BORDER_WIDTH - self.BAR.height())

#$$$$$$$$$$#

class WINDOW(QFrame) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.PARENT = parent
        self.RESIZABLE = True
        self.PARENT.BODY = self
        self.PARENT.RESIZE_EVENT_ELEMENT.raise_()

        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5);\
                            border-width: 0px;\
                            border-color: rgb(255,0,0);\
                            border-top-left-radius: 0px;\
                            border-top-right-radius: 0px;\
                            border-bottom-left-radius: {blr}px;\
                            border-bottom-right-radius: {brr}px".
                           format(blr=self.PARENT.PARENT.height()//42,
                                  brr=self.PARENT.PARENT.height()//42))

        self.resize_ref = self.resize
        self.setGeometry_ref = self.setGeometry
        self.setMinimumSize_ref = self.setMinimumSize
        self.setMinimumWidth_ref = self.setMinimumWidth
        self.setMinimumHeight_ref = self.setMinimumHeight
        self.move_ref = self.move

        self.resize = self.new_resize
        self.setGeometry = self.new_setGeometry
        self.setMinimumSize = self.new_setMinimumSize
        self.setMinimumWidth = self.new_setMinimumWidth
        self.setMinimumHeight = self.new_setMinimumHeight
        self.move = self.new_move

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.new_setMinimumSize(0,0)
        self.new_setGeometry(self.PARENT.PARENT.width()//2 - self.PARENT.width()//2,
                             self.PARENT.PARENT.height()//2 - self.PARENT.height()//2,
                             0, 0)
        self.show()

    def new_resize(self, x, y) :
        self.PARENT.new_resize(x, y)

    def new_setGeometry(self, xi, yi, x, y) :
        self.PARENT.new_setGeometry(xi, yi, x, y)

    def new_setMinimumSize(self, x, y) :
        self.PARENT.new_setMinimumSize(x, y)

    def new_setMinimumWidth(self, x) :
        self.PARENT.new_setMinimumWidth(x)

    def new_setMinimumHeight(self, y) :
        self.PARENT.new_setMinimumHeight(y)

    def new_move(self, x, y) :
        self.PARENT.new_move(x, y)

    def set_resizable(self, value) :
        self.RESIZABLE = value

    def mousePressEvent(self, event) :
        pass

    def mouseMoveEvent(self, event) :
        pass

    def resizeEvent(self, event) :
        pass

#$$$$$$$$$$#

class MEMORY_RELEASER(QObject) :
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def add_parent_reference(self, parent) :
        self.PARENT = parent

    def run(self) :
        global APP
        while (True) :
            time.sleep(1)
            for _ in range(len(self.PARENT.WINDOWS_TO_DELETE)) :
                self.PARENT.LOCK.acquire()
                to_be_deleted = self.PARENT.WINDOWS_TO_DELETE.pop(0)
                to_be_deleted.close()
                to_be_deleted.deleteLater()
                to_be_deleted.setParent(None)
                sip.delete(to_be_deleted)
                self.PARENT.LOCK.release()
                APP.processEvents()
                APP.flush()
                gc.collect()

        self.finished.emit()

class UI_ENV(QMainWindow) :
    def __init__(self) :
        super().__init__()
        self.init_ui()

    def init_ui(self) :
        global COLORS_OBJ

        self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.LOCK = threading.Lock()
        self.WINDOWS_TO_DELETE = []

        self.THREAD = QThread()
        self.MEMORY_RELEASING_PROCESS = MEMORY_RELEASER()
        self.MEMORY_RELEASING_PROCESS.add_parent_reference(self)
        self.MEMORY_RELEASING_PROCESS.moveToThread(self.THREAD)
        self.THREAD.started.connect(self.MEMORY_RELEASING_PROCESS.run)
        self.MEMORY_RELEASING_PROCESS.finished.connect(self.THREAD.quit)
        self.MEMORY_RELEASING_PROCESS.finished.connect(self.MEMORY_RELEASING_PROCESS.deleteLater)
        self.THREAD.finished.connect(self.THREAD.deleteLater)
        self.MEMORY_RELEASING_PROCESS.progress.connect(self.progress_tracker)
        self.THREAD.start()

        flags = Qt.WindowFlags(Qt.FramelessWindowHint |
                               Qt.WindowStaysOnTopHint)

        self.setWindowFlags(flags)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(QtWidgets.QDesktopWidget().screenGeometry(-1).width(),
                    QtWidgets.QDesktopWidget().screenGeometry(-1).height())
        self.setStyleSheet(COLORS_OBJ.MAIN_WINDOW["BACKGROUND"])
        self.add_background_image()

        self.CLOSE_BUTTON = CLOSE_BUTTON(self)
        self.CLOSE_BUTTON.init_ui()
        self.CLOSE_BUTTON.show()

    def add_background_image(self) :
        self.blurlabel = QLabel(self)
        self.blurlabel.setGeometry(0, 0,
                                   QtWidgets.QDesktopWidget().screenGeometry(-1).width(),
                                   QtWidgets.QDesktopWidget().screenGeometry(-1).height())
        pixmap = QPixmap('BACKGROUND.jpg')
        self.blurlabel.setPixmap(pixmap)
        self.blurlabel.setScaledContents(True)
        self.blurlabel.show()
        sip.delete(pixmap)

    def add_window_to_delete(self, window) :
        self.LOCK.acquire()
        self.WINDOWS_TO_DELETE.append(window)
        self.LOCK.release()

    def show(self) :
        self.showFullScreen()

    def progress_tracker(self, value) :
        pass

#$$$$$$$$$$#

def CREATE_WINDOW(win_class, **wm_params) :
    global INTERFACE_ENVIREMENT
    window_manager_instance = WINDOW_MANAGER(**wm_params)
    window_instance = win_class[0](window_manager_instance, **win_class[1])
    window_manager_instance.show()
    return window_instance

def INIT_UI() :
    global COLORS_OBJ
    global INTERFACE_ENVIREMENT
    global APP

    COLORS_OBJ = COLORS()
    APP = QApplication(sys.argv)
    INTERFACE_ENVIREMENT = UI_ENV()
