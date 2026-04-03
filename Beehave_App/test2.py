import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QProgressBar, 
                             QFileDialog, QStackedWidget, QGraphicsOpacityEffect)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QUrl, QSize
from PySide6.QtGui import QMovie, QFont
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

class BeeTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beehave")
        self.setMinimumSize(1100, 750)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.init_splash_screen()
        self.init_home_screen()

        self.stack.setCurrentIndex(0)
        self.play_loading_video()
        
        # Start transition after 3 seconds
        QTimer.singleShot(500, self.fade_out_splash)

    def init_splash_screen(self):
        self.splash_page = QWidget()
        self.splash_page.setStyleSheet("background-color: white;")
        layout = QVBoxLayout(self.splash_page)
        layout.setContentsMargins(0, 0, 0, 0)

        # Back to QVideoWidget for hardware-accelerated, lag-free playback
        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("background-color: white;")
        
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0)

        layout.addWidget(self.video_widget)
        self.stack.addWidget(self.splash_page)

    def play_loading_video(self):
        video_path = os.path.join(os.path.dirname(__file__), "LOGO/LoadingLogo.mov") 
        if os.path.exists(video_path):
            self.media_player.setSource(QUrl.fromLocalFile(video_path))
            self.media_player.play()

    def init_home_screen(self):
        self.home_page = QWidget()
        self.home_page.setObjectName("HomePage")
        
        self.home_page.setStyleSheet("""
            #HomePage {
                background-image: url('LOGO/blurlogo.png');
                background-repeat: no-repeat;
                background-position: center;
                background-color: #fcfcfc;
            }
            QLabel#Title {
                font-family: 'Academy Engraved LET';
                font-size: 54px;
                color: #1a1a1a;
                padding-top: 50px;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.95);
                color: #444;
                border: 1px solid #e5e5e5;
                padding: 16px;
                border-radius: 4px;
                font-size: 13px;
                font-weight: 500;
                min-width: 280px;
                max-width: 320px;
            }
            QPushButton:hover {
                background-color: #ffffff;
                border-color: #bbb;
            }
            QProgressBar {
                border: 1px solid #f0f0f0;
                border-radius: 2px;
                text-align: center;
                background-color: #f9f9f9;
                height: 6px;
            }
            QProgressBar::chunk {
                background-color: #333;
            }
        """)

        layout = QVBoxLayout(self.home_page)
        self.title = QLabel("BEEHAVE")
        self.title.setObjectName("Title")
        self.title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(self.title)

        layout.addStretch(1)

        button_container = QVBoxLayout()
        button_container.setAlignment(Qt.AlignCenter)
        button_container.setSpacing(15)

        self.btn_select = QPushButton("CHOOSE VIDEO SOURCE")
        self.btn_select.clicked.connect(self.select_file)
        
        self.btn_analyze = QPushButton("START ANALYSIS")
        self.btn_analyze.setEnabled(False)
        self.btn_analyze.clicked.connect(self.start_analysis)
        
        button_container.addWidget(self.btn_select)
        button_container.addWidget(self.btn_analyze)
        layout.addLayout(button_container)

        layout.addStretch(2)

        # Status Layout
        status_layout = QHBoxLayout()
        status_layout.setAlignment(Qt.AlignLeft)

        self.status_label = QLabel("SYSTEM IDLE")
        self.status_label.setStyleSheet("""
            color: #a1a1a6; 
            font-size: 10px; 
            font-weight: 300; 
            letter-spacing: 0.8px;
            text-transform: uppercase;
        """)
        
        self.spinner_label = QLabel()
        self.spinner_movie = QMovie("LOGO/spinner.gif") 
        # Large Spinner for better visibility
        self.spinner_movie.setScaledSize(QSize(32, 32)) 
        self.spinner_label.setMovie(self.spinner_movie)
        self.spinner_label.hide()

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.spinner_label)
        layout.addLayout(status_layout)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        self.stack.addWidget(self.home_page)

    # --- ANIMATION LOGIC ---

    def fade_out_splash(self):
        self.splash_opacity = QGraphicsOpacityEffect()
        self.splash_page.setGraphicsEffect(self.splash_opacity)
        
        self.anim_out = QPropertyAnimation(self.splash_opacity, b"opacity")
        self.anim_out.setDuration(1200) 
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.setEasingCurve(QEasingCurve.InQuad)
        
        self.anim_out.finished.connect(self.fade_in_home)
        self.anim_out.start()

    def fade_in_home(self):
        self.media_player.stop()
        self.stack.setCurrentIndex(1)
        
        self.home_opacity = QGraphicsOpacityEffect()
        self.home_page.setGraphicsEffect(self.home_opacity)
        
        self.anim_in = QPropertyAnimation(self.home_opacity, b"opacity")
        self.anim_in.setDuration(1200) 
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.setEasingCurve(QEasingCurve.OutQuad)
        self.anim_in.start()

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Videos (*.mp4 *.mov)")
        if file_path:
            self.status_label.setText(f"FILE LOADED: {os.path.basename(file_path).upper()}")
            self.btn_analyze.setEnabled(True)

    def start_analysis(self):
        self.status_label.setText("ANALYZING BEE BEHAVIOUR...")
        self.spinner_label.show()
        self.spinner_movie.start()
        self.btn_analyze.setEnabled(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BeeTrackerApp()
    window.show()
    sys.exit(app.exec())