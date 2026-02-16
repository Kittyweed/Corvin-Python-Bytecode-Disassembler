import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.analyzer import PycReader
from src.disassembler import BytecodeDisassembler
from src.visualization import ControlFlowAnalyzer, CFGVisualizer


def test_pyc_reader():
    print("Test 1: PycReader")
    print("-" * 60)
    try:
        from examples.sample import fibonacci
        import py_compile
        
        test_file = Path("tests/test_sample.pyc")
        py_compile.compile("examples/sample.py", cfile=str(test_file))
        
        pyc_reader = PycReader(str(test_file))
        print("PycReader instantiated successfully")
        print(f"Header: {pyc_reader.header}")
        print(f"Code object: {pyc_reader.code_object.co_name}")
        print("PASS\n")
        return True
    except Exception as e:
        print(f"FAIL: {e}\n")
        return False


def test_bytecode_disassembler():
    print("Test 2: BytecodeDisassembler")
    print("-" * 60)
    try:
        from examples.sample import fibonacci
        disassembler = BytecodeDisassembler(fibonacci.__code__)
        instructions = disassembler.get_instructions()
        print(f"Instructions count: {len(instructions)}")
        print(f"First instruction: {instructions[0]}")
        print("PASS\n")
        return True
    except Exception as e:
        print(f"FAIL: {e}\n")
        return False


def test_control_flow_analyzer():
    print("Test 3: ControlFlowAnalyzer")
    print("-" * 60)
    try:
        from examples.sample import check_status
        disassembler = BytecodeDisassembler(check_status.__code__)
        cfg = ControlFlowAnalyzer(disassembler)
        blocks = cfg.get_blocks()
        edges = cfg.get_edges()
        print(f"Blocks: {len(blocks)}")
        print(f"Edges: {len(edges)}")
        print("PASS\n")
        return True
    except Exception as e:
        print(f"FAIL: {e}\n")
        return False


def test_cfg_visualizer():
    print("Test 4: CFGVisualizer")
    print("-" * 60)
    try:
        from examples.sample import calculate_sum
        disassembler = BytecodeDisassembler(calculate_sum.__code__)
        cfg = ControlFlowAnalyzer(disassembler)
        visualizer = CFGVisualizer(cfg)
        
        dot = visualizer.generate_dot()
        json_output = visualizer.generate_json()
        text = visualizer.generate_text_graph()
        
        print(f"DOT output length: {len(dot)}")
        print(f"JSON output length: {len(json_output)}")
        print(f"Text output length: {len(text)}")
        print("PASS\n")
        return True
    except Exception as e:
        print(f"FAIL: {e}\n")
        return False


def run_all_tests():
    print("=" * 60)
    print("Running Tests")
    print("=" * 60 + "\n")
    
    results = []
    results.append(("PycReader", test_pyc_reader()))
    results.append(("BytecodeDisassembler", test_bytecode_disassembler()))
    results.append(("ControlFlowAnalyzer", test_control_flow_analyzer()))
    results.append(("CFGVisualizer", test_cfg_visualizer()))
    
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
    
    print(f"\nTotal: {passed}/{total} passed")


if __name__ == "__main__":
    run_all_tests()
