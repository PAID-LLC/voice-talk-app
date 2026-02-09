"""GUI Application Launcher"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.config.logger import LoggerManager, get_logger

logger = get_logger(__name__)


def main():
    """Launch GUI application"""
    # Initialize logging
    LoggerManager.initialize()
    logger.info("Starting Voice Talk GUI Application")

    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Voice Talk Application")
    app.setApplicationVersion("0.1.0")

    # Create and show main window
    window = MainWindow()
    window.show()

    logger.info("GUI application launched")

    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
