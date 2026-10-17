import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p=sys.argv[1]
d=open(p,'rb').read()
cnt=struct.unpack_from('<I',d,4)[0]
offs=[struct.unpack_from('<I',d,8+4*i)[0] for i in range(cnt)]
print('offset count', len(offs))
print('first 6 offsets', [hex(o) for o in offs[:6]])
print('monotonic?', all(offs[i]<=offs[i+1] for i in range(len(offs)-1)))
print('data starts', hex(offs[0]))
print('header bytes 0..0x20', d[:0x20].hex())
# The 3.0 dict may be a trie: check for 'Ime trie header'
print('trie marker', d.find(b'Ime trie header'))