# -*- coding:utf-8 -*-
from buildfuc import *
import pyqtgraph as pg
from diaLogs import *
import global_inst


class TObject(pg.GraphicsObject):
    sigHoverEvent = QtCore.Signal(object)
    sigClicked = QtCore.Signal(object, object)
    def __init__(self):
        super(TObject, self).__init__()
        self.mouseHovering = False
        self.selectFlag = False
        self.currentPen = QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
    def hoverEvent(self, ev):
        hover = False
        if not ev.isExit():
            # if self.translatable and ev.acceptDrags(QtCore.Qt.LeftButton):
            #     hover=True
            for btn in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton, QtCore.Qt.MidButton]:
                if int(self.acceptedMouseButtons() & btn) > 0 and ev.acceptClicks(btn):
                    hover = True
            # hover = True
            if self.contextMenuEnabled():
                ev.acceptClicks(QtCore.Qt.RightButton)
            if self.selectFlag:
                hover = False
        if hover:
            # self.setAcceptHoverEvents(True)
            self.setMouseHover(True)
            self.sigHoverEvent.emit(self)
            ev.acceptClicks(
                QtCore.Qt.LeftButton)  ## If the ROI is hilighted, we should accept all clicks to avoid confusion.
            ev.acceptClicks(QtCore.Qt.RightButton)
            ev.acceptClicks(QtCore.Qt.MidButton)
        else:
            self.setMouseHover(False)
    def setMouseHover(self, hover):
        # print self.selectFlag
        ## Inform the ROI that the mouse is(not) hovering over it
        if self.mouseHovering == hover or self.selectFlag:
            return
        self.mouseHovering = hover
        if hover:
            self.currentPen = QtGui.QPen(QtCore.Qt.green, 0.4, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
        else:
            self.currentPen = self.pen
        self.update()

    def contextMenuEnabled(self):
        return True

    def raiseContextMenu(self, ev):
        if not self.contextMenuEnabled():
            return
        menu = self.getMenu()
        # menu = self.scene().addParentContextMenus(self, menu, ev)
        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def getMenu(self):
        self.menu = QtGui.QMenu()
        self.menu.setTitle("ROI")
        remAct = QtGui.QAction(self.tr("Remove selected items"), self.menu)
        remAct.triggered.connect(global_inst.win_.vb.remove)

        cancAct = QtGui.QAction(self.tr("Cancle"), self.menu)
        cancAct.triggered.connect(self.mouseCancleMenue)

        if self.selectFlag == False:
            remAct.setEnabled(False)
            cancAct.setEnabled(False)
        else:
            remAct.setEnabled(True)
            cancAct.setEnabled(True)
        self.menu.addAction(remAct)
        # self.menu.remAct = remAct

        remAllAct = QtGui.QAction(self.tr("Remove all items"), self.menu)
        remAllAct.triggered.connect(global_inst.win_.vb.removeAll)
        self.menu.addAction(remAllAct)
        self.menu.addAction(cancAct)
        # self.menu.cancAct = cancAct

        return self.menu

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton and self.contextMenuEnabled():
            self.raiseContextMenu(ev)
            ev.accept()

        elif global_inst.win_.mode is  'NoMode' and ev.button() == QtCore.Qt.LeftButton:
            if self.selectFlag and (ev.modifiers() & QtCore.Qt.ShiftModifier):
                # self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable,False)
                # self.setSelected(False)
                # self.selectFlag = self.isSelected()
                self.selectFlag = False
                self.currentPen = self.pen
            else:
                # self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable,True)
                # self.setSelected(True)
                # self.selectFlag = self.isSelected()
                self.selectFlag = True
                self.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
            # self.update()
            ev.accept()
        elif int(ev.button() & self.acceptedMouseButtons()) > 0:
            ev.accept()
            self.sigClicked.emit(self, ev)
        else:
            ev.ignore()
        self.update()


    def mouseCancleMenue(self):
        # self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable,False)
        # self.setSelected(False)
        # self.selectFlag = self.isSelected()
        self.selectFlag = False
        self.currentPen = self.pen
        self.update()
