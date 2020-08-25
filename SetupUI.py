"""
Last update: 21 August 2020
Created: 21 August 2020

core UI layout to control motorised VAT valve series 590

@author: Victor Rogalev
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction


class Ui_MainWindow(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.w = 400
        self.h = 100
        self.setGeometry(300, 300, self.w, self.h)
        self.my_menu_bar = self.menuBar()
        self.statusbar = self.statusBar()
        self.statusbar.showMessage('Ready')

        # self.options_menu = self.my_menu_bar.addMenu('Options')
        # self.toggle_mode_action = QAction('God Mode', self, checkable=True)
        # self.toggle_mode_action.setStatusTip('Enable God Mode')
        # self.toggle_mode_action.setChecked(False)
        # self.options_menu.addAction(self.toggle_mode_action)

        self.setup_ui()

    def setup_ui(self):

        self.layoutWidget = QtWidgets.QWidget(self)
        # self.layoutWidget.setGeometry(QtCore.QRect(10, 10, self.w-10, self.h-10))
        self.layoutWidget.setObjectName("layoutWidget")
        self.layoutWidget.setStyleSheet("background-color:grey;")
        self.setCentralWidget(self.layoutWidget)

        self.MainVerticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.MainHorizontalLayout = QtWidgets.QHBoxLayout()

        """Create control labels/buttons and pack them into a dictionary self.objects_dict which looks like
        {"Position [0-1000]":SingleControlDict, "Pressure [mbar]":SingleControlDict}"""
        self.VerticalLayoutXYZ = QtWidgets.QVBoxLayout()
        self.VerticalLayoutXYZ.setContentsMargins(0, 0, 0, 0)
        self.VerticalLayoutXYZ.setObjectName("VerticalLayoutXYZ")
        self.names_tuple = ("Position [0-1000]", "Pressure [mbar]")
        self.objects_dict = {}
        for i in range(len(self.names_tuple)):
            self.SetHorizontalLayout()
            self.SingleControlDict[0].setText(self.names_tuple[i])
            self.objects_dict[self.names_tuple[i]]=self.SingleControlDict

        self.MainHorizontalLayout.addLayout(self.VerticalLayoutXYZ)
        self.MainVerticalLayout.addLayout(self.MainHorizontalLayout)

    def SetHorizontalLayout(self):
        self.SingleControlDict = {}
        self.HorizontalLayout = QtWidgets.QHBoxLayout()

        "Label showing name of the action"
        self.Label = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.Label.sizePolicy().hasHeightForWidth())
        self.Label.setFixedWidth(130)
        self.Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Label.setFont(font)
        self.Label.setAlignment(QtCore.Qt.AlignCenter)
        self.HorizontalLayout.addWidget(self.Label)
        self.SingleControlDict[0] = self.Label
        self.HorizontalLayout.addStretch()

        "Label showing current value"
        self.Label = QtWidgets.QLabel(self.layoutWidget)
        # sizePolicy.setHeightForWidth(self.Label.sizePolicy().hasHeightForWidth())
        self.Label.setFixedWidth(110)
        self.Label.setSizePolicy(sizePolicy)
        self.Label.setFont(font)
        self.Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Label.setStyleSheet("color: rgb(52,181,52); background: rgb(0,0,0);")
        self.Label.setText(" 0.00 ")
        self.HorizontalLayout.addWidget(self.Label)
        self.SingleControlDict[1] = self.Label

        "LineEdit to enter the required value"
        self.LineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(self.LineEdit.sizePolicy().hasHeightForWidth())
        self.LineEdit.setSizePolicy(sizePolicy)
        self.LineEdit.setFont(font)
        self.LineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.LineEdit.setStyleSheet("background-color:white;")
        self.HorizontalLayout.addWidget(self.LineEdit)
        self.SingleControlDict[2] = self.LineEdit
        self.HorizontalLayout.addStretch()

        self.VerticalLayoutXYZ.addLayout(self.HorizontalLayout)