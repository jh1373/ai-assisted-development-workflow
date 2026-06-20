$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$checker = Join-Path $repoRoot 'scripts\check-initialization.ps1'
$structureTool = Join-Path $repoRoot 'scripts\project-structure.py'
$directoryChecker = Join-Path $repoRoot 'scripts\check-directory-map.ps1'
$fixture = Join-Path ([System.IO.Path]::GetTempPath()) ("initialization-checker-" + [guid]::NewGuid().ToString('N'))
$powerShellExecutable = if ($PSVersionTable.PSEdition -eq 'Desktop') { 'powershell.exe' } else { 'pwsh' }

function Assert-Result {
    param([Parameter(Mandatory = $true)][string]$Expected)
    $actual = (& $powerShellExecutable -NoProfile -File (Join-Path $fixture 'scripts\check-initialization.ps1')).Trim()
    if ($actual -ne $Expected) {
        throw "Expected $Expected, got $actual"
    }
}

function Write-State {
    param(
        [Parameter(Mandatory = $true)][string]$Status,
        [Parameter(Mandatory = $true)][string]$Approved
    )
    $stateDir = Join-Path $fixture '.ai-workflow'
    New-Item -ItemType Directory -Force -Path $stateDir | Out-Null
    @(
        'schema_version=1'
        "initialization_status=$Status"
        "user_approved=$Approved"
    ) | Set-Content -LiteralPath (Join-Path $stateDir 'project-state.conf')
}

