#!/usr/bin/env python3
"""Extract ASCII + UTF-16LE strings, filter by keyword, dump full to TSV."""
import sys, re, os, json
from pathlib import Path

ASCII_RE = re.compile(rb"[\x20-\x7e]{4,}")
UTF16_RE = re.compile(rb"(?:[\x20-\x7e]\x00){4,}")

KEYWORDS = [
    "http://","https://","wss://","ws://","api","/cgi","/cgi-bin",".com","/.php",
    "token","secret","key=","apikey","appid","app_id","sign","signature","nonce",
    "salt","iv=","aes","rsa","md5","sha1","sha256","hmac","encrypt","decrypt",
    "device","deviceid","imei","guid","uuid","userid","uin","qq","wxid","openid",
    "report","stat","log","upload","download","config","setting","version","update",
    "login","auth","verify","register","bind","sync","cloud","backup",
    "protobuf","pb.","grpc","socket","port","host","domain","cdn","dns",
    "Tencent","tencent","weixin","wechat","wetype","WeType","mmtls","XNet",
    "sqlite","leveldb","rocksdb","redis","mysql",
    "证书","密钥","加密","解密","接口","服务器","上报","统计","用户","设备",
]

def gen(data):
    for m in ASCII_RE.finditer(data):
        yield m.start(), "A", m.group().decode("ascii","replace")
    for m in UTF16_RE.finditer(data):
        yield m.start(), "U", m.group().decode("utf-16-le","replace")

def main():
    src = Path(sys.argv[1]); outdir = Path(sys.argv[2]); outdir.mkdir(parents=True, exist_ok=True)
    files = [src] if src.is_file() else [p for p in src.rglob("*") if p.is_file()]
    for f in files:
        try: data = f.read_bytes()
        except Exception as e:
            print(f"[skip] {f}: {e}"); continue
        rows = []
        hits = []
        seen = set()
        for off, enc, s in gen(data):
            rows.append((off, enc, s))
            low = s.lower()
            if any(k.lower() in low for k in KEYWORDS):
                key = (enc, s)
                if key not in seen:
                    seen.add(key); hits.append((off, enc, s))
        outp = outdir / (f.name + ".strings.tsv")
        with outp.open("w", encoding="utf-8") as fh:
            for off, enc, s in rows:
                fh.write(f"{off}\t{enc}\t{s}\n")
        outp2 = outdir / (f.name + ".hits.tsv")
        with outp2.open("w", encoding="utf-8") as fh:
            for off, enc, s in hits:
                fh.write(f"{off}\t{enc}\t{s}\n")
        print(f"{f.name}: total={len(rows)} hits={len(hits)} -> {outp.name}")

if __name__ == "__main__":
    main()
