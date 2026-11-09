# claude-code-config

Claude Code のカスタム設定スクリプト集。

## statusline

Claude Code のステータスライン（画面下部のバー）に **モデル名**・**effort**・**コンテキスト使用率**・**5時間枠 / 週次(7日)枠の使用率とリセットまでの残り時間** を表示するスクリプト。

```
Opus 4.6 high   ctx 42%   5h 24% (resets in 2h10m)   7d 41% (resets in 3d4h)
```

### セットアップ

`~/.claude/settings.json` に以下を追加:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/path/to/claude-code-config/statusline/statusline.py --threshold 70",
    "refreshInterval": 5
  }
}
```

スクリプトに実行権限を付与:

```bash
chmod +x statusline/statusline.py
```

### オプション

| オプション | デフォルト | 説明 |
|---|---|---|
| `--threshold <N>` | `70` | コンテキスト使用率が N% 以上になると `!` を表示 |
| `--limit-threshold <N>` | `80` | 5時間/週次の使用率が N% 以上になると `!` を表示 |

しきい値を変更する場合は `command` にオプションを追加:

```json
"command": "/path/to/statusline.py --threshold 80"
```

### 表示フォーマット

```
<model> <effort>   ctx <context%>[!]   5h <used%>[!] (resets in <残り>)   7d <used%>[!] (resets in <残り>)
```

| フィールド | 例 | 備考 |
|---|---|---|
| model | `Opus 4.6` | モデルの表示名 |
| effort | `high` | 未設定時は省略 |
| ctx | `ctx 42%` | コンテキストウィンドウ使用率。`--threshold`（デフォルト70%）以上で `!` 付与 |
| 5h | `5h 24% (resets in 2h10m)` | 5時間枠の使用率とリセットまでの残り時間。`--limit-threshold`（デフォルト80%）以上で `!` 付与 |
| 7d | `7d 41% (resets in 3d4h)` | 週次(7日)枠の使用率とリセットまでの残り時間。同上 |

### 色

項目の区切りは記号ではなく空白（3つ）と色で表す。`NO_COLOR` 環境変数を設定すると無着色になる。

| 項目 | 通常 | しきい値以上 |
|---|---|---|
| model / effort | シアン | - |
| ctx | 緑 | 赤 + `!` |
| 5h / 7d | 黄 | 赤 + `!` |

### rate_limits の表示条件

`5h` / `7d` は Claude Code が渡す `rate_limits` から取得する。次の場合は該当部分を表示しない（エラーにはならない）。

- claude.ai の Pro / Max / Ultra 契約ではない（API キー利用など）
- セッション内で最初の API 応答が返る前
- リセット時刻を過ぎた窓（使用率のみ残り時間なしで表示、Claude Code 側が窓を落とした場合は非表示）

Sonnet / Fable などモデル別の週次上限は statusLine の JSON に含まれないため、表示できない。
