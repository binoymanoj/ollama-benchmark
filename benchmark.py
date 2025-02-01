import time
import json
from typing import List, Dict
import requests

class OllamaBenchmark:
    def __init__(self, models: List[str], base_url: str = "http://localhost:11434"):
        self.models = models
        self.base_url = base_url
        self.results = {}

    def generate_response(self, model: str, prompt: str) -> tuple:
        start_time = time.time()
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            }
        )
        
        end_time = time.time()
        response_time = end_time - start_time
        
        if response.status_code == 200:
            return response.json()["response"], response_time
        else:
            return None, response_time

    def run_benchmark(self, test_cases: List[Dict]):
        for model in self.models:
            print(f"\nTesting model: {model}")
            model_results = {
                "response_times": [],
                "responses": []
            }
            
            for case in test_cases:
                print(f"Running test case: {case['name']}")
                response, response_time = self.generate_response(model, case["prompt"])
                
                model_results["response_times"].append({
                    "test_case": case["name"],
                    "time": response_time
                })
                model_results["responses"].append({
                    "test_case": case["name"],
                    "response": response
                })
                
                print(f"Response time: {response_time:.2f} seconds")
                
            self.results[model] = model_results
            
    def generate_report(self):
        report = {
            "summary": {},
            "detailed_results": self.results
        }
        
        for model in self.models:
            times = [r["time"] for r in self.results[model]["response_times"]]
            report["summary"][model] = {
                "average_response_time": sum(times) / len(times),
                "min_response_time": min(times),
                "max_response_time": max(times)
            }
            
        return report

# Example usage
if __name__ == "__main__":
    # List your models here
    models = ["llama3.2", "deepseek-r1"]  # Replace with your actual models
    
    # Define test cases relevant to Next.js development
    test_cases = [
        {
            "name": "Component Creation",
            "prompt": "Create a Next.js component for a responsive navigation bar with authentication status."
        },
        {
            "name": "API Route",
            "prompt": "Write a Next.js API route handler for user authentication using JWT."
        },
        {
            "name": "Data Fetching",
            "prompt": "Show how to implement server-side data fetching in Next.js using getServerSideProps."
        }
    ]
    
    # Run benchmark
    benchmark = OllamaBenchmark(models)
    benchmark.run_benchmark(test_cases)
    
    # Generate and print report
    report = benchmark.generate_report()
    print("\nBenchmark Results:")
    print(json.dumps(report["summary"], indent=2))
