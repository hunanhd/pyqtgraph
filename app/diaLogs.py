# -*- coding: utf-8 -*-
import sys

from PyQt4 import QtGui


class TunnelDlg(QtGui.QDialog):
    def __init__(self):
        super(TunnelDlg, self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.lenthLabel = QtGui.QLabel(self.tr("Lenth"))
        self.lenthEdit = QtGui.QLineEdit()

        self.widthLabel = QtGui.QLabel(self.tr("Width"))
        self.widthEdit = QtGui.QLineEdit()

        self.speedLabel = QtGui.QLabel(self.tr("Speed"))
        self.speedEdit = QtGui.QLineEdit()

        self.quaLabel = QtGui.QLabel(self.tr("air quantity"))
        self.quaEdit = QtGui.QLineEdit()

        self.windageLabel = QtGui.QLabel(self.tr("windage"))
        self.windageEdit = QtGui.QLineEdit()

        self.mainLayout.addWidget(self.lenthLabel, 0, 0)
        self.mainLayout.addWidget(self.lenthEdit, 0, 1)

        self.mainLayout.addWidget(self.widthLabel, 1, 0)
        self.mainLayout.addWidget(self.widthEdit, 1, 1)

        self.mainLayout.addWidget(self.speedLabel, 2, 0)
        self.mainLayout.addWidget(self.speedEdit, 2, 1)

        self.mainLayout.addWidget(self.quaLabel, 3, 0)
        self.mainLayout.addWidget(self.quaEdit, 3, 1)

        self.mainLayout.addWidget(self.windageLabel, 4, 0)
        self.mainLayout.addWidget(self.windageEdit, 4, 1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("Tunnel"))


class TTunnelDlg(QtGui.QDialog):
    def __init__(self):
        super(TTunnelDlg, self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.lenthLabel = QtGui.QLabel(self.tr("Lenth"))
        self.lenthEdit = QtGui.QLineEdit()

        self.widthLabel = QtGui.QLabel(self.tr("Width"))
        self.widthEdit = QtGui.QLineEdit()

        self.mainLayout.addWidget(self.lenthLabel, 0, 0)
        self.mainLayout.addWidget(self.lenthEdit, 0, 1)

        self.mainLayout.addWidget(self.widthLabel, 1, 0)
        self.mainLayout.addWidget(self.widthEdit, 1, 1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("TTunnel"))

class VMethodDlg(QtGui.QDialog):
    def __init__(self):
        super(VMethodDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.methodLabel = QtGui.QLabel(self.tr("method"))
        self.methodCmb = QtGui.QComboBox()
        methodList = [self.tr("pressin"),self.tr("extraction")]
        self.methodCmb.addItems(methodList)

        self.wayLabel = QtGui.QLabel(self.tr("way"))
        self.wayCmb = QtGui.QComboBox()
        wayList = [self.tr("pressin"),self.tr("extraction")]
        self.wayCmb.addItems(wayList)

        self.mainLayout.addWidget(self.methodLabel,0,0)
        self.mainLayout.addWidget(self.methodCmb,0,1)

        self.mainLayout.addWidget(self.wayLabel,1,0)
        self.mainLayout.addWidget(self.wayCmb,1,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("Method"))

class HairDryerDlg(QtGui.QDialog):
    def __init__(self):
        super(HairDryerDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.lenthLabel = QtGui.QLabel(self.tr("Lenth"))
        self.lenthEdit = QtGui.QLineEdit()

        self.diameterLabel = QtGui.QLabel(self.tr("diameter"))
        self.diameterEdit = QtGui.QLineEdit()

        self.bendLabel = QtGui.QLabel(self.tr("bend"))
        self.bendEdit = QtGui.QLineEdit()

        self.natureLabel = QtGui.QLabel(self.tr("nature"))
        self.natureCmb = QtGui.QComboBox()
        natureList = [self.tr("figidity"),self.tr("flexibility")]
        self.natureCmb.addItems(natureList)

        self.junctionLabel = QtGui.QLabel(self.tr("junctionWay"))
        self.junctionCmb = QtGui.QComboBox()
        self.junctionList = [self.tr("Coil reverse side"),self.tr("plug in")]
        self.junctionCmb.addItems(self.junctionList)
        self.junctionCmb.setEditable(True)

        self.mainLayout.addWidget(self.lenthLabel,0,0)
        self.mainLayout.addWidget(self.lenthEdit,0,1)

        self.mainLayout.addWidget(self.diameterLabel,1,0)
        self.mainLayout.addWidget(self.diameterEdit,1,1)

        self.mainLayout.addWidget(self.bendLabel,2,0)
        self.mainLayout.addWidget(self.bendEdit,2,1)

        self.mainLayout.addWidget(self.natureLabel,3,0)
        self.mainLayout.addWidget(self.natureCmb,3,1)

        self.mainLayout.addWidget(self.junctionLabel,4,0)
        self.mainLayout.addWidget(self.junctionCmb,4,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("HairDryerDlg"))

class WindLibDlg(QtGui.QDialog):
    def __init__(self):
        super(WindLibDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.methodLabel = QtGui.QLabel(self.tr("fan"))
        self.methodCmb = QtGui.QComboBox()
        methodList = [self.tr("pressin"),self.tr("extraction")]
        self.methodCmb.addItems(methodList)

        self.numLabel = QtGui.QLabel(self.tr("number"))
        self.numEdit = QtGui.QLineEdit()

        self.sizeLabel = QtGui.QLabel(self.tr("size"))
        self.sizeEdit = QtGui.QLineEdit()

        self.resFactorLabel = QtGui.QLabel(self.tr("reserve factor"))
        self.resFactorEdit = QtGui.QLineEdit()


        self.mainLayout.addWidget(self.methodLabel,0,0)
        self.mainLayout.addWidget(self.methodCmb,0,1)

        self.mainLayout.addWidget(self.numLabel,1,0)
        self.mainLayout.addWidget(self.numEdit,1,1)

        self.mainLayout.addWidget(self.sizeLabel,2,0)
        self.mainLayout.addWidget(self.sizeEdit,2,1)

        self.mainLayout.addWidget(self.resFactorLabel,3,0)
        self.mainLayout.addWidget(self.resFactorEdit,3,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("The Wind Library"))

class WindCabinetDlg(QtGui.QDialog):
    def __init__(self):
        super(WindCabinetDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.numLabel = QtGui.QLabel(self.tr("number"))
        self.numEdit = QtGui.QLineEdit()

        self.sizeLabel = QtGui.QLabel(self.tr("size"))
        self.sizeEdit = QtGui.QLineEdit()

        self.resFactorLabel = QtGui.QLabel(self.tr("reserve factor"))
        self.resFactorEdit = QtGui.QLineEdit()


        self.mainLayout.addWidget(self.numLabel,0,0)
        self.mainLayout.addWidget(self.numEdit,0,1)

        self.mainLayout.addWidget(self.sizeLabel,1,0)
        self.mainLayout.addWidget(self.sizeEdit,1,1)

        self.mainLayout.addWidget(self.resFactorLabel,2,0)
        self.mainLayout.addWidget(self.resFactorEdit,2,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("The Wind cabinet"))

class DrilVentilationDlg(QtGui.QDialog):
    def __init__(self):
        super(DrilVentilationDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.numLabel = QtGui.QLabel(self.tr("fan number"))
        self.numEdit = QtGui.QLineEdit()

        self.diameterLabel = QtGui.QLabel(self.tr("diameter"))
        self.diameterEdit = QtGui.QLineEdit()

        self.resFactorLabel = QtGui.QLabel(self.tr("reserve factor"))
        self.resFactorEdit = QtGui.QLineEdit()


        self.mainLayout.addWidget(self.numLabel,0,0)
        self.mainLayout.addWidget(self.numEdit,0,1)

        self.mainLayout.addWidget(self.diameterLabel,1,0)
        self.mainLayout.addWidget(self.diameterEdit,1,1)

        self.mainLayout.addWidget(self.resFactorLabel,2,0)
        self.mainLayout.addWidget(self.resFactorEdit,2,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("The drilling vetilation"))

class DisconRamDlg(QtGui.QDialog):
    def __init__(self):
        super(DisconRamDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.numLabel = QtGui.QLabel(self.tr("number"))
        self.numEdit = QtGui.QLineEdit()

        self.diameterLabel = QtGui.QLabel(self.tr("diameter"))
        self.diameterEdit = QtGui.QLineEdit()

        self.resFactorLabel = QtGui.QLabel(self.tr("reserve factor"))
        self.resFactorEdit = QtGui.QLineEdit()


        self.mainLayout.addWidget(self.numLabel,0,0)
        self.mainLayout.addWidget(self.numEdit,0,1)

        self.mainLayout.addWidget(self.diameterLabel,1,0)
        self.mainLayout.addWidget(self.diameterEdit,1,1)

        self.mainLayout.addWidget(self.resFactorLabel,2,0)
        self.mainLayout.addWidget(self.resFactorEdit,2,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("The Discontinous Ram"))

class NodeProDlg(QtGui.QDialog):
    def __init__(self):
        super(NodeProDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.idLabel = QtGui.QLabel(self.tr("Id"))
        self.idEdit = QtGui.QLineEdit()

        self.diameterLabel = QtGui.QLabel(self.tr("diameter"))
        self.diameterEdit = QtGui.QLineEdit()

        self.elevLabel = QtGui.QLabel(self.tr("elevation"))
        self.elevEdit = QtGui.QLineEdit()

        self.pressLabel = QtGui.QLabel(self.tr("pressure"))
        self.pressEdit = QtGui.QLineEdit()

        self.temperLabel = QtGui.QLabel(self.tr("temperature"))
        self.temperEdit = QtGui.QLineEdit()

        self.mainLayout.addWidget(self.idLabel,0,0)
        self.mainLayout.addWidget(self.idEdit,0,1)

        self.mainLayout.addWidget(self.diameterLabel,1,0)
        self.mainLayout.addWidget(self.diameterEdit,1,1)

        self.mainLayout.addWidget(self.elevLabel,2,0)
        self.mainLayout.addWidget(self.elevEdit,2,1)

        self.mainLayout.addWidget(self.pressLabel,3,0)
        self.mainLayout.addWidget(self.pressEdit,3,1)

        self.mainLayout.addWidget(self.temperLabel,4,0)
        self.mainLayout.addWidget(self.temperEdit,4,1)

        self.btnBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

        self.mainLayout.addWidget(self.btnBox,5,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("The Node Property"))

    def accept(self):
        print self.temperEdit.getText()
        QtGui.QDialog.accept()

def main():
    app = QtGui.QApplication([])
    ttdia = TunnelDlg()
    v = VMethodDlg()
    h =HairDryerDlg()
    w = WindLibDlg()
    wc = WindCabinetDlg()
    d = DisconRamDlg()
    dd = DrilVentilationDlg()
    n = NodeProDlg()
    n.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()