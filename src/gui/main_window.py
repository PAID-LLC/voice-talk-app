"""Main Application Window - Voice Talk GUI"""

import sys
from pathlib import Path
from datetime import datetime
import asyncio
import threading

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel, QComboBox, QSlider,
    QSplitter, QStatusBar, QMessageBox, QDialog, QSystemTrayIcon, QMenu
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer, QRect
from PyQt6.QtGui import QIcon, QFont, QColor, QPixmap
from PyQt6.QtCharts import QChart, QChartView, QLineSeries
from PyQt6.QtCore import QPointF

from src.config.settings import get_settings
from src.config.logger import get_logger
from src.audio.capture import AudioCapture
from src.audio.playback import AudioPlayback
from src.speech.synthesis.pyttsx3_engine import get_pyttsx3_engine
from src.speech.recognition.vosk_engine import get_vosk_engine
from src.ai.conversation.huggingface_client import get_huggingface_client
from src.ai.quota_manager import get_quota_manager
from src.gui.settings_manager import get_gui_settings
from src.gui.styles.themes import get_stylesheet
from src.gui.dialogs.settings_dialog import SettingsDialog

logger = get_logger(__name__)


class VoiceInputThread(QThread):
    """Thread for capturing voice input with real-time transcription"""
    transcription_ready = pyqtSignal(str)
    transcription_partial = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    recording_started = pyqtSignal()
    recording_stopped = pyqtSignal()

    def __init__(self, duration_seconds: int = 5):
        super().__init__()
        self.is_recording = False
        self.audio_capture = AudioCapture()
        self.vosk_engine = get_vosk_engine()
        self.duration_seconds = duration_seconds
        self.final_text = ""

    def run(self):
        """Capture and transcribe audio in real-time"""
        try:
            settings = get_settings()

            # Check if Vosk is available
            if not self.vosk_engine.is_initialized:
                # Fallback to silent recording mode
                logger.warning("Vosk not initialized, will record silently")

            # Start recording
            if not self.audio_capture.start():
                self.error_occurred.emit("Failed to start audio capture")
                return

            self.is_recording = True
            self.recording_started.emit()

            # Record for specified duration
            import time
            import struct

            start_time = time.time()
            audio_data = bytearray()
            frame_count = 0
            partial_text = ""

            while self.is_recording and (time.time() - start_time) < self.duration_seconds:
                # Read audio frame
                try:
                    data = self.audio_capture.stream.read(
                        self.audio_capture.chunk_size,
                        exception_on_overflow=False
                    )
                    audio_data.extend(data)
                    frame_count += 1

                    # Process with Vosk if available
                    if self.vosk_engine.is_initialized:
                        transcribed, confidence = self.vosk_engine.transcribe_audio(bytes(data))
                        if transcribed and transcribed != partial_text:
                            partial_text = transcribed
                            self.transcription_partial.emit(f"Listening... {transcribed}")
                            self.final_text = transcribed

                    # Update UI every frame to show recording is active
                    if frame_count % 10 == 0:  # Update every ~0.3 seconds
                        elapsed = time.time() - start_time
                        self.transcription_partial.emit(f"Recording... {elapsed:.0f}s")

                except Exception as e:
                    logger.error(f"Error reading audio frame: {e}")
                    continue

            # Stop recording
            self.audio_capture.stop()
            self.is_recording = False
            self.recording_stopped.emit()

            # Emit final result
            if self.final_text:
                self.transcription_ready.emit(self.final_text)
            else:
                self.error_occurred.emit("No speech detected. Please try again.")

        except Exception as e:
            logger.error(f"Voice input error: {e}")
            self.error_occurred.emit(f"Voice error: {str(e)}")
        finally:
            if self.audio_capture.is_recording:
                self.audio_capture.stop()
            self.is_recording = False

    def stop_recording(self):
        """Stop the recording"""
        self.is_recording = False