try {
    New-Item -ItemType Directory -Force -Path (Join-Path $fixture 'scripts') | Out-Null
    Copy-Item -LiteralPath $checker -Destination (Join-Path $fixture 'scripts\check-initialization.ps1')
    Copy-Item -LiteralPath $structureTool -Destination (Join-Path $fixture 'scripts\project-structure.py')
    Copy-Item -LiteralPath $directoryChecker -Destination (Join-Path $fixture 'scripts\check-directory-map.ps1')

    Assert-Result 'INITIALIZATION_CHECK_FAILED'

    Write-State -Status 'not_started' -Approved 'false'
    Assert-Result 'INITIALIZATION_NOT_STARTED'

    $reviewPath = Join-Path $fixture 'docs\INITIALIZATION_REVIEW.md'
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $reviewPath) | Out-Null
    Set-Content -LiteralPath $reviewPath -Value 'Initialization Decision: Ready'
    Assert-Result 'INITIALIZATION_INVALID'
    Set-Content -LiteralPath $reviewPath -Value 'Initialization Decision: Not Ready'

    Write-State -Status 'in_progress' -Approved 'false'
    Assert-Result 'INITIALIZATION_IN_PROGRESS'

    Write-State -Status 'revisit_required' -Approved 'false'
    Assert-Result 'INITIALIZATION_REVISIT_REQUIRED'

    Write-State -Status 'ready' -Approved 'false'
    Assert-Result 'INITIALIZATION_INVALID'

    Write-State -Status 'unknown' -Approved 'false'
    Assert-Result 'INITIALIZATION_INVALID'

    Write-State -Status 'READY' -Approved 'true'
    Assert-Result 'INITIALIZATION_INVALID'

    Write-State -Status 'ready' -Approved 'True'
    Assert-Result 'INITIALIZATION_INVALID'

    @('Schema_version=1', 'initialization_status=not_started', 'user_approved=false') | Set-Content -LiteralPath (Join-Path $fixture '.ai-workflow\project-state.conf')
    Assert-Result 'INITIALIZATION_INVALID'

    @('schema_version=2', 'initialization_status=not_started', 'user_approved=false') | Set-Content -LiteralPath (Join-Path $fixture '.ai-workflow\project-state.conf')
    Assert-Result 'INITIALIZATION_INVALID'

    @('schema_version=1', 'schema_version=1', 'initialization_status=not_started', 'user_approved=false') | Set-Content -LiteralPath (Join-Path $fixture '.ai-workflow\project-state.conf')
    Assert-Result 'INITIALIZATION_INVALID'

    Write-State -Status 'ready' -Approved 'true'
    Assert-Result 'INITIALIZATION_INVALID'

    New-Item -ItemType Directory -Force -Path (Join-Path $fixture 'docs') | Out-Null
    @('## Project-specific Context', 'Product goal: configured', '## Initialization Routing', '## Task Workflow After Initialization') | Set-Content -LiteralPath (Join-Path $fixture 'AGENTS.md')
    @('- Initialization track: Discovery', '- Last confirmed by user: 2026-06-20') | Set-Content -LiteralPath (Join-Path $fixture 'docs\PROJECT_BRIEF.md')
    @('- Initialization track: Discovery', '## Phase 1: Validation') | Set-Content -LiteralPath (Join-Path $fixture 'docs\ROADMAP.md')
    Set-Content -LiteralPath (Join-Path $fixture 'docs\PROJECT_STATUS.md') -Value 'Current phase: Discovery'
    Set-Content -LiteralPath (Join-Path $fixture 'docs\DIRECTORY_MAP.md') -Value 'Map Status: Provisional'
    @('Initialization Decision: Ready', '- Approved by: User', '- Approved at: 2026-06-20', '- Confirmation summary: Approved for validation') | Set-Content -LiteralPath (Join-Path $fixture 'docs\INITIALIZATION_REVIEW.md')
    @{
        schema_version = 1
        status = 'provisional'
        project_name = 'Fixture'
        verified_at = $null
        verified_by = $null
        ignore_file = '.ai-workflow/directory-map.ignore'
        nodes = @()
        conventions = @()
    } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $fixture '.ai-workflow\directory-map.json')
    & python (Join-Path $fixture 'scripts\project-structure.py') --root $fixture generate | Out-Null
    Assert-Result 'INITIALIZATION_READY'

    @('## Project-specific Context', 'Product goal: Not initialized', '## Initialization Routing', '## Task Workflow After Initialization') | Set-Content -LiteralPath (Join-Path $fixture 'AGENTS.md')
    Assert-Result 'INITIALIZATION_INVALID'
    @('## Project-specific Context', 'Product goal: configured', '## Initialization Routing', '## Task Workflow After Initialization') | Set-Content -LiteralPath (Join-Path $fixture 'AGENTS.md')

    @('Map Status: Provisional', '[PROJECT_ROOT]/') | Set-Content -LiteralPath (Join-Path $fixture 'docs\DIRECTORY_MAP.md')
    Assert-Result 'INITIALIZATION_INVALID'
    Set-Content -LiteralPath (Join-Path $fixture 'docs\DIRECTORY_MAP.md') -Value 'Map Status: Provisional'

    @('Initialization Decision: Ready', '- Approved by:    ', '- Approved at: 2026-06-20', '- Confirmation summary: Approved for validation') | Set-Content -LiteralPath (Join-Path $fixture 'docs\INITIALIZATION_REVIEW.md')
    Assert-Result 'INITIALIZATION_INVALID'

    @('Initialization Decision: Ready', '- Approved by: User', '- Approved at: 2026-06-20', '- Confirmation summary: Approved for validation') | Set-Content -LiteralPath (Join-Path $fixture 'docs\INITIALIZATION_REVIEW.md')
    Set-Content -LiteralPath (Join-Path $fixture '.ai-workflow\directory-map.json') -Value '{'
    Assert-Result 'INITIALIZATION_INVALID'

    Set-Content -LiteralPath (Join-Path $fixture 'docs\INITIALIZATION_REVIEW.md') -Value 'Initialization Decision: Not Ready'
    Assert-Result 'INITIALIZATION_INVALID'

    Remove-Item -LiteralPath $fixture -Recurse -Force
    New-Item -ItemType Directory -Force -Path $fixture | Out-Null
    Copy-Item -Path (Join-Path $repoRoot 'examples\project-initialization\*') -Destination $fixture -Recurse -Force
    Copy-Item -LiteralPath (Join-Path $repoRoot 'examples\project-initialization\.ai-workflow') -Destination $fixture -Recurse -Force
    New-Item -ItemType Directory -Force -Path (Join-Path $fixture 'scripts') | Out-Null
    Copy-Item -LiteralPath $checker -Destination (Join-Path $fixture 'scripts\check-initialization.ps1')
    Copy-Item -LiteralPath $structureTool -Destination (Join-Path $fixture 'scripts\project-structure.py')
    Copy-Item -LiteralPath $directoryChecker -Destination (Join-Path $fixture 'scripts\check-directory-map.ps1')
    & python (Join-Path $fixture 'scripts\project-structure.py') --root $fixture generate | Out-Null
    Assert-Result 'INITIALIZATION_READY'

    Write-Output 'Initialization checker PowerShell tests passed.'
}
finally {
    if (Test-Path -LiteralPath $fixture) {
        Remove-Item -LiteralPath $fixture -Recurse -Force
    }
}
