$dir = "C:\khemis akram\OpenCode\ITS Profile\Planning\05_Daily_Notes"
$files = Get-ChildItem -Path $dir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }
$count = 0
foreach ($f in $files) {
    $content = Get-Content $f.FullName -Raw
    $changed = $false

    # Remove the Rule comment
    if ($content.Contains("> Rule: fill the Log ONLY - it is the source of truth. Leave the frontmatter numbers (energy/hours/revenue/yield) alone.")) {
        $content = $content.Replace("> Rule: fill the Log ONLY - it is the source of truth. Leave the frontmatter numbers (energy/hours/revenue/yield) alone.`r`n`r`n", "")
        $content = $content.Replace("> Rule: fill the Log ONLY - it is the source of truth. Leave the frontmatter numbers (energy/hours/revenue/yield) alone.`n`n", "")
        $changed = $true
    }

    # Remove Hours worked line (with or without value)
    $content = $content -replace "(?m)^- Hours worked:.*\r?\n", ""
    $content = $content -replace "(?m)^- Hours worked:.*\n", ""

    # Remove Billable hours line
    $content = $content -replace "(?m)^- Billable hours:.*\r?\n", ""
    $content = $content -replace "(?m)^- Billable hours:.*\n", ""

    # Remove Revenue line
    $content = $content -replace "(?m)^- Revenue \(DA\):.*\r?\n", ""
    $content = $content -replace "(?m)^- Revenue \(DA\):.*\n", ""

    # Remove Yield line
    $content = $content -replace "(?m)^- Yield \(DA/hr\).*\r?\n", ""
    $content = $content -replace "(?m)^- Yield \(DA/hr\).*\n", ""

    if ($changed -or $true) {
        Set-Content $f.FullName -Value $content -NoNewline
        $count++
    }
}
Write-Host "Updated $count files"
