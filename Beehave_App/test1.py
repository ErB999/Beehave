import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QProgressBar, QFileDialog, 
                             QStackedWidget, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QSize
from PySide6.QtGui import QMovie, QPixmap, QFont

class BeeTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beehave")
        self.setMinimumSize(1100, 750)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Initialize screens
        self.init_splash_screen()
        self.init_home_screen()

        # Start with Splash
        self.stack.setCurrentIndex(0)
        
        # Show GIF for 4 seconds, then transition
        QTimer.singleShot(4000, self.start_fade_transition)

    def init_splash_screen(self):
        self.splash_page = QWidget()
        self.splash_page.setStyleSheet("background-color: #ffffff;") # Pure white for light mode
        layout = QVBoxLayout(self.splash_page)
        
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        
        # Ensure the path is correct
        gif_path = os.path.join(os.path.dirname(__file__), "/Users/erwinbehpour/Downloads/Beehave/LOGO/Screen Recording 2026-03-29 at 6.18.29 PM.mov")
        
        if os.path.exists(gif_path):
            self.movie = QMovie(gif_path)
            # This ensures the GIF scales if it's too small/large
            self.movie.setScaledSize(QSize(400, 400)) 
            self.gif_label.setMovie(self.movie)
            self.movie.start()
        else:
            self.gif_label.setText("LOGO GIF NOT FOUND\n(Check file path)")
            self.gif_label.setStyleSheet("color: #cc0000; font-weight: bold;")

        layout.addWidget(self.gif_label)
        self.stack.addWidget(self.splash_page)

    def init_home_screen(self):
        self.home_page = QWidget()
        self.home_page.setObjectName("HomePage")
        
        # --- LIGHT MODE STYLING ---
        # background-image uses your png. We use rgba(255,255,255, 200) 
        # to "wash out" the background so text is readable.
        self.home_page.setStyleSheet("""
            #HomePage {
                background-image: url('/Users/erwinbehpour/Downloads/Beehave/LOGO/Beehave_13@2x.png');
                background-repeat: no-repeat;
                background-position: center;
                background-color: #f5f5f7; /* Soft Apple-style light gray */
            }
            QLabel#Title {
                font-family: 'Academy Engraved LET';
                font-size: 48px;
                color: #1d1d1f;
                background: none;
            }
            QPushButton {
                background-color: #ffffff;
                color: #1d1d1f;
                border: 1px solid #d2d2d7;
                padding: 18px;
                border-radius: 12px;
                font-size: 15px;
                font-weight: 500;
                min-width: 250px;
                max-width: 350px; /* Narrow buttons as requested */
            }
            QPushButton:hover {
                background-color: #f5f5f7;
                border: 1px solid #0071e3; /* Blue highlight */
            }
            QPushButton:disabled {
                color: #a1a1a6;
                background-color: #f5f5f7;
            }
            QProgressBar {
                border: 1px solid #d2d2d7;
                border-radius: 10px;
                text-align: center;
                height: 12px;
                background-color: #e5e5e7;
                color: #1d1d1f;
            }
            QProgressBar::chunk {
                background-color: #0071e3;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self.home_page)
        layout.setContentsMargins(60, 40, 60, 40)

        # 1. Header (Academy Engraved)
        self.title = QLabel("Beehave")
        self.title.setObjectName("Title")
        # Aligning Top-Middle as requested
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop) 
        layout.addWidget(self.title)

        # 2. Central Area with the blurred logo feel
        # We add a stretch to push buttons to middle
        layout.addStretch(1)

        button_container = QVBoxLayout()
        button_container.setAlignment(Qt.AlignCenter)
        button_container.setSpacing(25)

        self.btn_select = QPushButton("OPEN VIDEO FILE")
        self.btn_analyze = QPushButton("START BEHAVIUOR ANALYSIS")
        self.btn_analyze.setEnabled(False)

        button_container.addWidget(self.btn_select)
        button_container.addWidget(self.btn_analyze)
        
        layout.addLayout(button_container)
        
        # Push everything else down
        layout.addStretch(2)

        # 3. Bottom Status/Progress Area
        self.status_label = QLabel("SYSTEM STATUS: IDLE")
        self.status_label.setStyleSheet("color: #86868b; font-size: 12px; letter-spacing: 1px;")
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.stack.addWidget(self.home_page)

    def start_fade_transition(self):
        # Apply opacity effect to home page
        self.opacity_effect = QGraphicsOpacityEffect()
        self.home_page.setGraphicsEffect(self.opacity_effect)
        self.stack.setCurrentIndex(1)

        # Transition from transparent to visible
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(1200) 
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set a clean default font for the whole app
    default_font = QFont("Inter", 10)
    app.setFont(default_font)
    
    window = BeeTrackerApp()
    window.show()
    sys.exit(app.exec())