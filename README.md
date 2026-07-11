# claude-code-config

Claude Code のカスタム設定スクリプト集。

## statusline

Claude Code のステータスライン（画面下部のバー）に **モデル名**・**effort**・**コンテキスト使用率** を表示するスクリプト。

```
Opus 4.6 | high | 42%
```

### セットアップ

`~/.claude/settings.json` に以下を追加:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/path/to/claude-code-config/statusline/statusline.py",
    "refreshInterval": 5
  }
}
```

スクリプトに実行権限を付与:

```bash
chmod +x statusline/statusline.py
```

### 表示フォーマット

```
<model> | <effort> | <context%>[!]
```

| フィールド | 例 | 備考 |
|---|---|---|
| model | `Opus 4.6` | モデルの表示名 |
| effort | `high` | 未設定時は省略 |
| context% | `42%` | コンテキストウィンドウ使用率。200kトークン超で `!` 付与 |
