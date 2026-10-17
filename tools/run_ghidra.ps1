New-Item -ItemType Directory -Path D:\werev\proj -Force | Out-Null
New-Item -ItemType Directory -Path D:\werev\out -Force | Out-Null
$env:JAVA_HOME = "D:\werev\jdk"
$env:GHIDRA_JAVA_HOME = "D:\werev\jdk"
$env:PATH = "D:\werev\jdk\bin;" + $env:PATH
$env:GHIDRA_HEADLESS_MAXMEM = "6G"
foreach ($s in @("wetype_service.exe","wetype_server.exe")) {
  $n = $s -replace "\.exe$",""
  "===== ANALYZING $s ====="
  & "D:\werev\ghidra\support\analyzeHeadless.bat" "D:\werev\proj" $n -import "D:\werev\samples\$s" -postScript IndexDump.java "D:\werev\out\$n.index.txt" -scriptPath "D:\werev\scripts" -deleteProject 2>&1 | Select-String -NotMatch "^(INFO|WARN)" | Select-Object -Last 25
}