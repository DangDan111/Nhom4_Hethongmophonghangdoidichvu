from PySide6.QtCore import QDir, QFile, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidgetItem,
    QVBoxLayout,
)


def load_ui(ui_path):
    ui_file = QFile(str(ui_path))
    if not ui_file.open(QFile.ReadOnly):
        raise FileNotFoundError(f"Không mở được file giao diện: {ui_path}")
    current_dir = QDir.currentPath()
    try:
        QDir.setCurrent(str(ui_path.parent))
        widget = QUiLoader().load(ui_file)
    finally:
        QDir.setCurrent(current_dir)
        ui_file.close()
    if widget is None:
        raise RuntimeError(f"Không load được giao diện: {ui_path}")
    return widget


def find_required(parent, widget_type, object_name):
    widget = parent.findChild(widget_type, object_name)
    if widget is None:
        raise RuntimeError(f"Thiếu control {object_name} trong file .ui")
    return widget


def setup_table(table, headers, column_widths=None):
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(headers)
    header = table.horizontalHeader()
    header.setDefaultAlignment(Qt.AlignCenter)
    header.setMinimumHeight(40)
    if column_widths is None and table.objectName() == "tblQuay":
        column_widths = [66, 78, 112, 180]
    if column_widths is None:
        header.setSectionResizeMode(QHeaderView.Stretch)
    else:
        for column_index, width in enumerate(column_widths):
            header.setSectionResizeMode(column_index, QHeaderView.Fixed)
            table.setColumnWidth(column_index, width)
        header.setSectionResizeMode(len(headers) - 1, QHeaderView.Stretch)
    table.verticalHeader().setVisible(False)
    table.verticalHeader().setDefaultSectionSize(36)
    if table.objectName() == "tblQuay":
        table.verticalHeader().setDefaultSectionSize(30)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    table.setAlternatingRowColors(True)
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)


def fill_table(table, rows):
    table.clearSpans()
    if len(rows) == 0:
        table.setRowCount(1)
        item = QTableWidgetItem("Chưa có dữ liệu")
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(0, 0, item)
        if table.columnCount() > 1:
            table.setSpan(0, 0, 1, table.columnCount())
        return

    table.setRowCount(len(rows))
    for row_index, row in enumerate(rows):
        for col_index, value in enumerate(row):
            item = QTableWidgetItem(str(value))
            item.setTextAlignment(Qt.AlignCenter)
            table.setItem(row_index, col_index, item)


def confirm_logout(parent):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Xác nhận đăng xuất")
    dialog.setModal(True)
    dialog.setFixedSize(560, 280)
    dialog.setStyleSheet("""
        QDialog { background: #ffffff; font-family: 'Segoe UI'; }
        QLabel#title { color: #111827; font-size: 20px; font-weight: 700; }
        QLabel#message { color: #1f2937; font-size: 16px; }
        QPushButton { min-width: 140px; min-height: 46px; border-radius: 7px; font-size: 15px; font-weight: 600; }
        QPushButton#cancelButton { background: #eef2f7; color: #111827; border: 1px solid #cbd5e1; }
        QPushButton#cancelButton:hover { background: #e2e8f0; }
        QPushButton#logoutButton { background: #2563eb; color: white; border: 1px solid #1d4ed8; }
        QPushButton#logoutButton:hover { background: #1d4ed8; }
    """)

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(36, 32, 36, 30)
    layout.setSpacing(24)

    title = QLabel("Xác nhận đăng xuất")
    title.setObjectName("title")
    title.setAlignment(Qt.AlignCenter)

    message = QLabel("Bạn có muốn đăng xuất không?")
    message.setObjectName("message")
    message.setAlignment(Qt.AlignCenter)

    button_layout = QHBoxLayout()
    button_layout.setSpacing(16)
    button_layout.addStretch()

    cancel_button = QPushButton("Hủy")
    cancel_button.setObjectName("cancelButton")
    logout_button = QPushButton("Đăng xuất")
    logout_button.setObjectName("logoutButton")

    cancel_button.clicked.connect(dialog.reject)
    logout_button.clicked.connect(dialog.accept)

    button_layout.addWidget(cancel_button)
    button_layout.addWidget(logout_button)
    button_layout.addStretch()

    layout.addStretch()
    layout.addWidget(title)
    layout.addWidget(message)
    layout.addLayout(button_layout)
    layout.addStretch()

    cancel_button.setDefault(True)
    return dialog.exec() == QDialog.Accepted
