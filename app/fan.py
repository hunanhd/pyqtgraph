# -*- coding:utf-8 -*-

from tunnel import Tunnel
import pyqtgraph as pg
from buildfuc import *
import global_inst

class Fan(pg.GraphicsObject):
    sigClicked = QtCore.Signal(object, object)
    sigHoverEvent = QtCore.Signal(object)
    def __init__(self,width,lenth):
        super(Fan, self).__init__()
        # self.opts = {'pxMode': False}
        self.width = width
        self.lenth = lenth
        self.mouseHovering = False
        self.selectFlag = False
        self.pen = pg.fn.mkPen('w')
        self.currentPen = self.pen

    def paint(self,p,*args):
        p.setRenderHint(p.Antialiasing)
        p.setPen(self.currentPen)
        p.drawPath(self.shape())

    def shape(self):
        # return QtGui.QGraphicsPathItem.shape(self)
        return self.drawFanPath()
    def boundingRect(self):
        return self.shape().boundingRect()

#--------------------------------------------------------------------------------------------------------#
#        # self.isRawAble = True                                                                          #
#        # hspt = item.spt                                                                                #
#        # hept = item.ept                                                                                #
#        # break #只要最上面的一个，其他的Items不考虑，所以获得第一个就break,如果风筒用不同的类就没有必要这么做 #
#        # else:                                                                                          #
#        #     msg = QtGui.QMessageBox()                                                                  #
#        #     msg.setText("clicked Erro!")                                                               #
#        #     msg.exec_()                                                                                #
#        #     self.isRawAble = False                                                                     #
#        #     return -1                                                                                  #
#--------------------------------------------------------------------------------------------------------#

    #mousePt:鼠标点击的坐标（View的坐标） spt:巷道的始点坐标 ept：巷道的末点坐标
    def drawArrow(self, mousePt, spt, ept):
        pedal = pointToLine(spt, ept, mousePt)#计算一点到一条线的垂足
        #方便下民DrawFan函数使用，也可以重新计算一下，这么写有个缺点，必须先画出箭头才能画风机
        self.spt = pedal
        v = pg.Vector(ept - spt)
        #向量初始化
        v.normalize()
        # 向量旋转90度
        self.v = v_rotate(v,90)
        # 计算向量的转角
        angle = v_angle_2(v)
        angle = angle * 180 / math.pi
        arrow = pg.ArrowItem(angle = 180 + angle, tipAngle=58, baseAngle=40, headLen=self.lenth*0.45, tailLen=self.lenth*0.45, tailWidth=0.65, pen='w', brush=None,pxMode = False)
        arrowL = self.lenth*0.45/2
        # 让箭头的中点处在风机的中点位置，默认的是箭头尖端作为设置坐标点。风机的中点就是pedal，作为path的开始点
        posPt = vp_add(v*arrowL, pedal)
        arrow.setPos(posPt)
        self.arrow = arrow
        return arrow

    def drawFanPath(self):
        path = QtGui.QPainterPath()
        pt1 = vp_add(self.v * self.width * 0.25, self.spt)
        v = v_rotate(self.v, -90)
        pt2 = vp_add(v * self.lenth * 0.25, pt1)
        path.moveTo(pt1)
        path.lineTo(pt2)
        v = v_rotate(v, 45)
        pt3 = vp_add(v * self.width * 1.0 / (4*math.sin(45*math.pi/180)),pt2)
        path.lineTo(pt3)
        v = v_rotate(v, -135)
        pt4 = vp_add(v * self.width, pt3)
        path.lineTo(pt4)
        v = v_rotate(v, -135)
        pt5 = vp_add(v * self.width * 1.0 / (4*math.sin(45*math.pi/180)), pt4)
        path.lineTo(pt5)
        v = v_rotate(v, 45)
        pt6 = vp_add(v *self.lenth, pt5)
        path.lineTo(pt6)
        v = v_rotate(v, 45)
        pt7 = vp_add(v * self.width * 1.0 / (4*math.sin(45*math.pi/180)), pt6)
        path.lineTo(pt7)

        v = v_rotate(v, -135)
        pt8 = vp_add(v * self.width, pt7)
        path.lineTo(pt8)
        v = v_rotate(v, -135)
        pt9 = vp_add(v * self.width * 1.0 / (4*math.sin(45*math.pi/180)), pt8)
        path.lineTo(pt9)
        path.lineTo(pt1)
        return path
