from dataclasses import dataclass


def write_elf(filename, placements):
  with open(filename, 'wb') as f:
    for placement in placements:
      f.seek(placement.offset)
      f.write(bytearray(placement.bytes))


@dataclass
class Placement:
  offset: int
  bytes: list[int]

  def size(self):
    return len(self.bytes)

  def extent(self):
    return self.offset + self.size()


def le16(n):
  return [
    n & 0xFF,
    (n >> 8) & 0xFF
  ]


def le32(n):
  return [
    n & 0xFF,
    (n >> 8) & 0xFF,
    (n >> 16) & 0xFF,
    (n >> 24) & 0xFF
  ]


def le64(n):
  return [
    n & 0xFF,
    (n >> 8) & 0xFF,
    (n >> 16) & 0xFF,
    (n >> 24) & 0xFF,
    (n >> 32) & 0xFF,
    (n >> 40) & 0xFF,
    (n >> 48) & 0xFF,
    (n >> 56) & 0xFF
  ]


def make_elf_identifier():
  EI_MAGIC = [0x7f, 0x45, 0x4c, 0x46]
  EI_CLASS_64 = [0x02]
  EI_DATA_2LSB = [0x01]
  EI_VERSION_CURRENT = [0x01]
  EI_OSABI_NONE = [0x00]
  EI_ABIVERSION_NONE = [0x00]
  EI_PAD = [0x00] * 7

  return [
    *EI_MAGIC,
    *EI_CLASS_64,
    *EI_DATA_2LSB,
    *EI_VERSION_CURRENT,
    *EI_OSABI_NONE,
    *EI_ABIVERSION_NONE,
    *EI_PAD
  ]


def make_elf_header(entrypoint, program_header_offset, program_header_num):
  ET_TYPE_EXEC = le16(0x02)
  ET_MACHINE_AMD64 = le16(0x3E)
  ET_VERSION_CURRENT = le32(0x01)
  ET_ENTRY_POINT = le64(entrypoint)
  ET_PROGRAM_HEADER_OFFSET = le64(program_header_offset)
  ET_SECTION_HEADER_OFFSET = le64(0x00)
  ET_FLAGS = le32(0x00)
  ET_HEADER_SIZE = le16(0x40)
  ET_PROGRAM_HEADER_SIZE = le16(0x38)
  ET_PROGRAM_HEADER_NUM = le16(program_header_num)
  ET_SECTION_HEADER_SIZE = le16(0x00)
  ET_SECTION_HEADER_NUM = le16(0x00)
  ET_SECTION_HEADER_STR_INDEX = le16(0x00)

  return [
    *ET_TYPE_EXEC,
    *ET_MACHINE_AMD64,
    *ET_VERSION_CURRENT,
    *ET_ENTRY_POINT,
    *ET_PROGRAM_HEADER_OFFSET,
    *ET_SECTION_HEADER_OFFSET,
    *ET_FLAGS,
    *ET_HEADER_SIZE,
    *ET_PROGRAM_HEADER_SIZE,
    *ET_PROGRAM_HEADER_NUM,
    *ET_SECTION_HEADER_SIZE,
    *ET_SECTION_HEADER_NUM,
    *ET_SECTION_HEADER_STR_INDEX
  ]


PH_FLAG_R = 0x04
PH_FLAG_W = 0x02
PH_FLAG_X = 0x01

def make_program_header(flags, offset, vaddr, filesz, memsz):
  PT_TYPE_LOAD = le32(0x01)
  PT_FLAGS = le32(flags)
  PT_OFFSET = le64(offset)
  PT_VADDR = le64(vaddr)
  PT_PADDR = le64(0x00)
  PT_FILESZ = le64(filesz)
  PT_MEMSZ = le64(memsz)
  PT_ALIGN = le64(0x1000)

  return [
    *PT_TYPE_LOAD,
    *PT_FLAGS,
    *PT_OFFSET,
    *PT_VADDR,
    *PT_PADDR,
    *PT_FILESZ,
    *PT_MEMSZ,
    *PT_ALIGN,
  ]

