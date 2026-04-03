from PySide6.QtWidgets import QMainWindow, QPushButton

class ButtonHolder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beehave")
        button = QPushButton("Open File")
        self.setCentralWidget(button)