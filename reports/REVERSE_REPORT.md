# 微信输入法（WeType）2.1.4.6 / 3.0.0.34 逆向分析报告

> 用途：本地学习研究。所有样本均为本机已安装的公开分发包，未修改、未联网重放。
> 样本目录：`C:\Program Files\Tencent\WeType\{2.1.4.6,3.0.0.34}`，工作副本在 `D:\VibeCoding\微信输入法逆向\samples`。

## 0. 一句话结论

微信输入法不是「一个输入法程序」，而是**五进程 + 一套 IPC 总线 + 一个自研拼音引擎 + 一个 Flutter 界面 + 一整套云端 AB 配置**的组合体：

| 进程 / 模块 | 角色 |
|---|---|
| `wetype_server.exe` | 输入法引擎宿主（拼音/五笔/会话/词典/剪贴板/跨设备同步/上报），JSON+protobuf 命令总线 |
| `libwxhld.dll` | 真正的输入引擎（wxime），从 mozc 改造而来，内含 LightGBM + NNLM + XNet + TFLite 多后端 |
| `wetype_tip_core.dll` | TSF 文本服务（TIP），挂进宿主程序的输入线程，负责取上下文/上屏 |
| `wetype_renderer.exe` | Flutter(Dart AOT) 界面：候选窗、设置、剪贴板、翻译、语音 |
| `wetype_service.exe` | 服务管理进程（WeType Management Service） |
| `ime_net.dll` / `wcwss.dll` / `wetap_business.dll` / `XNet.dll` | 网络栈（Cronet + WebSocket + 自定义握手 + 深度学习推理） |

核心通信：命名管道 `\\.\pipe\wetype.*` + 共享内存 mmap + protobuf；UI↔TIP 用 `RendererCommand`；TIP↔server 用 `CommandV1/CommandBase`。

---

## 1. 模块划分与关键类

### 1.1 `wetype_server.exe`（引擎宿主）

RTTI 提取到 193 个命名空间 / 852 个类，vtable 导出 790 张。核心：

- `wetype::server::enginev2::{ImeEngine, WximeImpl, SessionInfo}` —— 引擎门面，`WximeImpl` 是 `libwxhld` 的 C API 包装。
- `wetype::server::data::{Config, KvHolder, LevelDBKV, PrefixDB, IKV}` —— LevelDB 键值层（用户词典/服务端 KV 都用它）。
- `wetype::server::handler::{CmdTransfer, DictManager, DictUpdater, GroupInfoTransfer, InputProcessor}` —— 命令分发。
- `wetype::server::clipboard::ClipboardDataManager` —— 剪贴板历史。
- `wetype::server::cross_platform::{CrossPlatformManager, MsgWindowManager, ClipboardHelper}` —— 跨设备同步。
- `wetype::server::wechat_message::WeChatMessageManager` —— 与微信客户端的表情/令牌联动。
- `wetype::server::network::Network`、`report::ImeReport`、`performance_monitor::PerformanceMonitor`、`vmode::VmodeDataManager`。
- `wetype::base::UniqueNamedPipe` —— 命名管道封装（`Connect/Receive/Send` + `GetNamedPipeClientProcessId`）。

### 1.2 `libwxhld.dll`（wxime 引擎）

2578 个类，706 个命名空间。分层：

