#!/usr/bin/env python3

import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.analyzer import PycReader
from src.disassembler import BytecodeDisassembler
from src.visualization import ControlFlowAnalyzer, CFGVisualizer


def analyze_single_function():
    print("Example 1: Analyzing .pyc file")
    print("=" * 80)
    
    pyc_path = Path(__file__).parent / "sample.pyc"
    
    if not pyc_path.exists():
        print(f"Creating sample.pyc from sample.py...")
        import py_compile
        py_compile.compile(
            str(Path(__file__).parent / "sample.py"),
            cfile=str(pyc_path)
        )
    
    try:
        pyc_reader = PycReader(str(pyc_path))
        
        print(pyc_reader.print_header_info())
        print()
        
        code_object = pyc_reader.get_code_object()
        disassembler = BytecodeDisassembler(code_object)
        
        print(disassembler.print_disassembly())
        print()
        
    except Exception as e:
        print(f"Error: {e}")


def analyze_control_flow():
    print("\nExample 2: Control Flow Analysis")
    print("=" * 80)
    
    pyc_path = Path(__file__).parent / "sample.pyc"
    
    if not pyc_path.exists():
        print("Creating sample.pyc...")
        import py_compile
        py_compile.compile(
            str(Path(__file__).parent / "sample.py"),
            cfile=str(pyc_path)
        )
    
    try:
        pyc_reader = PycReader(str(pyc_path))
        code_object = pyc_reader.get_code_object()
        disassembler = BytecodeDisassembler(code_object)
        cfg = ControlFlowAnalyzer(disassembler)
        visualizer = CFGVisualizer(cfg)
        
        visualizer.print_graph()
        
        dot_output = Path(__file__).parent / "cfg.dot"
        json_output = Path(__file__).parent / "cfg.json"
        
        visualizer.save_dot_file(str(dot_output))
        visualizer.save_json_file(str(json_output))
        
        print(f"\nSaved DOT file to: {dot_output}")
        print(f"Saved JSON file to: {json_output}")
        
    except Exception as e:
        print(f"Error: {e}")


def analyze_nested_functions():
    print("\nExample 3: Extracting nested functions")
    print("=" * 80)
    
    pyc_path = Path(__file__).parent / "sample.pyc"
    
    if not pyc_path.exists():
        print("Creating sample.pyc...")
        import py_compile
        py_compile.compile(
            str(Path(__file__).parent / "sample.py"),
            cfile=str(pyc_path)
        )
    
    try:
        pyc_reader = PycReader(str(pyc_path))
        functions = pyc_reader.extract_functions()
        
        print("Extracted functions:")
        for func_name, code_obj in functions.items():
            print(f"  {func_name}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    analyze_single_function()
    analyze_control_flow()
    analyze_nested_functions()
