from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.DelStuWidget import DelStuWidget
from WorkWidgets.ModifyStuWidget import ModifyStuWidget
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent
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
        header_label = LabelComponent(24, "Student Management System")
        self.tab_widget = TabWidgetComponent(16)
        
        self.tab_widget.add_new_pages(self.page_dict)        
        
        self.tab_widget.tabBarClicked.connect(self.on_tab_clicked)
        self.tab_widget.tabBarDoubleClicked.connect(self.on_tab_double_clicked)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(self.tab_widget, 1, 0, 1, 1)
        
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 6)

        self.setLayout(layout)

        

    def on_tab_double_clicked(self, idx):
        widget = self.tab_widget.widget(idx)
        if widget.double_click_event:
            widget.reset_widget(True)

    def on_tab_clicked(self, idx):
        widget = self.tab_widget.widget(idx)
        if widget.click_event:
            widget.reset_widget(True)

