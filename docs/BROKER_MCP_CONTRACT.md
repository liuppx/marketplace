# Broker MCP 契约

本文定义策略交易 skill 需要的 broker connector 最小能力。真实券商和模拟券商都应该尽量对齐这个工具面。

## 工具列表

### `dry_run_order`

校验订单但不提交。

输入：

- `symbol`：标的代码
- `side`：`buy` 或 `sell`
- `quantity`：数量
- `orderType`：`market` 或 `limit`
- `limitPrice`：限价单价格，可选

输出：

- `accepted`：是否通过校验
- `reason`：拒绝原因，可选
- `estimatedCashImpact`：预计资金影响
- `estimatedPositionImpact`：预计持仓影响

### `place_order`

提交订单。实盘 connector 必须要求上游显式确认后才允许执行。

输入：

- `symbol`
- `side`
- `quantity`
- `orderType`
- `limitPrice`
- `clientOrderId`

输出：

- `orderId`
- `status`
- `submittedAt`

### `cancel_order`

撤销未完成订单。

输入：

- `orderId`

输出：

- `orderId`
- `status`

### `query_orders`

查询订单。

输入：

- `status`：可选
- `symbol`：可选

输出：

- `orders`

### `query_positions`

查询持仓。

输入：

- `symbol`：可选

输出：

- `positions`

### `query_cash`

查询资金。

输出：

- `cash`
- `currency`
- `available`

## 安全规则

- 默认只允许 `dry_run_order`。
- 实盘 `place_order` 必须依赖用户显式确认。
- connector 必须返回订单 ID 和状态，不能只返回成功文本。
- connector 必须暴露资金、持仓和订单查询能力，便于 skill 做执行前后校验。
- connector 不应把密钥写进 marketplace 包；密钥只能由用户运行时配置。
