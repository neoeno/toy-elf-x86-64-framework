from elf import *
from instructions import mov_r32_imm32, syscall

data = Placement(0xf0, b"Hello, world!\n\0\0")

code = Placement(0xc0, [
  *mov_r32_imm32('rax', 0x01),
  *mov_r32_imm32('rdi', 0x01),
  *mov_r32_imm32('rsi', 0x600000 + data.offset),
  *mov_r32_imm32('rdx', data.size()),
  *syscall(),

  *mov_r32_imm32('rdi', 0x00),
  *mov_r32_imm32('rax', 0x3C),
  *syscall(),
])


write_elf('build/hello-world', [
  Placement(0x00, make_elf_identifier()),
  Placement(0x10, make_elf_header(
    entrypoint            = 0x400000 + code.offset,
    program_header_offset = 0x40,
    program_header_num    = 2)),
  Placement(0x40, make_program_header(
    flags  = PH_FLAG_R | PH_FLAG_X,
    offset = 0x0,
    vaddr  = 0x400000,
    filesz = code.extent(),
    memsz  = code.extent()
  )),
  Placement(0x78, make_program_header(
    flags  = PH_FLAG_R,
    offset = 0,
    vaddr  = 0x600000,
    filesz = data.extent(),
    memsz  = data.extent()
  )),
  code,
  data
])
