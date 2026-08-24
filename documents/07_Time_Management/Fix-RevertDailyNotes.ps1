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

    # Extract links line
    $linksMatch = [regex]::Match($content, '(?m)^>\s*\[\[.+\]\].*$')
    $links = if ($linksMatch.Success) { $linksMatch.Groups[0].Value } else { "> [[02_Task_Bank|Task Bank]] - [[03_Scripted_Actions|Scripts]] - [[01_Milestones|Milestones]]" }

    # Build old format body
    $focusLine = if ($focus) { "`n> Focus: $focus" } else { "" }

    $oldBody = @"
$links

## Previous evening (fill the day before)
- [ ] Tomorrow's 3 slots planned (Block 1+2 early / Block 3 before noon / Block 4 evening)
- [ ] Tomorrow's courses picked -> [[11_Course_Queue]]

## Early morning (deep work)
- [ ] Urgent client check (5 min max)
- [ ] Wake-up script Q1-Q4 -> energy + blockers
- [ ] **PCB course FIRST** -> [[11_Course_Queue|next PCB class]]
- [ ] **Block 1 [HIGH]:**
- [ ] **Block 2 [HIGH]:**
- [ ] SOMIK course 45 min -> [[10_Courses]]

## Before noon (steady work)
- [ ] **Block 3 [MEDIUM]:**
- [ ] VFD course 45 min -> [[10_Courses]]

## Evening (admin + close)
- [ ] **Block 4 [LOW] - optional:**
- [ ] Service or client work today? -> create + send the invoice -> [[ITS_Business]]
- [ ] Tick off what you finished today -> [[ITS_Kanban|Kanban]] - [[10_Courses|Courses]]
- [ ] Log hours + revenue + yield (target >= 1,000 DA/hr)
- [ ] Fill tomorrow's slots (previous-evening prep)

## Reminders - ITS assistant (requested list)
- [ ] Your requested reminders:


## Notes
"@

    $newContent = "$frontmatter`n`n$title`n$focusLine`n$oldBody"
    Set-Content $f.FullName -Value $newContent -NoNewline
    $count++
}
Write-Host "Reverted $count files"
