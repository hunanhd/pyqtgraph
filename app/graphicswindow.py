# -*- coding:utf-8 -*-

from tidsaxis import *
from junction import *
from customVB import *
import gc


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
        # gc.set_threshold(10, 5, 2)
        # 给风筒定义一个方向指标，如果是朝上就为1,否则为0
        self.directFlg = 1
        self.resize(*size)
        # gc.set_threshold(3,2,1)
        # gc.set_debug(gc.DEBUG_LEAK | gc.DEBUG_COLLECTABLE | gc.DEBUG_UNCOLLECTABLE | gc.DEBUG_INSTANCES | gc.DEBUG_OBJECTS | gc.DEBUG_SAVEALL)
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



        # 添加十字光标
        # self.vLine = pg.InfiniteLine(angle=90, movable=False)
        # self.hLine = pg.InfiniteLine(angle=0, movable=False)
        # self.vb.addItem(self.vLine, ignoreBounds=True)
        # self.vb.addItem(self.hLine, ignoreBounds=True)

        self.proxy = pg.SignalProxy(
            self.vb.scene().sigMouseMoved, rateLimit=60, slot=self.sceneMouseMoved)
        self.vb.scene().sigMouseClicked.connect(self.sceneMousePressed)

        # self.junction_timer = QtCore.QTimer(self)
        # self.junction_timer.timeout.connect(self.auto_junction)
        # self.junction_timer.start(1000 / 33)

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
            scenepoint = evt[0]
            self.msg = "x=%0.1f,y=%0.1f" % (mousePoint.x(), mousePoint.y())
            self.parent().statusBar().showMessage(self.msg)

            # self.vLine.setPos(mousePoint.x())
            # self.hLine.setPos(mousePoint.y())
            self.vb.scene().update()
        if not all(self.vb.autoRangeEnabled()):
            # global_inst.mw_.autoAct.setEnabled(True)
            self.parent().autoAct.setEnabled(True)
        else:
            self.parent().autoAct.setEnabled(False)

        self.setMenuParam()

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
                t2 = Tunnel(fourPts[0], fourPts[2])
                t3 = Tunnel(fourPts[3], fourPts[0])
                t1 = Tunnel(fourPts[0], fourPts[1],True)
                t4 = Tunnel(fourPts[1], fourPts[2],True)
                # t5 = Tunnel(fourPts[1], pg.Point(1000, 0))
                # t6 = Tunnel(fourPts[1], fourPts[3])
                self.vb.addItem(t2)
                self.vb.addItem(t3)
                self.vb.addItem(t1)
                # self.vb.addItem(t4)

                # self.vb.addItem(t5)
                # self.vb.addItem(t6)
                # self.auto_junction()
                # junctionClosure([t1,t4,t5,t6], fourPts[1])
                # junctionClosure([t2,t4], fourPts[2])
                # junctionClosure([t2,t3,t1], fourPts[0])
                # junctionClosure([t6], fourPts[3])
                # junctionClosure(self.vb, pg.Point(1000,0))

                del t1,t2,t3,t4

                # print gc.collect()
                # print gc.collect()

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
                # self.vb.addItem(h3)

                del h1,h2,h3

                # self.colorindex = self.colorindex + 1
                self.vb.scene().update()
            if self.mode == 'InsertFan':
                self.insertFan(evt)
        self.mode = 'NoMode'
        evt.accept()

    def insertFan(self, ev):
        #后面有测试代码--->**-**-**
        # items = self.scene().items(ev.scenePos())  #之前的理解有问题，用这种方法才是高效的
        item = self.scene().itemAt(ev.scenePos())
        mousePt = self.vb.mapSceneToView(ev.scenePos())
        h = item
        if type(h) is HairDryer:
            f = Fan(5,5)
            arrow = f.drawArrow(mousePt, h.spt, h.ept)
            self.vb.addItem(arrow)
            self.vb.addItem(f)
            del f

            # 动态箭头

            ax = np.linspace(h.spt.x(),h.ept.x(), 500)
            bx = np.linspace(h.ept.x(),h.ept.x()+120, 500)
            ay = np.linspace(h.spt.y(),h.ept.y(), 500)
            by = np.linspace(h.ept.y(),h.ept.y(), 500)
            #构造一条曲线curve(要输入x,y轴数据,不一定是递增或递减)
            #curve = pg.PlotDataItem(x=np.linspace(h.spt.x(),h.ept.x(), 500),y=np.linspace(h.spt.y(),h.ept.y(),500),pixMode = False)
            curve = pg.PlotDataItem(x=np.append(ax,bx),y=np.append(ay,by),pixMode = False)
            #设置空画笔,这样就可以看不见曲线了(实质内部仍然在绘制曲线)
            #或者从PlotDataItem派生,重载paint函数(函数内部什么也不做)
            curve.setPen(None)
            self.vb.addItem(curve)

            #构造一个曲线箭头(curve将变成a的parent)
            a = pg.CurveArrow(curve,pixMode = False)
            a.setStyle(headLen=20)

            #构造动画对象(一直循环)
            #duration用来调节速度,默认值1000,loop等于-1表示永久循环
            self.anim = a.makeAnimation(duration=3000,loop=-1)
            self.anim.start()

        else:
            msg = QtGui.QMessageBox()
            msg.setWindowTitle (self.tr("Warming"))
            msg.setText(self.tr("Fan must be in the hairDryer"))
            msg.exec_()

    def setMenuParam(self):
        all_items = self.vb.addedItems
        tunnels = findByClass(all_items,Tunnel)
        fans = findByClass(all_items,Fan)
        tSelectedNum = 0
        ttSelectedNum = 0
        hSelectedNum = 0
        fSelectedNum = 0
        for tunnel in tunnels:
            if tunnel.isTTunnel and type(tunnel) != HairDryer and tunnel.selectFlag:
                ttSelectedNum = ttSelectedNum + 1
            if tunnel.isTTunnel is False and type(tunnel) != HairDryer and tunnel.selectFlag:
                tSelectedNum = tSelectedNum + 1
            if tunnel.isTTunnel is False and type(tunnel) == HairDryer and tunnel.selectFlag:
                hSelectedNum = hSelectedNum + 1

        for fan in fans:
            if fan.selectFlag:
                fSelectedNum = fSelectedNum + 1

        if hSelectedNum is 1:
            global_inst.mw_.hairDryerProAct.setEnabled(True)
        else:
            global_inst.mw_.hairDryerProAct.setEnabled(False)

        if tSelectedNum is 1:
            global_inst.mw_.tunnelProAct.setEnabled(True)
        else:
            global_inst.mw_.tunnelProAct.setEnabled(False)

        if ttSelectedNum is 1:
            global_inst.mw_.ttunnelProAct.setEnabled(True)
        else:
            global_inst.mw_.ttunnelProAct.setEnabled(False)