- **会话层** `wxime::engine::session`（135 类）：`PinyinV2Session`、`WubiSessionV2`、`EnglishSessionV2`、`StrokeSession`、`NumberSession`、`AsyncSessionV2`、`VModeV2`、`CloudGeneralSearch`、`CloudLlmSearch`、`MostLikely*` 系列、`InterceptSensitiveResult`（敏感词拦截）、`SimplifiedToTraditional`（简繁）。
- **搜索层** `wxime::engine::searchers_v2`（60 类）：`SentenceSearcherV3`、`AsyncNNLMRanker`、`MixRank`、`WordSearchBySyllableGraph`、`UserDictSyllableGraph`，配合 `*BeamSizeSchedulerFunctor` 做 beam search 调度。
- **模型层** `wxime::engine::model`（33 类）：`lightgbm_model`、`nn_lm_model`、`xnet_nn_lm_model`、`tflite_nn_lm_model`、`decoder_only_gpu_nn_model`、`english_e2e_model`。
- **词典层** `wxime::data::dict`（190 类）：`large_dict` / `trie_index_large_dict` / `compact_kv_large_dict` + `*_huffman_codec`，用户词典 `user_dict_v2(_patch)`、`user_hot_word_*`、`sensitive_trie_dict`、`merged_intercept_sensitive_dict`。
- **云同步** `wxime::engine::group_sync`：`user_dict_syncer(_full/_inc)`、`user_hot_word_syncer`、`user_data_import_and_export`。
- **远程控制** `wxime::core::remote_command_executor` + `ReplayInput` —— 可从远端文件执行命令并回放输入（仅本机文件路径驱动，是内部调试通道）。

### 1.3 `wetype_tip_core.dll`（TSF 层）

652 个类。`wetype::win32::tsf::TipTextServiceImpl` 实现 `ITfTextInputProcessor`；保留键处理器 `PreservedKeyActionHandler` 及 4 个子类。

**实测保留键表**（静态表 `0x180363f58`，stride 0x30）：

| 名称 | vk | mod | action | 说明 |
|---|---|---|---|---|
| 全半角输入切换 | 0x20 | 4 | 7 | 空格+Ctrl 系组合 |
| 中文下中英标点切换 | 0xBE | 2 | 9 | 句号+Shift |
| 简繁体输入切换 | 0x46 | 6 | 7 | F+Ctrl+Shift |
| 快速唤醒AI问答 | 0x49 | 3 | 8 | I+Ctrl+Alt（可由配置覆盖） |

### 1.4 `wetype_renderer.exe`（Flutter 界面）

16.7MB Dart AOT 快照（`app.so` 是 ELF64，不是 PE）。387 个 Dart 模块，`package:my_desktop_app`：

- `modules/candidate`(109)、`modules/setting`(61)、`modules/clipboard`(19)、`modules/hotword`(16)、`modules/file_transfer`(15)、`modules/translation`(14)、`modules/voice`(8)、`modules/upgrade`(6)。
- 45 个 protobuf 生成文件（`common/protos/generated/*.pb.dart`）。
- 8 个 MethodChannel：`floatingChannel`、`kvChannel`、`logChannel`、`settingsChannel`、`stateChannel`、`upgradeChannel`、`utilChannel`、`voiceChannel`。
- 第三方：`sentry_flutter`（崩溃上报）、`webview_windows`、`window_manager`、`desktop_drop`、`encrypt`(AES)、`qr_flutter`、`lottie`。

---

## 2. 协议全貌

从 PE 里直接扫 `FileDescriptorProto` 还原出 **151 个 .proto**（server 40 / renderer 30 / tip_core 81），渲染稿在 `out/proto/<binary>/`。

### 2.1 IPC 与命令总线

```proto
// ipc.proto  —— 命名管道身份握手
package wetype.ipc;
message IPCPathInfo { required string key = 1; required uint32 process_id = 2;
  required uint32 thread_id = 3; required uint32 protocol_version = 4;
  required string product_version = 5; }

// renderer_command.proto —— TIP → Renderer 的窗口控制
package wetype.commands;
message RendererCommand { required int32 type = 1; optional KeyEvent key = 2;
  optional ApplicationInfo application_info = 4; optional Point menu_bar_pos = 7;
  optional StatusInfo input_status = 10; ... }
enum CommandType { NOOP=0; UPDATE=1; SENDKEY=2; SHUTDOWN=3; CHANGEPOS=4;
  SELECT_CUR_CANDIDATE=5; SHOW_FAST_MENU=8; MOVE_CURSOR=14; SUBMIT_PENDING=16; }
```

