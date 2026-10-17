
import sys,re,os
sys.stdout.reconfigure(encoding='utf-8')
D=r"D:\VibeCoding\微信输入法逆向\out\strings"
def grep(files,pats,limit=15,kind=None):
    rx=re.compile(pats)
    for fn in files:
        p=os.path.join(D,fn)
        if not os.path.exists(p): continue
        hits=[]
        with open(p,encoding='utf-8',errors='replace') as f:
            for line in f:
                parts=line.rstrip('\n').split('\t')
                if len(parts)<3: continue
                if kind and parts[1]!=kind: continue
                if rx.search(parts[2]): hits.append(parts[2])
                if len(hits)>=limit: break
        if hits:
            print("##### %s  (%d shown)"%(fn,len(hits)))
            for h in hits: print("   ",h[:200])
F=['wetype_server.exe.strings.tsv','wetype_tip_core.dll.strings.tsv','libwxhld.dll.strings.tsv','ime_net.dll.strings.tsv']
for pat in [r'\\\\\.\\pipe\\', r'UniqueNamedPipe', r'CreateFileMapping|MapViewOfFile',
            r'remote_command|RemoteCommand|remote_cmd|remote_exec',
            r'GetProcessIntegrity|IsDebuggerPresent|CheckRemoteDebuggerPresent|NtQueryInformationProcess',
            r'win_sandbox|Sandbox|sandbox', r'gethostbyname|WinHttp|curl_easy|libcurl',
            r'wetype\.server\.|wetype\.ipc', r'keygen|license|激活|授权']:
    print("\n================ PATTERN:", pat)
    grep(F, pat, 12)
