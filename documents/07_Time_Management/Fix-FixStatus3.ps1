$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw

    # Remove empty status lines (status: followed by newline)
    $content = $content -replace 'status:\r?\n', ''

    Set-Content $f.FullName -Value $content -NoNewline
    $count++
}
Write-Host "Fixed $count files"
