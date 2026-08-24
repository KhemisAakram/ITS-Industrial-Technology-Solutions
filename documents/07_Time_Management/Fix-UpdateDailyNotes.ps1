$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw

    # Extract focus line from old body (between > Focus: and next line)
    $focusMatch = [regex]::Match($content, '(?m)^>\s*Focus:\s*(.+)$')
    $focus = if ($focusMatch.Success) { $focusMatch.Groups[1].Value.Trim() } else { "" }

    # Build new body
    $newBody = @"

## Energy check
- Energy: fresh / medium / tired

## Today's 3 tasks (estimate hours)

| # | Task | Project | Est | Actual | Done |
|---|------|---------|-----|--------|------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## End of day
- [ ] Log hours + revenue (target >= 1,000 DA/hr)
- [ ] Move unfinished tasks -> tomorrow or [[ITS_Kanban|Kanban]]

## Notes
"@

    # Keep frontmatter as-is
    if ($content -match '(?s)(---.*?---)') {
        $frontmatter = $Matches[1]
        # Rebuild: frontmatter + title (from existing) + new body
        # Extract title line (# Day...)
        $titleMatch = [regex]::Match($content, '(?m)^(#\s+.+)$')
        $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { "" }

        # Extract the > line (links line)
        $linksMatch = [regex]::Match($content, '(?m)^>\s*\[\[.+\]\].*$')
        $links = if ($linksMatch.Success) { $linksMatch.Groups[0].Value } else { "> [[02_Task_Bank|Tasks]] * [[03_Scripted_Actions|Scripts]] * [[01_Milestones|Milestones]]" }

        if ($focus) {
            $focusLine = "> Focus: $focus"
        } else {
            $focusLine = ""
        }

        $newContent = "$frontmatter`n`n$title`n"
        if ($focusLine) {
            $newContent += "`n$focusLine`n"
        }
        $newContent += "$links`n$newBody`n"

        Set-Content $f.FullName -Value $newContent -NoNewline
        $count++
    }
}
Write-Host "Updated $count files"
