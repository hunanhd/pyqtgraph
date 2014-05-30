# -*- coding:utf-8 -*-

from tidsaxis import *
from junction import *
import pyqtgraph as pg
from hairdryer import HairDryer
from fan import Fan


class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.disableAutoRange(pg.ViewBox.XYAxes)
        self.setAspectLocked(True, ratio=None)
        self.state['targetRange'] = [[0, 300], [0, 200]]
        self.state['viewRange'] = [[0,300],[0,200]]

    def resizeEvent(self,ev):
        self.setPos(0,0)
    def remove(self):
        self.disableAutoRange(pg.ViewBox.XYAxes)
        for b in findAllTunnels(self):
            if b.selectFlag:
                self.removeItem(b)

    def removeAll(self):
        self.disableAutoRange(pg.ViewBox.XYAxes)
        for b in findAllTunnels(self):
            self.removeItem(b)

    def selectAll(self):
        # self.disableAutoRange(pg.ViewBox.XYAxes)
        for b in findAllTunnels(self):
            b.selectFlag = True
            b.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
        self.update()

    ## reimplement right-click to zoom out
    def mouseClickEvent(self, ev):
        pg.ViewBox.mouseClickEvent(self, ev)

    def mouseDragEvent(self, ev):
        pg.ViewBox.mouseDragEvent(self, ev)

    def mouseMoveEvent(self, ev):
        pg.ViewBox.mouseMoveEvent(self, ev)

    def keyPressEvent(self, ev):
        if ev.key() == QtCore.Qt.Key_Delete:
            self.remove()
        if ev.key() == QtCore.Qt.Key_Escape:
            for b in findAllTunnels(self):
                if b.selectFlag:
                    # b.setSelected(False)
                    b.selectFlag = False
                    b.currentPen = b.pen
                    b.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
                    self.update()
        if ev.key() == QtCore.Qt.Key_A and ev.modifiers() & QtCore.Qt.ControlModifier:
            self.selectAll()

    def contextMenuEnabled(self):
        return True

    def raiseContextMenu(self, ev):
        if not self.contextMenuEnabled():
            return
        menu = self.getMenu()
        menu = self.scene().addParentContextMenus(self, menu, ev)
        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def getMenu(self):
        self.menu = QtGui.QMenu()
        self.menu.setTitle("ViewBox options")

        viewAll = QtGui.QAction("View All", self.menu)
        viewAll.triggered.connect(self.autoBtnClicked)
        if global_inst.mw_.autoAct.isEnabled():
            viewAll.setEnabled(True)
        else:
            viewAll.setEnabled(False)
        self.menu.addAction(viewAll)

        remAct = QtGui.QAction("Remove selected items", self.menu)
        remAllAct = QtGui.QAction("Remove all items", self.menu)
        selAllAct = QtGui.QAction("Select all items", self.menu)
        remAllAct.triggered.connect(self.removeAll)
        remAct.triggered.connect(self.remove)
        selAllAct.triggered.connect(self.selectAll)

        allTunnels = findAllTunnels(self)
        if allTunnels == []:
            remAct.setEnabled(False)
            remAllAct.setEnabled(False)
            selAllAct.setEnabled(False)
        else:
            for b in allTunnels:
                if b.selectFlag == False:
                    remAct.setEnabled(False)
                    selAllAct.setEnabled(True)
                else:
                    remAct.setEnabled(True)
                    selAllAct.setEnabled(False)
            remAllAct.setEnabled(True)
        self.menu.addAction(remAct)
        self.menu.addAction(remAllAct)
        self.menu.addAction(selAllAct)
        return self.menu

    def autoBtnClicked(self):
        self.enableAutoRange()


#直接从GraphicsView派生
#参考example/Draw.py、GraphicsScene.py、customPlot.py

class GraphicsWindow(pg.GraphicsView):
    def __init__(self, title=None, size=(800, 800), **kargs):
        super(GraphicsWindow, self).__init__(**kargs)
        self.modes = ['InsertTunnel', 'InsertHairDryer', 'InsertFan', 'InsertNode', 'InsertFan' 'NoMode']
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

    def setFanMode(self):
        self.mode = 'InsertFan'

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
                t3 = Tunnel(fourPts[3], fourPts[0])
                t1 = Tunnel(fourPts[0], fourPts[1])
                t4 = Tunnel(fourPts[1], fourPts[2])
                # t5 = Tunnel(fourPts[1], pg.Point(1000, 0))
                # t6 = Tunnel(fourPts[1], fourPts[3])
                self.vb.addItem(t2)
                self.vb.addItem(t3)
                self.vb.addItem(t1)
                self.vb.addItem(t4)
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
                    h1 = HairDryer(fourPts[3], fourPts[0])
                    h2 = HairDryer(fourPts[0], fourPts[1])
                    h3 = HairDryer(fourPts[3], fourPts[1])
                elif self.directFlg == 1:
                    h1 = HairDryer(fourPts[0], fourPts[2])
                    h2 = HairDryer(fourPts[1], fourPts[0])
                    h3 = HairDryer(fourPts[1], fourPts[2])
                self.vb.addItem(h1)
                self.vb.addItem(h2)
                self.vb.addItem(h3)
                self.colorindex = self.colorindex + 1
                self.vb.scene().update()
            if self.mode == 'InsertFan':
                self.insertFan(evt)
        self.mode = 'NoMode'
        evt.accept()

    def insertFan(self, ev):
        #以下获取Items方法简单，但是有待研究
        #经过测试，下面这种方法不精确，因为在Tunnel中返回的boundingRect()不是精确的
        #下面这种方法获取的正是返回的矩形范围内的Items，而上面的方法获得的是鼠标之下的
        # items = self.scene().items(ev.scenePos())  #这种获取可能会更好一点
        mousePt = self.vb.mapSceneToView(ev.scenePos())
        # t = self.getTunnel(items)
        h = self.getHairDryer()
        if not h is None:
            f = Fan(5, 5)
            # f.paint()
            arrow = f.drawArrow(mousePt, h.spt, h.ept)
            self.vb.addItem(arrow)
            f.drawFan()
            self.vb.addItem(f)
        else:
            msg = QtGui.QMessageBox()
            msg.setWindowTitle (self.tr("Warming"))
            msg.setText(self.tr("Fan must be in the hairDryer"))
            msg.exec_()

    def getHairDryer(self):
        #获取鼠标下的Items
        #目前使用下面的方法
        h = None
        for hairDryer in findAllHairDryer(self.vb):
            if hairDryer.mouseHovering == True:
                h = hairDryer
                break
        return h

    # def getTunnel(self,items):
    #     t = None
    #     for item in items:
    #         if isinstance(item, Tunnel):
    #             t = item
    #             print t
    #             break
    #     return t

    def auto_junction(self):
        # print '[%s]auto_junction is called' % time.ctime()
        networks = buildNetworks(self.vb)
        # print '点个数:',len(networks)
        for pt in networks.keys():
            junctionClosure(networks[pt], pt)

        #
        if not all(global_inst.win_.vb.autoRangeEnabled()):
            # global_inst.mw_.autoAct.setEnabled(True)
            self.parent().autoAct.setEnabled(True)
        else:
            self.parent().autoAct.setEnabled(False)


def findAdjTunnels(vb, pt):
    tunnels = []
    for item in vb.addedItems:
        if isinstance(item, Tunnel):
            if pt == item.spt or pt == item.ept:
                tunnels.append(item)
    return tunnels

def findAllHairDryer(vb):
    hairDryer = []
    for item in vb.addedItems:
        if isinstance(item, HairDryer):
            hairDryer.append(item)
    return hairDryer


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
