from backend.benchmark import BenchmarkEngine

# 1. Initialize the benchmark engine
engine = BenchmarkEngine()

print("🚀 Starting all benchmark tests, please wait...\n")

# 2. Use the 'all-in-one' method to run all tests sequentially
all_results = engine.run_all_benchmarks()

# 3. Print the results to the console
print("--- TEST RESULTS ---")
for test_name, value in all_results.items():
    print(f"{test_name}: {value}")

print("\n✅ All tests completed successfully.")

#stability nerede