from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import pyqtSignal

class LabelComponent(QtWidgets.QLabel):
    def __init__(self, object_name:str, font_size, content, background_path=""):
        super().__init__()
        self.background_path = background_path
        self.setWordWrap(True)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.setObjectName(object_name)
        self.setFont(QtGui.QFont("Consolas", font_size))
        self.setText(content)
        self.set_color()
    def set_color(self, color="black"):
        self.setStyleSheet(f"color: {color};")
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap(self.background_path)
        scaled_pixmap = pixmap.scaled(self.size(), QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        x_offset = (self.width() - scaled_pixmap.width()) // 2
        y_offset = (self.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(0, 0, scaled_pixmap)
        super().paintEvent(event)

class LineEditComponent(QtWidgets.QLineEdit):
    def __init__(self, object_name:str, default_content="", length=10, width=200, font_size=16):
        super().__init__()
        self.setObjectName(object_name)
        self.setMaxLength(length)
        self.setText(default_content)
        self.setMinimumHeight(30)
        self.setMaximumWidth(width)
        self.setFont(QtGui.QFont("Consolas", font_size))
        self.setStyleSheet("""
                QLineEdit:enabled{
                    border:3px solid black;
                    border-radius: 10px;
                    background-color: #f0f0f0;
                    color: black;
                }
                QLineEdit:hover{
                    border:3px solid #CE0000;
                    border-radius: 10px;
                    background-color: #f0f0f0;
                    color: black;
                }
                QLineEdit:disabled{
                    border:3px solid black;
                    border-radius: 10px;
                    background-color: #4F4F4F;
                    color: white;
                }   
            """)

class ButtonComponent(QtWidgets.QPushButton):
    def __init__(self, object_name:str, text, font_size=16):
        super().__init__()
        self.setObjectName(object_name)
        self.setText(text)
        self.setFont(QtGui.QFont("Consolas", font_size))
        self.setStyleSheet("""
                QPushButton:enabled{
                    background:white;
                    border:2px solid #000;
                    border-radius: 15px;
                    color:black;
                    font-weight:normal;
                }
                QPushButton:hover{
                    border:5px solid #CE0000;
                    font-weight:bold;
                }
                QPushButton:disabled{
                    background:#4F4F4F;
                    border:2px solid #000;
                    border-radius: 15px;
                    color:white;
                }
            """)


class TextEditComponent(QtWidgets.QTextEdit):
    def __init__(self, object_name:str, text, font_size=16):
        super().__init__()
        self.setObjectName(object_name)
        self.setText(text)
        self.setFont(QtGui.QFont("微軟正黑體", font_size))
        self.setStyleSheet("""
                QTextEdit{
                    border:5px solid black;
                    border-radius: 10px;
                    font-weight:bold;
                    color:white;
                }
            """)
        

class TabWidgetComponent(QtWidgets.QTabWidget):
    def __init__(self, object_name:str, font_size=16):
        super().__init__()
        self.setObjectName(object_name)
        self.setFont(QtGui.QFont("Consolas", font_size))
        self.setStyleSheet("""
                QTabWidget{
                    height:60px;
                }
                QTabBar::tab:selected{
                    background: #000;
                    border:3px solid #CE0000;
                    border-top-right-radius: 10px;
                    border-top-left-radius: 10px;
                    font-weight:bold;
                }
                QTabBar::tab:hover{
                    background: #000;
                    border:3px solid #46A3FF;
                    border-radius: 5px;
                }
            """)

    def add_new_pages(self, widget_dict):
        for widget_name, widget in widget_dict.items():
            self.addTab(widget, widget_name)

class ComboBoxComponent(QtWidgets.QComboBox):
    def __init__(self, object_name:str, font_size=12):
        super().__init__()
        self.setObjectName(object_name)
        self.setFont(QtGui.QFont("Consolas", font_size))
        self.add_item("請選擇")
        self.setStyleSheet("""
                QComboBox:enabled{
                    background:white;
                    border:4px solid #000;
                    border-radius:10px;
                    color:black;
                    font-weight:normal;
                }
                QComboBox:hover{
                    border:4px solid #CE0000;
                    border-radius:10px;
                }
                QComboBox:drop-down{
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width:20px;
                    border-radius: 10px;
                }
                QComboBox:down-arrow{
                    border-image: url(Icons/down-arrow.png);
                    border-radius: 10px;
                    width:10px;
                    height:10px;
                }
                QComboBox:disabled{
                    background:#4F4F4F;
                    border:2px solid #000;
                    border-radius: 10px;
                    color:white;
                }
            """)
    def add_item(self, item_text):
        self.addItem(item_text)
    def reset_combobox(self):
        self.clear()
        self.add_item("請選擇")

class MessageBoxComponent(QtWidgets.QMessageBox):
    def __init__(self, object_name:str, font_size=16):
        super().__init__()
        self.setObjectName(object_name)
        self.setFont(QtGui.QFont("Consolas", font_size))        
        
    def show(self, text):
        self.setText(text)
        self.Icon.Warning
        self.setStandardButtons(self.StandardButton.Cancel | self.StandardButton.Ok)
        self.setDefaultButton(self.StandardButton.Cancel)
        ret = self.exec()
        if ret == QtWidgets.QMessageBox.StandardButton.Ok:
            return True
        else:
            return False