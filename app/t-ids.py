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
        self.win = GraphicsWindow()
        self.win.setMainWindow(self)
        self.setCentralWidget(self.win)

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
        self.win.setMode()

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
                                    statusTip="Cut the current selection's contents to the clipboard", )
        # triggered=self.textEdit.cut

        self.copyAct = QtGui.QAction(QtGui.QIcon(':/images/copy.png'),
                                     "&Copy", self, enabled=False, shortcut=QtGui.QKeySequence.Copy,
                                     statusTip="Copy the current selection's contents to the clipboard", )
        # triggered=self.textEdit.copy

        self.pasteAct = QtGui.QAction(QtGui.QIcon(':/images/paste.png'),
                                      "&Paste", self, shortcut=QtGui.QKeySequence.Paste,
                                      statusTip="Paste the clipboard's contents into the current selection", )
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
    def __init__(self, title=None, size=(800, 800), **kargs):
        # mkQApp()
        super(GraphicsWindow, self).__init__(**kargs)
        self.modes = ['InsertTunnel', 'NoMode']
        self.mode = 'NoMode'
        self.resize(*size)
        if title is not None:
            self.setWindowTitle(title)
        self.vb = self.addViewBox()
        self.vb.disableAutoRange(pg.ViewBox.XYAxes)
        self.vb.setAspectLocked(True,ratio=None)
        # self.vb.setMouseEnabled(False,False)
        # self.vb.setBackgroundColor('w')
        self.mw = None
        self.axis = Axis(100)
        self.axis.setPos(0,0)
        self.axis.setRotation(0)
        self.vb.addItem(self.axis)
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

    def caclTunPts(self, pt, l, h):
        fourPts = [pt]
        fourPts.append(QtCore.QPointF(pt.x() + l, pt.y()))
        fourPts.append(QtCore.QPointF(pt.x(), pt.y() + h))
        fourPts.append(QtCore.QPointF(pt.x(), pt.y() - h))
        return fourPts

    def scenemousePressed(self, evt):
        if evt.buttons() & QtCore.Qt.LeftButton and self.mode == 'InsertTunnel':
            mousePt = self.vb.mapSceneToView(evt.scenePos())
            fourPts = self.caclTunPts(mousePt, 150, 80)
            t1 = TTunnel(fourPts[0], fourPts[1])
            t2 = Tunnel(fourPts[0], fourPts[2])
            t3 = Tunnel(fourPts[0], fourPts[3])
            self.vb.addItem(t1)
            self.vb.addItem(t2)
            self.vb.addItem(t3)
            self.vb.scene().update()
        self.mode = 'NoMode'
        evt.accept()


def vp_add(v, p):
    return pg.Point(v.x() + p.x(), v.y() + p.y())

def v_rotate(v, angle):
    tr = pg.SRTTransform3D()
    tr.setRotate(angle, (0, 0, 1))
    return tr.map(v)

