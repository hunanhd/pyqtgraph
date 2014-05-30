# -*- coding : utf-8 -*-

from buildfuc import *


class Axis(QtGui.QGraphicsPathItem):
    def __init__(self, l):
        super(Axis, self).__init__()
        self.opts = {'pxMode': False}
        self.l = l
        path = QtGui.QPainterPath()
        path.moveTo(0, 0)
        path.lineTo(0, l)
        path.moveTo(0, 0)
        path.lineTo(l, 0)
        angle = 150
        arrowL = 10

        path.moveTo(l, 0)
        v = v_rotate(pg.Vector(1, 0), -angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(l, 0))
        path.lineTo(pt)

        path.moveTo(l, 0)
        v = v_rotate(pg.Vector(1, 0), angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(l, 0))
        path.lineTo(pt)

        path.moveTo(0, l)
        v = v_rotate(pg.Vector(0, 1), angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(0, l))
        path.lineTo(pt)

        path.moveTo(0, l)
        v = v_rotate(pg.Vector(0, 1), -angle)
        v = v * arrowL
        pt = vp_add(v, pg.Point(0, l))
        path.lineTo(pt)
        self.setPath(path)
        self.setPen(pg.fn.mkPen(color='w'))
        if self.opts['pxMode']:
            self.setFlags(self.flags() | self.ItemIgnoresTransformations)
        else:
            self.setFlags(self.flags() & ~self.ItemIgnoresTransformations)

    def paint(self, p, *args):
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        QtGui.QGraphicsPathItem.paint(self, p, *args)

    def shape(self):
        #if not self.opts['pxMode']:
        return QtGui.QGraphicsPathItem.shape(self)
        # return self.path()

    ## dataBounds and pixelPadding methods are provided to ensure ViewBox can
    ## properly auto-range
    def dataBounds(self, ax, frac, orthoRange=None):
        pw = 0
        pen = self.pen()
        if not pen.isCosmetic():
            pw = pen.width() * 0.7072
        if self.opts['pxMode']:
            return [0, 0]
        else:
            br = self.boundingRect()
            if ax == 0:
                return [br.left() - pw, br.right() + pw]
            else:
                return [br.top() - pw, br.bottom() + pw]

    def pixelPadding(self):
        pad = 0
        if self.opts['pxMode']:
            br = self.boundingRect()
            pad += (br.width() ** 2 + br.height() ** 2) ** 0.5
        pen = self.pen()
        if pen.isCosmetic():
            pad += max(1, pen.width()) * 0.7072
        return pad

