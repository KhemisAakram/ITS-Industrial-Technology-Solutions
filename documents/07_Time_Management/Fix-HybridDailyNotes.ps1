$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw

    # Extract frontmatter
    if ($content -match '(?s)(---.*?---)') {
        $frontmatter = $Matches[1]
    } else { continue }

    # Extract title
    $titleMatch = [regex]::Match($content, '(?m)^(#\s+.+)$')
    $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { "" }

    # Extract focus line
    $focusMatch = [regex]::Match($content, '(?m)^>\s*Focus:\s*(.+)$')
    $focus = if ($focusMatch.Success) { $focusMatch.Groups[1].Value.Trim() } else { "" }

    $focusLine = if ($focus) { "`n> Focus: $focus" } else { "`n> Focus:" }

    # Build hybrid body
    $newBody = @"
> [[02_Task_Bank|Tasks]] · [[03_Scripted_Actions|Scripts]] · [[01_Milestones|Milestones]]

## Energy check
- Energy: fresh / medium / tired

## Today's 3 tasks (estimate hours)

| # | Task | Project | Est | Actual | Done |
|---|------|---------|-----|--------|------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## Previous evening (fill the day before)
- [ ] Tomorrow's 3 tasks planned
- [ ] Tomorrow's courses picked -> [[11_Course_Queue]]

## Early morning (deep work)
- [ ] Urgent client check (5 min max)
- [ ] Wake-up script Q1-Q4 -> energy + blockers
- [ ] **PCB course FIRST** -> [[11_Course_Queue|next PCB class]]

## Before noon
- [ ] VFD course 45 min -> [[10_Courses]] (if working on VFD)

## Evening (admin + close)
- [ ] Service or client work today? -> create + send the invoice -> [[ITS_Business]]
- [ ] Log hours + revenue + yield (target >= 1,000 DA/hr)
- [ ] Move unfinished tasks -> tomorrow or [[ITS_Kanban|Kanban]]

## Reminders - ITS assistant (requested list)
- [ ] Your requested reminders:

## Notes
"@

    $newContent = "$frontmatter`n`n$title`n$focusLine`n$newBody"
    Set-Content $f.FullName -Value $newContent -NoNewline
    $count++
}
Write-Host "Updated $count files to hybrid format"
