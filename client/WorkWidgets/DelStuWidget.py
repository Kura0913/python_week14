from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, TextEditComponent, ButtonComponent, ComboBoxComponent, MessageBoxComponent
from SocketClient.SocketClient import SocketClient 
from SocketClient.ServiceController import ExecuteConfirmCommand
import json

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self, client:SocketClient):
        super().__init__()
        self.init_selection = "請選擇"
        self.click_event = True
        self.double_click_event = False
        self.setObjectName("del_stu_widget")
        self.client = client
        layout = QtWidgets.QGridLayout()
        
        # set combo box
        self.name_combobox = ComboBoxComponent("name_combobox")
        self.name_combobox.currentIndexChanged.connect(self.check_name_selected)
        self.name_combobox.setEnabled(True)
        # set button
        self.send_button = ButtonComponent("send_button", "Send", 16)
        self.send_button.setIcon(QtGui.QIcon(QtGui.QPixmap("./Icons/send.png")))
        self.send_button.setIconSize(QtCore.QSize(30,30)) 
        self.send_button.setEnabled(True)
        self.send_button.clicked.connect(self.send_action)
        # set message box
        self.msg_box = MessageBoxComponent("msg_box", 16)
        self.msg_box.setWindowTitle("Warning!!")
        self.msg_box.setIcon(self.msg_box.Icon.Warning)
        # set label
        header_label = LabelComponent("header_label", 20, "Delete Student", "Icons/title_del.png")
        name_label = LabelComponent("name_label", 16, "Name", "Icons/label.png")
        name_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.message_label = LabelComponent("message_label", 16, "")
        # set text edit 
        self.student_score_text_edit = TextEditComponent("student_score_text_edit", "", 16)
        self.student_score_text_edit.setReadOnly(True)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_combobox, 1, 1, 1, 1)
        layout.addWidget(self.send_button, 5, 3, 1, 1)
        layout.addWidget(self.message_label, 1, 3, 2, 2)
        layout.addWidget(self.student_score_text_edit, 2, 0, 2, 2)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 4)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 2)
        layout.setRowStretch(2, 2)
        layout.setRowStretch(3, 2)
        layout.setRowStretch(4, 1)
        layout.setRowStretch(5, 2)

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

    # send button clicked event
    def send_action(self):
        if self.name_combobox.currentText() != self.init_selection:
            parameters = {"name":self.name_combobox.currentText()}
            if(self.msg_box.show(f"Are you sure you want to delete :{self.name_combobox.currentText()} all his/her grades??")):
                self.send_command = ExecuteConfirmCommand(self.client, "del", parameters)
                self.send_command.start()
                self.send_command.result_msg.connect(self.send_action_result)
        else:
            self.set_message_text("Please select the name you want to delete", "red")

    # get del execute result
    def send_action_result(self, result):
        result_message = json.loads(result)
        if result_message["status"] == "OK":
            self.set_message_text(f"Delete {self.name_combobox.currentText()}'s sbjects and score save success.", "green", True)
            self.reset_widget()
    def check_name_selected(self):
        if self.name_combobox.currentText() != self.init_selection and self.name_combobox.currentText() != '':
            self.set_score_text_edit_content(self.current_stu_data[self.name_combobox.currentText()]["scores"])
            self.send_button.setEnabled(True)
        else:
            self.send_button.setEnabled(False)
    def set_name_combobox(self, result):
        self.name_combobox.reset_combobox()
        result_message = json.loads(result)
        if result_message['status'] == "OK":
            self.current_stu_data = result_message["parameters"]
            for name, _ in result_message["parameters"].items():
                self.name_combobox.add_item(name)
    # set student score text edit content
    def set_score_text_edit_content(self, parameters):
        content = f"Name:{self.name_combobox.currentText()}\n"
        for subject, score in parameters.items():
            content += f"   {subject} : {score}\n"
        self.student_score_text_edit.setText(content)

    def reset_widget(self, message_label_reset=False):
        self.message_label.setText("")
        self.student_score_text_edit.setText("")
        self.send_command = ExecuteConfirmCommand(self.client, "show", dict())
        self.send_command.start()
        self.send_command.result_msg.connect(self.set_name_combobox)
        if message_label_reset: self.message_label.setText("")

    def set_message_text(self, message, color, reset=False):
        def reset_message_text():
           self.message_label.setText("") 
        self.message_label.set_color(color)
        self.message_label.setText(message)
        if reset:
            QtCore.QTimer.singleShot(2000, reset_message_text)

    def load(self):
        print("del widget")
        self.reset_widget()

