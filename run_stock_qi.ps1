# 每日三支股票推荐 — 自动执行脚本
$projectDir = "C:\Users\robin\OneDrive\Desktop\George Learning AI\Cursor Claude"
Set-Location $projectDir

# 运行 Claude Code 执行 stock-qi skill
# --print: 非交互模式，执行完退出
# --permission-mode bypassPermissions: 跳过权限确认
# --no-session-persistence: 不保存会话
claude --print --permission-mode bypassPermissions --no-session-persistence "/stock-qi"
