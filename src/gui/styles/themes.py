"""GUI Styles and Themes"""


DARK_STYLESHEET = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
}

QTextEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #444444;
    border-radius: 5px;
    padding: 5px;
    font-family: 'Courier New';
}

QLabel {
    color: #ffffff;
}

QComboBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #444444;
    border-radius: 5px;
    padding: 5px;
}

QComboBox::drop-down {
    border: none;
}

QSlider::groove:horizontal {
    background-color: #444444;
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background-color: #4CAF50;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}

QPushButton {
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
    background-color: #555555;
}

QPushButton:hover {
    background-color: #666666;
}

QPushButton:pressed {
    background-color: #444444;
}

QStatusBar {
    background-color: #2d2d2d;
    color: #ffffff;
    border-top: 1px solid #444444;
}

QDialog {
    background-color: #1e1e1e;
    color: #ffffff;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 8px 20px;
    border-right: 1px solid #444444;
}

QTabBar::tab:selected {
    background-color: #4CAF50;
}
"""

LIGHT_STYLESHEET = """
QMainWindow {
    background-color: #f5f5f5;
    color: #000000;
}

QWidget {
    background-color: #f5f5f5;
    color: #000000;
}

QTextEdit {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 5px;
    font-family: 'Courier New';
}

QLabel {
    color: #000000;
}

QComboBox {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #cccccc;
    border-radius: 5px;
    padding: 5px;
}

QComboBox::drop-down {
    border: none;
}

QSlider::groove:horizontal {
    background-color: #dddddd;
    height: 8px;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background-color: #4CAF50;
    width: 18px;
    margin: -5px 0;
    border-radius: 9px;
}

QPushButton {
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px;
    font-weight: bold;
    background-color: #999999;
}

QPushButton:hover {
    background-color: #777777;
}

QPushButton:pressed {
    background-color: #555555;
}

QStatusBar {
    background-color: #eeeeee;
    color: #000000;
    border-top: 1px solid #cccccc;
}

QDialog {
    background-color: #f5f5f5;
    color: #000000;
}

QTabBar::tab {
    background-color: #eeeeee;
    color: #000000;
    padding: 8px 20px;
    border-right: 1px solid #cccccc;
}

QTabBar::tab:selected {
    background-color: #4CAF50;
    color: #ffffff;
}
"""


def get_stylesheet(theme: str = "light") -> str:
    """Get stylesheet for theme"""
    if theme.lower() == "dark":
        return DARK_STYLESHEET
    else:
        return LIGHT_STYLESHEET
