$ErrorActionPreference = 'Stop'

function Write-ResultAndExit {
    param([Parameter(Mandatory = $true)][string]$Result)
    Write-Output $Result
    exit 0
}

try {
    $projectRoot = Split-Path -Parent $PSScriptRoot
    $stateFile = Join-Path $projectRoot '.ai-workflow\project-state.conf'

    if (-not (Test-Path -LiteralPath $stateFile)) {
        Write-ResultAndExit 'INITIALIZATION_CHECK_FAILED'
    }

    if (-not (Test-Path -LiteralPath $stateFile -PathType Leaf)) {
        Write-ResultAndExit 'INITIALIZATION_CHECK_FAILED'
    }

    $lines = @(Get-Content -LiteralPath $stateFile | Where-Object { $_ -ne '' })
    if ($lines.Count -ne 3) {
        Write-ResultAndExit 'INITIALIZATION_INVALID'
    }

    $values = @{}
    foreach ($line in $lines) {
        if ($line -notmatch '^(schema_version|initialization_status|user_approved)=([^\s]+)$') {
            Write-ResultAndExit 'INITIALIZATION_INVALID'
        }
        if ($values.ContainsKey($Matches[1])) {
            Write-ResultAndExit 'INITIALIZATION_INVALID'
        }
        $values[$Matches[1]] = $Matches[2]
    }

    if ($values.Count -ne 3 -or $values['schema_version'] -ne '1') {
        Write-ResultAndExit 'INITIALIZATION_INVALID'
    }

    $status = $values['initialization_status']
    $approved = $values['user_approved']

    switch ($status) {
        'not_started' {
            if ($approved -ne 'false') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            $reviewPath = Join-Path $projectRoot 'docs\INITIALIZATION_REVIEW.md'
            if ((Test-Path -LiteralPath $reviewPath -PathType Leaf) -and ((Get-Content -LiteralPath $reviewPath) -contains 'Initialization Decision: Ready')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            Write-ResultAndExit 'INITIALIZATION_NOT_STARTED'
        }
        'in_progress' {
            if ($approved -ne 'false') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            Write-ResultAndExit 'INITIALIZATION_IN_PROGRESS'
        }
        'revisit_required' {
            if ($approved -ne 'false') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            Write-ResultAndExit 'INITIALIZATION_REVISIT_REQUIRED'
        }
        'ready' {
            if ($approved -ne 'true') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            $requiredFiles = @(
                'AGENTS.md',
                'docs\PROJECT_BRIEF.md',
                'docs\ROADMAP.md',
                'docs\PROJECT_STATUS.md',
                'docs\DIRECTORY_MAP.md',
                'docs\INITIALIZATION_REVIEW.md'
            )
            foreach ($relativePath in $requiredFiles) {
                $path = Join-Path $projectRoot $relativePath
                if (-not (Test-Path -LiteralPath $path -PathType Leaf) -or (Get-Item -LiteralPath $path).Length -eq 0) {
                    Write-ResultAndExit 'INITIALIZATION_INVALID'
                }
            }
            $reviewPath = Join-Path $projectRoot 'docs\INITIALIZATION_REVIEW.md'
            if ((Get-Content -LiteralPath $reviewPath) -notcontains 'Initialization Decision: Ready') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (Select-String -LiteralPath (Join-Path $projectRoot 'AGENTS.md') -SimpleMatch 'Not initialized' -Quiet) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $projectBrief = Get-Content -LiteralPath (Join-Path $projectRoot 'docs\PROJECT_BRIEF.md')
            if (-not ($projectBrief -match '^- Initialization track: (Discovery|Build-ready)$')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if ($projectBrief -contains '- Last confirmed by user: Not confirmed') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $roadmap = Get-Content -LiteralPath (Join-Path $projectRoot 'docs\ROADMAP.md')
            if (-not ($roadmap -match '^- Initialization track: (Discovery|Build-ready)$')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if ((Get-Content -LiteralPath (Join-Path $projectRoot 'docs\PROJECT_STATUS.md')) -contains 'Project Initialization: Not started') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $directoryMap = Get-Content -LiteralPath (Join-Path $projectRoot 'docs\DIRECTORY_MAP.md')
            if (-not ($directoryMap -match '^Map Status: (Provisional|Verified)$')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            Write-ResultAndExit 'INITIALIZATION_READY'
        }
        default {
            Write-ResultAndExit 'INITIALIZATION_INVALID'
        }
    }
}
catch {
    Write-ResultAndExit 'INITIALIZATION_CHECK_FAILED'
}
