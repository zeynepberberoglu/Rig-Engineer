import os
import psutil
import platform
import GPUtil
import subprocess

class HardwareScraper:
    def __init__(self):
        """Initialize the hardware scraper module."""
        pass

    def get_static_info(self):
        """Retrieves static system information such as CPU model and total RAM."""
        try:
            cpu_name = subprocess.check_output("wmic cpu get name", shell=True).decode().split('\n')[1].strip()
        except Exception:
            cpu_name = platform.processor()

        os_base = platform.system()
        if os_base == "Windows":
            os_name = f"{os_base} {platform.release()}"
        else:
            os_name = os_base

        return {
            "processor": cpu_name,
            "total_ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "os": os_name
        }
    
    def get_dynamic_info(self):
        """Retrieves real-time system metrics like CPU and RAM usage percentage."""
        return {
            "cpu_usage_pct": psutil.cpu_percent(interval=1),
            "ram_usage_pct": psutil.virtual_memory().percent,
            "gpu_status": self._get_gpu_info()
        }

    def get_disk_info(self):
        #Finds all disk partitions and their free space
        disks = []
        partitions = psutil.disk_partitions()
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                free_gb = round(usage.free / (1024**3), 2)
                disks.append({
                    "device" : p.device,
                    "mountpoint": p.mountpoint,
                    "fstype": p.fstype,
                    "free_gb": free_gb,
                    "total_gb": round(usage.total / (1024**3), 2)
                })
            except PermissionError:
                continue
        return disks


    def _get_gpu_info(self):
        """Checks for available GPUs and returns details."""
        try:
            gpus = GPUtil.getGPUs()

            if gpus:
                return [
                    {
                        "name": g.name, 
                        "load": g.load * 100, 
                        "temp": g.temperature,
                        "memoryTotal": g.memoryTotal 
                    } for g in gpus
                ]
        except Exception:
            pass

        if platform.system() == "Windows" and not gpus:
            try:
                # Get absolute path to the PowerShell script in the same directory
                current_dir = os.path.dirname(os.path.abspath(__file__))
                script_path = os.path.join(current_dir, "get_vram.ps1")
                
                cmd = f'powershell -ExecutionPolicy Bypass -File "{script_path}"'
                output = subprocess.check_output(cmd,shell=True).decode("utf-8").strip()


                lines = output.split("\n")
                for line in lines:
                    line = line.replace('"', '').strip()
                    
                    # Skip empty lines or the Header line (DriverDesc)
                    if not line or "DriverDesc" in line:
                        continue
                        
                    parts = line.split(",")
                    
                    if len(parts) >= 2:
                        try:
                            # 1. WMI'dan gelen Byte'ı MB'a çeviriyoruz (1024^2)
                            # parts[1] (QwMemorySize) string olduğu için int() ile çevir
                            ram_bytes = int(parts[1])
                            vram_mb = ram_bytes / (1024**2) 
                        except:
                            vram_mb = 0

                        # parts[0] -> DriverDesc (Name)
                        name = parts[0].strip()
                            
                        return[
                            {
                            "name": name,
                            "load": "N/A", 
                            "temp": "N/A", 
                            "memoryTotal": vram_mb,
                            }
                        ]
            except Exception as e:
                print(f"WMI Error: {e}")
        
        return gpus
            
        
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
            gpu_name = first_gpu.get("name", "Unknown GPU")
            is_dedicated = True
        else:
            vram_gb = 0 
            gpu_name = "Integrated Graphics / Unknown"
            is_dedicated = False

        scraper_data = {
            "os_name": static["os"],
            "processor": static["processor"],
            "total_ram_gb": static["total_ram_gb"],
            "available_ram_gb": self.get_available_ram(),
            "vram_gb": vram_gb,
            "gpu_name": gpu_name,
            "is_dedicated": is_dedicated,
            "disks": self.get_disk_info()
        }
        return scraper_data
