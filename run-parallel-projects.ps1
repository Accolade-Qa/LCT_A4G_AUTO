param(
    [string[]]$Projects = @('lct','sampark','swaraj','trio'),
    [string]$PyCmd = 'python -m pytest',
    [string]$TestsPath = 'tests',
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

    # Build the command to run under cmd.exe start with affinity and background (/b)
    # start "<title>" /b /affinity <hex> <command> > "logfile" 2>&1
    # Build start command by concatenation to avoid PowerShell interpolation/quoting issues
    $startCommand = 'start "' + $proj + '" /b /affinity ' + $hexMask + ' ' + $PyCmd + ' ' + $TestsPath + ' -q --project ' + $proj + ' > "' + $LogDir + '\\' + $proj + '.log" 2>&1'
    $arg = '/c ' + $startCommand

    Write-Host "Launching project '$proj' on core $core (mask 0x$hexMask)"
    Start-Process -FilePath cmd.exe -ArgumentList $arg -WindowStyle Hidden
}

Write-Host "Launched $($Projects.Length) test processes. Logs: $LogDir"
