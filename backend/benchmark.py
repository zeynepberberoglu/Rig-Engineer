import time
import os
import speedtest
import psutil

class BenchmarkEngine:
    def __init__(self):
        """Initializes the benchmarking engine for performance testing."""
        pass

    def run_cpu_stress_test(self, limit=1000000):
        """
        Calculates prime numbers up to a limit to stress the CPU.
        Returns the time taken in seconds.
        """
        start_time = time.time() 
        
        # CPU Stress Logic: Finding prime numbers
        primes = []
        # This optimization significantly reduces CPU cycles during benchmarking.
        for num in range(2, limit): 
            for i in range(2, int(num**0.5) + 1): #A number is prime if it is not divisible by any integer up to its square root.
                if (num % i) == 0:
                    break
            else:
                primes.append(num)
                
        end_time = time.time()
        duration = round(end_time - start_time, 4) #Rounding duration to 4 decimal places for clean data reporting and UI display.
        return duration

    def run_ram_latency_test(self, size=10**6):
        """
        Performs a synthetic memory stress test by allocating a large integer list and executing 
        bulk operations. This measures RAM write/read speeds and memory bus latency
        """
        start_time = time.time()
        
        # RAM Stress Logic: List manipulation
        data = [i for i in range(size)]
        data = [x * 2 for x in data]
        
        end_time = time.time()
        return round(end_time - start_time, 4)
    


    def run_disk_test(self):
        """Measures Disk Write Speed by creating a temporary 100MB file."""

        start_time = time.time()
        file_name = "test_speed.tmp"
        data = os.urandom(1024 * 1024 * 100) # 100MB of random data

        with open(file_name, "wb") as f:
            f.write(data)
        
        os.remove(file_name) # Cleanup
        end_time = time.time()
        return round(end_time - start_time, 4)
    

    def run_network_test(self):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000 # Mbps
            ping = st.results.ping
            return {"download_mbps": round(download_speed, 2), "ping_ms": ping}
        except:
            return {"download_mbps": 0, "ping_ms": 0}
    

    def get_battery_health(self):
    
        """Returns battery percentage and power plug status."""
        battery = psutil.sensors_battery()
        if battery:
            return {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "seconds_left": battery.secsleft 
            }
        else:
            return None
        
    def run_thermal_stability_test(self):
        """
        Evaluates CPU thermal stability by measuring frequency drop under load.
        This detects if the system is 'throttling' due to heat.
        """
        # Capture the initial CPU clock speed (in MHz) before the stress
        initial_speed = psutil.cpu_freq().current
        
        # Apply a short-term synthetic load to heat up the processor
        # We use a lower limit for a quick 5-10 second diagnostic
        self.run_cpu_stress_test(limit=500000)
        
        # Capture the final CPU clock speed after the stress period
        final_speed = psutil.cpu_freq().current
        
        # Calculate the stability ratio. 
        # A result near 100% indicates excellent cooling/thermal management.
        stability = (final_speed / initial_speed) * 100
        
        # Return the stability percentage rounded for clean reporting
        return round(stability, 2)