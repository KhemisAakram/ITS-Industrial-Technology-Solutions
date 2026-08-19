$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    $old = "- [ ] **PCB course FIRST** -> [[11_Course_Queue|next PCB class]]`r`n- [ ] Wake-up script Q1-Q4 -> energy + blockers`r`n- [ ] Urgent client check (5 min max)"
    $new = "- [ ] Urgent client check (5 min max)`r`n- [ ] Wake-up script Q1-Q4 -> energy + blockers`r`n- [ ] **PCB course FIRST** -> [[11_Course_Queue|next PCB class]]"
    if ($content.Contains($old)) {
        $content = $content.Replace($old, $new)
        Set-Content $f.FullName -Value $content -NoNewline
        $count++
    } else {
        $old2 = "- [ ] **PCB course FIRST** -> [[11_Course_Queue|next PCB class]]`n- [ ] Wake-up script Q1-Q4 -> energy + blockers`n- [ ] Urgent client check (5 min max)"
        if ($content.Contains($old2)) {
            $new2 = "- [ ] Urgent client check (5 min max)`n- [ ] Wake-up script Q1-Q4 -> energy + blockers`n- [ ] **PCB course FIRST** -> [[11_Course_Queue|next PCB class]]"
            $content = $content.Replace($old2, $new2)
            Set-Content $f.FullName -Value $content -NoNewline
            $count++
        }
    }
}
Write-Host "Updated $count files"
