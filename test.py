import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QMenuBar, QMenu, QAction,
    QHBoxLayout, QVBoxLayout, QGridLayout, QFrame, QPushButton, QLabel,
    QComboBox, QGroupBox, QRadioButton, QButtonGroup, QLineEdit
)

class ControlPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Penguins ROV - Control Page")
        self.setGeometry(100, 100, 1280, 720)

        # 1) Dark palette for the entire window
        darkColor = QColor("#2b2b2b")
        palette = QPalette()
        palette.setColor(QPalette.Window, darkColor)
        palette.setColor(QPalette.Base, darkColor)
        palette.setColor(QPalette.AlternateBase, darkColor)
        palette.setColor(QPalette.Text, QColor("#ffffff"))
        palette.setColor(QPalette.Button, QColor("#0D47A1"))
        palette.setColor(QPalette.ButtonText, QColor("#ffffff"))
        self.setPalette(palette)

        # 2) Menu bar
        menuBar = QMenuBar(self)
        fileMenu = QMenu("File", self)
        helpMenu = QMenu("Help", self)
        fileMenu.addAction(QAction("Open", self))
        fileMenu.addAction(QAction("Save", self))
        helpMenu.addAction(QAction("About", self))
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(helpMenu)
        self.setMenuBar(menuBar)

        # 3) Central widget + main horizontal layout
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout = QHBoxLayout(centralWidget)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(15)

        # -------------------------------
        # LEFT PANEL: top buttons + camera feed
        # -------------------------------
        leftPanel = QVBoxLayout()
        leftPanel.setSpacing(10)

        # (a) Top row of big blue buttons
        topButtonsLayout = QHBoxLayout()
        btnFont = QFont("Arial", 10, QFont.Bold)

        self.changeUserBtn = QPushButton("CHANGE USER")
        self.changeUserBtn.setFont(btnFont)
        self.changeUserBtn.setFixedHeight(40)
        self.changeUserBtn.setObjectName("blueButton")
        self.changeUserBtn.setStyleSheet("""font-size: 10pt;""");

        self.controlPanelBtn = QPushButton("CONTROL PANEL")
        self.controlPanelBtn.setFont(btnFont)
        self.controlPanelBtn.setFixedHeight(40)
        self.controlPanelBtn.setObjectName("blueButton")

        self.configurationBtn = QPushButton("CONFIGURATION")
        self.configurationBtn.setFont(btnFont)
        self.configurationBtn.setFixedHeight(40)
        self.configurationBtn.setObjectName("blueButton")

        topButtonsLayout.addWidget(self.changeUserBtn)
        topButtonsLayout.addWidget(self.controlPanelBtn)
        topButtonsLayout.addWidget(self.configurationBtn)
        leftPanel.addLayout(topButtonsLayout)

        # (b) Primary Feed label + combo
        feedLayout = QHBoxLayout()
        feedLabel = QLabel("Primary Feed:")
        feedLabel.setStyleSheet("color: white; font-weight: bold;")
        self.primaryFeedCombo = QComboBox()
        self.primaryFeedCombo.addItems(["None", "Camera 1", "Camera 2"])
        feedLayout.addWidget(feedLabel)
        feedLayout.addWidget(self.primaryFeedCombo)
        feedLayout.addStretch(1)
        leftPanel.addLayout(feedLayout)

        # (c) Big camera feed area
        self.cameraFeedFrame = QFrame()
        self.cameraFeedFrame.setFrameShape(QFrame.Box)
        self.cameraFeedFrame.setStyleSheet("background-color: black;")
        self.cameraFeedFrame.setMinimumSize(640, 400)

        # Centered label for "Camera Feed"
        cameraLayout = QVBoxLayout(self.cameraFeedFrame)
        cameraLayout.setAlignment(Qt.AlignCenter)
        self.feedLabel = QLabel("Camera Feed")
        self.feedLabel.setStyleSheet("color: white; font-size: 20pt;")
        self.feedLabel.setAlignment(Qt.AlignCenter)
        cameraLayout.addWidget(self.feedLabel)

        leftPanel.addWidget(self.cameraFeedFrame, stretch=1)

        # Add left panel to main layout
        mainLayout.addLayout(leftPanel, stretch=3)

        # -------------------------------
        # RIGHT PANEL: (no Cameras group), only the rest
        # -------------------------------
        rightPanel = QVBoxLayout()
        rightPanel.setSpacing(15)

        # (1) Controller Sensitivity
        ctrlGroup = QGroupBox("Controller Sensitivity")
        ctrlGroup.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        ctrlLayout = QGridLayout(ctrlGroup)

        joystickLabel = QLabel("Joystick")
        yawLabel = QLabel("Yaw")
        joystickLabel.setStyleSheet("color: white;")
        yawLabel.setStyleSheet("color: white;")

        self.jsLow = QRadioButton("Low")
        self.jsNormal = QRadioButton("Normal")
        self.jsHigh = QRadioButton("High")
        self.jsLow.setChecked(True)

        self.yawLow = QRadioButton("Low")
        self.yawNormal = QRadioButton("Normal")
        self.yawHigh = QRadioButton("High")
        self.yawLow.setChecked(True)

        ctrlLayout.addWidget(joystickLabel, 0, 0)
        ctrlLayout.addWidget(self.jsLow,     0, 1)
        ctrlLayout.addWidget(self.jsNormal,  0, 2)
        ctrlLayout.addWidget(self.jsHigh,    0, 3)

        ctrlLayout.addWidget(yawLabel,       1, 0)
        ctrlLayout.addWidget(self.yawLow,    1, 1)
        ctrlLayout.addWidget(self.yawNormal, 1, 2)
        ctrlLayout.addWidget(self.yawHigh,   1, 3)

        rightPanel.addWidget(ctrlGroup)

        # (2) Communication Setup
        commsGroup = QGroupBox("Communication Setup")
        commsGroup.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        commsLayout = QGridLayout(commsGroup)

        rovLabel = QLabel("ROV")
        rovLabel.setStyleSheet("color: white;")
        self.rovConnectBtn = QPushButton("CONNECT")
        self.rovConnectBtn.setObjectName("blueButton")
        self.rovConnectBtn.setFont(btnFont)
        self.rovConnectBtn.setFixedHeight(40)

        controllerLabel = QLabel("Controller")
        controllerLabel.setStyleSheet("color: white;")
        self.controllerConnectBtn = QPushButton("CONNECT")
        self.controllerConnectBtn.setObjectName("blueButton")
        self.controllerConnectBtn.setFont(btnFont)
        self.controllerConnectBtn.setFixedHeight(40)

        commsLayout.addWidget(rovLabel,               0, 0)
        commsLayout.addWidget(self.rovConnectBtn,     0, 1)
        commsLayout.addWidget(controllerLabel,        1, 0)
        commsLayout.addWidget(self.controllerConnectBtn, 1, 1)

        rightPanel.addWidget(commsGroup)

        # (3) Sensors Reading
        sensorsGroup = QGroupBox("Sensors Reading")
        sensorsGroup.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        sensorsLayout = QGridLayout(sensorsGroup)

        self.frontDistLabel = QLabel("Front Distance (CM)")
        self.frontDistLabel.setStyleSheet("color: white;")
        self.frontDistValue = QLineEdit("--")
        self.frontDistValue.setReadOnly(True)
        self.frontDistValue.setStyleSheet("background-color: #4f4f4f; color: white;")

        self.floorDistLabel = QLabel("Floor Distance (CM)")
        self.floorDistLabel.setStyleSheet("color: white;")
        self.floorDistValue = QLineEdit("--")
        self.floorDistValue.setReadOnly(True)
        self.floorDistValue.setStyleSheet("background-color: #4f4f4f; color: white;")

        self.phLabel = QLabel("PH Sensor (ph)")
        self.phLabel.setStyleSheet("color: white;")
        self.phValue = QLineEdit("--")
        self.phValue.setReadOnly(True)
        self.phValue.setStyleSheet("background-color: #4f4f4f; color: white;")

        sensorsLayout.addWidget(self.frontDistLabel, 0, 0)
        sensorsLayout.addWidget(self.frontDistValue, 0, 1)
        sensorsLayout.addWidget(self.floorDistLabel, 1, 0)
        sensorsLayout.addWidget(self.floorDistValue, 1, 1)
        sensorsLayout.addWidget(self.phLabel,        2, 0)
        sensorsLayout.addWidget(self.phValue,        2, 1)

        rightPanel.addWidget(sensorsGroup)

        # (4) Competition Time
        timeGroup = QGroupBox("Competition Time")
        timeGroup.setStyleSheet("QGroupBox { color: white; font-weight: bold; }")
        timeLayout = QVBoxLayout(timeGroup)

        self.timerLabel = QLabel("00 : 00 : 00 : 00")
        self.timerLabel.setStyleSheet("color: white; font-size: 16pt;")
        self.timerLabel.setAlignment(Qt.AlignCenter)

        buttonLayout = QHBoxLayout()
        self.startTimeBtn = QPushButton("Start")
        self.startTimeBtn.setObjectName("blueButton")
        self.startTimeBtn.setFont(btnFont)
        self.startTimeBtn.setFixedHeight(35)

        self.resetTimeBtn = QPushButton("Reset")
        self.resetTimeBtn.setStyleSheet("background-color: #606060; color: white; border-radius: 8px;")
        self.resetTimeBtn.setFont(btnFont)
        self.resetTimeBtn.setFixedHeight(35)

        buttonLayout.addWidget(self.startTimeBtn)
        buttonLayout.addWidget(self.resetTimeBtn)

        timeLayout.addWidget(self.timerLabel)
        timeLayout.addLayout(buttonLayout)

        rightPanel.addWidget(timeGroup)

        # push everything up
        rightPanel.addStretch(1)

        # Add right panel to main layout
        mainLayout.addLayout(rightPanel, stretch=1)

        # 4) Style for “blueButton”
        self.setStyleSheet("""
            QPushButton#blueButton {
                background-color: #0D47A1;
                color: white;
                border-radius: 8px;
            }
            QPushButton#blueButton:hover {
                background-color: #1565C0;
            }
            QPushButton#blueButton:pressed {
                background-color: #0D47A1;
                padding-left: 2px;
                padding-top: 2px;
            }
        """)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ControlPage()
    sys.exit(app.exec_())
