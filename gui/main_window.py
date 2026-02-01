
import sys
import json
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QComboBox, QPushButton, QStackedWidget, 
                             QProgressBar, QFrame, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon

from backend.logic import DecisionEngine
from backend.workers import ScraperWorker, BenchmarkWorker
from gui.styles import DARK_THEME

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rig-Engineer: System Analyzer")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet(DARK_THEME)

        # Initialize Logic
        try:
            self.logic = DecisionEngine("data/requirements.json")
            self.apps = list(self.logic.software_info.keys())
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "data/requirements.json not found!")
            sys.exit()

        # Central Widget & Stack layout for pages
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Pages
        self.init_home_page()
        self.init_loading_page()
        self.init_results_page()
        
        # State
        self.selected_app = None
        self.scraper_data = None
        self.benchmark_data = None

    def init_home_page(self):
        self.home_page = QWidget()
        layout = QVBoxLayout(self.home_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Logo/Title
        title = QLabel("RIG-ENGINEER")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Bold))
        title.setStyleSheet("color: #BB86FC;")
        layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        subtitle = QLabel("Select an engineering application to test compatibility")
        subtitle.setStyleSheet("color: #B0B0B0; font-size: 16px;")
        layout.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)

        # Dropdown
        self.app_selector = QComboBox()
        self.app_selector.addItems(self.apps)
        self.app_selector.setFixedWidth(400)
        self.app_selector.setFixedHeight(40)
        layout.addWidget(self.app_selector, alignment=Qt.AlignmentFlag.AlignCenter)

        # Start Button
        btn_start = QPushButton("START ANALYSIS")
        btn_start.setFixedWidth(200)
        btn_start.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_start.clicked.connect(self.start_analysis)
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stacked_widget.addWidget(self.home_page)

    def init_loading_page(self):
        self.loading_page = QWidget()
        layout = QVBoxLayout(self.loading_page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(30)

        self.loading_label = QLabel("Analyzing Hardware Scanned...")
        self.loading_label.setFont(QFont("Segoe UI", 18))
        layout.addWidget(self.loading_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(500)
        self.progress_bar.setRange(0, 0) # Indeterminate
        layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.stacked_widget.addWidget(self.loading_page)

    def init_results_page(self):
        self.results_page = QWidget()
        main_layout = QVBoxLayout(self.results_page)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # Header: App Name
        self.result_title = QLabel("RESULTS: SOLIDWORKS")
        self.result_title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        self.result_title.setStyleSheet("color: #03DAC6;")
        main_layout.addWidget(self.result_title)

        # Content Area (2 Columns)
        content_layout = QHBoxLayout()
        
        # Left: Score
        left_panel = QFrame()
        left_panel.setObjectName("Card")
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.score_circle = QLabel("85%")
        self.score_circle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_circle.setStyleSheet("""
            border: 4px solid #03DAC6;
            border-radius: 75px;
            font-size: 48px;
            color: #03DAC6;
            font-weight: bold;
        """)
        self.score_circle.setFixedSize(150, 150)
        left_layout.addWidget(self.score_circle)
        
        self.status_label = QLabel("EXCELLENT")
        self.status_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.status_label.setStyleSheet("color: #03DAC6; margin-top: 10px;")
        left_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        content_layout.addWidget(left_panel, stretch=1)

        # Right: Details & Warnings
        right_panel = QFrame()
        right_panel.setObjectName("Card")
        self.right_layout = QVBoxLayout(right_panel)
        
        self.specs_label = QLabel("Specs Summary:\nCPU: ...\nRAM: ...")
        self.specs_label.setWordWrap(True)
        self.right_layout.addWidget(self.specs_label)
        
        self.warnings_scroll = QScrollArea()
        self.warnings_scroll.setWidgetResizable(True)
        
        # Container for warning items
        self.warnings_container = QWidget()
        self.warnings_layout = QVBoxLayout(self.warnings_container)
        self.warnings_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.warnings_scroll.setWidget(self.warnings_container)
        
        self.right_layout.addWidget(QLabel("Warnings / Recommendations:"))
        self.right_layout.addWidget(self.warnings_scroll)

        content_layout.addWidget(right_panel, stretch=2)
        main_layout.addLayout(content_layout)

        # Footer Button
        btn_back = QPushButton("TEST ANOTHER APP")
        btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        main_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignRight)

        self.stacked_widget.addWidget(self.results_page)

    def start_analysis(self):
        self.selected_app = self.app_selector.currentText()
        self.stacked_widget.setCurrentIndex(1)
        self.loading_label.setText(f"Scanning Hardware for {self.selected_app}...")
        
        # Start Scraper Worker
        self.scraper_thread = ScraperWorker()
        self.scraper_thread.finished.connect(self.on_scraper_finished)
        self.scraper_thread.start()

    def on_scraper_finished(self, data):
        self.scraper_data = data
        
        # Check compatibility first
        hasPassed, problems = self.logic.theoretical_compatibility_test(self.selected_app, data)
        
        if not hasPassed:
            self.show_failure(problems)
            return

        # Start Benchmarks
        self.loading_label.setText("Running Performance Benchmarks...")
        self.benchmark_thread = BenchmarkWorker()
        self.benchmark_thread.finished.connect(self.on_benchmark_finished)
        self.benchmark_thread.start()

    def on_benchmark_finished(self, bench_results):
        self.benchmark_data = bench_results
        
        # Calculate Final Score
        score, warnings = self.logic.calculate_performance_score(
            self.selected_app, self.scraper_data, self.benchmark_data
        )
        
        self.show_results(score, warnings)

    def show_results(self, score, warnings):
        self.stacked_widget.setCurrentIndex(2)
        self.result_title.setText(f"RESULTS: {self.selected_app.upper()}")
        self.score_circle.setText(f"{score}%")
        
        # Color Coding
        color = "#03DAC6" if score >= 80 else "#FFB74D" if score >= 50 else "#CF6679"
        status = "EXCELLENT" if score >= 80 else "GOOD" if score >= 50 else "WEAK"
        
        self.score_circle.setStyleSheet(f"""
            border: 4px solid {color};
            border-radius: 75px;
            font-size: 48px;
            color: {color};
            font-weight: bold;
        """)
        self.status_label.setText(status)
        self.status_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")
        
        # Specs Summary
        cpu = self.scraper_data.get("processor", "Unknown")
        ram = self.scraper_data.get("available_ram_gb", 0)
        total_ram = self.scraper_data.get("total_ram_gb", 0)
        gpu_vram = self.scraper_data.get("vram_gb", 0)
        
        self.specs_label.setText(
            f"CPU: {cpu}\n"
            f"RAM: {ram:.1f}GB Available (Total: {total_ram}GB)\n"
            f"VRAM: {gpu_vram}GB"
        )
        
        # Clear old warnings
        while self.warnings_layout.count():
            item = self.warnings_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        # Add new warnings
        if warnings:
            for w in warnings:
                self.add_warning_card(w, is_warning=True)
        else:
            self.add_warning_card("No critical warnings. System is optimized!", is_warning=False)

    def add_warning_card(self, text, is_warning=True):
        card = QFrame()
        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(10, 10, 10, 10)
        
        # Icon (Text based for now)
        icon = QLabel("⚠" if is_warning else "✔")
        icon.setFixedWidth(30)
        icon.setStyleSheet("font-size: 20px; color: " + ("#CF6679" if is_warning else "#03DAC6") + ";")
        card_layout.addWidget(icon)
        
        # Message
        msg = QLabel(text)
        msg.setWordWrap(True)
        msg.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        card_layout.addWidget(msg)
        
        # Styling
        # Warning: Red bg, Info/Success: Green/Teal bg
        bg_color = "rgba(207, 102, 121, 0.2)" if is_warning else "rgba(3, 218, 198, 0.2)"
        border_color = "#CF6679" if is_warning else "#03DAC6"
        
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 5px;
            }}
        """)
        
        self.warnings_layout.addWidget(card)

    def show_failure(self, problems):
        QMessageBox.warning(self, "Compatibility Check Failed", 
                            "Your system does not meet the requirements:\n\n" + "\n".join(problems))
        self.stacked_widget.setCurrentIndex(0)

