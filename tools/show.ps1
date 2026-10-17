$R = "D:\VibeCoding\微信输入法逆向\out\reports"
function Sec($file, $name, $max) {
  $c = Get-Content (Join-Path $R $file) -Raw
  $i = $c.IndexOf("===== [" + $name + "]")
  if ($i -lt 0) { return "  <none>" }
  $nx = $c.IndexOf("===== [", $i + 10)
  if ($nx -lt 0) { $nx = $c.Length }
  return $c.Substring($i, [Math]::Min($max, $nx - $i))
}
"##### wetype_server ANTI-DEBUG #####"; Sec "wetype_server.exe.probe.txt" "ANTI-DEBUG" 4000
"##### wetype_server KEYS #####"; Sec "wetype_server.exe.probe.txt" "KEYS" 3000
"##### wetype_server IPC #####"; Sec "wetype_server.exe.probe.txt" "IPC" 2000
"##### wetype_server HOOK #####"; Sec "wetype_server.exe.probe.txt" "HOOK/INJECT" 2000