#-------------------------------------------------------------------------#
        # 之前没有注释ViewBox里面的setFlag是捕捉得到的是boundingRect返回的矩形
        # 但是邓哥修改注释之后返回的是shape()的矩形框，所以在捕捉的时候能精确，所以
        # 这些辅助函数是多余的
        # h = self.getHairDryer()
        # if not h is None:
        #     f = Fan(5, 5)
        #     # f.paint()
        #     arrow = f.drawArrow(mousePt, h.spt, h.ept)
        #     self.vb.addItem(arrow)
        #     self.vb.addItem(f)
        #     del f
        # else:
        #     msg = QtGui.QMessageBox()
        #     msg.setWindowTitle (self.tr("Warming"))
        #     msg.setText(self.tr("Fan must be in the hairDryer"))
        #     msg.exec_()

    # def getHairDryer(self):
    #     #获取鼠标下的Items
    #     #目前使用下面的方法（没有注释setFlag之前的方法）
    #     h = None
    #     all_items = global_inst.win_.vb.addedItems
    #     hairDryers = findByClass(all_items,HairDryer)
    #     for hairDryer in hairDryers:
    #         if hairDryer.mouseHovering == True:
    #             h = hairDryer
    #             break
    #     return h

    # def mouseDoubleClickEvent(self, evt):
    #     all_items = global_inst.win_.vb.addedItems
    #     tunnels = findByClass(all_items,Tunnel)
    #     hairDryers = findByClass(all_items,HairDryer)
    #     fans = findByClass(all_items,Fan)
    #     if len(tunnels) + len(hairDryers) + len(fans) != 0 and evt.button() == QtCore.Qt.LeftButton:
    #         self.clickByObct(tunnels,evt)
    #         self.clickByObct(hairDryers,evt)
    #         self.clickByObct(fans,evt)
    #     else:
    #         QtGui.QGraphicsView.mouseDoubleClickEvent(self, evt)
    #
    # def clickByObct(self,items,evt):
    #     for item in items:
    #         if item.mouseHovering is True:
    #             if type(item) == HairDryer:
    #                 item.hMouseClickEvent(evt)
    #             if type(item) == Tunnel:
    #                 item.tMouseClickEvent(evt)
    #             if type(item) == Fan:
    #                 item.fMouseClickEvent(evt)
    #             evt.accept()
    #         else:
    #             QtGui.QGraphicsView.mouseDoubleClickEvent(self, evt)
