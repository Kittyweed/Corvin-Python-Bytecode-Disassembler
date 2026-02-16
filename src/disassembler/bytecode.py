import dis
import sys
from typing import List, Dict, Optional, Set, Tuple
from .instruction import Instruction


class BytecodeDisassembler:
    def __init__(self, code_object):
        self.code_object = code_object
        self.instructions: List[Instruction] = []
        self._disassemble()

    def _disassemble(self) -> None:
        self.instructions = []
        bytecode = self.code_object.co_code
        lnotab = self.code_object.co_lnotab
        
        offset = 0
        line_number = self.code_object.co_firstlineno
        line_offset = 0

        i = 0
        while i < len(bytecode):
            op = bytecode[i]
            opname = dis.opname[op]
            
            if sys.version_info >= (3, 6):
                arg = bytecode[i + 1] if i + 1 < len(bytecode) else 0
                arg_ext = bytecode[i + 2] if i + 2 < len(bytecode) else 0
                if sys.version_info >= (3, 6):
                    arg = arg | (arg_ext << 8)
                i += 2
            else:
                arg = bytecode[i + 1] if i + 1 < len(bytecode) else 0
                i += 2

            if op >= dis.HAVE_ARGUMENT:
                argval, argrepr = self._resolve_arg(op, arg)
            else:
                argval, argrepr = None, ''
                arg = None

            line_num = self._calculate_line_number(offset, lnotab, line_number)

            instr = Instruction(
                offset=offset,
                opname=opname,
                opcode=op,
                arg=arg,
                argval=argval,
                argrepr=argrepr,
                line_number=line_num
            )
            self.instructions.append(instr)
            offset += 2

    def _resolve_arg(self, op: int, arg: int) -> Tuple[any, str]:
        try:
            if op in dis.hasconst:
                const = self.code_object.co_consts[arg]
                return const, repr(const)
            elif op in dis.hasname:
                if arg < len(self.code_object.co_names):
                    name = self.code_object.co_names[arg]
                    return name, name
            elif op in dis.haslocal:
                if arg < len(self.code_object.co_varnames):
                    name = self.code_object.co_varnames[arg]
                    return name, name
            elif op in dis.hasfree:
                cellvars_len = len(self.code_object.co_cellvars)
                if arg < cellvars_len:
                    name = self.code_object.co_cellvars[arg]
                elif arg - cellvars_len < len(self.code_object.co_freevars):
                    name = self.code_object.co_freevars[arg - cellvars_len]
                else:
                    return arg, str(arg)
                return name, name
            elif op in dis.hasjabs or op in dis.hasjrel:
                return arg, str(arg)
        except (IndexError, AttributeError):
            pass
        return arg, str(arg)

    def _calculate_line_number(self, offset: int, lnotab: bytes, first_line: int) -> int:
        line = first_line
        addr = 0
        i = 0
        
        while i < len(lnotab) and addr <= offset:
            addr += lnotab[i]
            line += lnotab[i + 1]
            i += 2

        return line

    def get_instructions(self) -> List[Instruction]:
        return self.instructions

    def get_instruction_at(self, offset: int) -> Optional[Instruction]:
        for instr in self.instructions:
            if instr.offset == offset:
                return instr
        return None

    def get_basic_blocks(self) -> Dict[int, List[Instruction]]:
        blocks = {}
        current_block = []
        block_start = 0

        for instr in self.instructions:
            if not current_block and instr.offset not in blocks:
                block_start = instr.offset

            current_block.append(instr)

            if instr.is_jump() or instr.is_return():
                blocks[block_start] = current_block
                current_block = []

            for i, target_instr in enumerate(self.instructions):
                if i > 0 and target_instr.offset in [instr.argval for instr in self.instructions if instr.is_jump()]:
                    if current_block and target_instr not in current_block:
                        blocks[block_start] = current_block
                        current_block = []
                        break

        if current_block:
            blocks[block_start] = current_block

        return blocks

    def print_disassembly(self) -> str:
        output = []
        output.append(f"Disassembly of {self.code_object.co_name}")
        output.append("=" * 80)
        output.append(f"{'Offset':>6} {'Opcode':20} {'Arg':>5} {'Argval':20} {'Line':>5}")
        output.append("-" * 80)

        for instr in self.instructions:
            line_info = f"{instr.line_number}" if instr.line_number else "-"
            output.append(
                f"{instr.offset:6d} {instr.opname:20} {str(instr.arg or ''):>5} {instr.argrepr[:20]:20} {line_info:>5}"
            )

        return "\n".join(output)
