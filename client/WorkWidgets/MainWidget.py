from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import TabWidgetComponent
from SocketClient.SocketClient import SocketClient



class MainWidget(QtWidgets.QWidget):
    def __init__(self, client : SocketClient):
        super().__init__()
        self.setObjectName("main_widget")
        self.client = client
        self.page_dict = {
            "Add": AddStuWidget(self.client),
            "Show": ShowStuWidget(self.client),
            "Delete": DelStuWidget(self.client),
            "Modify": ModifyStuWidget(self.client)
        }

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent("header_label", 24, "Student Management System", "Icons/title.png")
        self.tab_widget = TabWidgetComponent("tab_widget", 16)
        
        self.tab_widget.add_new_pages(self.page_dict)        
        
        self.tab_widget.tabBarClicked.connect(self.on_tab_clicked)
        self.tab_widget.tabBarDoubleClicked.connect(self.on_tab_double_clicked)
        self.tab_widget.setMaximumHeight(330)

        layout.addWidget(header_label, 0, 0, 1, 1)
        layout.addWidget(self.tab_widget, 1, 0, 1, 1)
        
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 6)        

        self.setLayout(layout)


    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("Icons/main_bg.jpg")
        scaled_pixmap = pixmap.scaled(self.size(), QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        x_offset = (self.width() - scaled_pixmap.width()) // 2
        y_offset = (self.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
        super().paintEvent(event)

    def on_tab_double_clicked(self, idx):
        widget = self.tab_widget.widget(idx)
        if widget.double_click_event:
            widget.reset_widget(True)

    def on_tab_clicked(self, idx):
        widget = self.tab_widget.widget(idx)
        if widget.click_event:
            widget.reset_widget(True)

