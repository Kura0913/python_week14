from PyQt6 import QtWidgets, QtGui, QtCore
from WorkWidgets.WidgetComponents import LabelComponent, LineEditComponent, ButtonComponent, ComboBoxComponent, TextEditComponent
from SocketClient.SocketClient import SocketClient 
from SocketClient.ServiceController import ExecuteConfirmCommand
import json

class ModifyStuWidget(QtWidgets.QWidget):
    def __init__(self, client:SocketClient):
        super().__init__()
        self.click_event = True
        self.double_click_event = False
        self.setObjectName("modify_stu_widget")
        self.client = client
        layout = QtWidgets.QGridLayout()
        # init content
        self.init_selection = "請選擇"
        self.manual_entry_content = "add new..."
        # validator
        int_validator = QtGui.QIntValidator(0, 100)

        # set label
        header_label = LabelComponent(20, "Modify Student")
        name_label = LabelComponent(16, "Name: ")
        subject_label = LabelComponent(16, "Subject:")
        score_label = LabelComponent(16, "Score:")
        self.message_label = LabelComponent(16, "")

        # set combo box
        self.name_combobox = ComboBoxComponent()
        self.name_combobox.currentIndexChanged.connect(self.check_name_selected)
        self.subject_combobox = ComboBoxComponent()
        self.subject_combobox.currentIndexChanged.connect(self.check_subject_selected)
        # set button
        self.send_button = ButtonComponent("Send", 16)
        self.send_button.setEnabled(False)
        self.send_button.clicked.connect(self.send_action)
        # editor label
        self.subject_editor_label = LineEditComponent("Subject")
        self.subject_editor_label.mousePressEvent = self.clear_subject_editor_content
        self.subject_editor_label.textChanged.connect(self.subject_editor_text_changed)
        self.subject_editor_label.setEnabled(False)

        self.score_editor_label = LineEditComponent("")
        self.score_editor_label.setValidator(int_validator)
        self.score_editor_label.setEnabled(False)

        self.student_score_text_edit = TextEditComponent("", 16)
        self.student_score_text_edit.setReadOnly(True)

        layout.addWidget(header_label, 0, 0, 1, 2)
        layout.addWidget(name_label, 1, 0, 1, 1)
        layout.addWidget(self.name_combobox, 1, 1, 1, 1)
        layout.addWidget(self.message_label, 1, 3, 2, 2)
        layout.addWidget(subject_label, 2, 0, 1, 1)
        layout.addWidget(self.subject_combobox, 2, 1, 1, 1)
        layout.addWidget(self.subject_editor_label, 2, 2, 1, 1)
        layout.addWidget(score_label, 3, 0, 1, 1)
        layout.addWidget(self.score_editor_label, 3, 1, 1, 1)
        layout.addWidget(self.student_score_text_edit, 4, 0, 2, 2)

        
        layout.addWidget(self.send_button, 5, 3, 1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 3)
        layout.setColumnStretch(3, 3)
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
        if self.name_combobox.currentText() != self.init_selection:
            parameters = {"name":self.name_combobox.currentText()}
            if self.score_editor_label.text() != "":
                if self.subject_combobox.currentText() != self.init_selection:
                    if self.subject_combobox.currentText() != self.manual_entry_content:
                        parameters["scores"] = {self.subject_combobox.currentText() : self.score_editor_label.text()}
                    else:
                        parameters["scores"] = {self.subject_editor_label.text() : self.score_editor_label.text()}
                    self.send_command = ExecuteConfirmCommand(self.client, "modify", parameters)
                    self.send_command.start()
                    self.send_command.result_msg.connect(self.send_action_result)
                    
                else:
                    self.set_message_text(f"Please select the subject you want to modify for {self.name_combobox.currentText()}.", "red")
            else:
                self.set_message_text(f"Please input the score.", "red")
        else:
            self.set_message_text(f"Please select the student you want to modify.", "red")

    def send_action_result(self, result):
        result_message = json.loads(result)
        if result_message["status"] == "OK":
            self.set_message_text(f"Modify {self.name_combobox.currentText()}'s score success.", "green", True)
            self.reset_widget()
            
    
    # get current data in db
    def get_current_data(self, result):
        result_message = json.loads(result)
        if result_message['status'] == "OK":
            self.current_stu_data = result_message["parameters"]
            self.set_name_combobox(self.current_stu_data)

    # set name combo box
    def set_name_combobox(self, parameters):
        self.name_combobox.reset_combobox()
        for name, _ in parameters.items():
                self.name_combobox.add_item(name)

    # set subject combo box
    def set_subject_combobox(self, parameters):
        self.subject_combobox.reset_combobox()
        for subject, _ in parameters.items():
                self.subject_combobox.add_item(subject)
        self.subject_combobox.add_item(self.manual_entry_content)

    def clear_subject_editor_content(self, event):
        self.subject_editor_label.clear()

    # subject editor label text changed event
    def subject_editor_text_changed(self, text):
        self.subject_editor_label.setText(text)

        if self.subject_combobox.currentText() == self.manual_entry_content and (text == "Subject" or text == ""):
            self.send_button.setEnabled(False)
            self.score_editor_label.setEnabled(False)
        else:
            self.send_button.setEnabled(True)
            self.score_editor_label.setEnabled(True)

    # check name combobox selected
    def check_name_selected(self):
        if self.name_combobox.currentText() != self.init_selection and self.name_combobox.currentText() != '':
            self.subject_combobox.setEnabled(True)
            self.set_subject_combobox(self.current_stu_data[self.name_combobox.currentText()]["scores"])
            self.set_score_text_edit_content(self.current_stu_data[self.name_combobox.currentText()]["scores"])
        else:
            self.subject_combobox.reset_combobox()
            self.subject_combobox.setEnabled(False)
            self.score_editor_label.setEnabled(False)

    # check subject combobox selected
    def check_subject_selected(self):
        if self.subject_combobox.currentText() == self.manual_entry_content:
            self.subject_editor_label.setEnabled(True)
            self.score_editor_label.setEnabled(False)
            self.send_button.setEnabled(False)
        elif self.subject_combobox.currentText() == self.init_selection:
            self.subject_editor_label.setEnabled(False)
            self.score_editor_label.setEnabled(False)
            self.send_button.setEnabled(False)
        else:
            self.subject_editor_label.setEnabled(False)
            self.score_editor_label.setEnabled(True)
            self.send_button.setEnabled(True)

    # set student score text edit content
    def set_score_text_edit_content(self, parameters):
        content = f"{self.name_combobox.currentText()}\n"
        for subject, score in parameters.items():
            content += f"   {subject} : {score}\n"
        self.student_score_text_edit.setText(content)

    def reset_widget(self, message_label_reset=False):
        self.score_editor_label.setText("")
        self.subject_editor_label.setText("Subject")
        self.student_score_text_edit.setText("")
        self.send_command = ExecuteConfirmCommand(self.client, "show", dict())
        self.send_command.start()
        self.send_command.result_msg.connect(self.get_current_data)
        if message_label_reset: self.message_label.setText("")

    def set_message_text(self, message, color, reset=False):
        def reset_message_text():
           self.message_label.setText("") 
        self.message_label.set_color(color)
        self.message_label.setText(message)
        if reset:
            QtCore.QTimer.singleShot(2000, reset_message_text)

    def load(self):
        print("Modify widget")
        self.reset_widget()