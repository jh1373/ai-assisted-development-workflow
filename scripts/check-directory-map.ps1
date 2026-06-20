$ErrorActionPreference = 'Stop'

$tool = Join-Path $PSScriptRoot 'project-structure.py'

try {
    if (Get-Command python -ErrorAction SilentlyContinue) {
        & python $tool validate --require-generated @args
        exit $LASTEXITCODE
    }
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 $tool validate --require-generated @args
        exit $LASTEXITCODE
    }
}
catch {
    Write-Output 'DIRECTORY_MAP_CHECK_FAILED'
    exit 0
}

Write-Output 'DIRECTORY_MAP_CHECK_FAILED'
exit 0