class ConversationThread(QThread):
    """Thread for AI conversation"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, message: str):
        super().__init__()
        self.message = message
        self.ai_client = get_huggingface_client()

    def run(self):
        """Get AI response in thread"""
        try:
            response, success = self.ai_client.chat(self.message)
            if success and response:
                self.response_ready.emit(response)
            else:
                self.error_occurred.emit("Failed to get AI response")
        except Exception as e:
            logger.error(f"Conversation error: {e}")
            self.error_occurred.emit(f"Error: {str(e)}")


class MainWindow(QMainWindow):
    """Main Application Window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voice Talk Application")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize components
        self.settings = get_settings()
        self.gui_settings = get_gui_settings()
        self.tts_engine = get_pyttsx3_engine()
        self.quota_manager = get_quota_manager()
        self.conversation_history = []

        # Setup UI
        self.setup_ui()
        self.setup_styles()
        self.setup_status_bar()
        self.setup_system_tray()
        self.update_quota_display()

        # Start quota update timer
        self.quota_timer = QTimer()
        self.quota_timer.timeout.connect(self.update_quota_display)
        self.quota_timer.start(30000)  # Update every 30 seconds

        logger.info("Main window initialized")

    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        # Left panel - Chat display
        left_widget = QWidget()
        left_layout = QVBoxLayout()

        # Chat title
        title = QLabel("Conversation History")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        left_layout.addWidget(title)

        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFont(QFont("Courier", 10))
        left_layout.addWidget(self.chat_display)

        # Input area
        input_layout = QVBoxLayout()

        input_label = QLabel("Your Message:")
        input_layout.addWidget(input_label)

        self.text_input = QTextEdit()
        self.text_input.setMaximumHeight(80)
        self.text_input.setFont(QFont("Arial", 10))
        input_layout.addWidget(self.text_input)

        # Buttons
        button_layout = QHBoxLayout()

        self.send_button = QPushButton("Send Message")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        button_layout.addWidget(self.send_button)

        self.voice_button = QPushButton("🎤 Record Voice")
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.voice_button.clicked.connect(self.record_voice)
        button_layout.addWidget(self.voice_button)

        self.clear_button = QPushButton("Clear History")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.clear_button.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clear_button)

        input_layout.addLayout(button_layout)
        left_layout.addLayout(input_layout)

        left_widget.setLayout(left_layout)
        main_layout.addWidget(left_widget, 2)

        # Right panel - Settings and status
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        # Settings section
        settings_title = QLabel("Settings")
        settings_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        right_layout.addWidget(settings_title)

        # Voice selection
        voice_label = QLabel("Voice:")
        right_layout.addWidget(voice_label)
        self.voice_combo = QComboBox()
        voices = self.tts_engine.list_voices()
        for voice in voices:
            self.voice_combo.addItem(voice["name"], voice["index"])
        self.voice_combo.currentIndexChanged.connect(self.change_voice)
        right_layout.addWidget(self.voice_combo)

        # Speech speed
        speed_label = QLabel("Speech Speed:")
        right_layout.addWidget(speed_label)
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setMinimum(50)
        self.speed_slider.setMaximum(200)
        self.speed_slider.setValue(150)
        self.speed_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.speed_slider.sliderMoved.connect(self.change_speed)
        right_layout.addWidget(self.speed_slider)
        self.speed_label = QLabel("Normal")
        right_layout.addWidget(self.speed_label)

        # API Status
        api_title = QLabel("API Status")
        api_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        right_layout.addWidget(api_title)

        self.ai_backend_label = QLabel("AI Backend: HuggingFace")
        right_layout.addWidget(self.ai_backend_label)

        self.quota_label = QLabel("Daily Quota: 1000")
        right_layout.addWidget(self.quota_label)

        self.remaining_label = QLabel("Remaining: Calculating...")
        right_layout.addWidget(self.remaining_label)

        # Settings button
        settings_button = QPushButton("⚙️ Advanced Settings")
        settings_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        settings_button.clicked.connect(self.open_settings)
        right_layout.addWidget(settings_button)

        # Stretch at bottom
        right_layout.addStretch()

        right_widget.setLayout(right_layout)
        main_layout.addWidget(right_widget, 1)

        central_widget.setLayout(main_layout)

    def setup_styles(self):
        """Setup application styles based on saved theme"""
        theme = self.gui_settings.get("theme", "light")
        stylesheet = get_stylesheet(theme)
        self.setStyleSheet(stylesheet)
        logger.info(f"Applied theme: {theme}")

    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)

        # Recording indicator
        self.recording_label = QLabel("")
        self.status_bar.addPermanentWidget(self.recording_label)

    def setup_system_tray(self):
        """Setup system tray icon"""
        tray_menu = QMenu()
        tray_menu.addAction("Show", self.show_window)
        tray_menu.addAction("Hide", self.hide_window)
        tray_menu.addSeparator()
        tray_menu.addAction("Exit", self.close_application)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def send_message(self):
        """Send a message to AI"""
        message = self.text_input.toPlainText().strip()
        if not message:
            QMessageBox.warning(self, "Empty Message", "Please enter a message")
            return

        # Display user message
        self.add_to_chat("You", message)
        self.text_input.clear()
        self.send_button.setEnabled(False)
        self.status_label.setText("Getting AI response...")

        # Get AI response in thread
        self.conversation_thread = ConversationThread(message)
        self.conversation_thread.response_ready.connect(self.on_ai_response)
        self.conversation_thread.error_occurred.connect(self.on_ai_error)
        self.conversation_thread.start()

    def on_ai_response(self, response: str):
        """Handle AI response"""
        self.add_to_chat("Assistant", response)
        self.send_button.setEnabled(True)
        self.status_label.setText("Ready")

        # Speak response
        try:
            self.tts_engine.speak(response[:500])  # Limit to 500 chars
        except Exception as e:
            logger.error(f"TTS error: {e}")

        # Track quota
        self.quota_manager.track_usage("huggingface")
        self.update_quota_display()

    def on_ai_error(self, error: str):
        """Handle AI error"""
        QMessageBox.critical(self, "AI Error", error)
        self.send_button.setEnabled(True)
        self.status_label.setText("Error occurred")

    def record_voice(self):
        """Record voice input"""
        self.voice_button.setEnabled(False)
        self.status_label.setText("Recording... (5 seconds)")
        self.recording_label.setText("🔴 RECORDING")

        # Record in thread
        self.voice_thread = VoiceInputThread(duration_seconds=5)
        self.voice_thread.transcription_ready.connect(self.on_transcription_ready)
        self.voice_thread.transcription_partial.connect(self.on_transcription_partial)
        self.voice_thread.error_occurred.connect(self.on_voice_error)
        self.voice_thread.start()

    def on_transcription_ready(self, text: str):
        """Handle transcription"""
        self.text_input.setText(text)
        self.voice_button.setEnabled(True)
        self.status_label.setText("Transcription complete")
        self.recording_label.setText("")
        self.send_message()  # Auto-send

    def on_transcription_partial(self, text: str):
        """Handle partial transcription (live update)"""
        self.status_label.setText(text)

    def on_voice_error(self, error: str):
        """Handle voice error"""
        QMessageBox.critical(self, "Voice Error", error)
        self.voice_button.setEnabled(True)
        self.status_label.setText("Voice error")
        self.recording_label.setText("")

    def add_to_chat(self, speaker: str, message: str):
        """Add message to chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted = f"[{timestamp}] {speaker}: {message}\n\n"
        self.chat_display.append(formatted)
        self.conversation_history.append({"speaker": speaker, "message": message, "timestamp": timestamp})

    def clear_history(self):
        """Clear chat history"""
        reply = QMessageBox.question(self, "Clear History", "Clear all conversation history?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.chat_display.clear()
            self.conversation_history = []
            self.status_label.setText("History cleared")

    def change_voice(self):
        """Change voice"""
        voice_index = self.voice_combo.currentData()
        if voice_index is not None:
            self.tts_engine.set_voice(voice_index)
            logger.info(f"Voice changed to index {voice_index}")

    def change_speed(self):
        """Change speech speed"""
        speed = self.speed_slider.value()
        self.tts_engine.set_rate(speed)

        # Update label
        if speed < 100:
            speed_text = "Slow"
        elif speed < 150:
            speed_text = "Slower"
        elif speed < 200:
            speed_text = "Normal"
        elif speed < 250:
            speed_text = "Faster"
        else:
            speed_text = "Fast"

        self.speed_label.setText(speed_text)

    def update_quota_display(self):
        """Update API quota display"""
        quota_ok, remaining = self.quota_manager.check_quota("huggingface")
        status = "✓ Available" if quota_ok else "✗ Exceeded"
        self.remaining_label.setText(f"Remaining: {remaining} ({status})")

    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Reload theme if changed
            theme = self.gui_settings.get("theme", "light")
            stylesheet = get_stylesheet(theme)
            self.setStyleSheet(stylesheet)
            logger.info("Settings applied")

    def show_window(self):
        """Show window from tray"""
        self.showNormal()
        self.activateWindow()

    def hide_window(self):
        """Hide window to tray"""
        self.hide()

    def closeEvent(self, event):
        """Handle window close"""
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()

    def close_application(self):
        """Close application"""
        self.tray_icon.hide()
        self.close()
        sys.exit(0)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    main()
