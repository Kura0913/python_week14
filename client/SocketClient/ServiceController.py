from PyQt6 import QtWidgets, QtGui, QtCore
from SocketClient.SocketClient import SocketClient 
from PyQt6.QtCore import pyqtSignal
import json

class ExecuteConfirmCommand(QtCore.QThread):
    result_msg = pyqtSignal(str)

    def __init__(self, client: SocketClient, command, parameters):
        super().__init__()
        self.client = client
        self.command = command
        self.parameters = parameters

    def run(self):
        self.client.send_command(self.command, self.parameters)
        result = self.client.wait_response()
        print(f"Received response: {result}")
        self.result_msg.emit(json.dumps(result))