# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ass2ultrastar.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(580, 341)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.artistLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.artistLineEdit.setObjectName("artistLineEdit")
        self.gridLayout.addWidget(self.artistLineEdit, 0, 1, 1, 1)
        self.editionLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.editionLineEdit.setObjectName("editionLineEdit")
        self.gridLayout.addWidget(self.editionLineEdit, 3, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)
        self.gapLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.gapLineEdit.setEnabled(False)
        self.gapLineEdit.setObjectName("gapLineEdit")
        self.gridLayout.addWidget(self.gapLineEdit, 5, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 0, 1, 1)
        self.titleLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.titleLineEdit.setObjectName("titleLineEdit")
        self.gridLayout.addWidget(self.titleLineEdit, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 4, 2, 1, 1)
        self.pitchPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pitchPushButton.setObjectName("pitchPushButton")
        self.gridLayout.addWidget(self.pitchPushButton, 4, 3, 1, 1)
        self.coverPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.coverPushButton.setObjectName("coverPushButton")
        self.gridLayout.addWidget(self.coverPushButton, 1, 1, 1, 1)
        self.backgroundPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.backgroundPushButton.setObjectName("backgroundPushButton")
        self.gridLayout.addWidget(self.backgroundPushButton, 1, 3, 1, 1)
        self.mp3PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.mp3PushButton.setObjectName("mp3PushButton")
        self.gridLayout.addWidget(self.mp3PushButton, 2, 1, 1, 1)
        self.videoPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.videoPushButton.setObjectName("videoPushButton")
        self.gridLayout.addWidget(self.videoPushButton, 2, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 6, 0, 1, 1)
        self.bpmLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.bpmLineEdit.setEnabled(False)
        self.bpmLineEdit.setObjectName("bpmLineEdit")
        self.gridLayout.addWidget(self.bpmLineEdit, 6, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 5, 2, 1, 1)
        self.videoGAPdoubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.videoGAPdoubleSpinBox.setObjectName("videoGAPdoubleSpinBox")
        self.gridLayout.addWidget(self.videoGAPdoubleSpinBox, 5, 3, 1, 1)
        self.ASSFilePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.ASSFilePushButton.setObjectName("ASSFilePushButton")
        self.gridLayout.addWidget(self.ASSFilePushButton, 6, 3, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 6, 2, 1, 1)
        self.genreComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.genreComboBox.setEditable(True)
        self.genreComboBox.setObjectName("genreComboBox")
        self.gridLayout.addWidget(self.genreComboBox, 3, 1, 1, 1)
        self.languageComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.languageComboBox.setEditable(True)
        self.languageComboBox.setCurrentText("")
        self.languageComboBox.setObjectName("languageComboBox")
        self.gridLayout.addWidget(self.languageComboBox, 4, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.u2aPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.u2aPushButton.setObjectName("u2aPushButton")
        self.horizontalLayout.addWidget(self.u2aPushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.vaPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.vaPushButton.setObjectName("vaPushButton")
        self.horizontalLayout.addWidget(self.vaPushButton)
        self.a2uPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.a2uPushButton.setObjectName("a2uPushButton")
        self.horizontalLayout.addWidget(self.a2uPushButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 580, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpenASS = QtWidgets.QAction(MainWindow)
        self.actionOpenASS.setObjectName("actionOpenASS")
        self.actionOpenUltrastar = QtWidgets.QAction(MainWindow)
        self.actionOpenUltrastar.setObjectName("actionOpenUltrastar")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionCreate_Aubio = QtWidgets.QAction(MainWindow)
        self.actionCreate_Aubio.setObjectName("actionCreate_Aubio")
        self.actionCreate_Praat = QtWidgets.QAction(MainWindow)
        self.actionCreate_Praat.setObjectName("actionCreate_Praat")
        self.menuFile.addAction(self.actionOpenASS)
        self.menuFile.addAction(self.actionOpenUltrastar)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASS 2 Ultrastar"))
        self.label_5.setText(_translate("MainWindow", "MP3"))
        self.label_6.setText(_translate("MainWindow", "VIDEO"))
        self.label.setText(_translate("MainWindow", "Artist"))
        self.label_9.setText(_translate("MainWindow", "GAP"))
        self.label_8.setText(_translate("MainWindow", "Edition"))
        self.label_4.setText(_translate("MainWindow", "Background"))
        self.label_2.setText(_translate("MainWindow", "Title"))
        self.label_7.setText(_translate("MainWindow", "Genre"))
        self.label_3.setText(_translate("MainWindow", "Cover"))
        self.label_11.setText(_translate("MainWindow", "Language"))
        self.label_12.setText(_translate("MainWindow", "Pitch File"))
        self.pitchPushButton.setText(_translate("MainWindow", "Pitch File"))
        self.coverPushButton.setText(_translate("MainWindow", "Cover File"))
        self.backgroundPushButton.setText(_translate("MainWindow", "Background File"))
        self.mp3PushButton.setText(_translate("MainWindow", "MP3 File"))
        self.videoPushButton.setText(_translate("MainWindow", "Video File"))
        self.label_10.setText(_translate("MainWindow", "BPM"))
        self.label_13.setText(_translate("MainWindow", "Video Gap"))
        self.ASSFilePushButton.setText(_translate("MainWindow", "ASSFile"))
        self.label_14.setText(_translate("MainWindow", "ASS"))
        self.u2aPushButton.setText(_translate("MainWindow", "Ultrastar2ASS"))
        self.vaPushButton.setText(_translate("MainWindow", "Audio from Video"))
        self.a2uPushButton.setText(_translate("MainWindow", "ASS2Ultrastar"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpenASS.setText(_translate("MainWindow", "Open ASS"))
        self.actionOpenUltrastar.setText(_translate("MainWindow", "Open Ultrastar"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionCreate_Aubio.setText(_translate("MainWindow", "Create Aubio"))
        self.actionCreate_Praat.setText(_translate("MainWindow", "Create Praat"))

