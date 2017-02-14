# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DashWindows.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QAxContainer import *
import kiwoom.kiwoomcaller as kiwoomcaller
import importlib

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.btnMonth = QtGui.QPushButton(self.centralwidget)
        self.btnMonth.setGeometry(QtCore.QRect(210, 30, 93, 28))
        self.btnMonth.setObjectName(_fromUtf8("btnMonth"))
        self.cbMonth = QtGui.QComboBox(self.centralwidget)
        self.cbMonth.setGeometry(QtCore.QRect(40, 30, 151, 21))
        self.cbMonth.setObjectName(_fromUtf8("cbMonth"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(50, 80, 661, 441))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tb1 = QtGui.QWidget()
        self.tb1.setObjectName(_fromUtf8("tb1"))
        self.tableView = QtGui.QTableView(self.tb1)
        self.tableView.setGeometry(QtCore.QRect(30, 40, 331, 331))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tabWidget.addTab(self.tb1, _fromUtf8(""))
        self.tb2 = QtGui.QWidget()
        self.tb2.setObjectName(_fromUtf8("tb2"))
        self.tabWidget.addTab(self.tb2, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.btnMonth.setText(_translate("MainWindow", "PushButton", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tb1), _translate("MainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tb2), _translate("MainWindow", "Tab 2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Page", None))


        self.init_kiwwom()


    def init_kiwwom(self):
        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")
        self.kiwoom.connect(self.kiwoom, QtCore.SIGNAL("OnEventConnect(int)"), self.OnEventConnect)

    def OnEventConnect(self, ErrCode):
        if ErrCode == 0:
            print("@@@ 로그인 성공 @@@")
            #kiwoomcaller.callCommRealData(self, self.kiwoom)
            data = kiwoomcaller.GetActPriceList(self, self.kiwoom).split(';')

            for item in data:
                self.cbMonth.addItem(item[:3] + '.' + item[3:])


    def btn2_clicked(self):
        importlib.reload(kiwoomcaller)
        # importlib.reload(mymongo)
        # importlib.reload(ThreadTest)
        # importlib.reload(R50068)
        kiwoomcaller.callCommRealData(self, self.kiwoom)

    def OnReceiveTrData(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrorCode, Message, SplmMsg):
        importlib.reload(kiwoomcaller)
        kiwoomcaller.receiveTR(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrorCode, Message, SplmMsg)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())