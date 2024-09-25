from elf import le32

# You can add your own instructions to the end of this file

registers = {
  'ax': 0,
  'cx': 1,
  'dx': 2,
  'bx': 3,
  'sp': 4,
  'bp': 5,
  'si': 6,
  'di': 7,
  'al': 0, # When moving a single byte, you can use these 8-bit registers
  'cl': 1,
  'dl': 2,
  'bl': 3,
  'ah': 4,
  'ch': 5,
  'dh': 6,
  'bh': 7
}


def reg_code(reg_name):
  base_name = reg_name[-2:]
  if base_name not in registers:
    raise ValueError(f"Unknown register: {reg_name} (base: {base_name})")
  return registers[base_name]


def mov_r32_imm32(reg_name, imm32):
  reg = reg_code(reg_name)
  return [
    0xC7, 0b11000000 | reg, *le32(imm32)
  ]


def syscall():
  return [0x0F, 0x05]


def nop():
  return [
    0x90
  ]
