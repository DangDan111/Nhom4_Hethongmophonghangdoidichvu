from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTableWidgetItem


def load_ui(ui_path):
    ui_file = QFile(str(ui_path))
    if not ui_file.open(QFile.ReadOnly):
        raise FileNotFoundError(f"Không mở được file giao diện: {ui_path}")
    try:
        widget = QUiLoader().load(ui_file)
    finally:
        ui_file.close()
    if widget is None:
        raise RuntimeError(f"Không load được giao diện: {ui_path}")
    return widget


def find_required(parent, widget_type, object_name):
    widget = parent.findChild(widget_type, object_name)
    if widget is None:
        raise RuntimeError(f"Thiếu control {object_name} trong file .ui")
    return widget


def setup_table(table, headers):
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.verticalHeader().setVisible(False)
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)


def fill_table(table, rows):
    table.setRowCount(len(rows))
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
