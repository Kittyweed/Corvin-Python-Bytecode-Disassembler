import marshal
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
import struct


@dataclass
class PycHeader:
    magic_number: bytes
    timestamp: int
    size: int
    version: str

    def __str__(self) -> str:
        return f"Magic: {self.magic_number.hex()}, Timestamp: {self.timestamp}, Size: {self.size}, Python: {self.version}"


class PycReader:
    def __init__(self, pyc_path: str):
        self.pyc_path = Path(pyc_path)
        self.header: Optional[PycHeader] = None
        self.code_object = None
        self._read_pyc()

    def _read_pyc(self) -> None:
        if not self.pyc_path.exists():
            raise FileNotFoundError(f"File not found: {self.pyc_path}")

        if not self.pyc_path.suffix == '.pyc':
            raise ValueError(f"Not a .pyc file: {self.pyc_path}")

        with open(self.pyc_path, 'rb') as f:
            magic = f.read(4)
            timestamp = struct.unpack('<I', f.read(4))[0]
            size = struct.unpack('<I', f.read(4))[0]
            
            python_version = self._magic_to_version(magic)
            self.header = PycHeader(
                magic_number=magic,
                timestamp=timestamp,
                size=size,
                version=python_version
            )

            self.code_object = marshal.load(f)

    def _magic_to_version(self, magic: bytes) -> str:
        magic_versions = {
            b'\x55\r\r\n': '3.5',
            b'\x61\r\r\n': '3.6',
            b'\x9e\r\r\n': '3.7',
            b'\x0d\r\r\n': '3.8',
            b'\x15\r\r\n': '3.9',
            b'\x19\r\r\n': '3.10',
            b'c\r\r\n': '3.11',
            b'\x8f\r\r\n': '3.12',
        }
        return magic_versions.get(magic, f"Unknown (0x{magic.hex()})")

    def get_code_object(self):
        return self.code_object

    def get_header_info(self) -> Dict[str, Any]:
        return {
            'magic_number': self.header.magic_number.hex(),
            'timestamp': self.header.timestamp,
            'size': self.header.size,
            'python_version': self.header.version,
        }

    def extract_functions(self):
        functions = {}
        self._extract_from_code(self.code_object, functions)
        return functions

    def _extract_from_code(self, code_obj, functions: Dict):
        if hasattr(code_obj, 'co_name'):
            functions[code_obj.co_name] = code_obj

        if hasattr(code_obj, 'co_consts'):
            for const in code_obj.co_consts:
                if hasattr(const, 'co_name'):
                    self._extract_from_code(const, functions)

    def print_header_info(self) -> str:
        return f"PYC File Information:\n{self.header}"

    def get_code_info(self) -> Dict[str, Any]:
        code = self.code_object
        return {
            'name': code.co_name,
            'argcount': code.co_argcount,
            'posonlyargcount': getattr(code, 'co_posonlyargcount', 0),
            'kwonlyargcount': code.co_kwonlyargcount,
            'nlocals': code.co_nlocals,
            'stacksize': code.co_stacksize,
            'flags': code.co_flags,
            'varnames': code.co_varnames,
            'cellvars': code.co_cellvars,
            'freevars': code.co_freevars,
            'filename': code.co_filename,
            'firstlineno': code.co_firstlineno,
            'constants': code.co_consts,
            'names': code.co_names,
        }