`commands.proto`（1271 行 / 43KB）是引擎命令总线：`KeyEvent`（77 个 `SpecialKey` 枚举 + 位标志 `ModifierKey`）、`CandidateList`、`PendingWord`、`FuzzyPYInfo`（20 个模糊音开关）、`DictItem`、`Input`。

### 2.2 微信联动（`wetype_wechat.proto`）

`WTVerifyToken` → `WTSayHello` → `WTSupportEmoji` → `WTEmitEmoji`。`WTEmitEmojiRequest` 里带 `Md5`、`FileName`、**`AesKey`**、`FileType`、`PendingText`、`sessionId` —— 表情包是「先拉文件、再用会话里下发的 AES key 解密、再塞进输入框」。错误码 `ErrorTokenExpired=6`、`ErrorDecryptFail=3`、`ErrorInputBoxNotFirstResponder=5`。

### 2.3 跨设备（`multi_platform_sync.proto`）

`GetMatchCode` → `BindMatchCode` → `FetchBindStatus` → `SendClipboardMsg`；`ClipboardMsg` 字段：`version,type,data,expire_at,binary_data,from_uin,extra_info,trace_id`。另有 `UserHotWords` 同步。

### 2.4 词典下发（`update.proto`）

`ImeDictDownloadItem { cdnUrl, md5, cdnKey, decryptMd5, algorithm, compressionMd5 }` —— 词库走 CDN，带独立 `cdnKey` 与 `decryptMd5`（下载后二次校验），`ImeDictCondition` 控制投放条件，`ABTestHitedInfo.HitType{WhiteList,LaunchLayer,BaseAB,DefaultParam}` 做灰度。

### 2.5 前端 AI（`WtAskAI.proto`）

`BaseReq{id,uin,cmd,header,body}` + `CmdStartPageReq{res_key,is_used}` + `CmdMultiTurnReq`，`CmdId{CmdTypeStartPage=1,CmdTypeMultiTurn=2}` —— AI 问答是**服务端渲染 HTML 回填到 WebView**，不是客户端本地生成。

---

## 3. 网络与加密

三层栈：

1. **`ime_net.dll`（wetap::net）** —— 自研隧道。握手：`ECDHPubKeyReq_V2` → `GenUinReq_V2` → `GetSvrTimestamp`，本地 `ThreadSafeECDHKey::GenerateAesKey` 由 ECDH 派生对称密钥；之后 `Crypto::AES::Encrypt/Decrypt`（CryptoPP Rijndael）。日志里明确打印 `get aes key success, aes_key:%s***%s ret %d`。
2. **`wcwss.dll`** —— WebSocket 客户端（websocketpp + boost::asio + HappyEyeballs）。请求头带 **`sign` + `body_md5` + `timestamp` + `device_code` + `uin` + `cmd_id`** 的鉴权签名方案。
3. **`libcurl`（嵌在 server 内）** —— HTTPS，启用 **证书公钥固定**：`CURLOPT_PINNEDPUBLICKEY` 格式 `sha256//<base64>`，错误串 `SSL public key does not match pinned public key`。

静态扫描结论：**无内嵌 PEM 私钥、无硬编码静态密钥**；AES 密钥全部运行时由 ECDH 派生或服务端随会话下发。

---

## 4. 词库体系（重点）

### 4.1 两级词库

- **内置 `BuildIn/`**（29 个文件，随安装包）：基础词典 + 语言模型 + 编码表。
- **云端 `Dict/`**（`cell_dict.ssrc` / `cell_dict.newhot.common` / `cell_dict.fi`）：按 `version` 建子目录（`763/`、`1332/`、`7369/`），`CommonDictIndexV2.json` 与 `HotDictIndexV2.json` 记录 `md5 / version / timestamp / type / dict_type / is_new_hot / match_version`。

### 4.2 内置词库格式实测（29 个文件的完整体检见 `out/reports/buildin_catalog.tsv`）

