#! /usr/bin/env python
import sys
import re
pid = sys.argv[1]
maps_file = open("/proc/%s/maps" % pid, 'r')
mem_file = open("/proc/%s/mem" % pid, 'r', 0)
for line in maps_file.readlines():  # for each mapped region
    m = re.match(r'([0-9A-Fa-f]+)-([0-9A-Fa-f]+) ([-r])', line)
    if m.group(3) == 'r':  # if this is a readable region
        start = int(m.group(1), 16)
        end = int(m.group(2), 16)
        pos = min(end, start + 1000000000)
        while pos < end:
            print("Reading %d to %d" % (start, pos))
            mem_file.seek(start)  # seek to region start
            chunk = mem_file.read(pos - start)  # read region contents
            start = pos
            pos = min(end, start + 1000000000)
        #print chunk,  # dump contents to standard output
maps_file.close()
mem_file.close()

