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
        if ($line -cnotmatch '^(schema_version|initialization_status|user_approved)=([^\s]+)$') {
            Write-ResultAndExit 'INITIALIZATION_INVALID'
        }
        if ($values.ContainsKey($Matches[1])) {
            Write-ResultAndExit 'INITIALIZATION_INVALID'
        }
        $values[$Matches[1]] = $Matches[2]
    }

    if ($values.Count -ne 3 -or $values['schema_version'] -cne '1') {
        Write-ResultAndExit 'INITIALIZATION_INVALID'
    }

    $status = $values['initialization_status']
    $approved = $values['user_approved']

    switch -CaseSensitive ($status) {
        'not_started' {
            if ($approved -cne 'false') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            $reviewPath = Join-Path $projectRoot 'docs\INITIALIZATION_REVIEW.md'
            if ((Test-Path -LiteralPath $reviewPath -PathType Leaf) -and ((Get-Content -LiteralPath $reviewPath) -ccontains 'Initialization Decision: Ready')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            Write-ResultAndExit 'INITIALIZATION_NOT_STARTED'
        }
        'in_progress' {
            if ($approved -cne 'false') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            Write-ResultAndExit 'INITIALIZATION_IN_PROGRESS'
        }
        'revisit_required' {
            if ($approved -cne 'false') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            Write-ResultAndExit 'INITIALIZATION_REVISIT_REQUIRED'
        }
        'ready' {
            if ($approved -cne 'true') { Write-ResultAndExit 'INITIALIZATION_INVALID' }
            $requiredFiles = @(
                'AGENTS.md',
                'docs\PROJECT_BRIEF.md',
                'docs\ROADMAP.md',
                'docs\PROJECT_STATUS.md',
                'docs\DIRECTORY_MAP.md',
                'docs\INITIALIZATION_REVIEW.md',
                '.ai-workflow\directory-map.json',
                'scripts\project-structure.py',
                'scripts\check-directory-map.ps1'
            )
            foreach ($relativePath in $requiredFiles) {
                $path = Join-Path $projectRoot $relativePath
                if (-not (Test-Path -LiteralPath $path -PathType Leaf) -or (Get-Item -LiteralPath $path).Length -eq 0) {
                    Write-ResultAndExit 'INITIALIZATION_INVALID'
                }
            }
            $reviewPath = Join-Path $projectRoot 'docs\INITIALIZATION_REVIEW.md'
            $review = Get-Content -LiteralPath $reviewPath
            if ($review -cnotcontains 'Initialization Decision: Ready') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $agents = Get-Content -LiteralPath (Join-Path $projectRoot 'AGENTS.md')
            if ($agents -cnotcontains '## Project-specific Context' -or
                $agents -cnotcontains '## Initialization Routing' -or
                $agents -cnotcontains '## Task Workflow After Initialization') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (Select-String -LiteralPath (Join-Path $projectRoot 'AGENTS.md') -SimpleMatch 'Not initialized' -Quiet -CaseSensitive:$false) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (Select-String -LiteralPath (Join-Path $projectRoot 'AGENTS.md') -SimpleMatch '[project-specific' -Quiet -CaseSensitive:$false) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $projectBrief = Get-Content -LiteralPath (Join-Path $projectRoot 'docs\PROJECT_BRIEF.md')
            if (-not ($projectBrief -cmatch '^- Initialization track: (Discovery|Build-ready)$')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (-not ($projectBrief -cmatch '^- Last confirmed by user: .*\S')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if ($projectBrief -ccontains '- Last confirmed by user: Not confirmed') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $roadmap = Get-Content -LiteralPath (Join-Path $projectRoot 'docs\ROADMAP.md')
            if (-not ($roadmap -cmatch '^- Initialization track: (Discovery|Build-ready)$')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (-not ($roadmap -cmatch '^## Phase 1: .*\S')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if ((Get-Content -LiteralPath (Join-Path $projectRoot 'docs\PROJECT_STATUS.md')) -ccontains 'Project Initialization: Not started') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $directoryMap = Get-Content -LiteralPath (Join-Path $projectRoot 'docs\DIRECTORY_MAP.md')
            if (-not ($directoryMap -cmatch '^Map Status: (Provisional|Verified)$')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if ($directoryMap -cmatch '\[(PROJECT_ROOT|path|responsibility|boundary or important note|task type|primary path|related paths or tests|boundary not to cross)\]') {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (-not ($review -cmatch '^- Approved by: .*\S')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (-not ($review -cmatch '^- Approved at: [0-9]{4}-[0-9]{2}-[0-9]{2}$')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            if (-not ($review -cmatch '^- Confirmation summary: .*\S')) {
                Write-ResultAndExit 'INITIALIZATION_INVALID'
            }
            $directoryMapChecker = Join-Path $projectRoot 'scripts\check-directory-map.ps1'
            $directoryMapResult = (& $directoryMapChecker | Out-String).Trim()
            switch -CaseSensitive ($directoryMapResult) {
                'DIRECTORY_MAP_PROVISIONAL' { }
                'DIRECTORY_MAP_VERIFIED' { }
                'DIRECTORY_MAP_CHECK_FAILED' { Write-ResultAndExit 'INITIALIZATION_CHECK_FAILED' }
                default { Write-ResultAndExit 'INITIALIZATION_INVALID' }
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