class Tunnel(pg.GraphicsObject):
    def __init__(self, start, end):
        pg.GraphicsObject.__init__(self)
        self.start = start
        self.end = end
        self.width = 15

    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        p.setPen(
            QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))
        pts = self.caclVector()

        lx = min(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        rx = max(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        ty = max(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        dy = min(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())

        p.drawLine(pts[0], pts[1])
        p.drawLine(pts[2], pts[3])
        p.setPen(
            QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DotLine, QtCore.Qt.SquareCap))
        p.drawRect(lx,-ty,rx-lx,ty-dy)

    def caclVector(self):
        pts = []
        spt = self.start
        ept = self.end
        v = pg.Vector(ept - spt)

        v.normalize()
        v = v * self.width
        v = v_rotate(v,90)

        pts.append(vp_add(v, spt))
        pts.append(vp_add(v, ept))

        v = v_rotate(v,180)

        pts.append(vp_add(v, spt))
        pts.append(vp_add(v, ept))

        return pts

    def mouseDoubleClickEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton:
            msg = QtGui.QMessageBox()
            msg.setText("XXXX")
            msg.exec_()
            evt.accept()

    def boundingRect(self):
        pts = self.caclVector()
        lx = min(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        rx = max(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        ty = max(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        dy = min(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        return QtCore.QRectF(lx,-ty,rx-lx,ty-dy)
        # return QtCore.QRectF()

class TTunnel(Tunnel):
    def __init__(self, start, end):
        super(TTunnel, self).__init__(start, end)

    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        p.setPen(QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))
        pts = Tunnel.caclVector(self)
        p.drawLine(pts[0], pts[1])
        p.drawLine(pts[2], pts[3])
        p.drawLine(pts[1], pts[3])

        lx = min(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        rx = max(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        ty = max(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        dy = min(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        p.setPen(
            QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DotLine, QtCore.Qt.SquareCap))
        p.drawRect(lx,-ty,rx-lx,ty-dy)
        # p.drawRect(self.bound)
        def boundingRect(self):
            pts = self.caclVector()
            lx = min(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
            rx = max(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
            ty = max(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
            dy = min(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
            return QtCore.QRectF(lx,-ty,rx-lx,ty-dy)

    def mouseDoubleClickEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton:
            msg = QtGui.QMessageBox()
            msg.setText("TunnelWK")
            msg.exec_()
            evt.accept()


class Axis(QtGui.QGraphicsPathItem):
    def __init__(self,l):
        super(Axis,self).__init__()
        self.opts = {'pxMode':True}
        self.l = l
        path = QtGui.QPainterPath()
        path.moveTo(0,0)
        path.lineTo(0,-l)
        path.moveTo(0,0)
        path.lineTo(l,0)
        angle = 150
        arrowL = 20

        path.moveTo(l,0)
        v = v_rotate(pg.Vector(1,0),-angle)
        v = v*arrowL
        pt = vp_add(v,pg.Point(l,0))
        path.lineTo(pt)

        path.moveTo(l,0)
        v = v_rotate(pg.Vector(1,0),angle)
        v = v*arrowL
        pt = vp_add(v,pg.Point(l,0))
        path.lineTo(pt)

        path.moveTo(0,-l)
        v = v_rotate(pg.Vector(0,-1),angle)
        v = v*arrowL
        pt = vp_add(v,pg.Point(0,-l))
        path.lineTo(pt)

        path.moveTo(0,-l)
        v = v_rotate(pg.Vector(0,-1),-angle)
        v = v*arrowL
        pt = vp_add(v,pg.Point(0,-l))
        path.lineTo(pt)
        self.setPath(path)
        self.setPen(pg.fn.mkPen(color = 'w'))
        self.setFlags(self.flags() | self.ItemIgnoresTransformations)
        # self.setBrush(pg.fn.mkBrush()
    def paint(self, p, *args):
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        QtGui.QGraphicsPathItem.paint(self, p, *args)

    def shape(self):
        #if not self.opts['pxMode']:
            #return QtGui.QGraphicsPathItem.shape(self)
        return self.path()

    ## dataBounds and pixelPadding methods are provided to ensure ViewBox can
    ## properly auto-range
    def dataBounds(self, ax, frac, orthoRange=None):
        pw = 0
        pen = self.pen()
        if not pen.isCosmetic():
            pw = pen.width() * 0.7072
        if self.opts['pxMode']:
            return [0,0]
        else:
            br = self.boundingRect()
            if ax == 0:
                return [br.left()-pw, br.right()+pw]
            else:
                return [br.top()-pw, br.bottom()+pw]

    def pixelPadding(self):
        pad = 0
        if self.opts['pxMode']:
            br = self.boundingRect()
            pad += (br.width()**2 + br.height()**2) ** 0.5
        pen = self.pen()
        if pen.isCosmetic():
            pad += max(1, pen.width()) * 0.7072
        return pad


def test():
    spt = pg.Point(0, 0)
    ept = pg.Point(1, 1)
    v = pg.Vector(ept - spt)

    tr = pg.SRTTransform3D()
    tr.setRotate(90, (0, 0, 1))
    v1 = tr.map(v)

    print pg.Vector(spt) + v1

    print v.length()
    v.normalize()
    print v * 20
    print v


def main():
    app = QtGui.QApplication([])
    mainWindow = MainWindow()

    mainWindow.show()
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()  # Start Qt event loop unless running in interactive mode or using pyside.


if __name__ == '__main__':
    main()
    # test()



