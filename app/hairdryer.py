# -*- coding:utf-8 -*-

from tunnel import *

class HairDryer(Tunnel):
    def __init__(self, start, end, i):
        super(HairDryer,self).__init__(start, end)
        self.spt = start
        self.ept = end
        self.spt1 = None
        self.spt2 = None
        self.ept1 = None
        self.ept2 = None
        self.width = 2
        self.colorindex = i % 8
        self.caclVector()
        self.colors = [QtCore.Qt.red, QtCore.Qt.white, QtCore.Qt.magenta, QtCore.Qt.yellow, QtCore.Qt.darkRed, QtCore.Qt.cyan, QtCore.Qt.gray, QtCore.Qt.blue]
        self.currentPen = QtGui.QPen(self.colors[self.colorindex], 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)

    def paint(self, p, *args):
        #设置画笔为NoPen,即不绘制多边形的边框(border)
        p.setPen(QtCore.Qt.NoPen)
        #设置画刷颜色为(30,40,34),即背景色
        p.setBrush(QtGui.QBrush(QtGui.QColor(39, 40, 34)))
        #绘制填充polygon
        p.drawPolygon(self.spt, self.spt2, self.ept2, self.ept, self.ept1, self.spt1)

        #设置画笔的颜色、线型(实线)
        p.setRenderHint(p.Antialiasing)
        #有布置多条风筒的可能，在没有实现修改颜色的时候，选择用不同颜色绘制，每增加一条风筒下标加1
        p.setPen(self.currentPen)
        p.drawLine(self.spt1, self.ept1)
        p.drawLine(self.spt2, self.ept2)

    def setMouseHover(self, hover):
        ## Inform the ROI that the mouse is(not) hovering over it
        if self.mouseHovering == hover:
            return
        self.mouseHovering = hover
        if hover:
            self.currentPen = QtGui.QPen(QtCore.Qt.lightGray, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
        else:
            self.currentPen = QtGui.QPen(self.colors[self.colorindex], 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
        self.update()

    def mouseDoubleClickEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton:
            hdpro = HairDryerDlg()
            if hdpro.exec_() == QtGui.QDialog.Accepted:
                print "hairDryerProInput"
                print hdpro.lenthEdit.text()
            evt.accept()

