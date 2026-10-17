# 微信输入法（WeType）Windows 版逆向分析

对腾讯微信输入法（WeType）Windows 客户端做的静态逆向工程研究报告与全部可复现产物。

> **性质说明**：本仓库仅包含**分析结论、还原的协议 schema、反编译文本与工具脚本**，不包含任何腾讯的原始二进制、词典数据或用户运行时数据。所有样本均为本机已安装的官方签名分发包，分析过程除静态读取外未做任何修改。

## 目标版本

| 项 | 值 |
|---|---|
| 产品 | 微信输入法（WeType） |
| 分析版本 | 2.1.4.6（主报告）；词库章节已按升级后的 **3.0.0.34** 复核 |
| 平台 | Windows x64（另有 x86 TIP 核心） |
| 签名 | Authenticode 有效，`CN=Tencent Technology (Shenzhen) Company Limited` |

## 一句话结论

它不是一个输入法程序，而是「五进程 + 一套命名管道 IPC 总线 + 自研拼音引擎 + Flutter 界面 + 整套云端 AB 配置」的组合体：

| 模块 | 角色 |
|---|---|
| `wetype_server.exe` | 引擎宿主：会话 / 词典 / 剪贴板 / 跨设备同步 / 上报 |
| `libwxhld.dll` | 真正的输入引擎（`wxime`），拼音核心源自 **Google mozc**，排序器含 LightGBM + 多后端神经网络 |
| `wetype_tip_core.dll` | TSF 文本服务（TIP），挂进宿主输入线程，负责取上下文与上屏 |
| `wetype_renderer.exe` | Flutter（Dart AOT）界面：候选窗 / 设置 / 剪贴板 / 翻译 / 语音 |
| `wetype_service.exe` | 服务管理进程 |
| `ime_net.dll` / `wcwss.dll` / `XNet.dll` | 网络栈（Cronet + WebSocket + 自定义 ECDH 握手）+ 自研 DNN 推理 |

核心通信：命名管道 `\\.\pipe\wetype.*` + 共享内存 mmap + protobuf。

## 仓库结构

```
report/            主报告（12 章，约 59 KB）+ 分卷源文件
proto/             151 个从 PE 描述符还原的 .proto（按二进制分目录）
classes/           RTTI 反解出的 C++ 类清单（~7000 个类，13 个二进制）
rtti/              原始 RTTI 类型描述符命中
dart/              Dart AOT（app.so）解析：ELF 结构 / 快照字符串池 / 模块树 / KV key / 域名
logstr/            内嵌源码路径 + 限定函数名（PDB 路径、开发机目录）
pe/                28 个 PE 结构 JSON（节区 / 导入 / 导出 / 签名 / 时间戳 / PDB）
ghidra/            Ghidra headless 产物：函数表、vtable dump、关键路径反编译文本
reports/           聚合报告：词库格式体检、云控配置、繁简表、拼音表、URL/密钥聚合
tools/             全部解析脚本（Python + Ghidra Java 脚本 + PowerShell 封装）
```

## 主要发现

### 1. 协议全貌（151 个 .proto）

直接从二进制里扫序列化 `FileDescriptorProto` 还原，不是猜的：

- `wetype.ipc` —— 命名管道身份握手（`IPCPathInfo{key, process_id, thread_id, protocol_version}`）
- `wetype.commands` —— 引擎命令总线（1271 行 / 43 KB，`KeyEvent` 77 个特殊键枚举、`CandidateList`、`FuzzyPYInfo` 20 个模糊音开关）+ `RendererCommand`（TIP → Flutter 的窗口控制，16 种 `CommandType`）
- `wetype.server`（微信联动）—— `WTVerifyToken` → `WTSayHello` → `WTEmitEmoji`，表情包用会话下发的 `AesKey` 解密
- `wetype.multiplatform` —— 跨设备剪贴板 / 热词同步（`GetMatchCode` → `BindMatchCode` → `SendClipboardMsg`）
- `wetype.update` —— 词典 CDN 下发（`ImeDictDownloadItem{cdnUrl, md5, cdnKey, decryptMd5, algorithm}`）+ AB 灰度（`HitType{WhiteList, LaunchLayer, BaseAB, DefaultParam}`）
- `wetype.pb.askai` —— AI 问答，服务端渲染 HTML 回填 WebView（`CmdStartPage` / `CmdMultiTurn`）
- `wetype.server`（文件传输）—— P2P 直连（`GrpcNetInfo`、`AvailableNets{awdl,lan,wfd}`），对应 `WXP2PTransfer.dll`

