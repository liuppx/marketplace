# 策略交易 Skill 方案

## 目标

把交易想法沉淀成一个可安装、可配置、可持续迭代的 skill。第一阶段先解决策略定制、风险约束、下单计划和模拟执行；第二阶段再接 broker 连接器；第三阶段才做自动下单闭环。

## 角色分工

- `skill`：负责把用户输入变成策略定义、风控参数、执行计划和结果汇总。
- `marketplace`：负责发布 skill 包、未来的 broker MCP 包和数据源包。
- `Chat`：负责安装、启用、配置、状态展示和会话入口。

## 第一版范围

- 支持策略描述、仓位约束、止损止盈、频率、标的范围、执行模式。
- 默认输出 dry-run 订单票据。
- 不伪造实盘结果。
- 没有 broker connector 时，只给出待执行计划和缺失项。
- `paper-broker` 是可选 MCP；缺失时不阻塞技能启动，配置后可进入模拟执行。

## 后续扩展

### 1. Broker MCP

后续在 `mcp/servers/` 中增加真实 broker connector，至少要支持：

- `place_order`
- `cancel_order`
- `query_orders`
- `query_positions`
- `query_cash`
- `dry_run_order`

最小工具契约见：`docs/BROKER_MCP_CONTRACT.md`。

### 2. 策略模板

把常用策略沉淀成 starter：

- 趋势跟随
- 均值回归
- 网格 / 分批
- 事件驱动
- 风控止损

### 3. 安全约束

实盘必须显式确认，并满足：

- 最大仓位
- 单笔上限
- 日亏损上限
- 频率限制
- kill switch

## Chat 侧建议

- 技能页突出 `策略交易`，避免和普通聊天混淆。
- 进入技能后默认展示策略配置和风险约束，而不是让用户先猜应该怎么说。
- broker connector 未配置时，界面必须显示“仅可生成计划，不能实盘执行”。
