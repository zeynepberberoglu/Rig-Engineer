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
        """Checks for available GPUs and returns their current info as a list of dicts."""
        try:
            gpus = GPUtil.getGPUs()

            return [
                {
                    "name": g.name, 
                    "load": g.load * 100, 
                    "temp": g.temperature,
                    "memoryTotal": g.memoryTotal 
                } for g in gpus
            ]
        except Exception:
            return []
        
    def get_available_ram(self):
        """Retrieves currently available system memory."""
        mem = psutil.virtual_memory()
        
        # Converting bytes into GB
        available_ram_gb = mem.available / (1024 ** 3)
        
        return round(available_ram_gb, 2)



    def get_all_specs(self):
        static = self.get_static_info()
        gpus = self._get_gpu_info() 

        if gpus:
            first_gpu = gpus[0] #gpus is a dict
            vram_gb = round(first_gpu["memoryTotal"] / 1024, 1) 
            is_dedicated = True
        else:
            vram_gb = 0 
            is_dedicated = False

        scraper_data = {
            "os_name": static["os"],
            "processor": static["processor"],
            "total_ram_gb": static["total_ram_gb"],
            "available_ram_gb": self.get_available_ram(),
            "vram_gb": vram_gb,
            "is_dedicated": is_dedicated
        }
        return scraper_data
