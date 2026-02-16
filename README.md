# Corvin-Python-Bytecode-Disassembler
# WIP
 ⠀⠘⣄⠹⣿⣿⣧⠀⠀⠀⠈⡷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡘⢀⢃⠔⢊⠡⠤

 ⠀⠀⠹⡄⢹⣿⣿⣷⠀⠀⠀⠉⠉⠀⠐⠚⠦⣀⠀⠀⠀⠀⠀⡇⠸⢡⠞⠁⣀⣀

 ⠀⠀⠹⡄⢿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢄⡀⠤⠄⠒⠂⠉⠉⠁⠀⠀

 ⠒⠒⠒⠒⢻⢮⣾⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠

 ⠀⠀⠰⢂⣎⣿⡟⡇⢀⣠⠒⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣴⣶⣿⣿⣿⣿

 ⠴⠥⠒⢊⡟⣿⣧⡇⡎⠻⣯⠿⢠⠀⠀⢀⣀⣀⣀⡀⠀⣿⣿⣿⣿⣿⠟⠋⠉⠀

 ⠀⠀⠀⠀⠇⠻⠿⠀⠀⠀⠀⠜⢁⠔⠈⣠⣿⣿⣿⠃⠀⢿⣿⠟⠉⠀⠀⠀⠀⠀

 ⠀⠀⠀⠀⠙⡄⠀⡀⠀⠀⠀⣴⣿⣿⡿⢋⣠⠟⠁⡀⠀⠀⠉⠢⣤⡤⠤⠖⠒⠀

 ⠀⠀⠀⠀⠀⠘⢄⠙⠃⠀⠀⠀⠉⠉⠉⠁⣀⢴⡮⢣⠀⠀⠀⠀⠈⠳⡄⠀⠀⠀

 ⠀⠀⠀⠀⠀⠀⠀⠉⠒⠠⡤⠄⠤⠰⠦⠝⠂⠁⠀⠈⢆⠸⡦⡀⠀⠀⠈⢢⠀⠀

 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⠑⠢⢀⡀⠀⠀⣀⠔⠈⠈⢃⠹⢮⡑⠢⡀⠀⢣⢀

 ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡄⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠑⡆⠉⠢⣀⠑⡀⢃

 ⠀⠀⠀⠀⠀⠀⠀⢀⠔⠁⢡⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠑⣾⡘

 ⠀⠀⠀⠀⠀⢀⠔⠁⠀⠀⠀⢳⣄⡀⠀⡇⠀⠀⠀⠀⢀⠇⢀⠴⠃⠀⠀⠀⠺⠘
 
 ⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⢪⠻⢄⡀⠀⠀⠀⢀⣞⠔⠁⠀⠀⠀⠀⠀⠀⠀


lil' fun tool i made :3

## Features

- Parse .pyc files from Python 3.5 to 3.12
- Disassemble bytecode into human-readable instructions
- Analyze bytecode for jumps, returns, and control flow
- Generate control flow graphs (CFG)
- Export to multiple formats (DOT, JSON, text)
- Extract nested functions and code objects
- Command-line interface for quick analysis

## Installation

```bash
git clone https://github.com/Kittyweed/Corvin-Python-Bytecode-Disassembler.git
cd Corvin-Python-Bytecode-Disassembler
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Basic disassembly:
```bash
python main.py -f file.pyc --disassemble
```

Show file information:
```bash
python main.py -f file.pyc --info
```

Generate control flow graph:
```bash
python main.py -f file.pyc --cfg
```

Export to DOT format:
```bash
python main.py -f file.pyc --dot output.dot
```

Export to JSON format:
```bash
python main.py -f file.pyc --json output.json
```

Show all analysis:
```bash
python main.py -f file.pyc --all
```

### Python API

```python
from src.analyzer import PycReader
from src.disassembler import BytecodeDisassembler
from src.visualization import ControlFlowAnalyzer, CFGVisualizer

# Read .pyc file
pyc_reader = PycReader("file.pyc")
code_object = pyc_reader.get_code_object()

# Disassemble bytecode
disassembler = BytecodeDisassembler(code_object)
print(disassembler.print_disassembly())

# Analyze control flow
cfg = ControlFlowAnalyzer(disassembler)
visualizer = CFGVisualizer(cfg)
visualizer.print_graph()
visualizer.save_dot_file("output.dot")
```

## Project Structure

```
src/
  ├── disassembler/     Core bytecode disassembly
  │   ├── bytecode.py   BytecodeDisassembler class
  │   └── instruction.py Instruction class
  ├── analyzer/         .pyc file analysis
  │   └── pyc_reader.py  PycReader class
  └── visualization/    Control flow visualization
      ├── control_flow.py ControlFlowAnalyzer class
      └── visualizer.py   CFGVisualizer class
examples/               Example scripts and sample code
tests/                  Test suite
main.py                 Command-line interface
```

## Components

### PycReader
Reads and parses .pyc file headers and code objects.
- Detects Python version from magic number
- Extracts marshal-encoded code objects
- Retrieves file metadata (timestamp, size)

### BytecodeDisassembler
Converts bytecode to readable instructions.
- Parses instruction opcodes and arguments
- Resolves constants, names, and variables
- Identifies control flow instructions (jumps, returns)

### ControlFlowAnalyzer
Builds control flow graphs from bytecode.
- Identifies basic blocks
- Tracks instruction dependencies
- Maps predecessors and successors

### CFGVisualizer
Exports control flow graphs in multiple formats.
- DOT format for Graphviz
- JSON for programmatic analysis
- Text-based visualization

## Supported Python Versions

- Python 3.5 - 3.12

## Examples

Create sample .pyc file:
```bash
cd examples
python -c "import py_compile; py_compile.compile('sample.py')"
python usage_example.py
```

Run tests:
```bash
python tests/test_disassembler.py
```

## Output Formats

### DOT Format
Compatible with Graphviz:
```bash
dot -Tpng output.dot -o output.png
```

### JSON Format
Structured representation for programmatic access:
```json
{
  "blocks": {...},
  "edges": [{"from": 0, "to": 1}]
}
```

## Requirements

- Python 3.6+
- graphviz (optional, for DOT visualization)

## License

MIT

## Author

Kittyweed
