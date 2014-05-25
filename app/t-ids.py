# -*- coding: utf-8 -*-
"""
Demonstrates adding a custom context menu to a GraphicsItem
and extending the context menu of a ViewBox.

PyQtGraph implements a system that allows each item in a scene to implement its 
own context menu, and for the menus of its parent items to be automatically 
displayed as well. 

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import sdi_rc
from junction import *
from buildfuc import *
from tidsaxis import Axis
from mainwindow import MainWindow

def test2():
    a = [
        JunctionEdgInfo(Tunnel(pg.Point(0, 1), pg.Point(2, 2)), True, pg.Vector(1, -1)),
        JunctionEdgInfo(Tunnel(pg.Point(2, 3), pg.Point(3, 6)), False, pg.Vector(1, 1)),
        JunctionEdgInfo(Tunnel(pg.Point(10, 21), pg.Point(34, 12)), True, pg.Vector(-1, -1))
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
    #
    # print a[0].tunnel.spt, a[0].tunnel.spt1, a[0].tunnel.spt2, a[0].tunnel.ept, a[0].tunnel.ept1, a[
    #     0].tunnel.ept2
    #
    # a[0].tunnel.dealWithPointBoundary(pg.Point(3, 6), pg.Vector(1, 0))
    #
    # print a[0].tunnel.spt, a[0].tunnel.spt1, a[0].tunnel.spt2, a[0].tunnel.ept, a[0].tunnel.ept1, a[
    #     0].tunnel.ept2
    #


def test():
    spt = pg.Point(0, 0)
    ept = pg.Point(1, 1)
    v = pg.Vector(ept - spt)

    tr = pg.SRTTransform3D()
    tr.setRotate(90, (0, 0, 1))
    v1 = tr.map(v)

    line = QtCore.QLineF(spt, ept)
    pt = pg.Point()

    v1 = pg.Vector(-1, 1)
    print "v-->v1:", v_angle(v, v1)
    print "v1-->v:", v_angle(v1, v)
    # print line.intersect(QtCore.QLineF(pg.Point(-1, 0), pg.Point(0, -1)), pt)
    # print pt
    # print pg.Vector(spt) + v1
    #
    # print v.length()
    # v.normalize()
    # print v * 20
    # print v.x()
    # print -v

    v1 = pg.Vector(0, 1)
    v2 = pg.Vector(0, -1)
    print pg.Vector.crossProduct(v1, v2)


def main():
    app = QtGui.QApplication([])
    mainWindow = MainWindow()

    mainWindow.show()
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()  # Start Qt event loop unless running in interactive mode or using pyside.


if __name__ == '__main__':
    main()
    # test()
    # test2()

    # testFind()



