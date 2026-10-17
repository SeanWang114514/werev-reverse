import sys, struct
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
d=open(sys.argv[1],'rb').read()
print('size',len(d))
print('u32[0:10]',[struct.unpack_from('<I',d,4*i)[0] for i in range(10)])
print('head hex', d[:64].hex())
print('head aslatin', d[:64].decode('latin1'))
print('has P01 marker', d.count(b'P\x01'))
print('cjk utf8 count', sum(1 for i in range(len(d)-2) if 0xe4<=d[i]<=0xe9 and 0x80<=d[i+1]<=0xbf))