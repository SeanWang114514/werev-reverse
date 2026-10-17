param([string]$bin, [string]$proj, [string]$pattern, [string]$out, [int]$maxF = 30, [int]$depth = 1, [switch]$fresh)
$env:JAVA_HOME = "D:\werev\jdk"
$env:GHIDRA_JAVA_HOME = "D:\werev\jdk"
$env:PATH = "D:\werev\jdk\bin;" + $env:PATH
$env:GHIDRA_HEADLESS_MAXMEM = "8G"
$ah = "D:\werev\ghidra\support\analyzeHeadless.bat"
$dir = Split-Path $out -Parent
if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
# patterns go through a file: cmd.exe would otherwise interpret '|' inside .bat args as a pipe
$pf = "D:\werev\out\_pattern_$proj.txt"
if (-not (Test-Path (Split-Path $pf -Parent))) { New-Item -ItemType Directory -Force -Path (Split-Path $pf -Parent) | Out-Null }
$pattern -split '\|' | Set-Content -Path $pf -Encoding ascii
$existing = (Test-Path "D:\werev\proj\$proj.rep") -and (-not $fresh)
if ($existing) {
  & $ah "D:\werev\proj" $proj -process $bin -noanalysis -postScript FindStr.java $out "@$pf" decompile $maxF $depth -scriptPath "D:\werev\scripts" 2>&1 | Select-String -Pattern "FindStr|ERROR|Exception|not recognized" | Select-Object -Last 8
} else {
  & $ah "D:\werev\proj" $proj -import "D:\werev\samples\$bin" -postScript FindStr.java $out "@$pf" decompile $maxF $depth -scriptPath "D:\werev\scripts" 2>&1 | Select-String -Pattern "FindStr|ERROR|Exception|not recognized" | Select-Object -Last 8
}
