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
        self.win.find()

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
        self.setBackground((39, 40, 34))
        if title is not None:
            self.setWindowTitle(title)
        self.vb = self.addViewBox()
        self.vb.disableAutoRange(pg.ViewBox.XYAxes)
        self.vb.setAspectLocked(True, ratio=None)
        # self.vb.setMouseEnabled(False,False)
        # self.vb.setBackgroundColor((39,40,34))
        self.mw = None
        self.axis = Axis(100)
        self.axis.setPos(0, 0)
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

    def find(self):
        fourPts = self.caclTunPts(pg.Point(0,0), 150, 80)
        t1 = TTunnel(fourPts[0], fourPts[1])
        t2 = Tunnel(fourPts[0], fourPts[2])
        # t3 = Tunnel(fourPts[0], fourPts[3])
        t4 = Tunnel(fourPts[1], fourPts[2])
        t5 = Tunnel(fourPts[1], fourPts[3])
        self.vb.addItem(t1)
        self.vb.addItem(t2)
        # self.vb.addItem(t3)
        self.vb.addItem(t4)
        self.vb.addItem(t5)
        junctionClosure_helper(self.vb,fourPts[1])
        # junctionClosure_helper(self.vb,fourPts[2])
        # junctionClosure_helper(self.vb,fourPts[0])

        self.vb.scene().update()

def vp_add(v, p):
    return pg.Point(v.x() + p.x(), v.y() + p.y())


def v_rotate(v, angle):
    tr = pg.SRTTransform3D()
    tr.rotate(-angle)
    return tr.map(v)

def v_angle(a, b):
    """Returns the angle in degrees between this vector and the vector a."""
    n1 = a.length()
    n2 = b.length()
    if n1 == 0. or n2 == 0.:
        return None
    ## Probably this should be done with arctan2 instead..
    ang1 = np.arccos(np.clip(QtGui.QVector3D.dotProduct(a, b) / (n1 * n2), -1.0, 1.0))  ### in radians
    # print 'aaa:',a
    a = v_rotate(a,90)
    # print 'aaa:',a
    ang2 = np.arccos(np.clip(QtGui.QVector3D.dotProduct(a, b) / (n1 * n2), -1.0, 1.0))

    # print "ang1:",np.rad2deg(ang1),"ang2:",np.rad2deg(ang2)
    if ang1 < 0.5*np.pi:
        if ang2 < 0.5*np.pi:
            ang = ang1
        else:
            ang = 2*np.pi - ang1
    else:
        if ang2 < 0.5*np.pi:
            ang = ang1
        else:
            ang = 2*np.pi - ang1
    print "v_angle:",np.rad2deg(ang)
    # c = b.cross(a)
    # print "c:",c
    # print "ang:",ang
    # if c > 0:
    #     # ang *= -1.
    #     ang = np.pi * 2 - ang

    return ang * 180. / np.pi

