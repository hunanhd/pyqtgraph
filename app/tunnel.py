# -*- cording:utf-8 -*-
from buildfuc import *

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
        p.setRenderHint(p.Antialiasing)
        p.setPen(
            QtGui.QPen(QtCore.Qt.green, 0, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap))

        # p.setBrush(QtGui.QBrush((255-39,255-40,255-34)))
        p.setBrush(QtGui.QBrush(QtGui.QColor(39, 40, 34)))
        # p.drawPolygon(self.spt, self.spt2, self.ept2, self.ept, self.ept1, self.spt1)

        p.drawLine(self.spt1, self.ept1)
        p.drawLine(self.spt2, self.ept2)
        if self.isTTunnel:
            p.drawLine(self.ept1, self.ept2)
        p.setPen(
            QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DotLine, QtCore.Qt.SquareCap))
        # p.drawRect(self.bound)

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
            # if self.isTTunnel:
            #     msg.setText("TTunnel")
            # else:
            #     msg.setText("VTunnel")
            msg.setText("VTunnel")
            msg.exec_()
            evt.accept()

    def boundingRect(self):
        self.bound = QtCore.QRectF(self.spt1, self.ept2)
        return self.bound

