<#
Run server helper for Windows PowerShell.

This script:
- Loads simple KEY=VALUE lines from `HerLens\\.env` into environment variables for this session (ignores commented lines).
- Runs the project's virtualenv Python to start uvicorn with the correct module path so imports work from the workspace root.

Usage: from C:\\HerLens run `./run_server.ps1`
#>

Param()

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = Join-Path $repoRoot 'HerLens\\.env'

Write-Host "Using repo root: $repoRoot"
if (Test-Path $envFile) {
    Write-Host "Loading env vars from $envFile"
    Get-Content $envFile | ForEach-Object {
        $_ = $_.Trim()
        if (-not ($_ -like '#*') -and $_ -match '^(.*?)=(.*)$') {
            $k = $matches[1].Trim()
            $v = $matches[2].Trim()
            # remove surrounding quotes if present
            if ($v -match '^"(.*)"$') { $v = $matches[1] }
            Write-Host "Setting env var $k"
            Set-Item -Path Env:\$k -Value $v
        }
    }
} else {
    Write-Host "No env file found at $envFile"
}

$python = Join-Path $repoRoot '.venv\\Scripts\\python.exe'
if (-Not (Test-Path $python)) {
    Write-Host "Virtualenv python not found at $python. If you haven't created the venv, create and activate it first or adjust this script." -ForegroundColor Yellow
}

Write-Host "Starting uvicorn via: $python -m uvicorn HerLens.app:app --reload --port 8000"
Start-Process -NoNewWindow -Wait -FilePath $python -ArgumentList '-m','uvicorn','HerLens.app:app','--reload','--port','8000'