class Tunnel(pg.GraphicsObject):
    def __init__(self, start, end):
        pg.GraphicsObject.__init__(self)
        self.spt = start
        self.ept = end
        self.spt1 = None
        self.spt2 = None
        self.ept1 = None
        self.ept2 = None
        self.width = 15

        self.caclVector()

    def __repr__(self):
        return "Tunnel:"+repr((self.spt, self.ept))

    def paint(self, p, *args):
        p.setRenderHint(p.Antialiasing)
        p.setPen(
            QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))

        # p.setBrush(QtGui.QBrush((255-39,255-40,255-34)))
        p.setBrush(QtGui.QBrush(QtGui.QColor(39, 40, 34)))
        # p.drawPolygon(self.spt, self.spt2, self.ept2, self.ept, self.ept1, self.spt1)


        # lx = min(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        # rx = max(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        # ty = max(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        # dy = min(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        #
        p.drawLine(self.spt1, self.ept1)
        p.drawLine(self.spt2, self.ept2)
        # p.setPen(
        #     QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DotLine, QtCore.Qt.SquareCap))
        # p.drawRect(lx,-ty,rx-lx,ty-dy)

    def caclVector(self):
        spt = self.spt
        ept = self.ept
        v = pg.Vector(ept - spt)

        v.normalize()
        v = v * self.width
        v = v_rotate(v, 90)

        self.spt1 = vp_add(v, spt)
        self.ept1 = vp_add(v, ept)

        v = v_rotate(v, 180)

        self.spt2 = vp_add(v, spt)
        self.ept2 = vp_add(v, ept)

    def dealWithPointBoundary(self, pt, v):
        line1 = QtCore.QLineF(self.spt1, self.ept1)
        line2 = QtCore.QLineF(self.spt2, self.ept2)
        pt1 = QtCore.QPointF()
        pt2 = QtCore.QPointF()
        isStart = False
        if pt == self.spt:
            isStart = True

        if line1.intersect(QtCore.QLineF(pt, vp_add(v, pt)), pt1) != QtCore.QLineF.NoIntersection:
            v1 = pg.Vector(pt1 - pt)
            v1.normalize()
            v.normalize()
            if (v + v1).length() != 0:
                if isStart:
                    self.spt1 = pt1
                else:
                    self.ept1 = pt1
        if line2.intersect(QtCore.QLineF(pt, vp_add(v, pt)), pt2) != QtCore.QLineF.NoIntersection:
            v2 = pg.Vector(pt2 - pt)
            v2.normalize()
            v.normalize()
            if (v + v2).length() != 0:
                if isStart:
                    self.spt2 = pt2
                else:
                    self.ept2 = pt2


    def mouseDoubleClickEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton:
            msg = QtGui.QMessageBox()
            msg.setText("XXXX")
            msg.exec_()
            evt.accept()

    def boundingRect(self):
        # lx = min(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        # rx = max(pts[0].x(),pts[3].x(),pts[2].x(),pts[1].x())
        # ty = max(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        # dy = min(pts[0].y(),pts[3].y(),pts[2].y(),pts[1].y())
        # return QtCore.QRectF(lx,-ty,rx-lx,ty-dy)
        return QtCore.QRectF(0, 0, 100, 80)


class TTunnel(Tunnel):
    def __init__(self, start, end):
        super(TTunnel, self).__init__(start, end)

    # def paint(self, p, *args):
    #     pts = Tunnel.caclVector(self)
    #     p.setRenderHint(p.Antialiasing)
    #     p.setPen(QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))
    #     p.setBrush(QtGui.QBrush(QtGui.QColor(39, 40, 34)))
    #     p.drawPolygon(self.spt, pts[0], pts[1], self.ept, pts[3], pts[2])
    #     p.drawLine(pts[0], pts[1])
    #     p.drawLine(pts[2], pts[3])
    #     p.drawLine(pts[1], pts[3])
    #
    #     lx = min(pts[0].x(), pts[3].x(), pts[2].x(), pts[1].x())
    #     rx = max(pts[0].x(), pts[3].x(), pts[2].x(), pts[1].x())
    #     ty = max(pts[0].y(), pts[3].y(), pts[2].y(), pts[1].y())
    #     dy = min(pts[0].y(), pts[3].y(), pts[2].y(), pts[1].y())
    #     p.setPen(
    #         QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DotLine, QtCore.Qt.SquareCap))
    #     # p.drawRect(lx,-ty,rx-lx,ty-dy)
    #     # p.drawRect(self.bound)
    #     def boundingRect(self):
    #         pts = self.caclVector()
    #         lx = min(pts[0].x(), pts[3].x(), pts[2].x(), pts[1].x())
    #         rx = max(pts[0].x(), pts[3].x(), pts[2].x(), pts[1].x())
    #         ty = max(pts[0].y(), pts[3].y(), pts[2].y(), pts[1].y())
    #         dy = min(pts[0].y(), pts[3].y(), pts[2].y(), pts[1].y())
    #         return QtCore.QRectF(lx, -ty, rx - lx, ty - dy)
    #
    # def mouseDoubleClickEvent(self, evt):
    #     if evt.button() == QtCore.Qt.LeftButton:
    #         msg = QtGui.QMessageBox()
    #         msg.setText("TunnelWK")
    #         msg.exec_()
    #         evt.accept()


