from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, TextEditComponent
from SocketClient.ServiceController import ExecuteConfirmCommand
from SocketClient.SocketClient import SocketClient 
import json

class ShowStuWidget(QtWidgets.QWidget):
    def __init__(self, client : SocketClient):
        super().__init__()
        self.click_event = True
        self.double_click_event = False
        self.setObjectName("show_stu_widget")
        self.client = client
        layout = QtWidgets.QVBoxLayout()

        header_label = LabelComponent("header_label", 20, "Show Student", "Icons/title_show.png")

        self.students_list_text_edit = TextEditComponent("students_list_text_edit", "", 16)
        self.students_list_text_edit.setReadOnly(True)


        layout.addWidget(header_label, stretch=1)
        layout.addWidget(self.students_list_text_edit, stretch=9)

        self.setLayout(layout)

        self.load()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        pixmap = QtGui.QPixmap("Icons/bg1.png")
        scaled_pixmap = pixmap.scaled(self.size(), QtCore.Qt.AspectRatioMode.IgnoreAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        x_offset = (self.width() - scaled_pixmap.width()) // 2
        y_offset = (self.height() - scaled_pixmap.height()) // 2
        painter.drawPixmap(x_offset, y_offset, scaled_pixmap)
        super().paintEvent(event)

    def show_all_result(self, result):
        result_message = json.loads(result)
        if result_message['status'] == "OK":
            format_message = "====Student List====\n"
            for name, subjects_and_scores in result_message["parameters"].items():
                format_message = format_message + f"Name: {name}\n"
                for subject, score in subjects_and_scores['scores'].items():
                    format_message = format_message + f"  subject: {subject}, score:{score}\n"
                format_message = format_message + '\n'
                    
            self.students_list_text_edit.setText(format_message)

    def reset_widget(self, message_label_reset=False):
        self.send_command = ExecuteConfirmCommand(self.client, "show", dict())
        self.send_command.start()
        self.send_command.result_msg.connect(self.show_all_result)
        

    def load(self):
        print("show widget")
        self.reset_widget()
        
