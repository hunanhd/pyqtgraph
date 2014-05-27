# -*- coding:utf-8 -*-

from tidsaxis import *
from junction import *
import pyqtgraph as pg
from hairdryer import HairDryer

class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.disableAutoRange(pg.ViewBox.XYAxes)
        self.setAspectLocked(True, ratio=None)
        # self.vb.setMouseEnabled(False,False)

        self.autoBtn = pg.ButtonItem(pg.pixmaps.getPixmap('auto'), 14, self)
        self.autoBtn.mode = 'auto'
        self.autoBtn.clicked.connect(self.autoBtnClicked)

    def autoBtnClicked(self):
        if self.autoBtn.mode == 'auto':
            self.enableAutoRange()
            self.autoBtn.show()
            # self.autoBtn.hide()

    def resizeEvent(self, ev):
        if self.autoBtn is None:  ## already closed down
            return
        btnRect = self.mapRectFromItem(self.autoBtn, self.autoBtn.boundingRect())
        y = self.size().height() - btnRect.height()
        self.autoBtn.setPos(0, y)

    def remove(self):
        # self.removeItem()
        print self.scene().selectedItems()

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        pg.ViewBox.mouseClickEvent(self, ev)

    def mouseDragEvent(self, ev):
        pg.ViewBox.mouseDragEvent(self, ev)

    def mouseMoveEvent(self, ev):
        pg.ViewBox.mouseMoveEvent(self, ev)


#直接从GraphicsView派生
#参考example/Draw.py、GraphicsScene.py、customPlot.py

