"""Settings Dialog - Application Configuration"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QSpinBox, QCheckBox, QTabWidget,
    QWidget, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from src.config.logger import get_logger
from src.audio.capture import AudioCapture
from src.audio.playback import AudioPlayback

logger = get_logger(__name__)


class SettingsDialog(QDialog):
    """Settings and configuration dialog"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Advanced Settings")
        self.setGeometry(200, 200, 600, 500)
        self.setup_ui()

    def setup_ui(self):
        """Setup settings dialog UI"""
        layout = QVBoxLayout()

        # Tabs
        tabs = QTabWidget()

        # Audio tab
        audio_tab = self.create_audio_tab()
        tabs.addTab(audio_tab, "Audio")

        # API tab
        api_tab = self.create_api_tab()
        tabs.addTab(api_tab, "API Keys")

        # Appearance tab
        appearance_tab = self.create_appearance_tab()
        tabs.addTab(appearance_tab, "Appearance")

        layout.addWidget(tabs)

        # Buttons
        button_layout = QHBoxLayout()

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def create_audio_tab(self):
        """Create audio settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Input device
        layout.addWidget(QLabel("Input Device (Microphone):"))
        self.input_device_combo = QComboBox()
        capture = AudioCapture()
        devices = capture.list_devices()
        for device in devices:
            self.input_device_combo.addItem(f"{device['name']} ({device['channels']}ch)",
                                           device['index'])
        layout.addWidget(self.input_device_combo)

        # Output device
        layout.addWidget(QLabel("Output Device (Speaker):"))
        self.output_device_combo = QComboBox()
        playback = AudioPlayback()
        devices = playback.list_output_devices()
        for device in devices:
            self.output_device_combo.addItem(f"{device['name']} ({device['channels']}ch)",
                                            device['index'])
        layout.addWidget(self.output_device_combo)

        # Sample rate
        layout.addWidget(QLabel("Sample Rate (Hz):"))
        self.sample_rate_combo = QComboBox()
        self.sample_rate_combo.addItems(["8000", "16000", "44100", "48000"])
        self.sample_rate_combo.setCurrentText("16000")
        layout.addWidget(self.sample_rate_combo)

        # Volume
        layout.addWidget(QLabel("Volume:"))
        self.volume_spin = QSpinBox()
        self.volume_spin.setMinimum(0)
        self.volume_spin.setMaximum(100)
        self.volume_spin.setValue(90)
        layout.addWidget(self.volume_spin)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_api_tab(self):
        """Create API keys tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # HuggingFace
        layout.addWidget(QLabel("HuggingFace API Token:"))
        self.hf_token_input = QLineEdit()
        self.hf_token_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.hf_token_input)

        # Azure
        layout.addWidget(QLabel("Azure Speech API Key:"))
        self.azure_key_input = QLineEdit()
        self.azure_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.azure_key_input)

        layout.addWidget(QLabel("Azure Region:"))
        self.azure_region_input = QLineEdit()
        self.azure_region_input.setText("eastus")
        layout.addWidget(self.azure_region_input)

        # Google
        layout.addWidget(QLabel("Google Cloud Credentials (JSON file):"))
        google_layout = QHBoxLayout()
        self.google_file_input = QLineEdit()
        self.google_file_input.setReadOnly(True)
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_google_file)
        google_layout.addWidget(self.google_file_input)
        google_layout.addWidget(browse_button)
        layout.addLayout(google_layout)

        # Test button
        test_button = QPushButton("Test API Connection")
        test_button.clicked.connect(self.test_api)
        layout.addWidget(test_button)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_appearance_tab(self):
        """Create appearance settings tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Theme
        layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        layout.addWidget(self.theme_combo)

        # Font size
        layout.addWidget(QLabel("Chat Font Size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setMinimum(8)
        self.font_size_spin.setMaximum(24)
        self.font_size_spin.setValue(10)
        layout.addWidget(self.font_size_spin)

        # Auto-save
        self.autosave_check = QCheckBox("Auto-save conversation history")
        self.autosave_check.setChecked(True)
        layout.addWidget(self.autosave_check)

        # Show timestamps
        self.timestamps_check = QCheckBox("Show message timestamps")
        self.timestamps_check.setChecked(True)
        layout.addWidget(self.timestamps_check)

        # Minimize to tray
        self.tray_check = QCheckBox("Minimize to system tray")
        self.tray_check.setChecked(True)
        layout.addWidget(self.tray_check)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def browse_google_file(self):
        """Browse for Google credentials file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Google Credentials JSON",
            "",
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.google_file_input.setText(file_path)

    def test_api(self):
        """Test API connections"""
        hf_token = self.hf_token_input.text()

        if not hf_token:
            QMessageBox.warning(self, "No API Key", "Please enter HuggingFace API token")
            return

        QMessageBox.information(self, "API Test",
                              "Testing API connections...\n\n"
                              "This feature coming soon!")

    def save_settings(self):
        """Save settings"""
        QMessageBox.information(self, "Settings Saved",
                              "Settings have been saved!\n\n"
                              "Settings persistence coming soon!")
        self.accept()
