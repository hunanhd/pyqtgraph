# -*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
from hairdryer import HairDryer
from fan import Fan
from tunnel import Tunnel
from findGE import *
import global_inst

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.disableAutoRange(pg.ViewBox.XYAxes)
        self.setAspectLocked(True, ratio=None)
        self.state['targetRange'] = [[0, 300], [0, 200]]
        self.state['viewRange'] = [[0,300],[0,200]]

    def resizeEvent(self,ev):
        self.setPos(0,0)

    def removeSelect(self):
        print "enter removeSelect+++++++++++++++"
        self.disableAutoRange(pg.ViewBox.XYAxes)
        all_items = global_inst.win_.vb.addedItems
        tunnels = findByClass(all_items,Tunnel)
        fans = findByClass(all_items,Fan)
        for b in tunnels:
            if b.selectFlag:
                # b.hide()
                self.removeItem(b)
        for f in fans:
            print f
            if f.selectFlag:
                self.removeItem(f)
                self.removeItem(f.arrow)
                # f.hide()
                # f.arrow.hide()
        print "leave removeSelect+++++++++++++++"

    def removeFans(self):
        all_items = global_inst.win_.vb.addedItems
        fans = findByClass(all_items,Fan)
        fan_Arrows = findByClass(all_items,pg.ArrowItem)
        for fan in fans:
            self.removeItem(fan)
            self.removeItem(fan.arrow)
            # fan.hide()
            # fan.arrow.hide()

    def removeAll(self):
        self.disableAutoRange(pg.ViewBox.XYAxes)
        all_items = global_inst.win_.vb.addedItems
        tunnels = findByClass(all_items,Tunnel)
        self.removeFans()
        for t in tunnels:
            print t
            # t.hide()
            self.removeItem(t)
        # for b in findAllTunnels(self):
        #     self.removeItem(b)

    def selectAll(self):
        # self.disableAutoRange(pg.ViewBox.XYAxes)
        all_items = global_inst.win_.vb.addedItems
        tunnels = findByClass(all_items,Tunnel)
        fans = findByClass(all_items,Fan)
        for b in tunnels:
            b.selectFlag = True
            b.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
        for f in fans:
            f.selectFlag = True
            f.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
            f.arrow.setStyle(pen = f.currentPen)
        self.update()

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        pg.ViewBox.mouseClickEvent(self, ev)

    def mouseDragEvent(self, ev):
        pg.ViewBox.mouseDragEvent(self, ev)

    def mouseMoveEvent(self, ev):
        pg.ViewBox.mouseMoveEvent(self, ev)

    def keyPressEvent(self, ev):
        all_items = global_inst.win_.vb.addedItems
        tunnels = findByClass(all_items,Tunnel)
        fans = findByClass(all_items,Fan)
        if ev.key() == QtCore.Qt.Key_Delete:
            self.removeSelect()
        if ev.key() == QtCore.Qt.Key_Escape:
            for b in tunnels:
                if b.selectFlag:
                    b.selectFlag = False
                    b.currentPen = b.pen
                    # b.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
                    self.update()
            for f in fans:
                if f.selectFlag:
                    f.selectFlag = False
                    f.currentPen = f.pen
                    # f.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
                    f.arrow.setStyle(pen = f.pen)
                    self.update()

        if ev.key() == QtCore.Qt.Key_A and ev.modifiers() & QtCore.Qt.ControlModifier:
            self.selectAll()

    def contextMenuEnabled(self):
        return True

    def raiseContextMenu(self, ev):
        if not self.contextMenuEnabled():
            return
        menu = self.getMenu()
        menu = self.scene().addParentContextMenus(self, menu, ev)
        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def getMenu(self):
        self.menu = QtGui.QMenu()
        self.menu.setTitle(self.tr("ViewBox options"))

        viewAll = QtGui.QAction(self.tr("View All"), self.menu)
        viewAll.triggered.connect(self.autoBtnClicked)
        if global_inst.mw_.autoAct.isEnabled():
            viewAll.setEnabled(True)
        else:
            viewAll.setEnabled(False)
        self.menu.addAction(viewAll)

        remAct = QtGui.QAction(self.tr("Remove selected items"), self.menu)
        remAllAct = QtGui.QAction(self.tr("Remove all items"), self.menu)
        remFanAct = QtGui.QAction(self.tr("Remove fans"), self.menu)
        selAllAct = QtGui.QAction(self.tr("Select all items"), self.menu)
        remAllAct.triggered.connect(self.removeAll)
        remAct.triggered.connect(self.removeSelect)
        remFanAct.triggered.connect(self.removeFans)
        selAllAct.triggered.connect(self.selectAll)

        all_items = global_inst.win_.vb.addedItems
        fans = findByClass(all_items,Fan)
        if len(fans) is 0:
            remFanAct.setEnabled(False)
        else:
            remFanAct.setEnabled(True)

        # allTunnels = findAllTunnels(self)
        allTunnels = findByClass(all_items,Tunnel)
        if len(allTunnels) is 0:
            remAct.setEnabled(False)
            remAllAct.setEnabled(False)
            selAllAct.setEnabled(False)
        else:
            i = 0
            for b in allTunnels:
                if b.selectFlag:
                    i = i+1
            if i == 0:
                remAct.setEnabled(False)
                selAllAct.setEnabled(True)
            else:
                remAct.setEnabled(True)
                selAllAct.setEnabled(False)
            remAllAct.setEnabled(True)

        self.menu.addAction(remAct)
        self.menu.addAction(remAllAct)
        self.menu.addAction(remFanAct)
        self.menu.addAction(selAllAct)
        return self.menu

    def autoBtnClicked(self):
        self.enableAutoRange()
