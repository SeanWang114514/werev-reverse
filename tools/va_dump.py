import sys
p = sys.argv[1]
base = int(sys.argv[2], 16)   # a known VA
anchor = sys.argv[3].encode()
va_list = [int(x,16) for x in sys.argv[4:]]
d = open(p,'rb').read()
i = d.find(anchor)
if i < 0:
    print("anchor not found"); sys.exit(1)
delta = base - i
print("anchor %r fileoff=0x%x  delta=0x%x" % (anchor, i, delta))
for va in va_list:
    off = va - delta
    # read until NUL or 200 bytes
    end = d.find(b'\x00', off, off+200)
    if end < 0: end = off+80
    print("%x -> fileoff 0x%x : %r" % (va, off, d[off:end]))
