#!/usr/bin/python
#from __future__ import print_function

import sys
import os
import struct
import mmap

fbuf = open('./buf','r')
start_addr = int(fbuf.readline())
end_addr = int(fbuf.readline())
fbuf.close()
page_size = int(os.sysconf("SC_PAGE_SIZE")) & 0x7FFFFFFFFFFFFF
print('START = '+str(hex(int(start_addr))))
print('END = '+str(hex(int(end_addr))))

# WRITING MEMORY
key = ''
i = 0
while key != 'q':
  i = (i+1)%0x100
  key = raw_input("\nWrite "+str(hex(i))+" to mem or q to exit... ")
  if key != 'q':
    with open("/dev/mem", "r+b") as f:
      count = 0
      for addr in range (start_addr,end_addr,1):
        page_addr=addr & (~(page_size-1))
	if page_addr != start_addr & (~(page_size-1)):
          break
        page_offs=addr-page_addr
        mm = mmap.mmap(f.fileno(), page_size, offset=page_addr)
        mm[page_offs] = struct.pack("B",i)
        count += 1
        mm.close()
      print(str(count)+" bytes written.")


