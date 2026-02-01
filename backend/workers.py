from PyQt6.QtCore import QThread, pyqtSignal
from backend.scraper import HardwareScraper
from backend.benchmark import BenchmarkEngine

class ScraperWorker(QThread):
    finished = pyqtSignal(dict)
    
    def run(self):
        scraper = HardwareScraper()
        data = scraper.get_all_specs()
        self.finished.emit(data)

class BenchmarkWorker(QThread):
    finished = pyqtSignal(dict)
    
    def run(self):
        benchmark = BenchmarkEngine()
        results = benchmark.run_all_benchmarks()
        self.finished.emit(results)
