from PyQt5 import QtWidgets, QtCore
from modules.visualization import config_window_ui
from PyQt5.QtWidgets import QTableWidgetItem
from modules.configuration import config


class ConfigWindow(QtWidgets.QDialog, config_window_ui.Ui_Dialog):
    def __init__(self, *args, **kwargs):
        super(ConfigWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.btn_save.clicked.connect(self.save_config)
        self.btn_createConfig.clicked.connect(self.create_config)
        self.btn_selectConfig.clicked.connect(self.select_config)
        self.btn_deleteConfig.clicked.connect(self.delete_config)
        self.tbl_existingConfs.cellClicked.connect(lambda row, col: self.select_config_row(row, col))
        self.tbl_editParams.cellClicked.connect(lambda row, col: self.parameter_clicked(row, col))

        self.locked = False
        self.selected_conf = -1
        self.refresh()

    def create_config(self):
        self.locked = True
        self.set_edit_state(True)
        params = config.get_parameters()
        for param in params:
            rowPosition = self.tbl_editParams.rowCount()
            self.tbl_editParams.insertRow(rowPosition)
            self.tbl_editParams.setItem(rowPosition, 0, QTableWidgetItem(param.parameter_name))

    def select_config_row(self, row, col):
        config_id = int(self.tbl_existingConfs.item(row, 0).text())
        self.selected_conf = config_id
        self.refresh()

    def save_config(self):
        conf = {}
        for row in range(self.tbl_editParams.rowCount()):
            conf[self.tbl_editParams.item(row, 0).text()] = self.tbl_editParams.item(row, 1).text()
        config.create_configuration(conf)
        self.locked = False
        self.set_edit_state(False)
        self.refresh()

    def select_config(self):
        config.select_config(int(self.selected_conf))
        self.refresh()

    def toggle_elements(self, state, elements):
        for elem in elements:
            elem.setEnabled(state)

    def delete_config(self):
        config.delete_config(self.selected_conf)
        self.refresh()

    def update_selected_info(self):
        items = config.get_config(self.selected_conf)
        entries = []
        for item in items:
            entries.append(f"{item}: {items[item]}")
        self.te_infobox.setPlainText("\n".join(entries))

    def parameter_clicked(self, row, col):
        params = config.get_parameters()
        self.te_infobox.setPlainText(params[row].description)

    def refresh(self):
        self.update_selected_info()
        for i in range(self.tbl_existingConfs.rowCount() - 1, -1, -1):
            self.tbl_existingConfs.removeRow(i)
        cfgs = config.get_configs()
        for conf in cfgs:
            row_position = self.tbl_existingConfs.rowCount()
            config_id_item = QTableWidgetItem(str(conf.configuration_id))
            config_name_item = QTableWidgetItem(str(conf.name))
            config_selected_item = QTableWidgetItem(str(conf.is_active))
            config_id_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            config_name_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            config_selected_item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tbl_existingConfs.insertRow(row_position)
            self.tbl_existingConfs.setItem(row_position, 0, config_id_item)
            self.tbl_existingConfs.setItem(row_position, 1, config_name_item)
            self.tbl_existingConfs.setItem(row_position, 2, config_selected_item)

    def set_edit_state(self, state):
        self.toggle_elements(
            not state,
            [self.btn_createConfig,
             self.btn_deleteConfig,
             self.btn_editConfig,
             self.btn_selectConfig]
        )
        self.toggle_elements(
            state,
            [self.btn_cancel, self.btn_save]
        )
