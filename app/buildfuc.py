# -*- coding:utf-8 -*-
import math

from PyQt4 import QtCore, QtGui
import numpy as np

import pyqtgraph as pg

#向量与点相加,返回一个点
def vp_add(v, p):
    return pg.Point(v.x() + p.x(), v.y() + p.y())

#向量旋转
#angle -- 单位: 度(不是弧度radian)
#注：使用np.rad2deg(弧度转角度), np.deg2rad(角度转弧度)
def v_rotate(v, angle):
    tr = pg.SRTTransform3D()
    tr.rotate(-angle)
    return tr.map(v)

#计算向量a->b的角度(使用math.atan2函数实现)
#单位:弧度, 范围: 0~2*pi
def v_angle_1(b, a=pg.Vector(1, 0)):
    """Returns the angle in degrees between this vector and the vector a."""
    n1 = a.length()
    n2 = b.length()
    if n1 == 0. or n2 == 0.:
        return None

    return math.atan2(QtGui.QVector3D.dotProduct(QtGui.QVector3D.crossProduct(b, a), QtGui.QVector3D(0, 0, 1)),
                      QtGui.QVector3D.dotProduct(b, a))


#计算向量a->b的角度(使用np.arctan2函数实现)
#单位:弧度, 范围: 0~2*pi
def v_angle_2(b, a=pg.Vector(1, 0)):
    """Returns the angle in degrees between this vector and the vector a."""
    n1 = a.length()
    n2 = b.length()
    if n1 == 0. or n2 == 0.:
        return None

    ## Probably this should be done with arctan2 instead..
    angs = np.arctan2([a.y(), b.y()], [a.x(), b.x()])  ### in radians
    ang = angs[1] - angs[0]
    return ang if ang >= 0 else (2 * np.pi + ang)


#计算向量a->b的角度(单位:弧度, 范围: 0~2*pi)
def v_angle(b, a=pg.Vector(1, 0)):
    # return v_angle_1(b, a)
    return v_angle_2(b, a)


if __name__ == '__main__':
    spt = pg.Point(0, 0)
    ept = pg.Point(1, 1)
    v = pg.Vector(ept - spt)

    tr = pg.SRTTransform3D()
    tr.setRotate(90, (0, 0, 1))
    v1 = tr.map(v)

    line = QtCore.QLineF(spt, ept)
    pt = pg.Point()

    v1 = pg.Vector(-1, 1)
    print "v-->v1:", v_angle2(v, v1)
    print "v1-->v:", v_angle2(v1, v)
    print line.intersect(QtCore.QLineF(pg.Point(-1, 0), pg.Point(0, -1)), pt)
    print pt
    print pg.Vector(spt) + v1

    print v_rotate(pg.Vector(-1, 0), 90)
    print v_rotate(pg.Vector(1, 0), 90)
    print v_rotate(pg.Vector(0, 1, 0), 90)
    print v_rotate(pg.Vector(0, -1), 90)

    v1 = pg.Vector(0, 1)
    v2 = pg.Vector(0, -1)
    print pg.Vector.crossProduct(v1, v2)