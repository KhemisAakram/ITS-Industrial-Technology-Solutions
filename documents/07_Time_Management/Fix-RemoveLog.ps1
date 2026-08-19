$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    $changed = $false

    # Remove "## Log\n\n- Blocker / one line: ..." section
    $content = $content -replace "(?s)## Log\r?\n\r?\n- Blocker / one line:.*?\r?\n", ""
    $content = $content -replace "(?s)## Log\n\n- Blocker / one line:.*?\n", ""

    # Also remove any empty "## Log\n\n## Notes" -> just "## Notes"
    $content = $content -replace "(?s)## Log\r?\n\r?\n## Notes", "## Notes"
    $content = $content -replace "(?s)## Log\n\n## Notes", "## Notes"

    Set-Content $f.FullName -Value $content -NoNewline
    $count++
}
Write-Host "Updated $count files"
