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

[`CLAUDE.global.md`](CLAUDE.global.md) 也放在這個 repo，透過 symlink 讓每台裝置共用。

`~/.claude/CLAUDE.md` 已經有內容時 `ln -s` 會失敗（`File exists`），不會蓋掉，先比對再決定怎麼併：

```sh
diff ~/.claude/CLAUDE.md CLAUDE.global.md
```

- 沒差異 → 刪掉本機那份，建 symlink。
- 差異每台都適用 → 先併進 `CLAUDE.global.md` 並 push，再刪本機那份、建 symlink。
- 差異只有這台適用（本機路徑、某個專案的規則）→ 不要進這個 repo，移到該專案的 `CLAUDE.md`。全域檔只放跨裝置都成立的規則。

```sh
rm ~/.claude/CLAUDE.md && ln -s "$(pwd)/CLAUDE.global.md" ~/.claude/CLAUDE.md
```

## 換裝置

```sh
git clone git@github.com:wk00100/skills.git ~/Github/skills && cd ~/Github/skills
ln -s "$(pwd)/operationalize" ~/.claude/skills/operationalize
ln -s "$(pwd)/trace-dataflow" ~/.claude/skills/trace-dataflow
```

全域指令照上一節處理。已經有 `contextualize` 的舊裝置要 `rm ~/.claude/skills/contextualize`（已併進 operationalize）。