| 文件 | 大小 | type | 格式判定 |
|---|---|---|---|
| `tts.bin` | 18,744 | 65573 | **完全可读**：u32[0]=0 后接连续 UTF-8「繁体+简体」成对字表，117 段 |
| `cell_dict.hf.zh` | 1,087,688 | 0 | 高频字转移表；尾部 89 条记录格式已定，中段为压缩流 |
| `nlrgpt2_nnlm.bin` | 16,211,368 | 65557 | **TensorFlow Lite flatbuffer**（`TFL3` @9），神经网络语言模型 |
| `md.bin` | 22,482 | 262145 | u64[0]=1 + ASCII hex 哈希表 |
| `swbd86/98/nc.bin` | ≈4.1MB×3 | 524291 | **五笔编码表**，纯 ASCII 编码串，可完整导出 |
| `bwcjpmac_jianpin.bin` | 12,630,429 | 65546 | 简拼索引；`0x25f600` 起为明文拼音表（`liang,sa'n,tian` 等） |
| `noun_tag_dict.bin` | 4,253,612 | 65580 | 名词标签（3.0 新增）；记录 = `[type:u32][4B token × type][标志串]`，词文本走独立 ID 空间 |
| `lmcnmac.bin` | 16,758,278 | 131072 | `u32[0]=0x80000001` + 递增偏移表的**分片 KV** |
| `ckvdmac.bin` | 39,717,069 | 65622 | 同上家族，超大 KV 分块 |
| `bwcnmac.bin` / `bwcnmacv8.bin` | 30.4MB / 31.7MB | 65536 / 65581 | 多音字/词转移主库，压缩块 |
| `slwd_pc_second_level.bin` | 51,694,531 | 65551 | 二级词库，最大文件，压缩流 |
| `sepd.bin` / `cell_dict.ssrc.zh` | 875KB / 320KB | 65571 / 7 | `Ime trie header` 前缀 → **trie 索引**（负偏移相对指针编码） |
| `cell_dict.sc.zh` | 32,056 | 0 | 简拼 cell dict |
| `pcc.bin` | 359,015 | 65565 | 与 cell_dict 同族（`0x56eaea00` 版本戳） |
| `stt.bin` / `wsd.bin` / `editpinyin.bin` | 1.2MB / 226KB / 727KB | 65572 / 65549 / 65625 | `u32[0]=0x80000001` 分片家族 |
| `wkvc2e.pc.bin` / `wwkvc2e.bin` | 1.1MB / 143KB | 65553 / 65566 | 词向量（word2vec）表，词以 32bit hash 引用 |
| `mdltrpc.bin` | 2,286,728 | 262149 | 带浮点权重的规则/特征配置（含 -3.0f / 0.6f 常量） |
| `prism_v2.bin` | 11,994 | 65578 | 3-bit 打包量化表 |
| `hpmac_base.bin` | 1,872 | 262144 | 高优先级词偏移/计数对 |
| `ln2py.bin` | 18,706 | 65547 | 字母→拼音映射 |
| `bccn.bin` / `bwcnenmac.bin` | 153KB / 6.0MB | 65538 / 65537 | 英文词库与 BPE/权重表 |

统一版本戳 `0x56eaea00`（1458176000 = 2016-03-17）出现在 cell_dict / pcc / hf 家族头部，是这套二进制格式的生日。

### 4.3 用户词典（LevelDB，可完整解码）

路径 `...\DictDir2\v5\<uid>\*.ldb`。SSTable 结构：footer magic `0xdb4775248b80fb57`，data block 前缀共享 key。

**key 命名规则：`!<namespace>!<文本>`**