#------------------------------------------------------------------------------#
#        # 如果想要画出的图形大小不变，可以让pxMode变为True                       #
#        # if self.opts['pxMode']:                                             #
#        #     self.setFlags(self.flags() | self.ItemIgnoresTransformations)   #
#        # else:                                                               #
#        #     self.setFlags(self.flags() & ~self.ItemIgnoresTransformations)  #
#------------------------------------------------------------------------------#

    def mouseDoubleClickEvent(self, evt):
        self.selectFlag = False
        if evt.button() == QtCore.Qt.LeftButton:
            msg = QtGui.QMessageBox()
            msg.setText(self.tr("is not define"))
            msg.exec_()
        evt.accept()

    def hoverEvent(self, ev):
        hover = False
        if not ev.isExit():
            # if self.translatable and ev.acceptDrags(QtCore.Qt.LeftButton):
            #     hover=True
            for btn in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton, QtCore.Qt.MidButton]:
                if int(self.acceptedMouseButtons() & btn) > 0 and ev.acceptClicks(btn):
                    hover = True
            if self.contextMenuEnabled():
                ev.acceptClicks(QtCore.Qt.RightButton)
            if self.selectFlag:
                hover = False
        if hover:
            self.setMouseHover(True)
            self.sigHoverEvent.emit(self)
            ev.acceptClicks(
                QtCore.Qt.LeftButton)  ## If the ROI is hilighted, we should accept all clicks to avoid confusion.
            ev.acceptClicks(QtCore.Qt.RightButton)
            ev.acceptClicks(QtCore.Qt.MidButton)
        else:
            self.setMouseHover(False)

    def setMouseHover(self, hover):
        if self.mouseHovering == hover or self.selectFlag:
            return
        self.mouseHovering = hover
        if hover:
            self.currentPen = QtGui.QPen(QtCore.Qt.green, 0.4, QtCore.Qt.SolidLine, QtCore.Qt.SquareCap)
        else:
            self.currentPen = self.pen

        self.arrow.setStyle(pen = self.currentPen)
        self.update()


    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.RightButton and self.contextMenuEnabled():
            self.raiseContextMenu(ev)
            ev.accept()

        elif global_inst.win_.mode is  'NoMode' and ev.button() == QtCore.Qt.LeftButton:
            if self.selectFlag and (ev.modifiers() & QtCore.Qt.ShiftModifier):
                self.selectFlag = False
                self.currentPen = self.pen
            else:
                self.selectFlag = True
                self.currentPen = QtGui.QPen(QtCore.Qt.yellow, 0, QtCore.Qt.DashLine, QtCore.Qt.SquareCap)
            ev.accept()
        elif int(ev.button() & self.acceptedMouseButtons()) > 0:
            ev.accept()
            self.sigClicked.emit(self, ev)
        else:
            ev.ignore()
        self.arrow.setStyle(pen = self.currentPen)
        self.update()

    def contextMenuEnabled(self):
        return True

    def raiseContextMenu(self, ev):
        if not self.contextMenuEnabled():
            return
        menu = self.getMenu()
        # menu = self.scene().addParentContextMenus(self, menu, ev)
        pos = ev.screenPos()
        menu.popup(QtCore.QPoint(pos.x(), pos.y()))

    def getMenu(self):
        self.menu = QtGui.QMenu()
        self.menu.setTitle(self.tr("FanMenu"))
        remAct = QtGui.QAction(self.tr("Remove select"), self.menu)
        remAct.triggered.connect(global_inst.win_.vb.remove)

        cancAct = QtGui.QAction(self.tr("Cancle"), self.menu)
        cancAct.triggered.connect(self.mouseCancleMenue)

        if self.selectFlag == False:
            remAct.setEnabled(False)
            cancAct.setEnabled(False)
        else:
            remAct.setEnabled(True)
            cancAct.setEnabled(True)
        self.menu.addAction(remAct)
        # self.menu.remAct = remAct

        remAllAct = QtGui.QAction(self.tr("Remove all items"), self.menu)
        remAllAct.triggered.connect(global_inst.win_.vb.removeAll)
        self.menu.addAction(remAllAct)
        self.menu.addAction(cancAct)
        # self.menu.cancAct = cancAct

        return self.menu

    def mouseCancleMenue(self):
        self.selectFlag = False
        self.currentPen = self.pen
        self.arrow.setStyle(pen = self.currentPen)
        self.update()
