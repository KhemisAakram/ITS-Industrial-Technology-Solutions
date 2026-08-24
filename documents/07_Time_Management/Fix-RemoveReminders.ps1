$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    $content = $content -replace "(?s)## Reminders - ITS assistant \(requested list\)\r?\n- \[ \] Your requested reminders:\r?\n\r?\n", ""
    $content = $content -replace "(?s)## Reminders - ITS assistant \(requested list\)\n- \[ \] Your requested reminders:\n\n", ""
    Set-Content $f.FullName -Value $content -NoNewline
    $count++
}
Write-Host "Removed reminders from $count files"
