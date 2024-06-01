from PyQt6 import QtWidgets, QtCore, QtGui


class LabelComponent(QtWidgets.QLabel):
    def __init__(self, font_size, content):
        super().__init__()

        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setText(content)
    def set_color(self, color="black"):
        self.setStyleSheet(f"color: {color};")

class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))


class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

class TextEditComponent(QtWidgets.QTextEdit):
    def __init__(self, text, font_size=16):
        super().__init__()
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, font_size=16):
        super().__init__()
        self.setFont(QtGui.QFont("微軟正黑體", font_size))

    def add_new_page(self, widget, widget_name):
        self.addTab(widget, widget_name)