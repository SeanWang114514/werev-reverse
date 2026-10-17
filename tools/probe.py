#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Targeted keyword probes across extracted strings."""
import re, sys, json
from pathlib import Path
from collections import defaultdict

S = Path(r"D:\VibeCoding\微信输入法逆向\out\strings")
REP = Path(r"D:\VibeCoding\微信输入法逆向\out\reports")

GROUPS = {
 "ANTI-DEBUG": r"IsDebuggerPresent|CheckRemoteDebugger|NtQueryInformationProcess|NtSetInformationThread|OutputDebugString|DebugActiveProcess|ProcessDebugPort|ProcessDebugFlags|DebugObject|NtGlobalFlag|PEB|BeingDebugged|ZwQuery|hardware breakpoint|DR0|trap flag|int3|0xCC|QueryPerformanceCounter|GetTickCount|CheckSumMappedFile|MiniDumpWriteDump|SetUnhandledExceptionFilter|VEH|TitanHide|ScyllaHide",
 "ANTI-VM": r"VMware|VirtualBox|VBOX|vbox|QEMU|qemu|Xen|Hyper-V|vmtoolsd|vboxtray|SbieDll|sandboxie|wine|Wine|Cuckoo|qemu-ga|virtual|hypervisor|CPUID|VBS|DeviceGuard|VBS_Enclave",
 "CRYPTO": r"AES|aes_|EVP_|RSA_|rsa_|MD5|SHA1|SHA256|SHA512|HMAC|hmac|PBKDF2|scrypt|bcrypt|curve25519|X25519|chacha|ChaCha|SM2|SM3|SM4|sm4|ECDH|ECDSA|TLS|SSL_|openssl|OpenSSL|BoringSSL|boringssl|mbedtls|libsodium|nacl|encrypt|decrypt|Encrypt|Decrypt",
 "KEYS": r"-----BEGIN|BEGIN RSA|BEGIN PRIVATE|PRIVATE KEY|PUBLIC KEY|CERTIFICATE|salt|Salt|SALT|nonce|Nonce|iv_len|key_len|secret_key|master_key|session_key|app_key|AppKey|aes_key|AES_KEY",
 "PROTO/PORT": r"^\d{2,5}$|:\d{4,5}\b|ws://|wss://|grpc|protobuf|proto3|protobuf-cpp",
 "IPC": r"\\\\\.\\pipe|\\\\\.\\|Local\\\\|NamedPipe|CreateNamedPipe|named pipe|ALPC|WM_COPYDATA|shared memory|CreateFileMapping|RPC|ncalrpc|rpcrt4",
 "TSF/TIP": r"ITf|ITfTextInputProcessor|TF_|CLSID|GUID|TextService|TIP|TSF|IMM32|ImmGetContext|ImeSetActiveContext|RegisterTextInputProcessor|LayoutOrTip|KeyboardLayout|HKEY_|SOFTWARE\\\\(Tencent|Microsoft)",
 "HOOK/INJECT": r"SetWindowsHookEx|WH_KEYBOARD|WH_MOUSE|GetAsyncKeyState|SetWinEventHook|SetWinEvent|GetForegroundWindow|GetWindowText|GetClassName|OpenProcess|WriteProcessMemory|ReadProcessMemory|CreateRemoteThread|VirtualAllocEx|NtCreateThreadEx|QueueUserAPC|SetThreadContext|LdrLoadDll|ManualMap|LoadLibrary|GetProcAddress|Detour|MinHook|InlineHook|IAT hook|EAT hook",
 "TELEMETRY": r"report|Report|stat|Stat|track|Track|beacon|Beacon|sentry|Sentry|bugly|Bugly|crash|Crash|analytics|Analytics|mmdata|datong|灯塔|上报|埋点",
 "SECURITY-SW": r"landun|Landun|tencent.*security|TDSData|ace|ACE|TP|腾讯.*安全|安全|加固|加密",
}

def load(name):
    p = S / name
    if not p.exists(): return []
    out = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            try: off = int(parts[0])
            except: off = -1
            out.append((off, parts[1], parts[2]))
    return out

report = {}
for f in sorted(S.glob("*.strings.tsv")):
    binname = f.name[:-len(".strings.tsv")]
    rows = load(f.name)
    rep = {}
    for gname, pat in GROUPS.items():
        rx = re.compile(pat, re.I if gname not in ("PROTO/PORT",) else 0)
        hits = []
        seen = set()
        for off, enc, s in rows:
            if rx.search(s) and s not in seen:
                seen.add(s); hits.append((off, enc, s))
        rep[gname] = hits
    report[binname] = rep
    with (REP / f"{binname}.probe.txt").open("w", encoding="utf-8") as fh:
        for gname, hits in rep.items():
            fh.write(f"\n===== [{gname}] {len(hits)} =====\n")
            for off, enc, s in hits[:500]:
                fh.write(f"  {off:#010x} {enc} {s}\n")
    print(binname, {k: len(v) for k, v in rep.items() if v})

(REP / "_probe_counts.json").write_text(json.dumps({b: {k: len(v) for k, v in r.items()} for b, r in report.items()}, indent=1), encoding="utf-8")