class GraphicsWindow(pg.GraphicsView):
    def __init__(self, title=None, size=(800, 800), **kargs):
        super(GraphicsWindow, self).__init__(**kargs)
        self.modes = ['InsertTunnel', 'InsertHairDryer', 'InsertFan', 'InsertNode', 'NoMode']
        self.mode = 'NoMode'
        self.hairDryerspt1 = None
        self.hairDryerspt2 = None
        self.colorindex = 0

        # 给风筒定义一个方向指标，如果是朝上就为1,否则为0
        self.directFlg = 1
        self.resize(*size)
        self.setBackground((39, 40, 34))
        if title is not None:
            self.setWindowTitle(title)

        #原来的GraphicsLayoutWidget.addViewBox会产生多余的QGraphicsRectItem
        #直接new生成一个ViewBox,添加到当前窗口中
        self.vb = CustomViewBox()
        self.setCentralItem(self.vb)

        self.axis = Axis(100)
        self.axis.setPos(0, 0)
        self.axis.setRotation(0)
        self.vb.addItem(self.axis)

        self.vLine = pg.InfiniteLine(angle=90, movable=False)
        self.hLine = pg.InfiniteLine(angle=0, movable=False)
        self.vb.addItem(self.vLine, ignoreBounds=True)
        self.vb.addItem(self.hLine, ignoreBounds=True)

        self.proxy = pg.SignalProxy(
            self.vb.scene().sigMouseMoved, rateLimit=60, slot=self.sceneMouseMoved)
        self.vb.scene().sigMouseClicked.connect(self.sceneMousePressed)

        self.junction_timer = QtCore.QTimer(self)
        self.junction_timer.timeout.connect(self.auto_junction)
        self.junction_timer.start(0)

    def setTunnelMode(self):
        self.mode = 'InsertTunnel'

    def setHairDryerMode(self):
        self.mode = 'InsertHairDryer'

    def setFanMode(self):
        self.mode = 'InsertFan'

    def setNodeMode(self):
        self.mode = 'InsertNode'

    # def setMainWindow(self, mw):
    #     self.mw = mw

    def sceneMouseMoved(self, evt):
        # using signal proxy turns original arguments into a tuple
        pos = evt[0]
        if self.vb.sceneBoundingRect().contains(pos):
            mousePoint = self.vb.mapSceneToView(pos)
            self.msg = "x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y())
            self.parent().statusBar().showMessage(self.msg)

            self.vLine.setPos(mousePoint.x())
            self.hLine.setPos(mousePoint.y())
            self.vb.scene().update()

    def caclTunPts(self, pt, l, h):
        fourPts = [pt]
        fourPts.append(QtCore.QPointF(pt.x() + l, pt.y()))
        fourPts.append(QtCore.QPointF(pt.x(), pt.y() + h))
        fourPts.append(QtCore.QPointF(pt.x(), pt.y() - h))
        return fourPts

    def sceneMousePressed(self, evt):
        if evt.buttons() & QtCore.Qt.LeftButton:
            mousePt = self.vb.mapSceneToView(evt.scenePos())
            fourPts = self.caclTunPts(mousePt, 150, 80)
            if self.mode == 'InsertTunnel':
                # fourPts = self.caclTunPts(pg.Point(0,0), 150, 80)
                t2 = Tunnel(fourPts[0], fourPts[2])
                t3 = Tunnel(fourPts[0], fourPts[3])
                t1 = Tunnel(fourPts[0], fourPts[1], True)
                # t4 = Tunnel(fourPts[1], fourPts[2])
                # t5 = Tunnel(fourPts[1], pg.Point(1000,0))
                # t6 = Tunnel(fourPts[1], fourPts[3])
                self.vb.addItem(t2)
                self.vb.addItem(t3)
                self.vb.addItem(t1)
                # self.vb.addItem(t4)
                # self.vb.addItem(t5)
                # self.vb.addItem(t6)

                # junctionClosure([t1,t4,t5,t6], fourPts[1])
                # junctionClosure([t2,t4], fourPts[2])
                # junctionClosure([t2,t3,t1], fourPts[0])
                # junctionClosure([t6], fourPts[3])
                # junctionClosure(self.vb, pg.Point(1000,0))

                self.vb.scene().update()

                self.hairDryerspt1 = pg.Point(fourPts[0].x() + 12, fourPts[0].y() - 12)
                self.hairDryerspt2 = pg.Point(fourPts[0].x() + 12, fourPts[0].y() + 10)

            #绘制风筒的时候有逻辑错误
            #现在实现的只能是先把朝下的风筒布置完，然后再布置朝上的风筒
            #
            if self.mode == 'InsertHairDryer':
                if self.hairDryerspt2 != None and mousePt.y() > self.hairDryerspt2.y() + 10:
                    fourPts = self.caclTunPts(self.hairDryerspt2, 120, 20)
                    self.hairDryerspt2 = None
                    self.directFlg = 1
                elif self.hairDryerspt1 != None and mousePt.y() <= self.hairDryerspt1.y() - 12:
                    fourPts = self.caclTunPts(self.hairDryerspt1, 120, 20)
                    self.hairDryerspt1 = None
                    self.directFlg = 0
                else:
                    fourPts = self.caclTunPts(mousePt, 125, 25)
                if self.directFlg == 0:
                    h1 = HairDryer(fourPts[0], fourPts[3], self.colorindex)
                    h2 = HairDryer(fourPts[0], fourPts[1], self.colorindex)
                elif self.directFlg == 1:
                    h1 = HairDryer(fourPts[0], fourPts[2], self.colorindex)
                    h2 = HairDryer(fourPts[0], fourPts[1], self.colorindex)
                self.vb.addItem(h1)
                self.vb.addItem(h2)
                self.colorindex = self.colorindex + 1

                self.vb.scene().update()
        self.mode = 'NoMode'
        evt.accept()

    def auto_junction(self):
        # print '[%s]auto_junction is called' % time.ctime()
        networks = buildNetworks(self.vb)
        # print '点个数:',len(networks)
        for pt in networks.keys():
            junctionClosure(networks[pt], pt)


def findAdjTunnels(vb, pt):
    tunnels = []
    for item in vb.addedItems:
        if isinstance(item, Tunnel):
            if pt == item.spt or pt == item.ept:
                tunnels.append(item)
    return tunnels


def findAllTunnels(vb):
    tunnels = []
    for item in vb.addedItems:
        if isinstance(item, Tunnel):
            tunnels.append(item)
    return tunnels


def buildNetworks(vb):
    #在viewbox中查找所有巷道
    tunnels = findAllTunnels(vb)
    #记录每一个节点关联的巷道(拓扑关系构成了图或者网络)
    networks = {}
    for t in tunnels:
        if not t.spt in networks:
            networks[t.spt] = [t]
        else:
            networks[t.spt].append(t)

        if not t.ept in networks:
            networks[t.ept] = [t]
        else:
            networks[t.ept].append(t)
    return networks
