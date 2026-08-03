# skills

個人化 Claude Code skills。安裝方式：symlink 到 `~/.claude/skills/`。

```sh
ln -s "$(pwd)/<skill-name>" ~/.claude/skills/<skill-name>
```

| Skill | 用途 |
|---|---|
| [operationalize](operationalize/SKILL.md) | 把文件的抽象形容詞改寫成可觀察、可執行的行為規格；保留背景與 Why |
| [trace-dataflow](trace-dataflow/SKILL.md) | 以問答引導使用者追蹤前端資料流 |
