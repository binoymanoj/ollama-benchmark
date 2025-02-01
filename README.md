# Ollama Model Benchmark Tool

A Python-based benchmarking tool for comparing different Ollama models' performance in Next.js development tasks. This tool helps developers evaluate and choose the most efficient model for their coding assistance needs.


![Ollama Benchmark Output](screenshots/preview.png)
*Sample benchmark results comparing response times across different models*

## Features

- Benchmark multiple Ollama models simultaneously
- Measure response times and performance metrics
- Test models against real-world Next.js development scenarios
- Generate detailed performance reports
- Isolated testing environment using Python virtual environment

## Prerequisites

- Python 3.8 or higher
- Ollama installed and running locally
- At least one Ollama model pulled and ready to use

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/binoymanoj/ollama-benchmark
cd ollama-benchmark
```

2. Create and activate virtual environment:

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Unix/MacOS:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the benchmark:
```bash
python benchmark.py
```

## Configuration

### Modifying Test Models

Edit the `models` list (line 76) in `benchmark.py` to include your installed Ollama models:

```python
models = ["codellama", "mistral", "neural-chat"]  # Replace with your models
```

### Customizing Test Cases

Add or modify test cases in `benchmark.py`:

```python
test_cases = [
    {
        "name": "Custom Test",
        "prompt": "Your custom prompt here"
    }
]
```

## Test Cases

Default test cases cover common Next.js development scenarios:

1. Component Creation
   - Tests model's ability to generate responsive React components
   - Evaluates understanding of Next.js patterns

2. API Route Implementation
   - Tests knowledge of Next.js API routes
   - Evaluates authentication handling

3. Data Fetching
   - Tests understanding of Next.js data fetching methods
   - Evaluates server-side rendering knowledge

## Output Format

The benchmark generates a JSON report with:

```json
{
  "summary": {
    "model_name": {
      "average_response_time": float,
      "min_response_time": float,
      "max_response_time": float
    }
  },
  "detailed_results": {
    "model_name": {
      "response_times": [...],
      "responses": [...]
    }
  }
}
```

## Project Structure

```
ollama-benchmark/
├── LICENSE
├── README.md
├── benchmark.py
├── requirements.txt
├── screenshots/
└── venv/
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Ollama team for providing the model serving infrastructure
- Next.js community for inspiration on test cases

## Support

If you encounter any issues or have questions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include your system information and Ollama version

---

Made with ❤️ by Binoy Manoj
