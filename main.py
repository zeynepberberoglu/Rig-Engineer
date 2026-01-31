try:
    import sys
    import time
    from backend.scraper import HardwareScraper
    from backend.benchmark import BenchmarkEngine
    from backend.logic import DecisionEngine
except ImportError as e:
    print(f"Import Error: {e}")
    print("Make sure your files are in the 'backend' folder with an '__init__.py' file.")
    sys.exit()

def main():
    print(" WELCOME TO RIG-ENGINEER: SYSTEM PERFORMANCE ANALYZER ")


    # 1-) start
    # read the requirements.json file
    try:
        logic = DecisionEngine("data/requirements.json")
    except FileNotFoundError:
        print(" Error: 'data/requirements.json' not found!")
        return
    
    apps = list(logic.software_info.keys())
    print("Available Engineering Programs: ")
    for i,app in enumerate(apps,1):
        print(f"{i}.{app}")

    try:
        target_index = int(input("Please select a program number to test: "))
        target_app = apps[target_index-1]
    except (ValueError, IndexError):
        print("Invalid selection. Exiting...")
        return
    
    scraper = HardwareScraper()
    scraper_data = scraper.get_all_specs() #tüm scraper datayı al

    # 2-) donanım taraması ilk test
    print(f"\n STEP 1- Scanning hardware for {target_app}...")
    print("This will take about 20-30 seconds. Please wait...")

    hasPassed , problems = logic.theoretical_compatibility_test(target_app,scraper_data)

    if hasPassed == False:
        print(problems)
        sys.exit()
    elif hasPassed==True:
        print("Passed the first test")
    


    benchmark = BenchmarkEngine()
    bench_results = benchmark.run_all_benchmarks() #data paketini al


    print("\n STEP 3-Calculating Performance Score...")
    score, warnings = logic.calculate_performance_score(target_app, scraper_data, bench_results)
    print(f"FINAL REPORT: {target_app.upper()}")
    status = "EXCELLENT" if score >= 80 else "GOOD" if score >= 50 else "WEAK"
    print(f"OVERALL SCORE  : {score}/100")
    print(f"PERFORMANCE    : {status}")

    if warnings:
        print("CRITICAL WARNINGS:")
        for warn in warnings:
            print(f"   -{warn}")
    else:
        print("Your system is perfectly optimized for this task!")


if __name__ == "__main__":
    try:
       main()
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user. See you next time!")
