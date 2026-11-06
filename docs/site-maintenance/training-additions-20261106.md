# T3 / T4 训练案例整合 · 2026-11-06

状态：独立作者制作、根审及本地预览检查完成，等待用户审阅；未推送或发布。

## 选择与证据

来源为 nx 的 `training-case-supervision-20261106/packages/training_steering_9_cases_20261106.zip`（11:52 更新，SHA256 `c0b7ddc716fa8e9945dca5b48b1f2dd73c56445733ec297ec0931c9ebd8ea36d`）。原始材料分别保存在 `data/cases/training_case/reviewed-20261106/` 两个目录，import manifest 记录逐文件来源及哈希。

| 编号 | 页面 | 重点 | 证据账本 |
| --- | --- | --- | --- |
| T3 | 限制银行卡国际交易，不能只填国家名单 | 国家名单不变，开关由允许全部国际交易改为执行国家限制 | [银行卡](cases/training/card-country-restriction.md) |
| T4 | 创建文件后，写入第二个匹配句 | 无指导会自行补建文件，但写入错误片段；指导后重新计数并正确写入 | [文件](cases/training/create-and-write-matching-sentence.md) |

T3：根据用户澄清，补做的比较本身不妨碍使用。根审确认 before/reference/after 前十条消息一致，各分支仅一次工具调用，local_state 紧接该调用保存，且分别与 final.db 字节一致。比较没有错轮次。数据库联合查询及完整表比较支持参考状态一致。页面写配置事实与参考对照，原始记录保留比较生成时间，不将后补比较描绘成当时控制续跑的 gate。create/update 两个接口均可建立记录，接口名差异不作为因果重点；不声称执行了真实交易测试。

T4：新 Teacher 请求不含终局失败反馈，第一次指导尝试即局部通过。touch 后的空文件与参考状态一致；后续请求撤去指导，再写入正确的第二个匹配句。页面区分这两个检查。可选推理保留误判、重新计数和明确纠正；无指导分支保留 touch 恢复动作，不误写成从未创建文件。根审删去 before 推理中跨动作拼接的恢复句，避免让不同阶段看起来连续。

## 模板与呈现

- 两例均复用 `training` 模板、EvidenceUI、共享任务折叠、目录、主题及完整记录页，无专属 CSS/renderer。
- T3/T4 短索引分别为“国家限制开关”“匹配句写入”；目录保持既有编号。
- T2 的动作表头措辞同步为“工具调用与返回”，与共享默认标题一致。
- 新增 16 处标注逐一核查其原始文本、颜色和因果用途；未使用自动高亮规则。
- 主文章与正文内嵌案例不变。后补状态比较的使用规则已写入 case author contract。

## 验收

- 19 个配置、245 个精确标注、1322 个来源 URL 校验通过。
- 现有 24 项测试通过；四个生成入口与模板一致；git whitespace 检查通过。
- 浏览器检查双栏桌面、400px 窄屏（无页面横向溢出）、原始任务/推理折叠、T3/T4 目录及完整轨迹入口。
- 检查指导表与执行结果共用行布局、短箭头、统一边缘，以及 red/blue 标注和中性返回。
- 本地入口：`design-lab/paper-cases.html?group=training&case=card-country-restriction`、`design-lab/paper-cases.html?group=training&case=create-and-write-matching-sentence`。