### 2. 网络与加密

三层栈：`ime_net.dll`（自研隧道，`ECDHPubKeyReq_V2` → `GenUinReq_V2` → `GenerateAesKey`，CryptoPP AES）→ `wcwss.dll`（WebSocket++，请求头带 `sign` + `body_md5` + `timestamp` + `device_code`）→ 内嵌 libcurl + OpenSSL 1.1.1k（**证书公钥固定**，`sha256//` pinning）。

静态结论：**无内嵌 PEM 私钥、无硬编码静态密钥**，AES 密钥全部运行时由 ECDH 派生或服务端随会话下发。

### 3. 词库体系

两级：内置 `BuildIn/`（29 个文件）+ 云端 `Dict/`（按 `version` 建子目录，`CommonDictIndexV2.json` 记 md5/version/timestamp）。

完全解出可读的：

| 文件 | 内容 |
|---|---|
| `tts.bin` | 繁简/异体字对照表（117 段）→ `reports/tts_trad_simp.txt` |
| `cell_dict.fi` | 56 条记录，113 条拼音词条（节日热词）→ `reports/cell_dict_fi_pinyin.txt` |
| `bwcjpmac_jianpin.bin` | 明文拼音表 + 57 万条简拼索引 |
| `swbd86/98/nc.bin` | 五笔编码全表（纯 ASCII） |
| `libwxhld.dll` | 704 条内嵌中文字面量：全国行政区划 521 条 + 二十四节气 + 中外节日表 + 星座文案 → `reports/libwxhld_cn_strings.txt` |

用户词典是 LevelDB（`DictDir2\v5\*.ldb`），key 规则 `!<namespace>!<文本>`（实测 namespace 如 `user_prefix2`、`user_prefix_and_emoji`，后者的 value 带 emoji 变体标记），value 是 31 字节 huffman 编码候选对（尾 `5a a5 5a` 校验哨兵）；热词库 `eadc` 命名空间的大块做了**逐字节 +7 位移混淆**。

未解出的格式（技术边界，如实标注）：`Ime trie header`（负偏移相对指针编码）、`noun_tag_dict`（纯 32bit token，文本在另一张表）、`bwcnmac` / `slwd_pc_second_level` 的压缩块、mars xlog 的 TEA 加密。

### 4. 离线 / 联网行为

**核心打字 100% 离线**。内置完整拼音/五笔词库 + 16MB TFLite 语言模型（`nlrgpt2_nnlm.bin`，`TFL3` flatbuffer）+ beam search 解码器。

云候选有硬性超时：`CloudInputMerger` 构造函数写死 `max_timeout_ms_ = 200`，每次输入按长度查预算表，超了直接丢弃（日志 `Cloud search result skip. time cost ms is X, but max cost ms is Y`）。这张表由云端 `configab_params` 下发，本机实测被抬到 **550ms**。

「离线模式」开关只存在于 Flutter/Dart 界面层（`wt_pc_app_action_click_open_offline_mode` 埋点），引擎侧没有任何「离线分支」——它本来就离线的。

### 5. TSF 保留键（反编译级确认）

| 名称 | vk | mod | action |
|---|---|---|---|
| 全半角输入切换 | 0x20 | 4 | 7 |
| 中文下中英标点切换 | 0xBE | 2 | 9 |
| 简繁体输入切换 | 0x46 | 6 | 7 |
| 快速唤醒AI问答 | 0x49 | 3 | 8 |

### 6. 隐私面（客观记录）

