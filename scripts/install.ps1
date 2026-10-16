# Copy skills into ~/.claude/skills (default) or ./.claude/skills (-Project).
param([switch]$Project)
$src = Join-Path (Split-Path $PSScriptRoot -Parent) "skills"
if ($Project) { $dest = Join-Path (Get-Location) ".claude/skills" } else { $dest = Join-Path $HOME ".claude/skills" }
New-Item -ItemType Directory -Force $dest | Out-Null
Get-ChildItem $src -Directory | ForEach-Object {
    $target = Join-Path $dest $_.Name
    if (Test-Path $target) { Remove-Item -Recurse -Force $target }
    Copy-Item -Recurse $_.FullName $target
    Write-Output "installed $($_.Name) -> $target"
}
