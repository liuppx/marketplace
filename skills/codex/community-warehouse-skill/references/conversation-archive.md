# 对话审查归档

当用户要求把 Codex、Claude 或其他模型工具的工作过程保存到 Warehouse 供事后审查时，生成同一归档目录下的三个对象：

```text
/personal/reviews/conversations/<conversationId>/transcript.md
/personal/reviews/conversations/<conversationId>/transcript.json
/personal/reviews/conversations/<conversationId>/manifest.json
```

- `transcript.md`：供人工阅读，包含请求、回复、工具调用摘要、结果、未完成项和导出范围说明。
- `transcript.json`：保留可获得的结构化消息、工具调用、工具结果和附件引用。
- `manifest.json`：记录 schema 版本、conversationId、来源工具、模型、起止时间、导出时间、是否完整、脱敏状态，以及前两个文件的 SHA-256。

使用 `warehouse.object.put` 逐个写入，默认 `overwrite=false`。路径应包含稳定的 conversationId；若用户明确要求修订已归档内容，先读取当前 ETag，再以 `overwrite=true` 和 `ifMatch=<etag>` 条件覆盖。每个调用传同一 `traceId`，便于关联三次写入。

Markdown 只是审查视图，不能单独宣称为完整或不可篡改的审计证据。来源工具不能导出隐藏上下文、完整工具输出或附件时，在 manifest 中明确标记 `complete=false` 和缺失项。

写入前移除访问令牌、密码、私钥、密钥文件正文和其他不应持久化的秘密。对普通隐私数据是否脱敏遵循用户要求；不得为了归档扩大当前授权范围，也不得把 Warehouse 凭证写入归档正文。
