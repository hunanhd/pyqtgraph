# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import sys

class TunnelDlg(QtGui.QDialog):
    def __init__(self):
        super(TunnelDlg,self).__init__()
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


        self.mainLayout.addWidget(self.lenthLabel,0,0)
        self.mainLayout.addWidget(self.lenthEdit,0,1)

        self.mainLayout.addWidget(self.widthLabel,1,0)
        self.mainLayout.addWidget(self.widthEdit,1,1)

        self.mainLayout.addWidget(self.speedLabel,2,0)
        self.mainLayout.addWidget(self.speedEdit,2,1)

        self.mainLayout.addWidget(self.quaLabel,3,0)
        self.mainLayout.addWidget(self.quaEdit,3,1)

        self.mainLayout.addWidget(self.windageLabel,4,0)
        self.mainLayout.addWidget(self.windageEdit,4,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("Tunnel"))

class TTunnelDlg(QtGui.QDialog):
    def __init__(self):
        super(TTunnelDlg,self).__init__()
        self.mainLayout = QtGui.QGridLayout()

        self.lenthLabel = QtGui.QLabel(self.tr("Lenth"))
        self.lenthEdit = QtGui.QLineEdit()

        self.widthLabel = QtGui.QLabel(self.tr("Width"))
        self.widthEdit = QtGui.QLineEdit()

        self.mainLayout.addWidget(self.lenthLabel,0,0)
        self.mainLayout.addWidget(self.lenthEdit,0,1)

        self.mainLayout.addWidget(self.widthLabel,1,0)
        self.mainLayout.addWidget(self.widthEdit,1,1)

        self.setLayout(self.mainLayout)
        #self.resize(400,300)
        self.setWindowTitle(self.tr("TTunnel"))


def main():
    app = QtGui.QApplication([])
    ttdia = TunnelDlg()
    ttdia.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()