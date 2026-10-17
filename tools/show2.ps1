$d = "C:\Program Files\Tencent\WeType\2.1.4.6\flutter_datas\business_data"
"=== AssetManifest.json head ==="
(Get-Content "$d\flutter_assets\AssetManifest.json" -Raw).Substring(0, 2000)
"=== FontManifest ==="
Get-Content "$d\flutter_assets\FontManifest.json" -Raw
"=== shaders ==="
Get-ChildItem "$d\flutter_assets\shaders" | Select-Object -ExpandProperty Name
"=== assets/modules tree (files) ==="
Get-ChildItem "$d\flutter_assets\assets" -Recurse -File | Group-Object { $_.Directory.Name } | Select-Object Name,Count | Format-Table -AutoSize | Out-String -Width 120
"=== candidate json ==="
Get-ChildItem "$d\flutter_assets\assets\modules\candidate\json" -File -ErrorAction SilentlyContinue | Select-Object Name,Length | Format-Table -AutoSize | Out-String