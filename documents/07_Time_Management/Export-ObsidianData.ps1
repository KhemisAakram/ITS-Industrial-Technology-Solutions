# Export-ObsidianData.ps1
# Parses all daily notes in 05_Daily_Notes/ and weekly notes in 06_Weekly_Notes/
# Outputs JSON files that the HTML Workshop Dashboard can load.

param(
    [string]$VaultPath = "C:\khemis akram\OpenCode\ITS Profile"
)

$dailyDir = Join-Path $VaultPath "Planning\05_Daily_Notes"
$weeklyDir = Join-Path $VaultPath "Planning\06_Weekly_Notes"
$outputDir = Join-Path $VaultPath "documents\07_Time_Management"

# --- Parse daily notes ---
$dailyEntries = @()
$dailyFiles = Get-ChildItem -Path $dailyDir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }

foreach ($file in $dailyFiles) {
    $content = Get-Content $file.FullName -Raw
    $entry = @{ date = $file.BaseName }

    # Extract YAML frontmatter between --- markers
    if ($content -match '(?s)^---\s*\r?\n(.*?)\r?\n---') {
        $yaml = $Matches[1]

        # Parse each YAML line
        foreach ($line in ($yaml -split '\r?\n')) {
            $line = $line.Trim()
            if ($line -match '^(\w+):\s*(.*)$') {
                $key = $Matches[1]
                $val = $Matches[2].Trim('"').Trim("'").Trim()

                switch ($key) {
                    'date'          { $entry.date = $val }
                    'week'          { $entry.weekNum = $val }
                    'day'           { $entry.dayNum = $val }
                    'energy'        { $entry.energy = $val }
                    'hours_worked'  { $entry.hoursWorked = $val }
                    'hours_billable'{ $entry.hoursBillable = $val }
                    'revenue_da'    { $entry.revenueDA = $val }
                    'yield_da_hr'   { $entry.yieldDAHR = $val }
                    'status'        { $entry.status = $val }
                }
            }
        }
    }

    # Extract body: look for task blocks, blocker, notes
    $body = if ($content -match '(?s)^---\s*\r?\n.*?\r?\n---\s*\r?\n(.*)$') { $Matches[1] } else { $content }

    # Extract blocker (stop before next section)
    if ($body -match '(?i)-\s*Blocker\s*/?\s*one line:\s*(.+?)(?:\r?\n|$)') {
        $val = $Matches[1].Trim()
        if ($val -and $val -notmatch '^##') {
            $entry.blocker = $val
        }
    }

    # Extract focus line
    if ($body -match '(?m)^>\s*Focus:\s*(.+)') {
        $entry.focus = $Matches[1].Trim()
    }

    # Extract checked tasks (count them)
    $checked = ([regex]::Matches($body, '\[x\]')).Count
    $total = ([regex]::Matches($body, '\[[ x]\]')).Count
    $entry.tasksChecked = $checked
    $entry.tasksTotal = $total

    $dailyEntries += $entry
}

# Sort by date
$dailyEntries = $dailyEntries | Sort-Object { $_.date }

# --- Parse weekly notes ---
$weeklyEntries = @()
$weeklyFiles = Get-ChildItem -Path $weeklyDir -Filter "*.md" | Where-Object { $_.Name -ne ".gitkeep" }

foreach ($file in $weeklyFiles) {
    $content = Get-Content $file.FullName -Raw
    $entry = @{ name = $file.BaseName }

    if ($content -match '(?s)^---\s*\r?\n(.*?)\r?\n---') {
        $yaml = $Matches[1]
        foreach ($line in ($yaml -split '\r?\n')) {
            $line = $line.Trim()
            if ($line -match '^(\w+):\s*(.*)$') {
                $key = $Matches[1]
                $val = $Matches[2].Trim('"').Trim("'").Trim()
                switch ($key) {
                    'date'       { $entry.date = $val }
                    'week'       { $entry.week = $val }
                    'week_range' { $entry.weekRange = $val }
                }
            }
        }
    }

    # Extract numbers section
    if ($content -match '(?s)## Numbers\s*\n(.*?)(?:\n##|\z)') {
        $numbers = $Matches[1]
        if ($numbers -match 'Billable hours total:\s*(.+)') { $entry.billableTotal = $Matches[1].Trim() }
        if ($numbers -match 'Revenue total \(DA\):\s*(.+)') { $entry.revenueTotal = $Matches[1].Trim() }
        if ($numbers -match 'Avg yield \(DA/hr\):\s*(.+)') { $entry.avgYield = $Matches[1].Trim() }
        if ($numbers -match 'Projects moved:\s*(.+)') { $entry.projectsMoved = $Matches[1].Trim() }
    }

    # Extract won section
    if ($content -match '(?s)## Won this week\s*\n(.*?)(?:\n##|\z)') {
        $won = $Matches[1].Trim()
        if ($won) { $entry.won = $won }
    }

    # Extract slippage
    if ($content -match '(?s)## Slippage.*?\s*\n.*?What fell behind:\s*(.+)') {
        $entry.slippage = $Matches[1].Trim()
    }

    $weeklyEntries += $entry
}

$weeklyEntries = $weeklyEntries | Sort-Object { $_.date }

# --- Build combined output ---
$output = @{
    exported = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    source = "Obsidian 05_Daily_Notes + 06_Weekly_Notes"
    daily = $dailyEntries
    weekly = $weeklyEntries
    summary = @{
        totalDays = $dailyEntries.Count
        daysWithData = ($dailyEntries | Where-Object { $_.hoursWorked -and $_.hoursWorked -ne "" -and $_.hoursWorked -ne "0" }).Count
        totalWeeks = $weeklyEntries.Count
    }
}

# Write JSON
$outputPath = Join-Path $outputDir "obsidian_data.json"
$output | ConvertTo-Json -Depth 5 | Set-Content -Path $outputPath -Encoding UTF8

Write-Host "Done! Exported $($dailyEntries.Count) daily notes + $($weeklyEntries.Count) weekly notes"
Write-Host "Output: $outputPath"

# Also show summary
$daysWithHrs = ($dailyEntries | Where-Object { $_.hoursWorked -and $_.hoursWorked -ne "" -and $_.hoursWorked -ne "0" })
$totalHrs = ($daysWithHrs | ForEach-Object { [double]($_.hoursWorked) } | Measure-Object -Sum).Sum
$totalBill = ($daysWithHrs | ForEach-Object { [double]($_.hoursBillable) } | Measure-Object -Sum).Sum
$totalRev = ($daysWithHrs | ForEach-Object { [int]($_.revenueDA) } | Measure-Object -Sum).Sum

Write-Host ""
Write-Host "=== Summary ==="
Write-Host "Days with data: $($daysWithHrs.Count) / $($dailyEntries.Count)"
Write-Host "Total hours: $totalHrs"
Write-Host "Total billable: $totalBill"
Write-Host "Total revenue: $totalRev DA"
if ($totalBill -gt 0) {
    $avgYield = [math]::Round($totalRev / $totalBill)
    Write-Host "Avg yield: $avgYield DA/hr"
}
