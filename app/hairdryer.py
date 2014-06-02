# -*- coding:utf-8 -*-

from tunnel import *

class HairDryer(Tunnel):
    def __init__(self, start, end):
        super(HairDryer,self).__init__(start, end)
        self.spt = start
        self.ept = end
        self.spt1 = None
        self.spt2 = None
        self.ept1 = None
        self.ept2 = None
        self.width = 2
        self.mouseHovering = False
        # self.colorindex = i % 8
        self.caclVector()
        self.currentPen = QtGui.QPen(QtCore.Qt.white, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)

    def paint(self, p, *args):
        #设置画笔为NoPen,即不绘制多边形的边框(border)
        p.setPen(QtCore.Qt.NoPen)
        #设置画刷颜色为(30,40,34),即背景色
        p.setBrush(QtGui.QBrush(QtGui.QColor(39, 40, 34)))
        #绘制填充polygon
        p.drawPolygon(self.spt, self.spt2, self.ept2, self.ept, self.ept1, self.spt1)

        #设置画笔的颜色、线型(实线)
        p.setRenderHint(p.Antialiasing)
        p.setPen(self.currentPen)
        p.drawLine(self.spt1, self.ept1)
        p.drawLine(self.spt2, self.ept2)

    def mouseDoubleClickEvent(self, evt):
        self.selectFlag = False
        if evt.button() == QtCore.Qt.LeftButton:
            hdpro = HairDryerDlg()
            if hdpro.exec_() == QtGui.QDialog.Accepted:
                print hdpro.lenthEdit.text()
            evt.accept()

#不能成功的翻译，所以重载次函数
    def getMenu(self):
        self.menu = QtGui.QMenu()
        self.menu.setTitle(self.tr("TObjectMenu"))
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

