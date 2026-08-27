# skills

個人化 Claude Code skills。安裝方式：symlink 到 `~/.claude/skills/`。

```sh
ln -s "$(pwd)/<skill-name>" ~/.claude/skills/<skill-name>
```

| Skill | 用途 |
|---|---|
| [operationalize](operationalize/SKILL.md) | 形容詞改寫成可觀察的行為規格＋用字依語境重選；保留背景與 Why |
| [trace-dataflow](trace-dataflow/SKILL.md) | 以問答引導使用者追蹤前端資料流 |

## 全域指令

[`CLAUDE.global.md`](CLAUDE.global.md) 放在這個 repo，是跨裝置共用的基線規則。

`~/.claude/CLAUDE.md` 維持實體檔，不建 symlink：同一台裝置常需要疊加只在這台適用的規則（某個工具的用字細節、本機路徑），symlink 會沒有空間放這些客製。

```sh
diff ~/.claude/CLAUDE.md CLAUDE.global.md
```

- repo 有、本機沒有的規則 → 併入本機 `CLAUDE.md`。
- 本機有、repo 沒有的規則 → 只有這台適用就留在本機，不動 repo；所有裝置都該套用才併進 `CLAUDE.global.md` 並 push。

## 換裝置

```sh
git clone git@github.com:wk00100/skills.git ~/Github/skills && cd ~/Github/skills
ln -s "$(pwd)/operationalize" ~/.claude/skills/operationalize
ln -s "$(pwd)/trace-dataflow" ~/.claude/skills/trace-dataflow
```

全域指令照上一節處理。已經有 `contextualize` 的舊裝置要 `rm ~/.claude/skills/contextualize`（已併進 operationalize）。
