#from __future__ import print_function
import ctypes
import os
import sys
import mmap
import binascii
import struct

def read_entry(path, offset, size=8):
  with open(path, 'r') as f:
    f.seek(offset, 0)
    return struct.unpack('Q', f.read(size))[0]

def get_pagemap_entry(pid, addr):
  maps_path = "/proc/{0}/pagemap".format(pid)
  if not os.path.isfile(maps_path):
    print("Process {0} doesn't exist.".format(pid))
    return
  page_size = os.sysconf("SC_PAGE_SIZE")
  pagemap_entry_size = 8
  offset  = (addr / page_size) * pagemap_entry_size
  return read_entry(maps_path, offset)

def get_offset(addr):
  page_size = os.sysconf("SC_PAGE_SIZE")
  return addr & (page_size-1)

def get_pfn(entry):
  return entry & 0x7FFFFFFFFFFFFF

os.system('clear')
print("\n")
writeMode=len(sys.argv)>2
endian="<" # little, ">" for big
page_size = int(os.sysconf("SC_PAGE_SIZE")) & 0x7FFFFFFFFFFFFF

# ALLOCATING MEMORY
buf_size = page_size
if len(sys.argv) >= 2:
  print("Reading length from command line\n")
  buf_size = int(sys.argv[1])
ctypes_alloc = ctypes.CDLL('./malloc_and_mlock.so').malloc_and_mlock
ctypes_alloc.restype = ctypes.c_void_p
ctypes_alloc.argtypes = ctypes.c_size_t,
buf_addr = ctypes_alloc(buf_size)
buf_pid = os.getpid()
print("PID = "+str(buf_pid))
print("ADDR = "+hex(buf_addr))
print("OFFS = "+hex(get_offset(buf_addr)))

# DETECTING PHYSICAL ADDRESS
entry = get_pagemap_entry(int(buf_pid),int(buf_addr))
mem_page = get_pfn(entry)
mem_page_offset = get_offset(int(buf_addr))
start_addr = int(mem_page*page_size+mem_page_offset) & 0x7FFFFFFFFFFFFF
end_addr = int(start_addr+buf_size) & 0x7FFFFFFFFFFFFF
print("\nPAGE = "+hex(mem_page))
print("START = "+hex(start_addr))
print("END   = "+hex(end_addr))

# SAVING ADDRESS
fbuf = open('./buf','w')
fbuf.write(str(start_addr)+'\n')
fbuf.write(str(end_addr)+'\n')
fbuf.close()

# READING MEMORY
key = ''
while key != 'q':
  key = raw_input("\nDisplay mem or q to exit...")
  if key != 'q':
    with open("/dev/mem", "r+b") as f:
      for addr in range (start_addr,end_addr+4,4):
        page_addr=addr & (~(page_size-1))
        if (addr == start_addr) or ((addr & 0x3f) == 0):
          print ("\n0x%08x:"%addr),
        page_offs=addr-page_addr
        mm = mmap.mmap(f.fileno(), page_size, offset=page_addr)
        data=struct.unpack(endian+"L",mm[page_offs:page_offs+4])
        d=data[0]
        print ("%08x"%d),
        mm.close()

