# -*- coding:utf-8 -*-
from TObject import *
from findGE import *
from junction import *
import global_inst
import gc

class Tunnel(TObject):
    def __init__(self, start=0, end=0, isTTunnel=False):
        TObject.__init__(self)
        self.spt = start
        self.ept = end
        self.isTTunnel = isTTunnel
        self.spt1 = None
        self.spt2 = None
        self.ept1 = None
        self.ept2 = None
        self.width = 15
        self.pen = pg.fn.mkPen('w')
        self.currentPen = self.pen
        self.mouseHovering = False
        self.selectFlag = False
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
        #设置显示为反锯齿
        p.setRenderHint(p.Antialiasing)

        p.setPen(self.currentPen)

        #临时保存QPainter的状态
        #原因: 即将修改QPainter的画笔和画刷
        # p.save()
        #用蓝色绘制spt1-->ept1这条线
        #没什么特别含义，就是临时用来区分一下这2条线
        #以后程序完成了再改回去即可
        # p.setPen(QtGui.QColor(0, 0, 255))
        p.drawLine(self.spt1, self.ept1)
        #恢复QPainter的状态: 画刷颜色为(30,40,34),即背景色; 画笔的颜色(绿色)、线型(实线)
        # p.restore()

        #用绿色实线绘制spt2-->ept2这条线
        p.drawLine(self.spt2, self.ept2)

        #绘制掘进头(一端封闭)
        if self.isTTunnel:
            p.drawLine(self.ept1, self.ept2)

        #绘制boundingRect
        # p.setPen(pg.fn.mkPen('g'))
        # p.drawRect(self.boundingRect())
        # p.setPen(pg.fn.mkPen('w'))

#-------------------------------------#
# 之前shape函数的写法，两种方法的效果一样
# polg = QtGui.QPolygonF()
# polg.append(self.spt)
# polg.append(self.spt1)
# polg.append(self.ept1)
# polg.append(self.ept)
# polg.append(self.ept2)
# polg.append(self.spt2)
# path = QtGui.QPainterPath()
# path.addPolygon(polg)
# self.path = path
# return path
#------------------------------------#

    def shape(self):
        path = QtGui.QPainterPath()
        path.moveTo(self.spt)
        path.lineTo(self.spt1)
        path.lineTo(self.ept1)
        path.lineTo(self.ept)
        path.lineTo(self.ept2)
        path.lineTo(self.spt2)
        return path

    def boundingRect(self):
        return self.shape().boundingRect()

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


    def tMouseClickEvent(self, evt):
        self.selectFlag = False
        if evt.button() == QtCore.Qt.LeftButton:
            if self.isTTunnel:
                ttpro = TTunnelDlg()
                if ttpro.exec_() == QtGui.QDialog.Accepted:
                    print ttpro.lenthEdit.text()
            else:
                tpro = TunnelDlg()
                if tpro.exec_() == QtGui.QDialog.Accepted:
                    print tpro.lenthEdit.text()
            evt.accept()

    def itemChange(self, change, value):
        ret = TObject.itemChange(self, change, value)
        objs = findByClass(global_inst.win_.vb.addedItems,Tunnel)
        if change == 21 or change == 22:
            return ret
        self.doJunction(self.spt,objs)
        self.doJunction(self.ept,objs)
        return ret

    def doJunction(self,pt,objs):
        tunnels = []
        for item in objs:
            if pt == item.spt or pt == item.ept:
                tunnels.append(item)
        junctionClosure(tunnels,pt)



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