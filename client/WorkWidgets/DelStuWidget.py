from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, ButtonComponent, ComboBoxComponent, MessageBoxComponent
from SocketClient.SocketClient import SocketClient 
from SocketClient.ServiceController import ExecuteConfirmCommand
import json

class DelStuWidget(QtWidgets.QWidget):
    def __init__(self, client:SocketClient):
        super().__init__()
        self.click_event = True
        self.double_click_event = False
        self.setObjectName("del_stu_widget")
        self.client = client
        layout = QtWidgets.QGridLayout()
        
        # set combo box
        self.name_combobox = ComboBoxComponent()
        # set button
        self.send_button = ButtonComponent("Send", 16)
        self.send_button.setEnabled(True)
        self.send_button.clicked.connect(self.send_action)
        # set message box
        self.msg_box = MessageBoxComponent(16)
        # set label
        header_label = LabelComponent(20, "Delete Student")
        name_label = LabelComponent(16, "Name: ")
        self.message_label = LabelComponent(16, "")

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_combobox, 1, 1, 1, 1)
        layout.addWidget(self.send_button, 5, 3, 1, 1)
        layout.addWidget(self.message_label, 1, 3, 2, 2)

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

    # send button clicked event
    def send_action(self):
        if self.name_combobox.currentText() != "請選擇":
            parameters = {"name":self.name_combobox.currentText()}
            if(self.msg_box.show(f"確定要刪除 {self.name_combobox.currentText()} 嗎?")):
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

    def set_name_combobox(self, result):
        self.name_combobox.reset_combobox()
        result_message = json.loads(result)
        if result_message['status'] == "OK":
            for name, _ in result_message["parameters"].items():
                self.name_combobox.add_item(name)

    def reset_widget(self, message_label_reset=False):
        self.message_label.setText("")
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

