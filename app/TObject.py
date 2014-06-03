# -*- coding:utf-8 -*-
from buildfuc import *
import pyqtgraph as pg
from dialogs import *
import global_inst

"""
问题：
    TObject作为基类，从他派生Tunnel和HairDryer两个类，在TObject中翻译了，但是在派生类中的
    右键菜单中没有翻译（派生类中没有右键菜单的重载函数）

解决过程：

    1.在派生类中建立右键菜单烦，就是重载了getMenu()函数，这样做显得有点麻烦，并且没有重载函数
    的必要性，为了一个翻译重载显得多余

    2.查找文档：
    通过开始菜单-->python(x,y)-->document-->Python(x,y) Documentation ，
    然后打开libraries文件夹，找到pyqt4/doc/index.html，
    看“Internationalisation of PyQt4 Applications”下的内容

    后面提到了，c++可以保证正确的上下文，但python就不行，
    所以后面的例子就告诉用QtCore.QCoreApplication.translate
    第一个参数，随便写个名字就可以了（只是认为的分组，区分一下要翻译的内容而已），
    class A::tr(xx) 等价于 QtCore.QCoreApplication.translate("A", xx)

    这样就可以解释为什么python里派生类没有翻译
    因为QtCore.QCoreApplication.translate()函数需要一个上下文（就是一个字符串）
    而tr函数默认用“当前调用所在的类名字”作为上下文，它是通过moc处理的，

    所以b.hello()中翻译的时候，用的是上下文“A”
    但pyqt里没有moc，所以它使用”当前对象的类名字”作为上下文，所以b.hello()中翻译的时候，
    用的上下文“B”，但此时"B"这个上下文不存在（因为我们没有在translate函数中明确的指定它）

    以上的A和B是文档例子的类名。具体参见文档

解决方法：
    把TObject的self.tr()函数换成QtCore.QCoreApplication.translate()函数,这样既不用重载没有必要重载的
    函数，也可以顺利解决问题
"""

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
        self.menu.setTitle(self.tr("TObjectMenu"))
        remAct = QtGui.QAction(QtCore.QCoreApplication.translate('TObject',"Remove selected items"), self.menu)
        remAct.triggered.connect(global_inst.win_.vb.removeSelect)

        cancAct = QtGui.QAction(QtCore.QCoreApplication.translate('TObject',"Cancle"), self.menu)
        cancAct.triggered.connect(self.mouseCancleMenue)

        if self.selectFlag == False:
            remAct.setEnabled(False)
            cancAct.setEnabled(False)
        else:
            remAct.setEnabled(True)
            cancAct.setEnabled(True)
        self.menu.addAction(remAct)
        # self.menu.remAct = remAct

        remAllAct = QtGui.QAction(QtCore.QCoreApplication.translate('TObject',"Remove all items"), self.menu)
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
                self.selectFlag = False
                self.currentPen = self.pen
            else:
                # self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable,True)
                # self.setSelected(True)
                # print global_inst.win_.scene().selectedItems()
                self.selectFlag = True
                self.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
            ev.accept()
        elif int(ev.button() & self.acceptedMouseButtons()) > 0:
            ev.accept()
            self.sigClicked.emit(self, ev)
        else:
            ev.ignore()
        self.update()

    # def mousePressEvent(self,ev):
    #     print "press"
    #     if ev.button() == QtCore.Qt.RightButton and self.contextMenuEnabled():
    #         self.raiseContextMenu(ev)
    #         ev.accept()
    #     elif global_inst.win_.mode is  'NoMode' and ev.button() == QtCore.Qt.LeftButton:
    #         if self.selectFlag and (ev.modifiers() & QtCore.Qt.ShiftModifier):
    #             self.selectFlag = False
    #             self.currentPen = self.pen
    #         else:
    #             self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable,True)
    #             self.setSelected(True)
    #             print self.isSelected()
    #             print global_inst.win_.scene().selectedItems()
    #             self.selectFlag = True
    #             self.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
    #         ev.accept()

    def mouseCancleMenue(self):
        self.selectFlag = False
        self.currentPen = self.pen
        self.update()
