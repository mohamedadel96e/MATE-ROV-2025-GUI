import sys
import cv2
import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QPushButton, QComboBox, QGridLayout, QGroupBox,
                             QSizePolicy)

# Color Constants
BACKGROUND_COLOR = "#2D2D2D"
GROUP_BOX_COLOR = "#3D3D3D"
TEXT_COLOR = "#FFFFFF"
ACCENT_COLOR = "#0078D4"
BUTTON_COLOR = "#005A9E"

class SerialReader(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, port):
        super().__init__()
        self.port = port
        self.running = True
        self.ser = None

    def run(self):
        try:
            self.ser = serial.Serial(self.port, baudrate=9600, timeout=1)
            while self.running:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode().strip()
                    self.data_received.emit(data)
        except Exception as e:
            print("Serial error:", e)
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()

    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROV Control Interface")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"background-color: {BACKGROUND_COLOR};")

        # Initialize serial threads
        self.rov_thread = None
        self.controller_thread = None
        self.cap = cv2.VideoCapture(0)  # Laptop camera

        # Create UI
        self.create_ui()
        self.init_camera_feed()

    def create_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QGridLayout(main_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        layout.setColumnStretch(1, 2)

        # Communication Setup Group
        comm_group = QGroupBox("COMMUNICATION SETUP")
        self.style_group_box(comm_group)
        comm_layout = QGridLayout()
        comm_layout.setSpacing(10)
        
        # ROV Connection
        self.rov_port_combo = QComboBox()
        self.style_combo(self.rov_port_combo)
        self.rov_connect_btn = QPushButton("CONNECT ROV")
        self.style_button(self.rov_connect_btn)
        self.rov_connect_btn.clicked.connect(lambda: self.toggle_connection("rov"))
        self.rov_status = QLabel("ROV Status: Disconnected")
        
        # Controller Connection
        self.controller_port_combo = QComboBox()
        self.style_combo(self.controller_port_combo)
        self.controller_connect_btn = QPushButton("CONNECT CONTROLLER")
        self.style_button(self.controller_connect_btn)
        self.controller_connect_btn.clicked.connect(lambda: self.toggle_connection("controller"))
        self.controller_status = QLabel("Controller Status: Disconnected")

        # Populate ports
        self.refresh_ports()
        
        # Add widgets to layout
        comm_layout.addWidget(QLabel("ROV Port:"), 0, 0)
        comm_layout.addWidget(self.rov_port_combo, 0, 1)
        comm_layout.addWidget(self.rov_connect_btn, 1, 0, 1, 2)
        comm_layout.addWidget(self.rov_status, 2, 0, 1, 2)
        
        comm_layout.addWidget(QLabel("Controller Port:"), 3, 0)
        comm_layout.addWidget(self.controller_port_combo, 3, 1)
        comm_layout.addWidget(self.controller_connect_btn, 4, 0, 1, 2)
        comm_layout.addWidget(self.controller_status, 5, 0, 1, 2)
        
        comm_group.setLayout(comm_layout)

        # Camera Feed Group
        cam_group = QGroupBox("CAMERA FEED")
        self.style_group_box(cam_group)
        self.cam_label = QLabel()
        self.cam_label.setAlignment(Qt.AlignCenter)
        self.cam_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cam_label.setMinimumSize(320, 240)
        self.cam_label.setStyleSheet(f"background-color: black;")
        cam_layout = QGridLayout()
        cam_layout.addWidget(self.cam_label)
        cam_group.setLayout(cam_layout)

        # Sensors Group
        sensors_group = QGroupBox("CONTROLLER SENSORS READING")
        self.style_group_box(sensors_group)
        sensors_layout = QGridLayout()
        sensors_layout.setSpacing(10)
        
        self.front_distance = QLabel("0")
        self.flow_distance = QLabel("0")
        self.style_sensor_label(self.front_distance)
        self.style_sensor_label(self.flow_distance)
        
        sensors_layout.addWidget(QLabel("Front Distance (CM):"), 0, 0)
        sensors_layout.addWidget(self.front_distance, 0, 1)
        sensors_layout.addWidget(QLabel("Flow Distance (CM):"), 1, 0)
        sensors_layout.addWidget(self.flow_distance, 1, 1)
        sensors_group.setLayout(sensors_layout)

        # Add groups to main layout
        layout.addWidget(comm_group, 0, 0)
        layout.addWidget(cam_group, 0, 1, 2, 1)
        layout.addWidget(sensors_group, 1, 0)

        # Set stretch factors
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)

    def style_group_box(self, group):
        group.setStyleSheet(f"""
            QGroupBox {{
                color: {ACCENT_COLOR};
                border: 2px solid {ACCENT_COLOR};
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }}
            QLabel {{
                color: {TEXT_COLOR};
            }}
        """)
        group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def style_button(self, button):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {BUTTON_COLOR};
                color: {TEXT_COLOR};
                border: none;
                padding: 8px;
                font-weight: bold;
                border-radius: 4px;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background-color: {ACCENT_COLOR};
            }}
        """)

    def style_combo(self, combo):
        combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {GROUP_BOX_COLOR};
                color: {TEXT_COLOR};
                padding: 5px;
                border: 1px solid {ACCENT_COLOR};
                border-radius: 4px;
            }}
        """)

    def style_sensor_label(self, label):
        label.setStyleSheet(f"""
            QLabel {{
                color: {TEXT_COLOR};
                font-size: 16px;
                font-weight: bold;
                background-color: {GROUP_BOX_COLOR};
                padding: 5px;
                border-radius: 4px;
                min-width: 80px;
                text-align: center;
            }}
        """)

    def init_camera_feed(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            
            scaled_pixmap = pixmap.scaled(
                self.cam_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.cam_label.setPixmap(scaled_pixmap)

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()
        self.rov_port_combo.clear()
        self.controller_port_combo.clear()
        for port in ports:
            self.rov_port_combo.addItem(port.device)
            self.controller_port_combo.addItem(port.device)

    def toggle_connection(self, device_type):
        if device_type == "rov":
            btn = self.rov_connect_btn
            status = self.rov_status
            combo = self.rov_port_combo
            thread_attr = "rov_thread"
        else:
            btn = self.controller_connect_btn
            status = self.controller_status
            combo = self.controller_port_combo
            thread_attr = "controller_thread"

        if btn.text().startswith("CONNECT"):
            port = combo.currentText()
            if port:
                thread = SerialReader(port)
                setattr(self, thread_attr, thread)
                if device_type == "rov":
                    thread.data_received.connect(self.update_sensors)
                thread.start()
                status.setText(f"{device_type.capitalize()} Status: Connected")
                btn.setText(f"DISCONNECT {device_type.upper()}")
        else:
            thread = getattr(self, thread_attr)
            if thread:
                thread.stop()
                thread.wait()
                status.setText(f"{device_type.capitalize()} Status: Disconnected")
                btn.setText(f"CONNECT {device_type.upper()}")

    def update_sensors(self, data):
        try:
            parts = data.split(',')
            front = parts[0].split(':')[1]
            flow = parts[1].split(':')[1]
            self.front_distance.setText(front)
            self.flow_distance.setText(flow)
        except Exception as e:
            print("Data parsing error:", e)

    def closeEvent(self, event):
        for thread in [self.rov_thread, self.controller_thread]:
            if thread and thread.isRunning():
                thread.stop()
                thread.wait()
        self.cap.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())