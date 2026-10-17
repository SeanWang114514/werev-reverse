
import os, binascii, importlib
D = r"D:\VibeCoding\微信输入法逆向\samples\runtime"
for m in ("zstandard","pyzstd","lz4","snappy","brotli"):
    try:
        importlib.import_module(m); print("MOD",m,"OK")
    except Exception as e: print("MOD",m,"no")
MAG = {"zstd":b"\x28\xb5\x2f\xfd","gzip":b"\x1f\x8b\x08","lz4":b"\x04\x22\x4d\x18","zlib78":b"\x78\x9c","zlib01":b"\x78\x01","zlibda":b"\x78\xda","xz":b"\xfd7zXZ"}
for n in ["MM_SERVER_20261017.xlog","MM_WETYPE_20261017.xlog","MM_RENDER_20261017.xlog","MM_SERVER.mmap3"]:
    p=os.path.join(D,n)
    if not os.path.exists(p): continue
    b=open(p,"rb").read()
    print("===",n,len(b))
    for name,mg in MAG.items():
        for key in range(0,256):
            tgt = bytes(x^key for x in mg)
            i = b.find(tgt)
            if i>=0:
                print("   ",name,"xor",hex(key),"@",i); break
