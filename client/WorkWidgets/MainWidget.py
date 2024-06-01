from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.AddStuWidget import AddStuWidget
from WorkWidgets.ShowStuWidget import ShowStuWidget
from WorkWidgets.WidgetComponents import LabelComponent
from WorkWidgets.WidgetComponents import ButtonComponent
from WorkWidgets.WidgetComponents import TabWidget
from SocketClient.SocketClient import SocketClient


class MainWidget(QtWidgets.QWidget):
    def __init__(self, client):
        super().__init__()
        self.setObjectName("main_widget")
        self.client = client

        layout = QtWidgets.QGridLayout()
        header_label = LabelComponent(24, "Student Management System")
        # function_widget = FunctionWidget(self.client)
        # menu_widget = MenuWidget(function_widget.update_widget)
        self.tab_widget = TabWidget(16)
        
        self.tab_widget.add_new_page(AddStuWidget(self.client), "Add")
        self.tab_widget.add_new_page(ShowStuWidget(self.client), "Show")
        
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
            widget.reset_widget()

    def on_tab_clicked(self, idx):
        widget = self.tab_widget.widget(idx)
        if widget.click_event:
            widget.reset_widget()


# class MenuWidget(QtWidgets.QWidget):
#     def __init__(self, update_widget_callback):
#         super().__init__()
#         self.setObjectName("menu_widget")
#         self.update_widget_callback = update_widget_callback

#         layout = QtWidgets.QVBoxLayout()
#         add_button = ButtonComponent("Add student")
#         show_button = ButtonComponent("Show all")
#         # https://medium.com/seaniap/python-lambda-函式-7e86a56f1996
#         add_button.clicked.connect(lambda: self.update_widget_callback("add"))
#         show_button.clicked.connect(lambda: self.update_widget_callback("show"))

#         layout.addWidget(add_button, stretch=1)
#         layout.addWidget(show_button, stretch=1)

#         self.setLayout(layout)


# class FunctionWidget(QtWidgets.QStackedWidget):
#     def __init__(self, client : SocketClient):
#         super().__init__()
#         self.widget_dict = {
#             "add": self.addWidget(AddStuWidget(client)),
#             "show": self.addWidget(ShowStuWidget(client))
#         }
#         self.update_widget("add")
    
#     def update_widget(self, name):
#         self.setCurrentIndex(self.widget_dict[name])
#         current_widget = self.currentWidget()
#         current_widget.load()