#-------------------------------------------------------------------------#
#---------------------------------------------------------------#
#**-**-**
# 问题：def insertFan(self, ev)：
# #以下获取Items方法简单，但是有待研究
# #经过测试，下面这种方法不精确，因为在Tunnel中返回的boundingRect()不是精确的
# #下面这种方法获取的正是返回的矩形范围内的Items，而上面的方法获得的是鼠标之下的
#
#测试：
# items = self.scene().items(ev.scenePos())  #这种获取可能会更好一点
# print 'scene pos:',ev.scenePos()
# print 'item pos:',ev.pos()
# for t in items:
#     print t
#     print t.contains(ev.pos())
#     print t.shape().contains(ev.pos())
#     print t.clipPath().contains(ev.pos())
#     print t.mapFromScene(ev.scenePos())
# return
#---------------------------------------------------------------#
#---------------------------------------------------------------#
# 之前用于自动实现巷道闭合的函数，但是这样会导致内存泄漏
# def auto_junction(self):
#     return
#     # print '[%s]auto_junction is called' % time.ctime()
#     networks = buildNetworks(self.vb)
#     # print '点个数:',len(networks)
#     for pt in networks.keys():
#         junctionClosure(networks[pt], pt)
#     del networks
#     # gc.collect()
#
#     if not all(global_inst.win_.vb.autoRangeEnabled()):
#         # global_inst.mw_.autoAct.setEnabled(True)
#         self.parent().autoAct.setEnabled(True)
#     else:
#         self.parent().autoAct.setEnabled(False)
#---------------------------------------------------------------#
# def buildNetworks(vb):
#     #在viewbox中查找所有巷道
#     tunnels = findAllTunnels(vb)
#     #记录每一个节点关联的巷道(拓扑关系构成了图或者网络)
#     networks = {}
#     for t in tunnels:
#         if not t.spt in networks:
#             networks[t.spt] = [t]
#         else:
#             networks[t.spt].append(t)
#
#         if not t.ept in networks:
#             networks[t.ept] = [t]
#         else:
#             networks[t.ept].append(t)
#     # tunnels = None
#     return networks
#---------------------------------------------------------------#
#---------------------------------------------------------------#
# 之前用于查找巷道的函数，现在用是"findGE.py"里面的查找函数
# def findAdjTunnels(vb, pt):
#     tunnels = []
#     for item in vb.addedItems:
#         if isinstance(item, Tunnel):
#             if pt == item.spt or pt == item.ept:
#                 tunnels.append(item)
#     return tunnels
#---------------------------------------------------------------#
# def findAllTunnels(vb):
#     tunnels = []
#     for item in vb.addedItems:
#         if isinstance(item, Tunnel):
#             tunnels.append(item)
#     return tunnels
#
#
#---------------------------------------------------------------#
#---------------------------------------------------------------#
# 用于查找风筒的函数，现在用"findGE.py"里面的查找函数
#  def findAllHairDryer(vb):
#     hairDryer = []
#     for item in vb.addedItems:
#         if isinstance(item, HairDryer):
#             hairDryer.append(item)
#     return hairDryer
#---------------------------------------------------------------#

