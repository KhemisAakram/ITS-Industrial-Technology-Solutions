# Daily-Workflow.ps1
# One-click: sync Obsidian data + open tracker + open dashboard
# Usage: Right-click -> Run with PowerShell, or from terminal:
#   powershell -ExecutionPolicy Bypass -File "C:\khemis akram\OpenCode\ITS Profile\documents\07_Time_Management\Daily-Workflow.ps1"

$base = "C:\khemis akram\OpenCode\ITS Profile"
$script = Join-Path $base "documents\07_Time_Management\Export-ObsidianData.ps1"
$tracker = Join-Path $base "documents\07_Time_Management\ITS_Daily_Tracker.html"
$dashboard = Join-Path $base "documents\07_Time_Management\Workshop_Dashboard.html"

Write-Host "ITS Daily Workflow" -ForegroundColor Yellow
Write-Host "==================" -ForegroundColor Yellow

# Step 1: Export Obsidian data
Write-Host ""
Write-Host "[1/3] Syncing Obsidian daily notes..." -ForegroundColor Cyan
& $script

# Step 2: Open tracker
Write-Host ""
Write-Host "[2/3] Opening Daily Tracker..." -ForegroundColor Cyan
Start-Process $tracker

# Step 3: Open dashboard
Write-Host ""
Write-Host "[3/3] Opening Workshop Dashboard..." -ForegroundColor Cyan
Start-Process $dashboard

Write-Host ""
Write-Host "Done! Both files opened in your browser." -ForegroundColor Green
Write-Host "Today's date: $((Get-Date).ToString('yyyy-MM-dd'))" -ForegroundColor Gray
