# Copy skills into ~/.claude/skills (default) or ./.claude/skills (-Project).
# Also installs Cloudflare's security-audit skill (MIT) as "cloudflare-security-audit" unless -NoThirdParty.
param([switch]$Project, [switch]$NoThirdParty)
$root = Split-Path $PSScriptRoot -Parent
if ($Project) { $dest = Join-Path (Get-Location) ".claude/skills" } else { $dest = Join-Path $HOME ".claude/skills" }
New-Item -ItemType Directory -Force $dest | Out-Null

function Install-Skill($from, $name) {
    $target = Join-Path $dest $name
    if (Test-Path $target) { Remove-Item -Recurse -Force $target }
    Copy-Item -Recurse $from $target
    Write-Host "installed $name -> $target"
    return $target
}

Get-ChildItem (Join-Path $root "skills") -Directory | ForEach-Object { Install-Skill $_.FullName $_.Name | Out-Null }

if (-not $NoThirdParty) {
    $t = Install-Skill (Join-Path $root "third_party/cloudflare-security-audit/security-audit") "cloudflare-security-audit"
    $md = Join-Path $t "SKILL.md"
    $text = [IO.File]::ReadAllText($md) -replace '(?m)^name:\s*security-audit\s*$', 'name: cloudflare-security-audit'
    [IO.File]::WriteAllText($md, $text)
    Install-Skill (Join-Path $root "third_party/playwright-skill/playwright-skill") "playwright-skill" | Out-Null
    Install-Skill (Join-Path $root "third_party/task-observer/task-observer") "task-observer" | Out-Null
    Write-Host "playwright-skill needs: cd $dest/playwright-skill; npm install; npx playwright install chromium"
}
