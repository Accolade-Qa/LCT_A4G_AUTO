param(
    [string[]]$Projects = @('lct','sampark','swaraj','trio', 'atcu'),
    [string]$PythonExe = 'python',
    [string]$ReportScript = 'utils\\generate_reports.py',
    [string]$ReportDir = 'reports',
    [string]$LogDir = 'logs'
)

if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}

$procCount = [Environment]::ProcessorCount
Write-Host "Processor count: $procCount"

for ($i = 0; $i -lt $Projects.Length; $i++) {
    $proj = $Projects[$i]
    $core = $i % $procCount
    $mask = 1 -shl $core
    $hexMask = ('{0:X}' -f $mask)
    $logFile = Join-Path $LogDir "$proj.log"
    $wrapper = Join-Path $LogDir "$proj-run.cmd"

    $wrapperCmd = '{0} {1} --project {2} --report-dir {3} > "{4}" 2>&1' -f $PythonExe, $ReportScript, $proj, $ReportDir, $logFile
    $wrapperContent = @(
        '@echo off',
        'cd /d "' + (Get-Location).Path + '"',
        $wrapperCmd
    )
    $wrapperContent | Set-Content -Path $wrapper -Encoding ASCII

    # Ensure each project has both a wrapper script and an initialized log file
    if (-not (Test-Path $logFile)) {
        New-Item -ItemType File -Path $logFile | Out-Null
    }

    $startCommand = 'start "' + $proj + '" /b /affinity 0x' + $hexMask + ' cmd /c ""' + $wrapper + '""'

    Write-Host "Launching project '$proj' on core $core (mask 0x$hexMask)"
    Start-Process -FilePath cmd.exe -ArgumentList '/c', $startCommand -WindowStyle Hidden
}

Write-Host "Launched $($Projects.Length) report processes. Logs: $LogDir"
