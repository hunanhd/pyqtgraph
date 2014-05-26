# -*- coding:utf-8 -*-

from PyQt4 import QtCore, QtGui

from graphicswindow import GraphicsWindow

import sdi_rc


class MainWindow(QtGui.QMainWindow):
    #sequenceNumber = 1

    def __init__(self, fileName=None):
        super(MainWindow, self).__init__()
        self.init()
        self.setWindowTitle(self.tr("MainWindown Title"))
        self.resize(900, 600)
        self.win = GraphicsWindow()
        self.win.setMainWindow(self)
        self.setCentralWidget(self.win)

    def closeEvent(self, event):
        pass

    def newFile(self):
        pass

    def open(self):
        pass

    def save(self):
        pass

    def saveAs(self):
        pass

    def printfile(self):
        # printer = QtGui.QPrinter()
        # dialog = QtGui.QPrintDialog(printer, self)
        # if (dialog.exec_() != QtGui.QDialog.Accepted):
        #     return
        # painter = QtGui.QPainter(printer)
        # self.win.setBackground('w')
        # self.win.vb.setBackground('w')
        # self.win.render(painter)
        # painter.end()
        pass

    def about(self):
        QtGui.QMessageBox.about(self, "About SDI",
                                "The <b>SDI</b> example demonstrates how to write single "
                                "document interface applications using Qt.")

    #修改模式为巷道绘制
    def setTunnelMode(self):
        self.win.setTunnelMode()

    #修改模式为风筒布置
    def setHairDryerMode(self):
        self.win.setHairDryerMode()

    def init(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

    def createActions(self):
        self.newAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'), "&New",
                                    self, shortcut=QtGui.QKeySequence.New,
                                    statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QtGui.QAction(QtGui.QIcon(':/images/open.png'),
                                     "&Open...", self, shortcut=QtGui.QKeySequence.Open,
                                     statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon(':/images/save.png'),
                                     "&Save", self, shortcut=QtGui.QKeySequence.Save,
                                     statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QtGui.QAction("Save &As...", self,
                                       shortcut=QtGui.QKeySequence.SaveAs,
                                       statusTip="Save the document under a new name",
                                       triggered=self.saveAs)

        self.printAct = QtGui.QAction(QtGui.QIcon(':/images/fileprint.png'),
                                      "print...", self, shortcut="Ctrl+P",
                                      statusTip="Print the file", triggered=self.printfile)

        self.closeAct = QtGui.QAction("&Close", self, shortcut="Ctrl+W",
                                      statusTip="Close this window", triggered=self.close)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                                     statusTip="Exit the application",
                                     triggered=QtGui.qApp.closeAllWindows)

        self.cutAct = QtGui.QAction(QtGui.QIcon(':/images/cut.png'), "Cu&t",
                                    self, enabled=False, shortcut=QtGui.QKeySequence.Cut,
                                    statusTip="Cut the current selection's contents to the clipboard", )
        # triggered=self.textEdit.cut

        self.copyAct = QtGui.QAction(QtGui.QIcon(':/images/copy.png'),
                                     "&Copy", self, enabled=False, shortcut=QtGui.QKeySequence.Copy,
                                     statusTip="Copy the current selection's contents to the clipboard", )
        # triggered=self.textEdit.copy

        self.pasteAct = QtGui.QAction(QtGui.QIcon(':/images/paste.png'),
                                      "&Paste", self, shortcut=QtGui.QKeySequence.Paste,
                                      statusTip="Paste the clipboard's contents into the current selection", )
        # triggered=self.textEdit.paste

        self.methodAct = QtGui.QAction("&method", self,
                                      statusTip="Choose method", triggered=self.open)

        self.wayAct = QtGui.QAction("&way", self,
                                      statusTip="Choose way", triggered=self.open)
        self.tunnelProAct = QtGui.QAction("&tunnelPro", self,
                                      statusTip="tunnelPro", triggered=self.open)
        self.hairDryerProAct = QtGui.QAction("&hairDryerPro", self,
                                      statusTip="hairDryerPro", triggered=self.open)
        self.windLibAct = QtGui.QAction("&windLib", self,
                                      statusTip="windLibAct", triggered=self.open)
        self.windCabinetAct = QtGui.QAction("&windCabinet", self,
                                      statusTip="windCabinet", triggered=self.open)
        self.discontinusRamAct = QtGui.QAction("&discontinusRam", self,
                                      statusTip="discontinusRam", triggered=self.open)
        self.seriesFanAct = QtGui.QAction("&seriesFan", self,
                                      statusTip="seriesFan", triggered=self.open)
        self.drillingVentAct = QtGui.QAction("&drillingVent", self,
                                      statusTip="drillingVent", triggered=self.open)
        self.nodeProAct = QtGui.QAction("&nodePro", self,
                                      statusTip="nodePro", triggered=self.open)


        self.TunnelCmdAct = QtGui.QAction(
            QtGui.QIcon(':/images/tunnel.png'), self.tr("DrawTunnel"), self,
            shortcut="Ctrl+T",
            statusTip=self.tr("Draw the Tunnel"),
            triggered=self.setTunnelMode)

        self.HairDryerCmdAct = QtGui.QAction(
            QtGui.QIcon(':/images/hairdryer.png'), self.tr("DrawHairDryer"), self,
            shortcut="Ctrl+H",
            statusTip=self.tr("Draw the HairDryer"),
            triggered=self.setHairDryerMode)

        self.aboutAct = QtGui.QAction("&About", self,
                                      statusTip="Show the application's About box",
                                      triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                                        statusTip="Show the Qt library's About box",
                                        triggered=QtGui.qApp.aboutQt)

        # self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)
        # self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu("&Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.DrawMenu = self.menuBar().addMenu(self.tr("Draw"))
        self.DrawMenu.addAction(self.TunnelCmdAct)
        self.DrawMenu.addAction(self.HairDryerCmdAct)

        self.menuBar().addSeparator()

        self.paramMenu = self.menuBar().addMenu(self.tr("Parameter"))
        self.paramMenu.addAction(self.methodAct)
        self.paramMenu.addAction(self.wayAct)
        self.paramMenu.addAction(self.tunnelProAct)
        self.paramMenu.addAction(self.hairDryerProAct)
        self.paramMenu.addAction(self.windLibAct)
        self.paramMenu.addAction(self.windCabinetAct)
        self.paramMenu.addAction(self.discontinusRamAct)
        self.paramMenu.addAction(self.seriesFanAct)
        self.paramMenu.addAction(self.drillingVentAct)
        self.paramMenu.addAction(self.nodeProAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.printAct)

        #把editToolBar加载到窗口的右边，可以移动，但是保存设置问题还没有涉及
        self.editToolBar = QtGui.QToolBar("Edit")
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.editToolBar)
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

        self.drawToolBar = QtGui.QToolBar("Draw")
        #把drawToolBar加载到窗口的左边，可以移动，但是保存设置问题还没有涉及
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.drawToolBar)
        self.drawToolBar.addAction(self.TunnelCmdAct)
        self.drawToolBar.addAction(self.HairDryerCmdAct)


    def createStatusBar(self):
        self.statusBar().showMessage("Ready")