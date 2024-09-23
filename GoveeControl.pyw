import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests

class SystemTrayApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.initUI()

    def initUI(self):
        self.setQuitOnLastWindowClosed(False)

        # Adding an icon
        icon = QIcon("E:/Coding/Govee Lightbars MiniApp/Logo.png")

        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        # Creating the options
        menu = QMenu()

        # ON
        self.on_action = QAction("On", self)
        self.on_action.triggered.connect(lambda: self.Toggle(1))
        menu.addAction(self.on_action)

        # OFF
        self.on_action = QAction("Off", self)
        self.on_action.triggered.connect(lambda: self.Toggle(0))
        menu.addAction(self.on_action)

        # QUIT
        self.quit_action = QAction("Quit")
        self.quit_action.triggered.connect(self.quit)
        menu.addAction(self.quit_action)
        

        # Add to System Tray
        self.tray.setContextMenu(menu)

    # Turn ON or OFF
    def Toggle(self, state):

        url = 'https://developer-api.govee.com/v1/devices/control'
        api_token = "REDACTED"
        device_mac = "REDACTED"
        device_model = "REDACTED"

        headers = {
            "Govee-API-Key": f"{api_token}"
        }

        body = ""

        if state:
            print("On")
            body = {
            "device": device_mac,
            "model": device_model,
            "cmd": {
                "name": "turn",
                "value": "on"
            }
        }
        else:
            print("Off")
            body = {
            "device": device_mac,
            "model": device_model,
            "cmd": {
                "name": "turn",
                "value": "off"
            }
        }
    
        try:
            response = requests.put(url, headers=headers, json=body)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            print("Device state successfully updated!")
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            
        

if __name__ == "__main__":
    app = SystemTrayApp()
    sys.exit(app.exec_())
