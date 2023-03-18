# QTNOME ENVIREMENT

![](ZZZ/ZZZ.jpg)

* [PROJECT LINK GITHUB](https://github.com/P-Y-R-O-B-O-T/QTNOME)

* [PROJECT LINK PYPI](https://pypi.org/project/QTNOME-P-Y-R-O-B-O-T)

* A UI envirement to create and run applications made in PyQt5.

* This gives a very simple but elegant look to the applications utilising QTNOME.

* Get rid of boring and ugly Window Managers.

* Special multi windowed applications need a dedicated envirement.

# CURRENT ISSUES FOR DESKTOP UIs

* We all are fond of ugly window managers and we hate them as we cant change them according to our needs.

* Whenever we hear about window managers, the first thing that comes to our mind is that they can't change colors according to developer's needs.

* Many a times we also need to create a UI in which the desktop of user is not required to be visible or we purposefully want it t be hidden so we use FullScreenWindows.

* But here the problem comes, we can't have multiple FullScreenWindows on single screen without being ineffecient at switching multiple FullScreenWindows.

* Also we can't have multiple NonFullScreenWindows along with FullScreenWindows without stacking them above or below FullScreenWindow and then doing Alt+Tab again and again.

* So overall issues that we have are :
	- Ugly(most of them) and Heavy(some of them) Window Managers
	- Situation in which we dont need Desktop UI to be visible
	- Multiple Windows with desktop UI hidden
	- And finally the combination of above three points

# COMPATIBILITY

* QTNOME is purely written in PyQt5 which means it is compatible with all Qt python bindings like PyQt5, PyQt6, PySide and etc.

* QTNOME works on Linux, OS-X, Windows (OS INDEPENDENT), the only condition is that the OS must have full Qt and python Qt binding support.

# INSTALLATION

> Install it using pip.

* Goto [PYPI](https://pypi.org/project/QTNOME-P-Y-R-O-B-O-T/)

# IMAGES AND VIDEOS

![](ZZZ/ZZZ0.png)

![](ZZZ/ZZZ1.png)

![](ZZZ/ZZZ2.png)

[See video demonstration here](https://drive.google.com/file/d/1cxeoc61BSyLolExkkdvrVIgnkHhjZhXE/view?usp=sharing)

# HOW IT WORKS ?

* Generally what happens when we create an application is we create a new window for each instance. Here only one window is opened and that is a FullScreenWindow. FullScreenWindow has a smooth and blurred image as background. Ths background image can be repalced by another image file as per choice.

* Windows that are instance of user defined UI classes can be opened. The UI classes need to be inherited from WINDOW class, except this thing large part of defining the class can go like defining a normal window class in Qt python bindings.

* These windows do not open as windows they are actually inplemented using frames inside the FullScreenWindow, they are movable and resizable QWidgets inside the FullScreenWindow that are maintained by WINDOW_MANAGER defined in QTNOME.

* The WINDOW_MANAGER is responsible for resizing the windows and closing them. Currently it has only these two features, will be upgraded as per need.

* Transparency effects can easily applied to create sophisticated looking application.

* Bottom-right corner of the window can be dragged to resize the window.

# HOW TO USE ?

* Firstly put a BACKGROUND.jpg in the work folder so that QTNOME can get the background image for application.

* Then consider the following code.

```python3
from QTNOME.QTNOME import *
from PyQt5 import QtWidgets

import sys

class WIN(QTNOME.WINDOW) :
    def __init__(self, parent, xi, yi, width, height) :
        super().__init__(parent)
        self.setGeometry(xi, yi, width, height)

if __name__ == "__main__" :
    from random import randint

    QTNOME.INIT_UI()

    for _ in range(10) :
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
```
