#!/usr/bin/env python3
# PreToolUse(Bash)：指令以 grep 當命令執行時拒絕，要求改用 rg
# 只比對命令位置的 grep（行首、管線、&&、;、子 shell、xargs 之後），`git grep` 不受影響
import json
import re
import sys

GREP_AS_COMMAND = re.compile(r"(?:^|[|;&(`]|\bxargs)\s*[ef]?grep\b", re.MULTILINE)

MESSAGE = (
    "此環境以 rg 取代 grep，請改用 rg 重新執行。"
    "注意參數差異：rg 預設遞迴且遵守 .gitignore（需要時加 -uu），"
    "rg -r 代表 replace 不是遞迴，grep -E 的 regex 直接寫即可。"
)


def main():
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    if not GREP_AS_COMMAND.search(command):
        return
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": MESSAGE,
            }
        },
        sys.stdout,
        ensure_ascii=False,
    )


if __name__ == "__main__":
    main()
