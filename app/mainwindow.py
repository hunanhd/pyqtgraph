#-*- coding:utf-8 -*-

from PyQt4 import QtCore

from dialogs import *
from graphicswindow import GraphicsWindow

import global_inst
import sdi_rc

class MainWindow(QtGui.QMainWindow):
    def __init__(self, fileName=None):
        super(MainWindow, self).__init__()
        self.init()
        self.setWindowTitle(self.tr("MainWindown Title"))
        self.resize(900, 600)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.win = GraphicsWindow()
        self.setCentralWidget(self.win)
        self.fltIsStart = False

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

    def autoViewAll(self):
        global_inst.win_.vb.enableAutoRange()

    # def test(self):
    #     global_inst.win_.vb.removeSelect()

    def methodChoose(self):
        mtd = VMethodDlg()
        if mtd.exec_() == QtGui.QDialog.Accepted:
            print "methodChoose"
            print mtd.methodCmb.currentText()

    def tunnelProInput(self):
        tpro = TunnelDlg()
        if tpro.exec_() == QtGui.QDialog.Accepted:
            print "tunnelProInput"
            print tpro.lenthEdit.text()

    def ttunnelProInput(self):
        ttpro = TTunnelDlg()
        if ttpro.exec_() == QtGui.QDialog.Accepted:
            print "ttunnelProInput"
            print ttpro.lenthEdit.text()

    def hairDryerProInput(self):
        hdpro = HairDryerDlg()
        if hdpro.exec_() == QtGui.QDialog.Accepted:
            print "hairDryerProInput"
            print hdpro.lenthEdit.text()

    def windLibProInput(self):
        wlPro = WindLibDlg()
        if wlPro.exec_() == QtGui.QDialog.Accepted:
            print "windLibProInput"
            print wlPro.numEdit.text()

    def windCabProInput(self):
        wcPro = WindCabinetDlg()
        if wcPro.exec_() == QtGui.QDialog.Accepted:
            print "windCabProInput"
            print wcPro.numEdit.text()

    def disRamProInput(self):
        drPro = DisconRamDlg()
        if drPro.exec_() == QtGui.QDialog.Accepted:
            print "disRamProInput"
            print drPro.numEdit.text()

    def drilVentProInput(self):
        dvPro = DrilVentilationDlg()
        if dvPro.exec_() == QtGui.QDialog.Accepted:
            print "drilVentProInput"
            print dvPro.numEdit.text()

    def nodeProInput(self):
        nodePro = NodeProDlg()
        if nodePro.exec_() == QtGui.QDialog.Accepted:
            print "nodeProInput"
            print nodePro.idEdit.text()

    def getSeriesFan(self):
        msg = QtGui.QMessageBox()
        msg.setText("There are some promblem!!!")
        msg.exec_()

    def afterDamp(self):
        aftDamp = CaclAfterDampDlg()
        if aftDamp.exec_() == QtGui.QDialog.Accepted:
            print aftDamp.timeEdit.text()

    def windSpeed(self):
        windspd = CaclWindSpeedDlg()
        if windspd.exec_() == QtGui.QDialog.Accepted:
            print windspd.speedEdit.text()

    def unitPower(self):
        untpow = CaclUnitPowerDlg()
        if untpow.exec_() == QtGui.QDialog.Accepted:
            print untpow.unitPowerEdit.text()

    def mineHeat(self):
        mineheat = CaclMineHeatDlg()
        if mineheat.exec_() == QtGui.QDialog.Accepted:
            print mineheat.sumPowerEdit.text()

    def workers(self):
        woks = CaclWorkerDlg()
        if woks.exec_() == QtGui.QDialog.Accepted:
            print woks.numWorkerEdit.text()

    def ensureQ(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("ensureQ"))
        msg.setText("max of Q is ")
        msg.exec_()

    def ensureVMetd(self):
        msg = QtGui.QMessageBox()
        msg.setWindowTitle(self.tr("ensureVmetd"))
        str = self.tr("the method is one fan")
        str.append("\n")
        str.append(self.tr("fan's typle: No6.0/4*22"))
        msg.setText(str)
        msg.exec_()

    def startFluent(self):
        import win32api,os,time
        # if os.path.exists('./scm/hd.msh') is False:
        delfiles = []
        for parent,dirname,filename in os.walk("."):
            for f in filename:
                subfix = os.path.splitext(f)[0]
                if subfix == "hd":
                    delfiles.append(f)
        # os.remove('hd.cas')
        for df in delfiles:
            try:
                os.remove('./scm/%s'%df)
            except  WindowsError:
                pass

        win32api.ShellExecute(0,'open','C:/Fluent.Inc/ntbin/ntx86/gambit.exe','-r2.4.6 -id "hd" -inputfile "writed.jou"' ,'./scm',1)
        time.sleep(0.01)
        handle = win32api.ShellExecute(0,'open','C:/Fluent.Inc/ntbin/ntx86/fluent.exe','-r6.3.26 2d -i "load.scm"' ,'./scm',1)
        if handle:
            self.fltIsStart = True
    def endFluent(self):
        import os
        if self.fltIsStart:
            os.system('taskkill /f /im fl6326s.exe')
            self.fltIsStart = False
        else:
            msg = QtGui.QMessageBox()
            msg.setWindowTitle(self.tr("warming"))
            msg.setText(self.tr("flunet is not start!"))
            msg.exec_()
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

    #修改模式为风机插入
    def setFanMode(self):
        self.win.setFanMode()

    #修改模式为节点插入
    def setNodeMode(self):
        self.win.setNodeMode()

    def init(self):
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

    def createActions(self):
        self.newAct = QtGui.QAction(QtGui.QIcon(':/images/new.png'), self.tr("&New"),
                                    self, shortcut=QtGui.QKeySequence.New,
                                    statusTip=self.tr("Create a new file"), triggered=self.newFile)

        self.openAct = QtGui.QAction(QtGui.QIcon(':/images/open.png'),
                                     self.tr("&Open..."), self, shortcut=QtGui.QKeySequence.Open,
                                     statusTip=self.tr("Open an existing file"), triggered=self.open)

        self.saveAct = QtGui.QAction(QtGui.QIcon(':/images/save.png'),
                                     self.tr("&Save"), self, shortcut=QtGui.QKeySequence.Save,
                                     statusTip=self.tr("Save the document to disk"), triggered=self.save)

        self.saveAsAct = QtGui.QAction(self.tr("Save &As..."), self,
                                       shortcut=QtGui.QKeySequence.SaveAs,
                                       statusTip=self.tr("Save the document under a new name"),
                                       triggered=self.saveAs)

        self.printAct = QtGui.QAction(QtGui.QIcon(':/images/fileprint.png'),
                                      self.tr("print..."), self, shortcut="Ctrl+P",
                                      statusTip=self.tr("Print the file"), triggered=self.printfile)

        self.closeAct = QtGui.QAction(self.tr("&Close"), self, shortcut="Ctrl+W",
                                      statusTip=self.tr("Close this window"), triggered=self.close)

        self.exitAct = QtGui.QAction(self.tr("E&xit"), self, shortcut="Ctrl+Q",
                                     statusTip=self.tr("Exit the application"),
                                     triggered=QtGui.qApp.closeAllWindows)

        self.cutAct = QtGui.QAction(QtGui.QIcon(':/images/cut.png'), self.tr("Cu&t"),
                                    self, enabled=False, shortcut=QtGui.QKeySequence.Cut,
                                    statusTip=self.tr("Cut the current selection's contents to the clipboard"), )
        # triggered=self.textEdit.cut

        self.copyAct = QtGui.QAction(QtGui.QIcon(':/images/copy.png'),
                                     self.tr("&Copy"), self, enabled=False, shortcut=QtGui.QKeySequence.Copy,
                                     statusTip=self.tr("Copy the current selection's contents to the clipboard"), )
        # triggered=self.textEdit.copy

        self.pasteAct = QtGui.QAction(QtGui.QIcon(':/images/paste.png'),
                                      self.tr("&Paste"), self, shortcut=QtGui.QKeySequence.Paste,
                                      statusTip=self.tr("Paste the clipboard's contents into the current selection"), )

        self.autoAct = QtGui.QAction(QtGui.QIcon(':/images/auto.png'),
                                      self.tr("&Auto"), self, shortcut='A',
                                      statusTip=self.tr("Auto Visible"), triggered=self.autoViewAll)

        # self.testAct = QtGui.QAction(self.tr("&Test"), self,
        #                               statusTip=self.tr("test"), triggered=self.test)

        # triggered=self.textEdit.paste

        self.methodAct = QtGui.QAction(self.tr("&method"), self,
                                       statusTip=self.tr("Choose method"), triggered=self.methodChoose)

        self.tunnelProAct = QtGui.QAction(self.tr("&tunnelPro"), self, enabled=False,
                                          statusTip=self.tr("tunnelPro"), triggered=self.tunnelProInput)
        self.ttunnelProAct = QtGui.QAction(self.tr("&ttunnelPro"), self, enabled=False,
                                           statusTip=self.tr("ttunnelPro"), triggered=self.ttunnelProInput)
        self.hairDryerProAct = QtGui.QAction(self.tr("&hairDryerPro"), self, enabled=False,
                                             statusTip=self.tr("hairDryerPro"), triggered=self.hairDryerProInput)
        self.windLibAct = QtGui.QAction(self.tr("&windLib"), self, enabled=False,
                                        statusTip=self.tr("windLibAct"), triggered=self.windLibProInput)
        self.windCabinetAct = QtGui.QAction(self.tr("&windCabinet"), self, enabled=False,
                                            statusTip=self.tr("windCabinet"), triggered=self.windCabProInput)
        self.discontinusRamAct = QtGui.QAction(self.tr("&discontinusRam"), self, enabled=False,
                                               statusTip=self.tr("discontinusRam"), triggered=self.disRamProInput)
        self.seriesFanAct = QtGui.QAction(self.tr("&seriesFan"), self, enabled=False,
                                          statusTip=self.tr("seriesFan"), triggered=self.getSeriesFan)
        self.drillingVentAct = QtGui.QAction(self.tr("&drillingVent"), self, enabled=False,
                                             statusTip=self.tr("drillingVent"), triggered=self.drilVentProInput)
        self.nodeProAct = QtGui.QAction(self.tr("&nodePro"), self, enabled=False,
                                        statusTip=self.tr("nodePro"), triggered=self.nodeProInput)

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

        self.fanCmdAct = QtGui.QAction(
            QtGui.QIcon(':/images/fan.png'), self.tr("FanInsert"), self,
            statusTip=self.tr("Insert the fan"),
            triggered=self.setFanMode)

        self.nodeCmdAct = QtGui.QAction(
            QtGui.QIcon(':/images/node.png'), self.tr("NodeInsert"), self,
            statusTip=self.tr("Insert the node"),
            triggered=self.setNodeMode)

        self.windlibCmdAct = QtGui.QAction(
            QtGui.QIcon(':/images/windlib.png'), self.tr("windlib"), self,
            statusTip=self.tr("wind library"),
            triggered=self.open)

        self.windcabCmdAct = QtGui.QAction(
            QtGui.QIcon(':/images/windcab.png'), self.tr("windcab"), self,
            statusTip=self.tr("wind cabinet"),
            triggered=self.open)

        self.aboutAct = QtGui.QAction(self.tr("&About"), self,
                                      statusTip=self.tr("Show the application's About box"),
                                      triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                                        statusTip="Show the Qt library's About box",
                                        triggered=QtGui.qApp.aboutQt)

        self.afterDampAct = QtGui.QAction(self.tr("After Damp"), self,
                                        statusTip=self.tr("caculate by after damp"),
                                        triggered=self.afterDamp)

        self.windSpeedAct = QtGui.QAction(self.tr("wind speed"), self,
                                        statusTip=self.tr("caculate by wind speed"),
                                        triggered=self.windSpeed)

        self.unitPowerAct = QtGui.QAction(self.tr("unit power"), self,
                                        statusTip=self.tr("caculate by unit power"),
                                        triggered=self.unitPower)

        self.mineHeatAct = QtGui.QAction(self.tr("mine heat"), self,
                                        statusTip=self.tr("caculate by mine heat"),
                                        triggered=self.mineHeat)

        self.workersAct = QtGui.QAction(self.tr("Workers"), self,
                                        statusTip=self.tr("caculate by workers"),
                                        triggered=self.workers)

        self.ensureQAct = QtGui.QAction(self.tr("ensureQ"), self,
                                        statusTip=self.tr("ensure Q"),
                                        triggered=self.ensureQ)

        self.ensureFansAct = QtGui.QAction(self.tr("ensureFans"), self,
                                        statusTip=self.tr("ensure the fans"),
                                        triggered=self.ensureQ)

        self.ensureHairDryerAct = QtGui.QAction(self.tr("ensureHairDryer"), self,
                                        statusTip=self.tr("ensure the hairDryer"),
                                        triggered=self.ensureQ)

        self.ensureHairDryerAct = QtGui.QAction(self.tr("ensureHairDryer"), self,
                                        statusTip=self.tr("ensure the hairDryer"),
                                        triggered=self.ensureQ)

        self.ensureVTPAct = QtGui.QAction(self.tr("ensureVTP"), self,
                                        statusTip=self.tr("ensure the VTP"),
                                        triggered=self.ensureQ)

        self.ensureVMetdAct = QtGui.QAction(self.tr("ensureMethod"), self,
                                        statusTip=self.tr("ensure the VMethod"),
                                        triggered=self.ensureVMetd)

        self.startFltAct = QtGui.QAction(self.tr("startFluent"), self,
                                        statusTip=self.tr("Start the fluent"),
                                        triggered=self.startFluent)

        self.endFltAct = QtGui.QAction(self.tr("endFluent"), self,
                                        statusTip=self.tr("End the fluent"),
                                        triggered=self.endFluent)

        # self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)
        # self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(self.tr("&File"))
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.closeAct)
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu(self.tr("&Edit"))
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.viewMenu = self.menuBar().addMenu(self.tr("&View"))
        self.viewMenu.addAction(self.autoAct)
        self.viewMenu.addAction(self.startFltAct)
        self.viewMenu.addAction(self.endFltAct)
        # self.viewMenu.addAction(self.testAct)

        self.menuBar().addSeparator()

        self.DrawMenu = self.menuBar().addMenu(self.tr("Draw"))
        self.DrawMenu.addAction(self.TunnelCmdAct)
        self.DrawMenu.addAction(self.HairDryerCmdAct)
        self.DrawMenu.addAction(self.fanCmdAct)
        self.DrawMenu.addAction(self.nodeCmdAct)
        self.DrawMenu.addAction(self.windcabCmdAct)
        self.DrawMenu.addAction(self.windlibCmdAct)

        self.menuBar().addSeparator()

        self.paramMenu = self.menuBar().addMenu(self.tr("Parameter"))
        self.tunnelMenu = QtGui.QMenu(self.tr("tunnelMenu"))
        self.paramMenu.addAction(self.methodAct)
        self.paramMenu.addMenu(self.tunnelMenu)
        self.tunnelMenu.addAction(self.tunnelProAct)
        self.tunnelMenu.addAction(self.ttunnelProAct)
        self.paramMenu.addAction(self.hairDryerProAct)
        self.paramMenu.addAction(self.windLibAct)
        self.paramMenu.addAction(self.windCabinetAct)
        self.paramMenu.addAction(self.discontinusRamAct)
        self.paramMenu.addAction(self.seriesFanAct)
        self.paramMenu.addAction(self.drillingVentAct)
        self.paramMenu.addAction(self.nodeProAct)

        self.menuBar().addSeparator()

        self.caculMenu = self.menuBar().addMenu(self.tr("Caculation"))
        self.caculMenu.addAction(self.afterDampAct)
        self.caculMenu.addAction(self.windSpeedAct)
        self.caculMenu.addAction(self.unitPowerAct)
        self.caculMenu.addAction(self.mineHeatAct)
        self.caculMenu.addAction(self.workersAct)
        self.caculMenu.addAction(self.ensureQAct)

        self.ensureMenu = self.menuBar().addMenu(self.tr("EnsureProject"))
        self.ensureMenu.addAction(self.ensureFansAct)
        self.ensureMenu.addAction(self.ensureHairDryerAct)
        self.ensureMenu.addAction(self.ensureVTPAct)
        self.ensureMenu.addAction(self.ensureVMetdAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar(self.tr("File"))
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)
        self.fileToolBar.addAction(self.printAct)

        #把editToolBar加载到窗口的右边，可以移动，但是保存设置问题还没有涉及
        self.editToolBar = QtGui.QToolBar(self.tr("Edit"))
        self.addToolBar(QtCore.Qt.RightToolBarArea, self.editToolBar)
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

        self.drawToolBar = QtGui.QToolBar(self.tr("Draw"))
        #把drawToolBar加载到窗口的左边，可以移动，但是保存设置问题还没有涉及
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.drawToolBar)
        self.drawToolBar.addAction(self.TunnelCmdAct)
        self.drawToolBar.addAction(self.HairDryerCmdAct)
        self.drawToolBar.addAction(self.fanCmdAct)
        self.drawToolBar.addAction(self.nodeCmdAct)
        self.drawToolBar.addAction(self.windcabCmdAct)
        self.drawToolBar.addAction(self.windlibCmdAct)

        self.viewToolBar = self.addToolBar(self.tr("View"))
        self.viewToolBar.addAction(self.autoAct)
        self.viewToolBar.addAction(self.startFltAct)
        self.viewToolBar.addAction(self.endFltAct)
        # self.viewToolBar.addAction(self.testAct)

    def createStatusBar(self):
        self.statusBar().showMessage(self.tr("Ready"))