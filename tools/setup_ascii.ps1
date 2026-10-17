$ErrorActionPreference="Continue"
New-Item -ItemType Junction -Path D:\werev\ghidra -Target "D:\VibeCoding\微信输入法逆向\tools\ghidra\ghidra_12.1.4_PUBLIC" -ErrorAction SilentlyContinue | Out-Null
New-Item -ItemType Junction -Path D:\werev\jdk -Target "D:\VibeCoding\微信输入法逆向\tools\jdk\jdk-21.0.12.1+1" -ErrorAction SilentlyContinue | Out-Null
New-Item -ItemType Junction -Path D:\werev\scripts -Target "D:\VibeCoding\微信输入法逆向\tools\ghidra_scripts" -ErrorAction SilentlyContinue | Out-Null
Get-ChildItem D:\werev | Select-Object Name,LinkType | Format-Table -AutoSize | Out-String
Test-Path D:\werev\ghidra\support\analyzeHeadless.bat
Test-Path D:\werev\jdk\bin\java.exe
Test-Path D:\werev\scripts\IndexDump.java
Get-ChildItem D:\werev\scripts | Select-Object -ExpandProperty Name