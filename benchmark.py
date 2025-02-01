import time
import json
import curses
import subprocess
import requests
from typing import List, Dict
import sys

def check_ollama_service() -> bool:
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/version")
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def get_ollama_models() -> List[str]:
    """Get list of available models from ollama list command"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        # Skip header line and empty lines, extract model names
        models = [line.split()[0] for line in result.stdout.split('\n')[1:] if line.strip()]
        return models
    except subprocess.CalledProcessError:
        print("Error running 'ollama list' command")
        return []

def select_models(stdscr) -> List[str]:
    """Interactive model selection using curses"""
    # Set up curses
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    
    # Get available models
    models = get_ollama_models()
    if not models:
        return []
        
    # Initialize selection variables
    current_pos = 0
    selected = [False] * len(models)
    
    while True:
        # Display models
        stdscr.clear()
        stdscr.addstr(0, 0, "Select models using SPACE, navigate with UP/DOWN or j/k. Press ENTER when done.\n")
        
        for idx, model in enumerate(models):
            prefix = '[*]' if selected[idx] else '[ ]'
            style = curses.A_REVERSE if idx == current_pos else curses.A_NORMAL
            stdscr.addstr(f"{prefix} {model}\n", style)
        
        # Get user input
        key = stdscr.getch()
        
        # Handle navigation
        if key in [curses.KEY_UP, ord('k')] and current_pos > 0:
            current_pos -= 1
        elif key in [curses.KEY_DOWN, ord('j')] and current_pos < len(models) - 1:
            current_pos += 1
        # Handle selection
        elif key == ord(' '):
            selected[current_pos] = not selected[current_pos]
        # Handle completion
        elif key == ord('\n'):
            break
            
    return [model for model, is_selected in zip(models, selected) if is_selected]

class OllamaBenchmark:
    def __init__(self, base_url: str = "http://localhost:11434"):
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
            
    def run_benchmark(self, models: List[str], test_cases: List[Dict]):
        self.models = models
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

def main():
    # Check if Ollama service is running
    if not check_ollama_service():
        print("Error: Ollama service is not running. Please start the service with 'systemctl start ollama' or 'ollama serve'")
        sys.exit(1)
    
    # Initialize curses for model selection
    selected_models = curses.wrapper(select_models)
    
    if not selected_models:
        print("No models selected. Exiting...")
        return
        
    print(f"Selected models: {selected_models}")
    
    # Define test cases
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
    benchmark = OllamaBenchmark()
    benchmark.run_benchmark(selected_models, test_cases)
    
    # Generate and print report
    report = benchmark.generate_report()
    print("\nBenchmark Results:")
    print(json.dumps(report["summary"], indent=2))

if __name__ == "__main__":
    main()
