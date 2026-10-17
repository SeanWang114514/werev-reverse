$env:JAVA_HOME = "D:\werev\jdk"
$env:GHIDRA_JAVA_HOME = "D:\werev\jdk"
$env:PATH = "D:\werev\jdk\bin;" + $env:PATH
$env:GHIDRA_HEADLESS_MAXMEM = "6G"
foreach ($s in @("wetype_server.exe","wetype_tip_core.dll","libwxhld.dll")) {
  $n = $s -replace "\.[a-z]+$",""
  "===== $s ====="
  & "D:\werev\ghidra\support\analyzeHeadless.bat" "D:\werev\proj" $n -import "D:\werev\samples\$s" -postScript VtableDump.java "D:\werev\out\$n.vt.txt" 96 -scriptPath "D:\werev\scripts" -deleteProject 2>&1 | Select-String -Pattern "VtableDump|ERROR|Exception" | Select-Object -Last 8
}