| namespace | 含义 | 样本 |
|---|---|---|
| `user_prefix2` | 用户输入过的前缀/联想法 | `!user_prefix2!<用户输入过的短语>`（实测存在大量中文短语） |
| `user_prefix_and_emoji!E!` | 前缀+表情组合 | `!user_prefix_and_emoji!E!<短语+emoji>` |
| `disd` | 热词基础记录 | 12B value |
| `eadc` | 热词大块（**逐字节 +7 位移混淆**） | `<位移样本已打码>` |
| `eadp!kHintInfoV2` | 热词提示 | — |
| `hwsc!CurrentInfoV2` / `hwsc!UserHotWordDictLastModifyTime` | 热词版本戳 | — |

`user_prefix2` 的 value 固定 31B，形如 `08 06 06 06 ab 68 71 70 06…18 00 00 00 5a a5 5a`：尾 `5a a5 5a` 校验哨兵、`18 00 00 00` 计数字段、主体是按 `06` 分隔的 3 字节 huffman 编码值 —— 对应 `wxime::data::dict::large_dict_value_huffman_codec`，真实词条 ID 要到 huffman 表里再查一层。

### 4.4 服务端 KV 与云控配置（`ServerKvDir\*.ldb`）

key 全部为 `config<字段>`，是**云端配置中心的本地缓存**：

- `configsessionConfig`（**明文 JSON**）：`cloud_engine_opt{cloud_search_by_input_predict_next_n:1, cloud_search_by_input_return_cnt:3, enable_cloud_correction:false, enable_cloud_most_likely:false}`、`enable_spelling_plus:true`、`input_augment_option`（30+ 模糊音/纠错开关）、`wubi_config{}`、`is_default_chinese:true`。
- `configab_params`（protobuf）：**云端下发的 AB 实验参数表**，实测出来的真实键值：
  - `mmkb_cli_engine_cloud_time_out_ms` = **`550`**（引擎内部硬编码默认 200ms，云端拉高到 550ms）
  - `mmkb_cli_engine_association_offline_expt_v2` = `14`
  - `mmkb_cli_engine_user_dict_clean_strategy` = `128,2,100000,10,5,2592000,30000,1`
  - `mmkb_cli_engine_cloud_local_merger_protect_user_expt` = `0.1,604800,2,1.0,1000`
  - `mmkb_cli_engine_pc_graph_v3_new` = `1`、`mmkb_cli_engine_pc_allow_cloud_force_top1_expt` = `1`
- `configwechat_token`（protobuf）：216 字符 Base64 形状的微信会话令牌。
- `vmodeclipboard`：**21.6MB 剪贴板历史**（`{文本, 毫秒时间戳, type=2}`），含真实用户复制内容。

---

## 5. 离线 / 联网行为（人话版）

**结论先说：核心打字 100% 离线；联网只做「锦上添花 + 云端遥控」。**

### 打字（最核心）——断网无感

内置了完整拼音词库、五笔词库、n-gram 语言模型（16MB TFLite）、beam-search 解码器。这些全在 `BuildIn/` 里，装完即用。断网只是少了「云端一句话补全」。

### 云候选 —— 到点就砍

`CloudInputMerger` 的构造函数里写死 `max_timeout_ms_ = 200`（毫秒）。每次输入按长度查一张 `timeout_by_input_length_` 表得到预算，超了就直接丢弃云结果并打日志 `Cloud search result skip. time cost ms is X, but max cost ms is Y`。所以云端再慢也不会卡键盘。而这张预算表由云端 `configab_params` 下发（本机实测被抬到 **550ms**）。

### AI 问答 / 翻译 / 表情 —— 完全依赖云端

AI 是服务端渲染 HTML 回 WebView（`CmdStartPageReq`/`CmdMultiTurnReq`）；表情包要先 `WTVerifyToken` 拿会话，再下载文件用 `AesKey` 解密。断网这些功能直接不可用。

### 语音 —— 半离线

