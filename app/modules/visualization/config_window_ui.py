# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\configuration_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(838, 898)
        self.tbl_editParams = QtWidgets.QTableWidget(Dialog)
        self.tbl_editParams.setGeometry(QtCore.QRect(30, 430, 491, 331))
        self.tbl_editParams.setShowGrid(True)
        self.tbl_editParams.setObjectName("tbl_editParams")
        self.tbl_editParams.setColumnCount(2)
        self.tbl_editParams.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_editParams.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_editParams.setHorizontalHeaderItem(1, item)
        self.tbl_editParams.horizontalHeader().setVisible(True)
        self.tbl_editParams.horizontalHeader().setCascadingSectionResizes(True)
        self.tbl_editParams.horizontalHeader().setDefaultSectionSize(245)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 15, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(30, 380, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.btn_createConfig = QtWidgets.QPushButton(Dialog)
        self.btn_createConfig.setGeometry(QtCore.QRect(60, 790, 191, 28))
        self.btn_createConfig.setObjectName("btn_createConfig")
        self.btn_editConfig = QtWidgets.QPushButton(Dialog)
        self.btn_editConfig.setGeometry(QtCore.QRect(300, 790, 191, 28))
        self.btn_editConfig.setObjectName("btn_editConfig")
        self.btn_deleteConfig = QtWidgets.QPushButton(Dialog)
        self.btn_deleteConfig.setGeometry(QtCore.QRect(60, 830, 191, 28))
        self.btn_deleteConfig.setObjectName("btn_deleteConfig")
        self.btn_selectConfig = QtWidgets.QPushButton(Dialog)
        self.btn_selectConfig.setGeometry(QtCore.QRect(300, 830, 191, 28))
        self.btn_selectConfig.setObjectName("btn_selectConfig")
        self.te_infobox = QtWidgets.QPlainTextEdit(Dialog)
        self.te_infobox.setEnabled(True)
        self.te_infobox.setGeometry(QtCore.QRect(540, 60, 281, 701))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.te_infobox.setFont(font)
        self.te_infobox.setStyleSheet("background: rgb(255, 255, 255)")
        self.te_infobox.setObjectName("te_infobox")
        self.btn_save = QtWidgets.QPushButton(Dialog)
        self.btn_save.setEnabled(False)
        self.btn_save.setGeometry(QtCore.QRect(620, 790, 121, 28))
        self.btn_save.setObjectName("btn_save")
        self.btn_cancel = QtWidgets.QPushButton(Dialog)
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.setGeometry(QtCore.QRect(620, 830, 121, 28))
        self.btn_cancel.setObjectName("btn_cancel")
        self.tbl_existingConfs = QtWidgets.QTableWidget(Dialog)
        self.tbl_existingConfs.setEnabled(True)
        self.tbl_existingConfs.setGeometry(QtCore.QRect(30, 60, 491, 311))
        self.tbl_existingConfs.setShowGrid(True)
        self.tbl_existingConfs.setObjectName("tbl_existingConfs")
        self.tbl_existingConfs.setColumnCount(3)
        self.tbl_existingConfs.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_existingConfs.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_existingConfs.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_existingConfs.setHorizontalHeaderItem(2, item)
        self.tbl_existingConfs.horizontalHeader().setVisible(True)
        self.tbl_existingConfs.horizontalHeader().setCascadingSectionResizes(True)
        self.tbl_existingConfs.horizontalHeader().setDefaultSectionSize(155)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.tbl_editParams.setSortingEnabled(False)
        item = self.tbl_editParams.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Имя параметра"))
        item = self.tbl_editParams.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Значение"))
        self.label.setText(_translate("Dialog", "Созданные конфигурации"))
        self.label_2.setText(_translate("Dialog", "Редактирование конфигурации"))
        self.btn_createConfig.setText(_translate("Dialog", "Создать конфигурацию"))
        self.btn_editConfig.setText(_translate("Dialog", "Редактировать конфигурацию"))
        self.btn_deleteConfig.setText(_translate("Dialog", "Удалить конфигурацию"))
        self.btn_selectConfig.setText(_translate("Dialog", "Выбрать конфигурацию"))
        self.btn_save.setText(_translate("Dialog", "Сохранить"))
        self.btn_cancel.setText(_translate("Dialog", "Отмена"))
        self.tbl_existingConfs.setSortingEnabled(False)
        item = self.tbl_existingConfs.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Идентификатор"))
        item = self.tbl_existingConfs.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Название"))
        item = self.tbl_existingConfs.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Выбран"))
