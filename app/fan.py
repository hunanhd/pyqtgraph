# -*- coding:utf-8 -*-

from buildfuc import *


class Fan(QtGui.QGraphicsPathItem):
    def __init__(self, spt):
        super(Fan, self).__init__()
        self.spt = spt
