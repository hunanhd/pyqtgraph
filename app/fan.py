# -*- coding:utf-8 -*-

from buildfuc import *
from tunnel import Tunnel

class Fan(QtGui.QGraphicsPathItem):
    def __init__(self,width,lenth):
        super(Fan, self).__init__()
        self.opts = {'pxMode': False}
        self.width = width
        self.lenth = lenth
        # self.pt = pt
        # self.items = items

    def paint(self,p,*args):
        p.setRenderHint(QtGui.QPainter.Antialiasing)
        QtGui.QGraphicsPathItem.paint(self, p, *args)

    def shape(self):
        return QtGui.QGraphicsPathItem.shape(self)

        # self.isRawAble = True
        # hspt = item.spt
        # hept = item.ept
        # break #只要最上面的一个，其他的Items不考虑，所以获得第一个就break,如果风筒用不同的类就没有必要这么做
        # else:
        #     msg = QtGui.QMessageBox()
        #     msg.setText("clicked Erro!")
        #     msg.exec_()
        #     self.isRawAble = False
        #     return -1

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
        return arrow

    def drawFan(self):
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

        self.setPath(path)
        self.setPen(pg.fn.mkPen(color='w'))

        # 如果想要画出的图形大小不变，可以让pxMode变为True
        if self.opts['pxMode']:
            self.setFlags(self.flags() | self.ItemIgnoresTransformations)
        else:
            self.setFlags(self.flags() & ~self.ItemIgnoresTransformations)

    def dataBounds(self, ax, frac, orthoRange=None):
        pw = 0
        pen = self.pen()
        if not pen.isCosmetic():
            pw = pen.self.width() * 0.7072
        if self.opts['pxMode']:
            return [0,0]
        else:
            br = self.boundingRect()
            if ax == 0:
                return [br.left()-pw, br.right()+pw]
            else:
                return [br.top()-pw, br.bottom()+pw]

    def pixelPadding(self):
        pad = 0
        if self.opts['pxMode']:
            br = self.boundingRect()
            pad += (br.self.width()**2 + br.height()**2) ** 0.5
        pen = self.pen()
        if pen.isCosmetic():
            pad += max(1, pen.width()) * 0.7072
        return pad
