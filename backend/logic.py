import platform
import json

class DecisionEngine:
    def __init__(self, requirements_path="data/requirements.json"):
        with open(requirements_path, "r") as f:
            self.software_info = json.load(f)

    def theoretical_compatibility_test(self, target_app, scraper_data):
        target_info = self.software_info.get(target_app) 
        if not target_info:
            return False, ["Application not found in database."]
        
        req_ram = target_info.get("min_ram", 0) 
        req_vram = target_info.get("min_vram", 0) 
        req_os = target_info.get("os_version", "Any")
        
        req_storage = target_info.get("min_storage", 0)  # GB
        
        problems = []
        messages = [] # Non-blocking messages (Info/Warnings)

        if scraper_data.get("total_ram_gb", 0) < req_ram:
            problems.append(f"Insufficient Total RAM: {req_ram}GB required.")
        
        if scraper_data.get("vram_gb", 0) < req_vram:
            problems.append(f"Insufficient VRAM: {req_vram}GB required.")

        # Disk Storage Check
        disks = scraper_data.get("disks", [])
        compatible_disks = [d for d in disks if d["free_gb"] >= req_storage]
        
        if not compatible_disks:
            problems.append(f"Insufficient Storage checking all drivers: {req_storage}GB required.")
        else:
            # Tell user which disks are valid
            valid_drives = [f"{d['device']} ({d['free_gb']}GB free)" for d in compatible_disks]
            messages.append(f"INFO: Installation possible on: {', '.join(valid_drives)}")

        os_name = scraper_data.get("os_name", "")
        if platform.system() == "Windows":
            if req_os == "Any":
                pass # Herhangi bir Windows sürümü kabul
            elif "Windows" in os_name and "Windows" in req_os:
                try:
                    # Sadece sayıları alıp karşılaştırıyoruz (Örn: "Windows 10" -> 10)
                    current_v = int(''.join(filter(str.isdigit, os_name)))
                    req_v = int(''.join(filter(str.isdigit, req_os)))
                    
                    if current_v < req_v:
                        problems.append(f"OS Mismatch: {req_os} or newer required.")
                except:
                    # Sayı bulunamazsa klasik string kontrolüne dön
                    if req_os != os_name:
                        problems.append(f"OS Mismatch: {req_os} required.")
            elif req_os != os_name:
                problems.append(f"OS Mismatch: {req_os} required.")
        else:
            print("Unsupported OS: Analysis targets Windows systems. Your OS ({os_name}) is incompatible.")
            
        if problems:
            return False, problems
            
        if messages:
            for msg in messages:
                print(msg)
        
        return True, []


    def calculate_performance_score(self, target_app, scraper_data, benchmark_data):
        target_info = self.software_info.get(target_app)
        if not target_info:
            return 0, ["Application data missing."]
        
        performance_score = 0
        warnings = []

        #RAM Tests (30 points total)
        req_ram = target_info.get("min_ram", 0) 
        available_ram = scraper_data.get("available_ram_gb", 0) 

        if available_ram >= req_ram + 2:
            performance_score += 15
        elif available_ram >= req_ram:
            performance_score += 10
        else:
            performance_score += 5
            warnings.append("Low available RAM. Please close background applications.")

        ram_latency = benchmark_data.get("ram_test_speed", 99)
        if ram_latency <= 0.1:
            performance_score += 15
        elif 0.1 < ram_latency <= 0.25:
            performance_score += 10
        elif 0.25 < ram_latency <= 0.5:
            performance_score += 5
        else:
            warnings.append("High RAM latency detected. Your memory response is slow.")

        #CPU Test (40 points max)
        cpu_duration = benchmark_data.get("cpu_stress_time", 99)
        if cpu_duration <= 0.4:
            performance_score += 40
        elif 0.4 < cpu_duration <= 0.8:
            performance_score += 25
        elif 0.8 < cpu_duration <= 1.5:
            performance_score += 10
        else:
            warnings.append("CPU performance is below optimal levels for this task.")

        #Thermal Deviation (20 points max)
        thermal_deviation = benchmark_data.get("thermal_deviation", 100)
        if thermal_deviation < 5:
            performance_score += 20
        elif 5 <= thermal_deviation < 15:
            performance_score += 10
        else:
            warnings.append("High thermal deviation! Your system might be overheating (Throttling).")

        #Disk Speed Test (10 points max)
        disk_speed = benchmark_data.get("disk_test_speed", 99)
        if disk_speed <= 0.3:
            performance_score += 10
        elif 0.3 < disk_speed <= 0.8:
            performance_score += 5
        else:
            warnings.append("Slow storage speed. This may cause long loading times.")

        #Battery & Power Control
        if not benchmark_data.get("is_plugged", True):
            performance_score -= 25
            warnings.append("System on battery. Power is throttled. Plug in for max performance!")
        
        # TODO: I think there is no need to decrease the score for battery percentage and plugged.

        if benchmark_data.get("battery_percent", 100) <= 20:
            performance_score -= 15
            warnings.append("Battery is critical (<20%). High-performance mode is disabled.")

        #Network Control
        ping = benchmark_data.get("network_test_speed", 0)
        if ping > 150:
            warnings.append(f"High network latency ({ping}ms). Cloud tools may experience lag.")

        # Skoru 0-100 arasında sınırla
        performance_score = max(0, min(100, performance_score))
        return performance_score, warnings
        
        

        
        
        
        

        
             
