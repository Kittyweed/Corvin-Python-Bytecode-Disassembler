import dis
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Instruction:
    offset: int
    opname: str
    opcode: int
    arg: Optional[int]
    argval: Any
    argrepr: str
    line_number: Optional[int]

    def __str__(self) -> str:
        return f"{self.offset:4d} {self.opname:20s} {self.arg if self.arg is not None else '':5} {self.argrepr}"

    def is_jump(self) -> bool:
        return self.opcode in dis.hasjrel or self.opcode in dis.hasjabs

    def is_conditional_jump(self) -> bool:
        conditional_opcodes = {
            dis.opmap.get('POP_JUMP_IF_TRUE', -1),
            dis.opmap.get('POP_JUMP_IF_FALSE', -1),
            dis.opmap.get('JUMP_IF_TRUE_OR_POP', -1),
            dis.opmap.get('JUMP_IF_FALSE_OR_POP', -1),
        }
        return self.opcode in conditional_opcodes

    def is_absolute_jump(self) -> bool:
        return self.opcode in dis.hasjabs

    def is_return(self) -> bool:
        return self.opname == 'RETURN_VALUE'
