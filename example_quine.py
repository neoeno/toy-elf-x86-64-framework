from elf import *
from instructions import mov_r32_imm32, syscall

def sub_show(address, length):
  return [
    *mov_r32_imm32('rax', 0x01),
    *mov_r32_imm32('rdi', 0x01),
    *mov_r32_imm32('rsi', address),
    *mov_r32_imm32('rdx', length),
    *syscall(),
  ]

def sub_exit(code=0):
  return [
    *mov_r32_imm32('rdi', code),
    *mov_r32_imm32('rax', 0x3C),
    *syscall(),
  ]

# To calculate the length to print out, we'll need to know the length of our own
# code, so we calculate the length here with a dummy value.
code_length = len([*sub_show(0x200000, 0x1000), *sub_exit()])

# Then write out the actual code.
code = Placement(0x1000, [
  *sub_show(0x200000, 0x1000 + code_length),
  *sub_exit()
])

write_elf('build/quine', [
  Placement(0x00, make_elf_identifier()),
  Placement(0x10, make_elf_header(
    entrypoint            = 0x400000,
    program_header_offset = 0x40,
    program_header_num    = 3)),
  Placement(0x40, make_program_header(
    flags  = PH_FLAG_R | PH_FLAG_X | PH_FLAG_W,
    offset = 0x0,
    vaddr  = 0x200000,
    filesz = code.extent(),
    memsz  = code.extent()
  )),
  Placement(0x78, make_program_header(
    flags  = PH_FLAG_R | PH_FLAG_X,
    offset = 0x1000,
    vaddr  = 0x400000,
    filesz = code.extent(),
    memsz  = code.extent()
  )),
  code
])