`voice_engine\vad\` 里有本地 VAD 模型（`model_16k_20210121_iter07.bin`、`CMS_40dim_chi.bin`）做端点检测，识别本身走云。Dart 侧有 `voice_input_action_download_offline` 埋点 → 说明存在可下载的离线语音包。

### 那么「离线模式」按钮是干嘛的？

`wt_pc_app_action_click_open_offline_mode` 这类埋点**只出现在 Dart/UI 层，server 与引擎里一条都没有**。也就是说：所谓离线模式只是 UI 状态位 + 提示文案（`wt_pc_app_scene_offline_mode_pc_notice`），引擎侧并没有「离线分支」——它本来就是离线的，联网失败时云候选超时被丢、自动降级到本地结果。

### 云端能控制什么（本机实测）

通过 `configab_params` 下发：云超时、云候选条数、AB 分组、用户词典清理阈值（`128,2,100000,10,5,2592000,30000,1`）、联想词离线实验组、图 v3 开关、是否允许云端强制 top1。词典本体也走 CDN 按版本下发（`cell_dict.newhot.common` 已到 `v7369`）。

---

## 6. 隐私面（客观记录）

1. **上下文捕获**：`context_capture\refetch_sync_legacy.log`（926KB，**明文**）记录了 2571 次「重新抓取宿主文本」，含 `host_exe`（chrome.exe 1839 次 / conhost 182 / chatgpt.exe 133 / explorer 133 / weixin 48 …）、`before_text` / `after_text` / `selected_text`。即 TIP 通过 TSF 读到了宿主输入框前后文与选中文本。
2. **剪贴板历史**：`vmodeclipboard` 存了 21.6MB 完整复制历史（明文）。
3. **崩溃上报**：Sentry（`https://wetype.weixin.qq.com/sentry/api/14/envelope/` + `minidump_v2`）。
4. **上报协议** 30+ 个：按键活跃度、候选点击、剪贴板动作、云候选行为、性能耗时、异常事件、AB 命中。
5. **日志加密**：`MM_*.xlog` 是 mars xlog 格式，payload 经 TEA 加密（`mars::xlog::LogCrypt`），**静态不可解**；唯一明文日志就是上面那份 context_capture。

---

## 7. 产物索引

| 路径 | 内容 |
|---|---|
| `out/proto/<bin>/*.proto` | 151 个还原出的 protobuf schema |
| `out/reports/buildin_catalog.tsv` | 29 个内置词库的类型/大小/头部指纹 |
| `out/reports/libwxhld_cn_strings.txt` | libwxhld 内 704 条中文字符串（行政区划/节日/节气/星座文案） |
| `out/reports/tts_trad_simp.txt` | tts.bin 繁简对照表（117 段） |
| `out/reports/cell_dict_fi_pinyin.txt` | cell_dict.fi 的 113 条拼音词条（节日热词） |
| `out/reports/serverkv.txt` / `serverkv_pb.txt` | 服务端 KV 云控配置（含 AB 参数树） |
| `out/reports/noun_tag_rows.tsv` | noun_tag_dict 记录结构（193344 条） |
| `out/strings_buildin/*.tsv` | 每个内置词库的 ASCII/UTF-16 串表 |
| `out/wetype_server.vtables.json` | 790 张 vtable + 槽位目标 |
| `out/classes/*.classes.txt` | 11 个二进制共 ~7000 个 C++ 类（RTTI 反解） |
| `out/dart/app_iso_strings.txt` | Dart AOT 快照字符串池（32312 条） |

---

## 8. 未能完成的部分（如实标注）

- **`Ime trie` 格式**（`sepd.bin` / `cell_dict.ssrc.zh`）：节点用负偏移相对指针编码，尚未逆出解码器。
- **`user_prefix2` value 的 huffman 表**：3 字节编码值到真实词条 ID 的映射表未定位。
- **`noun_tag_dict` 的词文本**：记录里只有 32bit token，文本在同 ID 空间的另一张表，未配平。
- **`bwcnmac` / `slwd_pc_second_level`** 的压缩块（疑似 zstd/LZ4 变体 + 分块索引），未解。
- **mars xlog**：TEA 密钥在进程内，静态不可还原。

这些都是明确的技术边界，不是访问限制。
