[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Path
)

$ErrorActionPreference = 'Stop'

function Resolve-TargetPath {
    param([Parameter(Mandatory = $true)][string]$InputPath)

    if ([System.IO.Path]::IsPathRooted($InputPath)) {
        return [System.IO.Path]::GetFullPath($InputPath)
    }

    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $InputPath))
}

function Stop-WithMessage {
    param([Parameter(Mandatory = $true)][string]$Message)

    [Console]::Error.WriteLine($Message)
    exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
$starterDir = Join-Path $repoRoot 'starter'

if (-not (Test-Path -LiteralPath $starterDir -PathType Container)) {
    Stop-WithMessage "starter directory was not found: $starterDir"
}

$targetDir = Resolve-TargetPath -InputPath $Path

if (Test-Path -LiteralPath $targetDir -PathType Leaf) {
    Stop-WithMessage "Target path is a file: $targetDir"
}

if (Test-Path -LiteralPath $targetDir -PathType Container) {
    $unexpectedItems = @(
        Get-ChildItem -LiteralPath $targetDir -Force |
            Where-Object { $_.Name -ne '.git' }
    )

    if ($unexpectedItems.Count -gt 0) {
        Stop-WithMessage "Target directory must be empty, or contain only .git: $targetDir"
    }
} else {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

Get-ChildItem -LiteralPath $starterDir -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $targetDir -Recurse -Force
}

$checker = Join-Path $targetDir 'scripts\check-initialization.ps1'
if (-not (Test-Path -LiteralPath $checker -PathType Leaf)) {
    Stop-WithMessage "Initialization checker was not copied: $checker"
}

$initializationResult = & $checker
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host ''
Write-Host 'AI-assisted development workflow was installed.'
Write-Host "Project: $targetDir"
Write-Host "Initialization check: $initializationResult"
Write-Host ''
Write-Host 'Next steps:'
Write-Host "1. cd `"$targetDir`""
Write-Host '2. Open AGENTS.md'
Write-Host '3. Start workflows/project-initialization.md'
Write-Host '4. Do not start normal tasks until INITIALIZATION_READY'
