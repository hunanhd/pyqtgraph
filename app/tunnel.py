# -*- coding:utf-8 -*-
from buildfuc import *
import pyqtgraph as pg
from PyQt4 import Qt

class Tunnel(pg.GraphicsObject):
    def __init__(self, start=0, end=0, isTTunnel=False):
        pg.GraphicsObject.__init__(self)
        self.spt = start
        self.ept = end
        self.isTTunnel = isTTunnel
        self.spt1 = None
        self.spt2 = None
        self.ept1 = None
        self.ept2 = None
        self.width = 15
        self.bound = None

        self.caclVector()

    def __repr__(self):
        return "Tunnel:" + repr((self.spt, self.ept))

    def paint(self, p, *args):
        #设置画笔为NoPen,即不绘制多边形的边框(border)
        p.setPen(QtCore.Qt.NoPen)
        #设置画刷颜色为(30,40,34),即背景色
        p.setBrush(QtGui.QBrush(QtGui.QColor(39, 40, 34)))
        #绘制填充polygon
        p.drawPolygon(self.spt, self.spt2, self.ept2, self.ept, self.ept1, self.spt1)

        #设置画笔的颜色(绿色)、线型(实线)
        p.setRenderHint(p.Antialiasing)
        p.setPen(QtGui.QPen(QtCore.Qt.green, 1, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))

        #临时保存QPainter的状态
        #原因: 即将修改QPainter的画笔和画刷
        p.save()
        #用蓝色绘制spt1-->ept1这条线
        #没什么特别含义，就是临时用来区分一下这2条线
        #以后程序完成了再改回去即可
        p.setPen(QtGui.QColor(0, 0, 255))
        p.drawLine(self.spt1, self.ept1)
        #恢复QPainter的状态: 画刷颜色为(30,40,34),即背景色; 画笔的颜色(绿色)、线型(实线)
        p.restore()

        #用绿色实线绘制spt2-->ept2这条线
        p.drawLine(self.spt2, self.ept2)

        #绘制掘进头(一端封闭)
        if self.isTTunnel:
            p.drawLine(self.ept1, self.ept2)

        #绘制boundingRect
        p.drawRect(self.bound)

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

    def trimSides(self, pt, v):
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
            #判断浮点数不能直接用==或!=号
            if (v + v1).length() > 1e-6:
                if isStart:
                    self.spt1 = pt1
                else:
                    self.ept1 = pt1
        if line2.intersect(QtCore.QLineF(pt, vp_add(v, pt)), pt2) != QtCore.QLineF.NoIntersection:
            v2 = pg.Vector(pt2 - pt)
            v2.normalize()
            v.normalize()
            #判断浮点数不能直接用==或!=号
            if (v + v2).length() > 1e-6:
                if isStart:
                    self.spt2 = pt2
                else:
                    self.ept2 = pt2


    def mouseDoubleClickEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton:
            msg = QtGui.QMessageBox()
            # if self.isTTunnel:
            #     msg.setText("TTunnel")
            # else:
            #     msg.setText("VTunnel")
            msg.setText("VTunnel")
            msg.exec_()
            evt.accept()

    def boundingRect(self):
        lx0 = qMin(self.spt1.x(),self.spt2.x())
        lx1 = qMin(self.ept1.x(),self.ept2.x())
        lx = qMin(lx0,lx1)
        rx0 = qMax(self.spt1.x(),self.spt2.x())
        rx1 = qMax(self.ept1.x(),self.ept2.x())
        rx = qMax(rx0,rx1)
        #ty是y值最大的点对应的y，但是在scene坐标系中y是相反的，屏幕坐标左上角才是零点
        ty0 = -qMin(self.spt1.y(),self.spt2.y())
        ty1 = -qMin(self.ept1.y(),self.ept2.y())
        ty = qMin(ty0,ty1)
        dy0 = -qMax(self.spt1.y(),self.spt2.y())
        dy1 = -qMax(self.ept1.y(),self.ept2.y())
        dy = qMax(dy0,dy1)
        self.bound = QtCore.QRectF(lx,ty,lx-rx,ty-dy)
        return self.bound


if __name__ == '__main__':
    a = [
        JunctionInfo(Tunnel(pg.Point(0, 1), pg.Point(2, 2)), True, pg.Vector(1, -1)),
        JunctionInfo(Tunnel(pg.Point(2, 3), pg.Point(3, 6)), False, pg.Vector(1, 1)),
        JunctionInfo(Tunnel(pg.Point(10, 21), pg.Point(34, 12)), True, pg.Vector(-1, -1))
    ]
    # print a[0].angle.angle(pg.Vector(1, 0))
    # print a[1].angle.angle(pg.Vector(1, 0))
    # print a[2].angle.angle(pg.Vector(1, 0))
    # print dir(pg.Vector(-1, -1))
    # print a
    # print a[0].tunnel.boundingRect()
    # a = sorted(a, key = lambda x: x.angle.angle(pg.Vector(1,0)))
    f = lambda info: v_angle(info.v, pg.Vector(1, 0))
    print a
    a.sort(key=f)
    print a
    print type(a[0])
    print f(a[0])
    # print a