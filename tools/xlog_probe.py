
import os, binascii, zlib
D = r"D:\VibeCoding\微信输入法逆向\samples\runtime"
for n in ["MM_SERVER_20261017.xlog","MM_WETYPE_20261017.xlog","MM_RENDER_20261017.xlog","context_capture/refetch_sync_legacy.log"]:
    p=os.path.join(D,n); b=open(p,"rb").read()
    print("=== ",n,len(b))
    print(binascii.hexlify(b[:128]).decode())
    for off in range(0,96):
        try:
            d=zlib.decompressobj(); out=d.decompress(b[off:off+8192])
            if len(out)>20:
                print("  raw zlib@",off,"->",out[:100]); break
        except Exception: pass
    # xor probe
    for key in range(1,256):
        seg=bytes(x^key for x in b[3:3+64])
        if seg[:2] in (b"\x78\x9c",b"\x78\x01",b"\x78\xda"):
            print("  xor key",hex(key),"at off 3 -> zlib magic",seg[:2].hex()); break
