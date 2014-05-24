# -*- coding: utf-8 -*-
"""
Demonstrates adding a custom context menu to a GraphicsItem
and extending the context menu of a ViewBox.

PyQtGraph implements a system that allows each item in a scene to implement its 
own context menu, and for the menus of its parent items to be automatically 
displayed as well. 

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from PyQt4.QtGui import QMainWindow

from PyQt4 import QtCore, QtGui
import sdi_rc

import math


class MainWindow(QtGui.QMainWindow):
    #sequenceNumber = 1

    def __init__(self, fileName=None):
        super(MainWindow, self).__init__()
        self.init()
        self.setWindowTitle(self.tr("MainWindown Title"))
        self.resize(900, 600)

    def closeEvent(self, event):
        pass

    def newFile(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def saveAs(self):
        pass

    def about(self):
        QtGui.QMessageBox.about(self, "About SDI",
                                "The <b>SDI</b> example demonstrates how to write single "
                                "document interface applications using Qt.")

    def setMode(self):
        win.setMode()

    def init(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

    def createActions(self):
        self.newAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'), "&New",
                                    self, shortcut=QtGui.QKeySequence.New,
                                    statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QtGui.QAction(QtGui.QIcon(':/images/open.png'),
                                     "&Open...", self, shortcut=QtGui.QKeySequence.Open,
                                     statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon(':/images/save.png'),
                                     "&Save", self, shortcut=QtGui.QKeySequence.Save,
                                     statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QtGui.QAction("Save &As...", self,
                                       shortcut=QtGui.QKeySequence.SaveAs,
                                       statusTip="Save the document under a new name",
                                       triggered=self.saveAs)

        self.closeAct = QtGui.QAction("&Close", self, shortcut="Ctrl+W",
                                      statusTip="Close this window", triggered=self.close)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                                     statusTip="Exit the application",
                                     triggered=QtGui.qApp.closeAllWindows)

        self.cutAct = QtGui.QAction(QtGui.QIcon(':/images/cut.png'), "Cu&t",
                                    self, enabled=False, shortcut=QtGui.QKeySequence.Cut,
                                    statusTip="Cut the current selection's contents to the clipboard",)
                # triggered=self.textEdit.cut

        self.copyAct = QtGui.QAction(QtGui.QIcon(':/images/copy.png'),
                                     "&Copy", self, enabled=False, shortcut=QtGui.QKeySequence.Copy,
                                     statusTip="Copy the current selection's contents to the clipboard",)
                # triggered=self.textEdit.copy

        self.pasteAct = QtGui.QAction(QtGui.QIcon(':/images/paste.png'),
                                      "&Paste", self, shortcut=QtGui.QKeySequence.Paste,
                                      statusTip="Paste the clipboard's contents into the current selection",)
                # triggered=self.textEdit.paste

        self.lineCmdAct = QtGui.QAction(
            QtGui.QIcon(':/images/linepointer.png'), self.tr("Drawline"), self,
            shortcut="Ctrl+L",
            statusTip=self.tr("Draw a line"),
            triggered=self.setMode)

        self.aboutAct = QtGui.QAction("&About", self,
                                      statusTip="Show the application's About box",
                                      triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                                        statusTip="Show the Qt library's About box",
                                        triggered=QtGui.qApp.aboutQt)

        # self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)
        # self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.lineCmdMenu = self.menuBar().addMenu(self.tr("Line"))
        self.lineCmdMenu.addAction(self.lineCmdAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

        self.lineCmdToolBar = self.addToolBar(self.tr("Line"))
        self.lineCmdToolBar.addAction(self.lineCmdAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")


class GraphicsWindow(pg.GraphicsLayoutWidget):

    def __init__(self, title=None, size=(800, 600), **kargs):
        # mkQApp()
        super(GraphicsWindow, self).__init__(**kargs)
        self.modes = ['InsertTunnel', 'NoMode']
        self.mode = 'NoMode'
        self.resize(*size)
        if title is not None:
            self.setWindowTitle(title)
        self.vb = self.addViewBox()
        self.mw = None

        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.vb.addItem(self.vLine, ignoreBounds=True)
        self.vb.addItem(self.hLine, ignoreBounds=True)

        self.proxy = pg.SignalProxy(
            self.vb.scene().sigMouseMoved, rateLimit=60, slot=self.scenemouseMoved)
        self.vb.scene().sigMouseClicked.connect(self.scenemousePressed)

    def setMode(self):
        self.mode = 'InsertTunnel'

    def setMainWindow(self, mw):
        self.mw = mw

    def scenemouseMoved(self, evt):
        # using signal proxy turns original arguments into a tuple
        pos = evt[0]
        if self.vb.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            self.msg = "x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y())
            self.mw.statusBar().showMessage(self.msg)
            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
            self.vb.scene().update()

    def caclFourPts(self, pt, l, h):
        fourPts = [pt]
        fourPts.append(QtCore.QPointF(pt.x() + l, pt.y()))
        fourPts.append(QtCore.QPointF(pt.x() + l, pt.y() + h))
        fourPts.append(QtCore.QPointF(pt.x(), pt.y() + h))
        return fourPts

    def scenemousePressed(self, evt):
        if evt.buttons() & QtCore.Qt.LeftButton and self.mode == 'InsertTunnel':
            mousePt = self.vb.mapSceneToView(evt.scenePos())
            fourPts = self.caclFourPts(mousePt, 100, 30)
            t1 = Tunnel(fourPts[0], fourPts[1])
            t2 = Tunnel(fourPts[1], fourPts[2])
            t3 = Tunnel(fourPts[2], fourPts[3])
            self.vb.addItem(t1)
            self.vb.addItem(t2)
            self.vb.addItem(t3)
            self.vb.scene().update()
            # ra = pg.PolyLineROI([[0,40], [100,40], [100,0], [0,0]], closed=False)
            # self.vb.addItem(ra)
        self.mode = 'NoMode'
        evt.accept()


class Tunnel(pg.GraphicsObject):
    sigClicked = QtCore.Signal(object)

    def __init__(self, start, end):
        pg.GraphicsObject.__init__(self)
        self.start = start
        self.end = end
        
    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        p.setPen(
            QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))
        p.drawLine(self.start, self.end)

    def mouseDoubleClickEvent(self, evt):
        # if (evt.pos().x() - self.points[0].x() <= 101 and  math.fabs(evt.pos().y() - self.points[0].y()) <= 2) or\
        # (math.fabs(evt.pos().x() - self.points[1].x()) <= 2 and evt.pos().y() - self.points[1].y() <= 42)\
                # or(evt.pos().x() - self.points[3].x() <= 102 and math.fabs(evt.pos().y() - self.points[3].y()) <= 2):
        # if evt.button() == QtCore.Qt.LeftButton:
        # evt.accept()
        pass

    def boundingRect(self):
        return QtCore.QRectF(self.start, QtCore.QPointF(self.start.x() + 100, self.start.y() + 30))

app = QtGui.QApplication([])
mainWindow = MainWindow()

win = GraphicsWindow()
win.setMainWindow(mainWindow)

mainWindow.setCentralWidget(win)
mainWindow.show()


# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
