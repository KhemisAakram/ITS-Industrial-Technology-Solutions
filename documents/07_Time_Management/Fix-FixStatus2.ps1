$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw

    # Remove empty status line if there's a second status with value
    if ($content -match 'status:\s*\nstatus: (\S+)') {
        $content = $content -replace 'status:\s*\nstatus: (\S+)', 'status: $1'
    }

    Set-Content $f.FullName -Value $content -NoNewline
    $count++
}
Write-Host "Fixed $count files"
