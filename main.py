import argparse
import sys
from pathlib import Path

from src.analyzer import PycReader
from src.disassembler import BytecodeDisassembler
from src.visualization import ControlFlowAnalyzer, CFGVisualizer


def main():
    parser = argparse.ArgumentParser(
        description="Python Bytecode Disassembler and Control Flow Analyzer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python main.py -f file.pyc\n"
               "  python main.py -f file.pyc --cfg\n"
               "  python main.py -f file.pyc --dot output.dot\n"
    )

    parser.add_argument('-f', '--file', type=str, required=True, help='Path to .pyc file')
    parser.add_argument('--disassemble', action='store_true', help='Show disassembly')
    parser.add_argument('--cfg', action='store_true', help='Show control flow graph')
    parser.add_argument('--info', action='store_true', help='Show file information')
    parser.add_argument('--dot', type=str, help='Save CFG as DOT format')
    parser.add_argument('--json', type=str, help='Save CFG as JSON format')
    parser.add_argument('--all', action='store_true', help='Show all information')

    args = parser.parse_args()

    try:
        pyc_reader = PycReader(args.file)
        code_object = pyc_reader.get_code_object()
        
        if args.all:
            args.info = True
            args.disassemble = True
            args.cfg = True

        if args.info or args.all:
            print("=" * 80)
            print("FILE INFORMATION")
            print("=" * 80)
            print(pyc_reader.print_header_info())
            print()
            code_info = pyc_reader.get_code_info()
            print("Code Object Information:")
            print(f"  Name: {code_info['name']}")
            print(f"  Arguments: {code_info['argcount']}")
            print(f"  Local Variables: {code_info['nlocals']}")
            print(f"  Stack Size: {code_info['stacksize']}")
            print(f"  Varnames: {code_info['varnames']}")
            print()

        if args.disassemble or args.all:
            print("=" * 80)
            print("BYTECODE DISASSEMBLY")
            print("=" * 80)
            disassembler = BytecodeDisassembler(code_object)
            print(disassembler.print_disassembly())
            print()

        if args.cfg or args.dot or args.json or args.all:
            disassembler = BytecodeDisassembler(code_object)
            cfg = ControlFlowAnalyzer(disassembler)
            visualizer = CFGVisualizer(cfg)

            if args.cfg or args.all:
                print("=" * 80)
                print("CONTROL FLOW GRAPH")
                print("=" * 80)
                visualizer.print_graph()
                print()

            if args.dot:
                visualizer.save_dot_file(args.dot)
                print(f"Saved DOT format to: {args.dot}")

            if args.json:
                visualizer.save_json_file(args.json)
                print(f"Saved JSON format to: {args.json}")

        if not any([args.info, args.disassemble, args.cfg, args.dot, args.json, args.all]):
            print("No output format specified. Use --help for options.")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
