import psutil
import platform
import GPUtil

class HardwareScraper:

    def __init__(self):
        """Initialize the hardware scraper module."""
        pass


    def get_static_info(self):
        """Retrieves static system information such as CPU model and total RAM."""
        return {
            "processor": platform.processor(),
            "total_ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "os": platform.system()
        }
    
    def get_dynamic_info(self):
        """Retrieves real-time system metrics like CPU and RAM usage percentage."""
        return {
            "cpu_usage_pct": psutil.cpu_percent(interval=1),
            "ram_usage_pct": psutil.virtual_memory().percent,
            "gpu_status": self._get_gpu_info()
        }
    
    def _get_gpu_info(self):
        """Checks for available GPUs and returns their current load/temperature."""
        try:
            gpus = GPUtil.getGPUs()
            return [{"name": g.name, "load": g.load * 100, "temp": g.temperature} for g in gpus]
        except Exception:
            return []