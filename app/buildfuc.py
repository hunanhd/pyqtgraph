# -*- coding:utf-8 -*-
import pyqtgraph as pg
from PyQt4 import QtCore, QtGui

def vp_add(v, p):
    return pg.Point(v.x() + p.x(), v.y() + p.y())


def v_rotate(v, angle):
    tr = pg.SRTTransform3D()
    tr.rotate(-angle)
    return tr.map(v)


def cross(b, a):
    a = pg.Vector(a)
    b = pg.Vector(b)
    return b[0] * a[1] - b[1] * a[0]


def v_angle(b, a):
    import math

    return math.atan2(QtGui.QVector3D.dotProduct(QtGui.QVector3D.crossProduct(b, a), QtGui.QVector3D(0, 0, 1)),
                      QtGui.QVector3D.dotProduct(b, a))

