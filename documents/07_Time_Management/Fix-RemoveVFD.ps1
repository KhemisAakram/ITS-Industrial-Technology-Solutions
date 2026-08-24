$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw

    # Replace VFD-only line with combined SOMIK/VFD line
    $content = $content -replace '(?m)^- \[ \] VFD course 45 min -> \[\[10_Courses\]\].*$', '- [ ] SOMIK/VFD course 45 min -> [[10_Courses]] (only if working on those projects today)'

    Set-Content $f.FullName -Value $content -NoNewline
    $count++
}
Write-Host "Updated $count files"
