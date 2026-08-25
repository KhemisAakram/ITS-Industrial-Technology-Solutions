$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw

    # Add expense fields to frontmatter if not present
    if ($content -notmatch 'income_da:') {
        $content = $content -replace '(status:)', "`$1`nincome_da: 0`nexpense_parts: 0`nexpense_tools: 0`nexpense_transport: 0`nexpense_overhead: 0"
    }

    # Add Money section before Notes if not present
    if ($content -notmatch '## Money today') {
        $content = $content -replace '(## Notes)', "## Money today`n- Income: ___ DA -- from:`n- Parts: ___ DA -- what:`n- Tools: ___ DA -- what:`n- Transport: ___ DA -- what:`n- Overhead: ___ DA -- what:`n`n`$1"
    }

    Set-Content $f.FullName -Value $content -NoNewline
    $count++
}
Write-Host "Updated $count files"
