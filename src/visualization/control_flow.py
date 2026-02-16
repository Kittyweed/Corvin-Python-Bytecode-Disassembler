from typing import Dict, Set, List, Tuple, Optional
from dataclasses import dataclass, field
import dis


@dataclass
class BasicBlock:
    block_id: int
    start_offset: int
    end_offset: int
    instructions: List = field(default_factory=list)
    predecessors: Set[int] = field(default_factory=set)
    successors: Set[int] = field(default_factory=set)

    def __str__(self) -> str:
        return f"Block_{self.block_id} [{self.start_offset}-{self.end_offset}]"


class ControlFlowAnalyzer:
    def __init__(self, disassembler):
        self.disassembler = disassembler
        self.blocks: Dict[int, BasicBlock] = {}
        self.edges: List[Tuple[int, int]] = []
        self._build_cfg()

    def _build_cfg(self) -> None:
        instructions = self.disassembler.get_instructions()
        
        if not instructions:
            return

        block_starts = {0}
        
        for i, instr in enumerate(instructions):
            if instr.is_jump():
                if instr.arg is not None:
                    block_starts.add(instr.arg)
                if i + 1 < len(instructions):
                    block_starts.add(instructions[i + 1].offset)
            elif instr.is_return():
                if i + 1 < len(instructions):
                    block_starts.add(instructions[i + 1].offset)

        block_starts = sorted(block_starts)
        block_id = 0

        for i, start in enumerate(block_starts):
            end = block_starts[i + 1] - 2 if i + 1 < len(block_starts) else instructions[-1].offset

            block_instrs = [instr for instr in instructions if start <= instr.offset <= end]
            
            if block_instrs:
                block = BasicBlock(
                    block_id=block_id,
                    start_offset=start,
                    end_offset=block_instrs[-1].offset,
                    instructions=block_instrs
                )
                self.blocks[block_id] = block
                block_id += 1

        self._connect_edges()

    def _connect_edges(self) -> None:
        for block_id, block in self.blocks.items():
            if not block.instructions:
                continue

            last_instr = block.instructions[-1]

            if last_instr.is_return():
                continue

            if last_instr.is_jump():
                target = last_instr.arg

                for bid, b in self.blocks.items():
                    if b.start_offset == target:
                        block.successors.add(bid)
                        b.predecessors.add(block_id)
                        self.edges.append((block_id, bid))
                        break

                if not last_instr.is_conditional_jump() and last_instr.is_absolute_jump():
                    continue

            next_block_id = block_id + 1
            if next_block_id in self.blocks:
                block.successors.add(next_block_id)
                self.blocks[next_block_id].predecessors.add(block_id)
                self.edges.append((block_id, next_block_id))

    def get_blocks(self) -> Dict[int, BasicBlock]:
        return self.blocks

    def get_edges(self) -> List[Tuple[int, int]]:
        return self.edges

    def get_entry_block(self) -> Optional[BasicBlock]:
        return self.blocks.get(0)

    def get_exit_blocks(self) -> List[BasicBlock]:
        exit_blocks = []
        for block in self.blocks.values():
            if not block.instructions:
                continue
            if block.instructions[-1].is_return():
                exit_blocks.append(block)
            elif not block.successors:
                exit_blocks.append(block)
        return exit_blocks
