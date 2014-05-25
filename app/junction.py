# -*- coding: utf-8 -*-
from tunnel import *
import numpy as np

class JunctionEdgInfo:
    def __init__(self, id=None, soe=False, v=pg.Vector()):
        self.tunnel = id
        self.startOrEnd = soe
        self.v = v

    def __eq__(self, b):
        return self.tunnel == b.tunnel and self.startOrEnd == b.startOrEnd and self.v == b.v

    def __repr__(self):
        return "JunctionEdgInfo" + repr((self.tunnel, self.startOrEnd, self.v))


def buildJunctionEdgeInfo(tunnels, pt):
    ges = []
    for t in tunnels:
        info = JunctionEdgInfo()
        info.tunnel = t
        v = pg.Vector(t.ept - t.spt)
        v.normalize()
        if t.spt == pt:
            info.startOrEnd = True
            info.v = v
        elif t.ept == pt:
            info.startOrEnd = False
            info.v = pg.Vector(-v)
        ges.append(info)
    return ges


#至少需要2个元素才能正确的闭合
def edgeJunctionClosureImpl(junctionPt, ges):
    f = lambda v1, v2: (v1 + v2 ) * (1.0 / np.sin(2 * np.pi - v_angle(v1, v2)))
    if len(ges) == 1:
        ges.append(ges[0])
    ges.append(ges[0])

    v3 = ges[0].v
    v3 = v_rotate(v3, 90)
    for i in range(len(ges) - 1):
        cv = pg.Vector.crossProduct(ges[i].v, ges[i + 1].v)
        if cv.length() != 0:
            v3 = f(ges[i].v, ges[i + 1].v)
        else:
            v3 = -v3
        ges[i].tunnel.dealWithPointBoundary(junctionPt, v3)
        ges[i + 1].tunnel.dealWithPointBoundary(junctionPt, v3)


def findLinesByPoint(vb, pt):
    all_items = vb.addedItems
    tunnels = []
    for item in all_items:
        if isinstance(item, Tunnel):
            if pt == item.spt or pt == item.ept:
                tunnels.append(item)
    return tunnels


def junctionClosure_helper(vb, pt):
    tunnels = findLinesByPoint(vb, pt)
    ges = buildJunctionEdgeInfo(tunnels, pt)
    f = lambda info: v_angle(info.v, pg.Vector(1, 0))
    if len(ges) > 0:
        ges.sort(key=f)
        edgeJunctionClosureImpl(pt, ges)