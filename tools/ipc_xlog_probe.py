
import os, binascii, zlib, struct
D = r"C:\Users\Administrator\AppData\LocalLow\Tencent\WeType"
for n in ["renderer_for_tip.ipc","server_for_renderer.ipc","session_v2.ipc","session_v2_update.ipc","update_for_renderer.ipc","update_session_v2.ipc"]:
    p=os.path.join(D,n); b=open(p,"rb").read()
    print("---",n,len(b)); print(b[:64]); print(binascii.hexlify(b[:64]).decode())
print("=== WeTypeSharedData.pb"); b=open(os.path.join(D,"WeTypeSharedData.pb"),"rb").read(); print(len(b)); print(binascii.hexlify(b).decode())
for n in ["MM_SERVER_20261017.xlog","MM_WETYPE_20261017.xlog","MM_RENDER_20261017.xlog","MM_SERVER.mmap3","MM_TIP.mmap3"]:
    p=os.path.join(D,n); b=open(p,"rb").read()
    print("=== ",n,len(b)); print(binascii.hexlify(b[:96]).decode())
    # try zlib at each offset
    for off in range(0,64):
        try:
            d=zlib.decompressobj()
            out=d.decompress(b[off:off+4096])
            if len(out)>20:
                print("   zlib@",off,"->",out[:120]); break
        except Exception: pass
