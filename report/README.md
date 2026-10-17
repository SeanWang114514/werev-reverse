# 微信输入法逆向 — 产物索引

工作区：`D:\VibeCoding\微信输入法逆向`

## 主交付物

| 文件 | 说明 |
|---|---|
| `报告\微信输入法逆向分析报告.md` | **主报告**（约 59.5 KB / 847 行，12 章） |
| `报告\_p1.md` / `_p2.md` / `_p3.md` | 报告分卷源文件 |

报告章节：
0. 结论速览
1. 样本与安装布局（目录树 / 哈希 / 运行时数据目录）
2. 进程与模块架构（架构图 / IPC / 消息总线协议）
3. 模块详解（tip 薄壳 / TSF 注册 / tip_core / server / libwxhld / 网络栈 / Flutter / 其他）
4. 通信协议全谱（158 个 .proto 还原）
5. 远程命令执行框架（17 种命令 + replay_input）
6. 上下文捕获与隐私（明文日志取证）
7. 词典与数据格式（BuildIn 37 项 + LevelDB + 语音模型）
8. 网络与加密（Cronet / WebSocket / mars / ECDH+AES / pinning / xlog）
9. 反调试、完整性校验与沙箱
10. 更新机制
11. 工具链与复现方法
12. 附录（字符串 / 函数 / 未完成项索引）

## 样本副本

`samples\`：app.so、flutter_windows.dll、ime_net.dll、input_dll_import_lib.dll、libwxhld.dll、
wcwss.dll、wetap_business.dll、wetype_renderer.exe、wetype_server.exe、wetype_service.exe、
wetype_tip_core.dll、WeUIResource.dll、XNet.dll
`samples\runtime\`：本机运行时数据目录副本（robocopy /B）

## 分析产物（out/）

| 目录 | 内容 |
|---|---|
| `out\pe\` | 28 个 PE 结构 JSON（节区/导入/导出/签名/时间戳/PDB） |
| `out\strings\` | 26 个字符串表（ASCII + UTF-16LE）+ 关键词命中 |
| `out\proto\` | **158 个还原的 .proto**（tip_core 81 / server 40 / renderer 30 等） |
| `out\classes\` | 13 个 RTTI 类清单（命名空间 → 类名） |
| `out\rtti\` | 13 个原始 RTTI 类型描述符命中 |
| `out\dart\` | 14 个 Dart AOT 产物（ELF 结构 / 快照字符串池 / 模块树 / KV / 域名） |
| `out\logstr\` | 26 个内嵌源码路径 + 限定函数名清单 |
| `out\reports\` | 30 个聚合报告（URL/域名/PDB/路径/词典格式/上下文统计） |

## Ghidra 产物（D:\werev\out\）

| 文件 | 大小 | 内容 |
|---|---|---|
| `wetype_server.index.txt` | 1.6 MB | 程序元信息 / 内存块 / 函数表 / 导入 / 已定义字符串 |
| `wetype_service.index.txt` | 394 KB | 同上 |
| `wetype_server.vt.txt` | 3.4 MB | vftable + RTTI 全量 dump（1933 vftable / 1025 RTTI） |
| `wetype_server.vtables.json` | 1.06 MB | 解析后的 **790 个真实 vtable** |
| `addrs.txt` | 5 KB | 各关键类前 10 个 vtable 槽地址 |
| `find\server_wechat.txt` | 127 KB | 微信消息处理路径反编译（16 函数） |
| `find\tip_reg.txt` | 93 KB | TSF 注册 + 保留键反编译（22 函数） |
| `find\wxhld_remote.txt` | 远程命令执行框架反编译（20 函数） |
| `find\server_vt_funcs.txt` | 47 KB | vtable 方法反编译 |

## 工具（tools/）

| 脚本 | 作用 |
|---|---|
| `pe_report.py` / `sum_pe.py` | PE 结构 + 签名 + 导入导出 |
| `strings_x.py` | ASCII/UTF-16LE 字符串提取 |
| `anal_strings.py` / `probe.py` / `g.py` | 字符串聚合与关键词探测 |
| `pb_extract.py` | protobuf FileDescriptorProto → .proto |
| `rtti_scan.py` / `rtti_classes.py` / `cls_show.py` | RTTI → 类清单 |
| `logstr.py` | 内嵌源码路径与函数名 |
| `elf_dart.py` / `dart_scan.py` / `dart_agg.py` | Dart AOT 解析 |
| `dict_hdr.py` / `dict_deep.py` / `dict_fmt.py` / `dict_tbl.py` | 词典格式测绘 |
| `refetch_stat.py` | 上下文捕获日志统计 |
| `xlog_*.py` | mars xlog 解密尝试（结论：TEA 加密，静态不可解） |
| `pk_table.py` / `pk_table2.py` | TSF 保留键表解析 |
| `vt_parse.py` / `vt_show.py` / `vt_addrs.py` | vtable 解析 |
| `wxhld_exports.py` | libwxhld 导出清单 |
| `idx.py` | Ghidra index 分段过滤 |
| `pipfix.py` | 绕过损坏的 pip 直接解包 wheel |
| `ghidra_scripts\*.java` | IndexDump / DecompileFuncs / VtableDump / FindStr / DecompileAddrs |
| `run_ghidra.ps1` / `run_find.ps1` / `run_vt.ps1` / `setup_ascii.ps1` | Ghidra headless 封装 |

## 复现要点

1. 建立 ASCII junction 根 `D:\werev\`（避免中文路径破坏 .bat 参数）：
   `ghidra` / `jdk` / `scripts` / `samples` / `out` / `proj`
2. `JAVA_HOME` / `GHIDRA_JAVA_HOME` 指向 JDK 21；`proj` 目录必须先存在。
3. 已导入项目必须用 `-process <bin> -noanalysis`，不能重复 `-import`。
4. pattern 含 `|` 时必须走 `@file` 传参（否则被 cmd 当管道）。