class Axis(QtGui.QGraphicsPathItem):
    def __init__(self, l):
        super(Axis, self).__init__()
        self.opts = {'pxMode': True}
        self.l = l
        path = QtGui.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(0, -l)
        path.moveTo(0, 0)
        path.lineTo(l, 0)
        angle = 150
        arrowL = 20

        path.moveTo(l, 0)
        v = v_rotate(pg.Vector(1, 0), -angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(l, 0))
        path.lineTo(pt)

        path.moveTo(l, 0)
        v = v_rotate(pg.Vector(1, 0), angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(l, 0))
        path.lineTo(pt)

        path.moveTo(0, -l)
        v = v_rotate(pg.Vector(0, -1), angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(0, -l))
        path.lineTo(pt)

        path.moveTo(0, -l)
        v = v_rotate(pg.Vector(0, -1), -angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(0, -l))
        path.lineTo(pt)
        self.setPath(path)
        self.setPen(pg.fn.mkPen(color='w'))
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
            return [0, 0]
        else:
            br = self.boundingRect()
            if ax == 0:
                return [br.left() - pw, br.right() + pw]
            else:
                return [br.top() - pw, br.bottom() + pw]

    def pixelPadding(self):
        pad = 0
        if self.opts['pxMode']:
            br = self.boundingRect()
            pad += (br.width() ** 2 + br.height() ** 2) ** 0.5
        pen = self.pen()
        if pen.isCosmetic():
            pad += max(1, pen.width()) * 0.7072
        return pad

class JunctionEdgInfo:
    def __init__(self, id=None, soe=False, v=pg.Vector()):
        self.tunnel = id
        self.startOrEnd = soe
        self.v = v

    def __eq__(self, b):
        return self.tunnel == b.tunnel and self.startOrEnd == b.startOrEnd and self.v == b.v

    def __repr__(self):
        return "JunctionEdgInfo"+repr((self.tunnel, self.startOrEnd, self.v))


def buildJunctionEdgeInfo(tunnels, pt):
    ges = []
    for t in tunnels:
        info = JunctionEdgInfo()
        info.tunnel = t
        v = pg.Vector(t.ept - t.spt)
        v.normalize()
        # print "spt--->:",t.spt,"=+=+=+ept--->:",t.ept
        if t.spt == pt:
            info.startOrEnd = True
            info.v = v
        elif t.ept == pt:
            info.startOrEnd = False
            info.v = pg.Vector(-v)
        # print info.v,"+++>",v_angle(info.v,pg.Vector(1,0))
        ges.append(info)
    return ges

#至少需要2个元素才能正确的闭合
def edgeJunctionClosureImpl(junctionPt, ges):
    print "buildJunctionEdgeInfo==================================================="
    f = lambda v1, v2:(v1  + v2 )*(1.0/np.sin(-1*v_angle(v1,v2)))
    if len(ges) == 1:
        ges.append(ges[0])  #这么构成循环?
    ges.append(ges[0])

    for info in ges:
        print "info.angle:",v_angle(info.v,pg.Vector(1, 0))
        print "info.v:",info.v

    v3 = ges[0].v
    v3 = v_rotate(v3, 90)
    for i in range( len(ges) - 1):
        cv = pg.Vector.crossProduct(ges[i].v,ges[i + 1].v)
        # print "cv.length:",cv.length()
        # print "cv.angle:",v_angle(ges[i].v,)
        # print "cv.angle:",v_angle(ges[i].v,ges[i + 1].v)
        if cv.length() != 0:
            v3 = f(ges[i].v, ges[i + 1].v)
            print "v3:",v3
        else:
            v3 = -v3
        ges[i].tunnel.dealWithPointBoundary(junctionPt,v3)
        ges[i+1].tunnel.dealWithPointBoundary(junctionPt,v3)

