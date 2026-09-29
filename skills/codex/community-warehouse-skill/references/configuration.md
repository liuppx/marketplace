# 配置约定

Warehouse skill 客户端统一支持环境变量和 TOML 配置文件：

```text
命令行 --config > YEYING_WAREHOUSE_CONFIG > ~/.yeying/skills/warehouse/config.toml
```

配置文件示例：

```toml
[warehouse]
url = "http://localhost:6065"
tool_token = ""
```

字段覆盖关系：

| 配置文件 | 环境变量 | 用途 |
| --- | --- | --- |
| `warehouse.url` | `YEYING_WAREHOUSE_URL` | Warehouse 服务根地址 |
| `warehouse.tool_token` | `YEYING_WAREHOUSE_TOOL_TOKEN` | 短期 scoped Tool credential |
| `warehouse.tool_token` | `YEYING_WAREHOUSE_TOKEN` | 交互式兼容凭证 |

`YEYING_WAREHOUSE_CONFIG` 可以指定其他 TOML 路径；命令行 `--config` 优先级最高。环境变量覆盖配置文件同名字段。配置文件可以只保存服务地址，把 token 通过环境变量或 Secret Manager 注入。

包含 `tool_token` 的配置文件必须是当前用户可读写，权限不应超过 `0600`。客户端不会打印 token，也不会把配置来源以外的敏感值写入日志。

其他 skill 应复用相同目录约定：

```text
$HOME/.yeying/skills/<skill-name>/config.toml
```
