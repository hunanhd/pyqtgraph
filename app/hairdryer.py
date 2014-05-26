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
        self.caclVector()
    def paint(self, p, *args):
        #设置画笔为NoPen,即不绘制多边形的边框(border)
        p.setPen(QtCore.Qt.NoPen)
        #设置画刷颜色为(30,40,34),即背景色
        p.setBrush(QtGui.QBrush(QtGui.QColor(39, 40, 34)))
        #绘制填充polygon
        p.drawPolygon(self.spt, self.spt2, self.ept2, self.ept, self.ept1, self.spt1)

        #设置画笔的颜色(绿色)、线型(实线)
        p.setRenderHint(p.Antialiasing)
        p.setPen(QtGui.QPen(QtCore.Qt.red, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))

        p.drawLine(self.spt1, self.ept1)

        #用绿色实线绘制spt2-->ept2这条线
        p.drawLine(self.spt2, self.ept2)
