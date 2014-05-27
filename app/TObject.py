# -*- coding:utf-8 -*-
from buildfuc import *
import pyqtgraph as pg
from dialogs import *
import global_inst


class TObject(pg.GraphicsObject):
    sigHoverEvent = QtCore.Signal(object)
    sigClicked = QtCore.Signal(object, object)
    def __init__(self):
        super(TObject, self).__init__()
        self.mouseHovering = False
        self.currentPen = QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
    def hoverEvent(self, ev):

        hover = False
        if not ev.isExit():
            # if self.translatable and ev.acceptDrags(QtCore.Qt.LeftButton):
            #     hover=True
            for btn in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton, QtCore.Qt.MidButton]:
                if int(self.acceptedMouseButtons() & btn) > 0 and ev.acceptClicks(btn):
                    hover = True
            if self.contextMenuEnabled():
                ev.acceptClicks(QtCore.Qt.RightButton)
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
        ## Inform the ROI that the mouse is(not) hovering over it
        if self.mouseHovering == hover:
            return
        self.mouseHovering = hover
        if not self.isSelected():
            if hover:
                self.currentPen = QtGui.QPen(QtCore.Qt.darkCyan, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
            else:
                self.currentPen = QtGui.QPen(QtCore.Qt.white, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
        self.update()

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
        self.menu.setTitle("ROI")
        remAct = QtGui.QAction("Remove ROI", self.menu)
        remAct.triggered.connect(global_inst.win_.vb.remove)
        self.menu.addAction(remAct)
        self.menu.remAct = remAct
        return self.menu

    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton and self.contextMenuEnabled():
            self.raiseContextMenu(ev)
            ev.accept()
        elif ev.button() == QtCore.Qt.LeftButton:
            self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
            self.setSelected(True)
            if self.isSelected():
                self.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
            else:
                self.currentPen = QtGui.QPen(QtCore.Qt.white, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
            ev.accept()

        elif int(ev.button() & self.acceptedMouseButtons()) > 0:
            ev.accept()
            self.sigClicked.emit(self, ev)
        else:
            ev.ignore()
        self.update()


