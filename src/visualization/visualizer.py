from typing import Dict, Optional
import json


class CFGVisualizer:
    def __init__(self, cfg_analyzer):
        self.cfg_analyzer = cfg_analyzer

    def generate_dot(self) -> str:
        output = []
        output.append("digraph ControlFlow {")
        output.append("    rankdir=TB;")
        output.append("    node [shape=box, style=rounded];")

        blocks = self.cfg_analyzer.get_blocks()
        
        for block_id, block in blocks.items():
            label = self._create_block_label(block)
            output.append(f'    {block_id} [label="{label}"];')

        for src, dst in self.cfg_analyzer.get_edges():
            output.append(f"    {src} -> {dst};")

        output.append("}")
        return "\n".join(output)

    def _create_block_label(self, block) -> str:
        lines = [f"Block {block.block_id}"]
        for instr in block.instructions[:5]:
            lines.append(f"{instr.offset}: {instr.opname}")
        if len(block.instructions) > 5:
            lines.append("...")
        return "\\n".join(lines)

    def generate_text_graph(self) -> str:
        output = []
        blocks = self.cfg_analyzer.get_blocks()
        edges = self.cfg_analyzer.get_edges()

        output.append("Control Flow Graph")
        output.append("=" * 60)

        for block_id, block in sorted(blocks.items()):
            output.append(f"\n{block}:")
            for instr in block.instructions:
                output.append(f"  {instr}")

            successors = list(block.successors)
            if successors:
                output.append(f"  Successors: {[f'Block_{s}' for s in successors]}")
            predecessors = list(block.predecessors)
            if predecessors:
                output.append(f"  Predecessors: {[f'Block_{p}' for p in predecessors]}")

        return "\n".join(output)

    def generate_json(self) -> str:
        blocks = self.cfg_analyzer.get_blocks()
        edges = self.cfg_analyzer.get_edges()

        blocks_data = {}
        for block_id, block in blocks.items():
            blocks_data[str(block_id)] = {
                'id': block.block_id,
                'start_offset': block.start_offset,
                'end_offset': block.end_offset,
                'instructions': [
                    {
                        'offset': instr.offset,
                        'opname': instr.opname,
                        'arg': instr.arg,
                        'argrepr': instr.argrepr,
                        'line': instr.line_number
                    }
                    for instr in block.instructions
                ],
                'successors': list(block.successors),
                'predecessors': list(block.predecessors),
            }

        data = {
            'blocks': blocks_data,
            'edges': [{'from': src, 'to': dst} for src, dst in edges],
        }

        return json.dumps(data, indent=2)

    def save_dot_file(self, filepath: str) -> None:
        with open(filepath, 'w') as f:
            f.write(self.generate_dot())

    def save_json_file(self, filepath: str) -> None:
        with open(filepath, 'w') as f:
            f.write(self.generate_json())

    def print_graph(self) -> None:
        print(self.generate_text_graph())
