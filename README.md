# skills

個人化 Claude Code 設定，跨裝置共用。內容分三部分：

- **Skills**：放在各自的資料夾，symlink 到 `~/.claude/skills/`
- **全域指令**：`CLAUDE.global.md`，手動併入 `~/.claude/CLAUDE.md`
- **Hooks**：`hooks/` 底下的腳本，symlink 到 `~/.claude/hooks/` 後在 `settings.json` 註冊

## Skills

| Skill | 用途 |
|---|---|
| [operationalize](operationalize/SKILL.md) | 形容詞改寫成可觀察的行為規格，用字依語境重選，保留背景與 Why |
| [trace-dataflow](trace-dataflow/SKILL.md) | 以問答引導使用者追蹤前端資料流 |

安裝：

```sh
ln -s "$(pwd)/<skill-name>" ~/.claude/skills/<skill-name>
```

## 全域指令

[`CLAUDE.global.md`](CLAUDE.global.md) 是跨裝置共用的基線規則。

`~/.claude/CLAUDE.md` 維持實體檔，不建 symlink。
同一台裝置常需要疊加只在本機適用的規則（某個工具的用字細節、本機路徑），symlink 會讓本機規則沒有地方放。

同步方式：

1. 比對兩份檔案：

   ```sh
   diff ~/.claude/CLAUDE.md CLAUDE.global.md
   ```

2. repo 有、本機沒有的規則：併入本機 `~/.claude/CLAUDE.md`。
3. 本機有、repo 沒有的規則：
   - 只有本機適用：留在本機，不動 repo
   - 所有裝置都該套用：併進 `CLAUDE.global.md` 並 push

## Hooks

`hooks/` 底下的腳本負責檢查全域指令裡的部分規則。

| 腳本 | 事件 | 用途 |
|---|---|---|
| `zh-tw-lint.py` | PostToolUse | 回報寫入檔案的內容違反用字規則的位置 |
| `prefer-rg.py` | PreToolUse | 拒絕以 grep 當命令的 Bash 指令，要求改用 rg |

安裝：

1. symlink 到 `~/.claude/hooks/`：

   ```sh
   ln -s "$(pwd)/hooks/zh-tw-lint.py" ~/.claude/hooks/zh-tw-lint.py
   ln -s "$(pwd)/hooks/prefer-rg.py" ~/.claude/hooks/prefer-rg.py
   ```

2. 在 `~/.claude/settings.json` 的 `hooks` 底下註冊：

   ```json
   {
     "PostToolUse": [
       {
         "matcher": "Write|Edit|MultiEdit",
         "hooks": [{ "type": "command", "command": "/usr/bin/python3 ~/.claude/hooks/zh-tw-lint.py", "timeout": 10 }]
       }
     ],
     "PreToolUse": [
       {
         "matcher": "Bash",
         "hooks": [{ "type": "command", "command": "/usr/bin/python3 ~/.claude/hooks/prefer-rg.py", "timeout": 10 }]
       }
     ]
   }
   ```

## 換裝置

1. clone repo：

   ```sh
   git clone git@github.com:wk00100/skills.git ~/Github/skills && cd ~/Github/skills
   ```

2. 安裝 skills：

   ```sh
   ln -s "$(pwd)/operationalize" ~/.claude/skills/operationalize
   ln -s "$(pwd)/trace-dataflow" ~/.claude/skills/trace-dataflow
   ```

3. 照「全域指令」一節同步 `~/.claude/CLAUDE.md`。
4. 照「Hooks」一節安裝並註冊 hooks。

舊裝置如果還有 `~/.claude/skills/contextualize`，要先刪除，該 skill 已經併進 operationalize：

```sh
rm ~/.claude/skills/contextualize
```
