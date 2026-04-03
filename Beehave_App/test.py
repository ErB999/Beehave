import sys
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QProgressBar, QFileDialog, 
                             QStackedWidget, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QThread, Signal

# --- WORKER THREAD FOR SUPERCOMPUTER ---
class AnalysisWorker(QThread):
    progress = Signal(int)
    status = Signal(str)
    finished = Signal(dict)

    def run(self):
        # This is where your SSH/Paramiko code will live
        self.status.emit("Uploading to Fir...")
        for i in range(1, 41): # Simulating Upload
            time.sleep(0.05)
            self.progress.emit(i)
            
        self.status.emit("Analyzing bee behaviour...")
        for i in range(41, 91): # Simulating Supercomputer Processing
            time.sleep(0.1)
            self.progress.emit(i)

        self.status.emit("Constructing data table...")
        self.progress.emit(100)
        self.finished.emit({"success": True})

# --- MAIN APP WINDOW ---
class BeeTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beehave - Bee Tr") # Replace with your program name
        self.setMinimumSize(800, 500)

        # Central Stack to handle Loading Screen -> Home Screen
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 1. Loading Screen
        self.init_loading_screen()
        # 2. Home Screen
        self.init_home_screen()

        # Start with Loading Screen
        self.stack.setCurrentIndex(0)
        self.run_fade_sequence()

    def init_loading_screen(self):
        self.loading_page = QWidget()
        layout = QVBoxLayout(self.loading_page)
        
        # Logo Placeholder (Replace 'logo.png' with your file)
        self.logo_label = QLabel("LOGO HERE") 
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)
        
        self.stack.addWidget(self.loading_page)

    def init_home_screen(self):
        self.home_page = QWidget()
        layout = QVBoxLayout(self.home_page)

        # Title
        title = QLabel("Beehave")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # File Select Button
        self.btn_select = QPushButton("Select Video File")
        self.btn_select.clicked.connect(self.select_file)
        layout.addWidget(self.btn_select)

        # Analyze Button
        self.btn_analyze = QPushButton("Start Analysis")
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.clicked.connect(self.start_analysis)
        layout.addWidget(self.btn_analyze)

        # Status Bar Area (Bottom)
        self.status_label = QLabel("Ready")
        layout.addStretch()
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.stack.addWidget(self.home_page)

    def run_fade_sequence(self):
        # Simple timer to fade from loading to home
        time.sleep(1) # Fake load time
        self.stack.setCurrentIndex(1)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mkv)")
        if file_path:
            self.status_label.setText(f"Selected: {file_path.split('/')[-1]}")
            self.btn_analyze.setEnabled(True)

    def start_analysis(self):
        self.worker = AnalysisWorker()
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, result):
        self.status_label.setText("Analysis Complete! Table generated.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeeTrackerApp()
    window.show()
    sys.exit(app.exec())