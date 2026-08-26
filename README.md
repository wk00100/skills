# skills

個人化 Claude Code skills。安裝方式：symlink 到 `~/.claude/skills/`。

```sh
ln -s "$(pwd)/<skill-name>" ~/.claude/skills/<skill-name>
```

| Skill | 用途 |
|---|---|
| [operationalize](operationalize/SKILL.md) | 形容詞改寫成可觀察的行為規格＋用字依語境重選；保留背景與 Why |
| [trace-dataflow](trace-dataflow/SKILL.md) | 以問答引導使用者追蹤前端資料流 |

全域指令 [`CLAUDE.global.md`](CLAUDE.global.md) 也放在這個 repo，換裝置時 symlink 過去：

```sh
ln -s "$(pwd)/CLAUDE.global.md" ~/.claude/CLAUDE.md
```
