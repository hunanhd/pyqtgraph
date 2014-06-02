# -*- coding: utf-8 -*-
"""
Demonstrates adding a custom context menu to a GraphicsItem
and extending the context menu of a ViewBox.

PyQtGraph implements a system that allows each item in a scene to implement its 
own context menu, and for the menus of its parent items to be automatically 
displayed as well. 

"""
from buildfuc import *
from mainwindow import MainWindow
import global_inst

def main():
    app = QtGui.QApplication([])

    translator = QtCore.QTranslator()
    translator.load("qt_zh_Tids.qm")
    app.installTranslator(translator)

    translator2 = QtCore.QTranslator()
    translator2.load("qt_zh_CN.qm")
    app.installTranslator(translator2)

    w = MainWindow()

    global_inst.mw_ = w
    global_inst.win_ = w.win

    w.show()

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()  # Start Qt event loop unless running in interactive mode or using pyside.


if __name__ == '__main__':
    main()