from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtCore import Qt
import sys
from button import ButtonHolder

def button_clicked():
    print("lol")

app = QApplication(sys.argv)
button=QPushButton("Choose File")
button.clicked.connect(button_clicked)

window = ButtonHolder()

window.show()

button.show()
app.exec()