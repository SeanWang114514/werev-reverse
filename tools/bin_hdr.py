import sys, struct, os
p = sys.argv[1]
d = open(p,'rb').read()
print("=== %s  size=%d ===" % (os.path.basename(p), len(d)))
n = min(160, len(d))
for i in range(0, n, 16):
    row = d[i:i+16]
    hx = ' '.join('%02x'%b for b in row)
    asc = ''.join(chr(b) if 32<=b<127 else '.' for b in row)
    print('%08x  %-47s  %s' % (i, hx, asc))
print('--- u32[0:24] ---')
print([struct.unpack_from('<I', d, i*4)[0] for i in range(min(24, len(d)//4))])
print('--- u64[0:8] ---')
print([struct.unpack_from('<Q', d, i*8)[0] for i in range(min(8, len(d)//8))])
print('--- marker scan (first 4KB) ---')
for m in [b'Ime trie header', b'TFL3', b'mmkv', b'leveldb', b'PK\x03\x04', b'\x1f\x8b', b'zstd', b'LZ4', b'lzma', b'onnx', b'ONNX']:
    i = d[:4096].find(m)
    if i >= 0: print('  hit %-16s @ %d' % (m, i))
# printable ratio of tail
tail = d[-4096:]
pr = sum(1 for b in tail if 32<=b<127 or b in (9,10,13))/len(tail)
print('tail printable ratio: %.3f' % pr)
