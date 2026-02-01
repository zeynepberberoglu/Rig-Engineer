
DARK_THEME = """
QMainWindow {
    background-color: #121212;
    color: #FFFFFF;
}

QWidget {
    background-color: #121212;
    color: #FFFFFF;
    font-family: 'Segoe UI', sans-serif;
    font-size: 14px;
}

QLabel {
    color: #E0E0E0;
}

QPushButton {
    background-color: #03DAC6;
    color: #000000;
    border-radius: 5px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 16px;
}

QPushButton:hover {
    background-color: #018786;
}

QPushButton:disabled {
    background-color: #333333;
    color: #666666;
}

QComboBox {
    background-color: #1E1E1E;
    border: 1px solid #333333;
    border-radius: 5px;
    padding: 8px;
    color: #FFFFFF;
}

QComboBox::drop-down {
    border: none;
}

QComboBox QAbstractItemView {
    background-color: #1E1E1E;
    selection-background-color: #03DAC6;
    selection-color: #000000;
}

QProgressBar {
    border: 1px solid #333333;
    border-radius: 5px;
    text-align: center;
    background-color: #1E1E1E;
    color: #FFFFFF;
}

QProgressBar::chunk {
    background-color: #BB86FC;
    width: 20px;
}

QScrollArea {
    border: none;
}

QFrame#Card {
    background-color: #1E1E1E;
    border-radius: 10px;
    padding: 15px;
}
"""
