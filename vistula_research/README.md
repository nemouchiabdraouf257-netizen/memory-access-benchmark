# Sequential vs. Strided Memory Access Benchmark

Reproducibility package for the Architecture of Computers (2026/27) research project at Vistula University by Abderaouf Nemouchi (ID: 77510).

## Contents
- `benchmark.py`: Python script measuring sequential (`stride = 1`) and strided (`stride = 8, 16, 64`) array reads across sizes `2,000`, `32,000`, `500,000`, and `4,000,000` elements (`3` warm-up runs and `20` measured runs per configuration)[cite: 5].
- `results.csv`: Raw and summary timing output generated on the test machine (`Python 3.15.2`, `Windows-11-10.0.26200-SP0`, `8` CPUs)[cite: 5].
- `README.md`: Documentation describing how to run the benchmark and reproduce the results.

## How to Run
1. Open Command Prompt / PowerShell / Terminal in the project directory[cite: 2, 4].
2. Run:
   ```bash
   python benchmark.py