$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw

    # Fix the merged status line
    $content = $content -replace 'expense_overhead: 0 (.+)', "expense_overhead: 0`nstatus: `$1"

    Set-Content $f.FullName -Value $content -NoNewline
    $count++
}
Write-Host "Fixed $count files"