def findLinesByPoint(vb,pt):
    all_items = vb.addedItems
    tunnels = []
    for item in all_items:
        if isinstance(item, Tunnel):
            if pt == item.spt or pt == item.ept:
                tunnels.append(item)
    return tunnels


def junctionClosure_helper(vb,pt):
    tunnels = findLinesByPoint(vb,pt)
    ges = buildJunctionEdgeInfo(tunnels, pt)
    print "len:", len(ges)
    f = lambda info: v_angle(info.v,pg.Vector(1, 0))
    if len(ges) > 0:
        print "befor sort:========================================================"
        for info in ges:
            print info.v,"--->",v_angle(info.v,pg.Vector(1,0))
        ges.sort(key = f)
        print "after sort:========================================================"
        for info in ges:
            print info.v,"--->",v_angle(info.v,pg.Vector(1,0))
        edgeJunctionClosureImpl(pt,ges)

def testFind():
    print findLinesByPoint(scene,pg.Point(0,0))

def test2():
    a = [
        JunctionEdgInfo(Tunnel(pg.Point(0, 1), pg.Point(2, 2)), True, pg.Vector(1, -1)),
        JunctionEdgInfo(Tunnel(pg.Point(2, 3), pg.Point(3, 6)), False, pg.Vector(1, 1)),
        JunctionEdgInfo(Tunnel(pg.Point(10, 21), pg.Point(34, 12)), True, pg.Vector(-1, -1))
    ]
    # print a[0].angle.angle(pg.Vector(1, 0))
    # print a[1].angle.angle(pg.Vector(1, 0))
    # print a[2].angle.angle(pg.Vector(1, 0))
    # print dir(pg.Vector(-1, -1))
    # print a
    # print a[0].tunnel.boundingRect()
    # a = sorted(a, key = lambda x: x.angle.angle(pg.Vector(1,0)))
    f = lambda info: v_angle(info.v,pg.Vector(1, 0))
    print a
    a.sort(key = f)
    print a
    print type(a[0])
    print f(a[0])
    # print a
    #
    # print a[0].tunnel.spt, a[0].tunnel.spt1, a[0].tunnel.spt2, a[0].tunnel.ept, a[0].tunnel.ept1, a[
    #     0].tunnel.ept2
    #
    # a[0].tunnel.dealWithPointBoundary(pg.Point(3, 6), pg.Vector(1, 0))
    #
    # print a[0].tunnel.spt, a[0].tunnel.spt1, a[0].tunnel.spt2, a[0].tunnel.ept, a[0].tunnel.ept1, a[
    #     0].tunnel.ept2
    #

def test():
    spt = pg.Point(0, 0)
    ept = pg.Point(1, 1)
    v = pg.Vector(ept - spt)

    tr = pg.SRTTransform3D()
    tr.setRotate(90, (0, 0, 1))
    v1 = tr.map(v)

    line = QtCore.QLineF(spt, ept)
    pt = pg.Point()

    v1 =pg.Vector(-1,1)
    print "v-->v1:",v_angle(v,v1)
    print "v1-->v:",v_angle(v1,v)
    # print line.intersect(QtCore.QLineF(pg.Point(-1, 0), pg.Point(0, -1)), pt)
    # print pt
    # print pg.Vector(spt) + v1
    #
    # print v.length()
    # v.normalize()
    # print v * 20
    # print v.x()
    # print -v

    v1 = pg.Vector(0, 1)
    v2 = pg.Vector(0, -1)
    print pg.Vector.crossProduct(v1, v2)


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
    # test2()

    # testFind()
    print v_rotate(pg.Vector(-1,0), 90)



