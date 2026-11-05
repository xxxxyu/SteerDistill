# 后备消融案例：指导与执行对应关系复核 · 2026-11-05

本轮只审查，不修改展示页，也不重跑模型。标准为：Ours 的指导及结果正确；对照指导中的具体错误或遗漏能对应后续动作和结果，而不是从正确指导下挑一个执行失败的随机样本。

## 结论

**现有后备包中，没有可以无条件直接加入的干净替代案例。** 最接近的是更新后的 03（`booking_and_scheduling_11_4`），它有明确的“指导要求字段 → 实际调用字段 → 数据库字段”对应，远强于语义相同指导下的成败差异。但进一步查看原始返回发现，预约日期与真实写入的 `booked_at` 不一致，和字段定义的同日语义冲突。因此只能作为待厘清环境时间语义的窄范围候选，不能仅因 verifier 通过就认定 Ours 的同日预约语义完全正确。

## 03：同日预约标志，局部对应明确，但时间语义待解决

来源是 nx 发布树 `data/cases/ablation_case/verified_20261104/booking_and_scheduling_11_4/`。核查本地只读副本；Teacher/Student/freeform 三份指导 SHA-256 与当前 nx 文件一致。下列路径相对此任务目录。

### 任务与字段含义

- `context.json[1].content` 的原始要求包含：`between 08:00 and 09:00 on 2026-02-03 ... then add a same-day sick visit booking ... with status 'scheduled'`。
- `openapi.json` 的 `components.schemas.BookingCreateRequest.properties.is_same_day_booking`：说明为 **`1 if booked on same day as appointment date`**，默认值 **0**。它是独立于 `visit_type_id=4`（Same-day Sick Visit）的字段。
- 任务确有 `same-day`，因此字段不是完全凭 verifier 凭空添加；但该字段描述的是预约创建日期与就诊日期是否相同，不能直接等同于就诊类型名称。

### 指导、调用和状态逐项对应

| 分支 | 实际指导 | 实际执行 | 实际数据库 |
| --- | --- | --- | --- |
| Teacher 结构化 | `teacher_structured/guidance.json` 的 decision_rule：`call 'mcp_server_create_booking' using the last available slot (SL-3004) ... with 'is_same_day_booking' set to 1` | `teacher_structured/student/trajectory.json` 消息16创建预约，显式 `is_same_day_booking:1`；消息17返回1 | `teacher_structured/student/final.db`，bookings.id=`BK-20`，该字段为1 |
| Student 结构化 | `student_structured/guidance.json` 错称 BK-20 已创建；没有要求设置同日标志，核验也只检查 scheduled 和时段容量 | 对应轨迹消息16仍创建预约，但省略该参数；消息17返回默认0 | 同一 BK-20 的该字段为0 |
| Teacher 自由文本 | `teacher_freeform/guidance.json` 错称任务已完成，列出预约类型和 scheduled 状态，但没有同日标志 | 对应轨迹消息16创建预约，省略参数；消息17返回默认0 | 同一 BK-20 的该字段为0 |

三者均针对患者2、时段 SL-3004、visit_type_id 4，其他核心预约属性相同。所有记录的执行请求都使用 seed 42、temperature 0；共享同一保存前缀。指导持续出现在各轮 system 消息的 `Procedural guidance` 段落中，不是训练方法的一次局部指导后移除。原始 actor response 的 reasoning 为 null，不可补写 agent 内心因果；但缺少推理并不会消除上述可见参数链。

### 新发现：实际时间戳与字段语义冲突

Teacher 创建返回（`student/trajectory.json` 消息17）写入：

- `appointment_slot_id: SL-3004`，该时段实际日期为 **2026-02-03**；
- `booked_at: 2026-11-03T12:31:08.850122`；
- `is_same_day_booking: 1`。

Student 和 freeform 的 booked_at 也为 2026-11-03。系统消息没有声明将环境时钟冻结到 2026-02-03。因此不能声称 Teacher 实现了字面意义上的“当天创建当天预约”；它只是遵照指导将标志写为1，而 verifier 检查该标志、不检查它与 booked_at/时段日期是否一致。

若将来证明这是基准的逻辑日期约定或修复环境时钟，可把展示压缩为“预约类型正确，还需写入同日标志”，默认 Teacher vs Student，自由文本/无指导作为补充。当前不能靠删去时间戳或改写任务来包装成无歧义优势。

### 其他需要避免的叙事

- `pre_state.db` 中 SL-3001–SL-3004 容量本来已经是3、base_capacity为2、is_overbook_capable为1。Teacher 再次更新三个返回时段是冗余操作，不能写成成功扩容的主要贡献。
- GPT 指导将查询列表没返回的08:00时段认作不存在，创建重复时段 SLOT-25，导致目标窗口由4变5；但原始库确实已有 SL-3001，查询的字符串日期过滤问题参与其中。它不是同日标志的失败分支（GPT也显式写1），不宜硬塞到同一简单对照里。
- `task_verifier.py` 的同日判断是 `is_same_day != 1`，没有核对真实创建日期；完整任务成功标签不足以解决上述语义问题。

## 其他候选

| 候选 | 核查后的排除理由 |
| --- | --- |
| 更新后 01：`verified_20261103/b2b_commerce_1_1` | Teacher、Student、freeform、GPT **都调用了定价工具**，其实际折扣差别来自 order_date：Teacher选2026-01-05，其他选2025-05-22。用户只指定 requested_ship_date，没有给定 order_date。不能再用旧案例“漏掉定价”叙事，也不能把未指定日期导致的折扣差异解释成明确指导质量优势。Teacher新版指导本身没有指定一个足以解释该日期差异的明确规则。 |
| 02：`verified_20261103/booking_and_reservations_5_0` | Ours 指导根据资料 updated_at 推测当前日期，并建议搜索整个2026年9月；用户要求 next 7 days。Ours 自身放宽时间约束，先不过正确性门槛。 |
| `reviewed-20261105/main/multi_turn_base_61` | Teacher/Student均给出42→49、补7的目标，自由文本也直接给7的调用；失败仍主要是没有执行正确指导。唯一成功Ours推理反复声称数据不足，最后才发出正确调用，不能补成清楚的指导差异因果例子。 |
| `reviewed-20261105/local-only/R02A` | 三种指导都要求先进入archive再重命名，主要差别为冗余复制/核验。其他分支后来也成功；Ours指导生成分析又把source查找失败误归因为destination位置。既缺少清楚的内容差异归因，也不满足干净Ours要求。 |

01/02 两份 Teacher 指导与当前 nx 发布文件 SHA-256 对照一致。R02A 复核了三份完整指导、Ours完整生成分析及真实后续调用；61 复核了选中指导和成功Ours的完整首轮推理。重命名27已由用户明确移除，本轮不尝试用相似目录主题重新加入。

## 建议

将03列为**唯一值得进一步厘清的窄范围后备**，不要立即制作新页面。先确认模拟环境的日期语义，才能判断其Ours字段值是任务正确性还是只匹配验收器。其余现有候选不因数量需求而补入。后续采集应优先寻找指导明确漏掉前置条件/工具参数、错误指导被实际执行，而正确指导补上该信息的对照，并保留受控运行与完整原始证据。
