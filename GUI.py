import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedWidget,
                             QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton)
from PyQt5.QtGui import QIcon, QCursor, QFont, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QEasingCurve

class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._bgColor = QColor("#ddd")
        self.desiredColor = QColor("#ddd")
        self.anim = QPropertyAnimation(self, b"bgColor")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.Linear)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFont(QFont("Arial", 10))
        self._hovered = False
        self.updateStyle()

    def updateStyle(self):
        textColor = "white" 
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: 10px;
                background-color: {self._bgColor.name()};
                color: {textColor};
                font-weight: bold;
                padding: 7px;
                font-size: 10pt;
            }}
        """)

    def enterEvent(self, event):
        self._hovered = True
        self.updateStyle()
        if self.desiredColor.name() == "#006699":
            targetColor = QColor("#005588")
        else:
            targetColor = QColor("#006699")
        self.anim.stop()
        self.anim.setStartValue(self._bgColor)
        self.anim.setEndValue(targetColor)
        self.anim.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.updateStyle()
        self.anim.stop()
        self.anim.setStartValue(self._bgColor)
        self.anim.setEndValue(self.desiredColor)
        self.anim.start()
        super().leaveEvent(event)

    def getBgColor(self):
        return self._bgColor

    def setBgColor(self, color):
        self._bgColor = color
        self.updateStyle()

    bgColor = pyqtProperty(QColor, fget=getBgColor, fset=setBgColor)

class PageOne(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Welcome to Page One")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        description = QLabel("This is page one filled with content. Enjoy!")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        text_area = QTextEdit()
        text_area.setPlaceholderText("Type your notes here...")
        text_area.setFixedHeight(200)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(text_area)
        layout.addStretch()
        self.setLayout(layout)

class PageTwo(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        title = QLabel("Welcome to Page Two")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold;")
        info = QLabel("This is page two. Here you might display summaries or feedback.")
        info.setAlignment(Qt.AlignCenter)
        info.setWordWrap(True)
        text_area = QTextEdit()
        text_area.setPlaceholderText("Share your feedback here...")
        text_area.setFixedHeight(200)
        layout.addWidget(title)
        layout.addWidget(info)
        layout.addWidget(text_area)
        layout.addStretch()
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Penguins")
        self.setWindowIcon(QIcon("Penguin.png"))
        self.setStyleSheet("background-color: #161616; color: #FFF;")
        self.resize(1600, 800)
        self.center_window()

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        self.top_button_layout = QHBoxLayout()
        self.top_button_layout.setSpacing(20)
        self.top_button_layout.setAlignment(Qt.AlignCenter)

        btnWidth = 150

        self.button1 = AnimatedButton("Page One")
        self.button1.clicked.connect(lambda: self.switch_page(0))
        self.button1.setFixedWidth(btnWidth)

        self.button2 = AnimatedButton("Page Two")
        self.button2.clicked.connect(lambda: self.switch_page(1))
        self.button2.setFixedWidth(btnWidth)

        self.top_button_layout.addWidget(self.button1)
        self.top_button_layout.addWidget(self.button2)

        self.stack = QStackedWidget()
        self.page_one = PageOne()
        self.page_two = PageTwo()
        self.stack.addWidget(self.page_one)
        self.stack.addWidget(self.page_two)

        main_layout.addLayout(self.top_button_layout)
        main_layout.addWidget(self.stack)
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.active_index = 0
        self.update_styles()

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2
        self.move(center_x, center_y)

    def switch_page(self, index):
        self.active_index = index
        self.stack.setCurrentIndex(index)
        self.update_styles()

    def update_styles(self):
        if self.active_index == 0:
            self.button1.desiredColor = QColor("#006699")
            self.button2.desiredColor = QColor("#424242")
        else:
            self.button1.desiredColor = QColor("#424242")
            self.button2.desiredColor = QColor("#006699")
        self.button1.setBgColor(self.button1.desiredColor)
        self.button2.setBgColor(self.button2.desiredColor)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