- **上下文捕获**：TIP 通过 TSF 读取宿主输入框前后文本与选中文本；`context_capture\refetch_sync_legacy.log` 是**明文**，实测 2571 条记录（1291 条成功），含 `host_exe`（chrome 1839 / conhost 182 / chatgpt 133 / explorer 133 / weixin 48）与 `before_text` / `after_text` / `selected_text` 原文。
- **剪贴板历史**：`vmodeclipboard` 键存了 21.6 MB 完整复制历史（明文）。
- 崩溃上报走 Sentry（`https://wetype.weixin.qq.com/sentry/api/14/envelope/` + `minidump_v2`），另有 CrashRpt、flurry。
- 40+ 个上报协议：按键活跃度、候选点击、剪贴板动作、云候选行为、性能耗时、异常事件、AB 命中。
- `MM_*.xlog` 是微信 mars xlog，payload 经 TEA 加密（`mars::xlog::LogCrypt`），静态不可解。

> 为保护隐私，本仓库**不包含**上述明文日志、剪贴板历史原文、微信会话令牌等任何运行时用户数据；`reports/serverkv_redacted.txt` 是对云控配置的脱敏版本。

## 复现方法

```bash
# 1. 环境：Python 3.12+，Ghidra 12.1.4 + JDK 21（headless 需要）
# 2. 把样本二进制放到自己的目录，改脚本里的路径常量
# 3. 逐步执行：

# PE 结构与签名
python tools/pe_report.py <binary>
# 字符串（ASCII + UTF-16LE）+ 关键词分组
python tools/strings_x.py <samples_dir> <out_dir>
python tools/probe.py <out_dir>
# RTTI → C++ 类清单
python tools/rtti_scan.py <binary>
python tools/rtti_classes.py <out_dir>
# protobuf 描述符还原（产出 .proto）
python tools/pb_extract.py <binary> <out_dir>
# Dart AOT 快照解析
python tools/elf_dart.py <app.so> <out_dir>
python tools/dart_scan.py <app.so>
# 词库格式测绘
python tools/bin_hdr.py <bin_file>
python tools/catalog.py <BuildIn_dir> <out.tsv>
# 用户词典 LevelDB 解码
python tools/ldb_dump.py <file.ldb> text 200
python tools/ldb_keys.py <file.ldb>
# Ghidra headless：函数表 / vtable / 按字符串追调用者并反编译
pwsh tools/run_ghidra.ps1 -bin wetype_server.exe -proj wtserver -script IndexDump
pwsh tools/run_ghidra.ps1 -bin wetype_server.exe -proj wtserver -script VtableDump
pwsh tools/run_find.ps1 -bin wetype_server.exe -proj wtserver -pattern "regex1|regex2" -out out.txt
```

## 工具链踩坑记录（省你几小时）

- Ghidra headless 在**含中文的路径**下会把 `.bat` 参数搞坏（报 `'\' is not recognized as an internal or external command`）→ 建 ASCII junction 根目录再跑。
- 对已存在的 Ghidra 项目重复 `-import` 会报 `Found conflicting program file in project` → 改用 `-process <bin> -noanalysis`。
- Ghidra 12.1.4 的 `getReferencesTo` 返回 `ReferenceIterator`，不能直接赋给 `Reference[]`。
- `pwsh -File x.ps1 -pattern "a|b"` 里的 `|` 会被 cmd 当管道 → 脚本里改成写 pattern 文件再传 `@file`。
- Python 往 PowerShell 管道输出非 GBK 字符会 `UnicodeEncodeError` → 脚本头 `sys.stdout.reconfigure(encoding='utf-8', errors='replace')` + `$env:PYTHONIOENCODING="utf-8"`。

## 免责声明

本仓库内容仅供**安全研究与技术学习**。所有分析对象均为本机合法安装的公开软件分发物，未进行任何破解、绕过授权或分发行为。微信输入法无自研授权/序列号机制，本仓库亦不涉及此类内容。分析中未修改任何二进制，未对任何服务端发起攻击性测试。
