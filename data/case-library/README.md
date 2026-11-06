# 正式案例原始数据

本目录对应网站当前定版的 19 个案例：训练修正 5 例、推理对照 9 例、自主恢复 5 例。训练修正含“修正过程”和“指导对照”两个子类。

每例使用稳定 slug 命名，不随显示编号变化：

- `raw/`：原交付文件，内容及内部相对目录保持不变。
- `manifest.json`：原目录位置、文件清单、字节数和 SHA-256。
- `records.zip`：该案例的完整 `raw/` 和清单。

[index.json](index.json) 是统一机器索引，含编号、标题、原路径、新路径及下载包哈希。原记录内的历史路径、时间、校验清单原样保留，通过 manifest 的 originalRoot 对照迁移位置。data/cases 中其余材料是候选或历史记录，不属于本次定版集。

| 编号 | 案例 | 原始文件 | 下载 |
| --- | --- | --- | --- |
| T1 | 读取文件前，先确认所在目录 | [46 个文件](training/directory-navigation/manifest.json) | [ZIP](training/directory-navigation/records.zip) |
| T2 | 新建文件，写入第二个包含关键词的句子 | [120 个文件](training/create-and-write-matching-sentence/manifest.json) | [ZIP](training/create-and-write-matching-sentence/records.zip) |
| T3 | 解锁车门时，误把列表序号加进工具名 | [160 个文件](training/tool-list-numbering/manifest.json) | [ZIP](training/tool-list-numbering/records.zip) |
| T4 | 限制银行卡的使用范围，不能只填国家名单 | [130 个文件](training/card-country-restriction/manifest.json) | [ZIP](training/card-country-restriction/records.zip) |
| T5 | 创建工单前，先登录工单系统 | [326 个文件](training/ticket-login-before-create/manifest.json) | [ZIP](training/ticket-login-before-create/records.zip) |
| I1 | 调用 Java 工具，保留工具名与参数名的大小写 | [52 个文件](inference/java-node-interface/manifest.json) | [ZIP](inference/java-node-interface/records.zip) |
| I2 | 查询两项科学发现，保持工具名一致 | [52 个文件](inference/recipe-science-tools/manifest.json) | [ZIP](inference/recipe-science-tools/records.zip) |
| I3 | 查询导出列表，区分排序字段与方向 | [54 个文件](inference/export-sort-direction/manifest.json) | [ZIP](inference/export-sort-direction/records.zip) |
| I4 | 预订十一月航班，避免误读为十二月 | [54 个文件](inference/eleventh-month-flight/manifest.json) | [ZIP](inference/eleventh-month-flight/records.zip) |
| I5 | 查询历史舞者，避免误用馆藏工具 | [54 个文件](inference/dancers-not-museum-artists/manifest.json) | [ZIP](inference/dancers-not-museum-artists/records.zip) |
| I6 | 预订火车票前，先补齐出发地与目的地 | [54 个文件](inference/train-route-clarification/manifest.json) | [ZIP](inference/train-route-clarification/records.zip) |
| I7 | 移除自选股前，先确认公司名称 | [54 个文件](inference/watchlist-disambiguation/manifest.json) | [ZIP](inference/watchlist-disambiguation/records.zip) |
| I8 | 计算三个阶乘，逐项完成工具调用 | [52 个文件](inference/three-factorials/manifest.json) | [ZIP](inference/three-factorials/records.zip) |
| I9 | 创建三个文件后，继续写入指定内容 | [54 个文件](inference/files-written-before-reading/manifest.json) | [ZIP](inference/files-written-before-reading/records.zip) |
| R1 | 加油超量报错后，查询余量再补足 | [20 个文件](recovery/fuel-capacity/manifest.json) | [ZIP](recovery/fuel-capacity/records.zip) |
| R2 | 查询油量报错后，改正工具名再加油 | [20 个文件](recovery/tool-name-recovery/manifest.json) | [ZIP](recovery/tool-name-recovery/records.zip) |
| R3 | 写入报错后，先创建文件再重试 | [8 个文件](recovery/create-before-write/manifest.json) | [ZIP](recovery/create-before-write/records.zip) |
| R4 | 消息发送接连报错，修正参数并登录重试 | [8 个文件](recovery/message-session-retry/manifest.json) | [ZIP](recovery/message-session-retry/records.zip) |
| R5 | 刹车踩到一半仍无法启动，踩到底后重试成功 | [8 个文件](recovery/brake-pressure-retry/manifest.json) | [ZIP](recovery/brake-pressure-retry/records.zip) |

从仓库根目录运行 `python3 scripts/case-library.py --check`，核对所有文件、ZIP 成员和网页引用。需要重新打包时运行 `python3 scripts/case-library.py --package`；脚本不会改写原始记录。
