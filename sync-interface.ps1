[CmdletBinding()]
param(
    [switch]$Check
)

$ErrorActionPreference = 'Stop'
$source = Join-Path $PSScriptRoot 'index.html'
$copies = @(
    (Join-Path $PSScriptRoot 'android\app\src\main\assets\index.html'),
    (Join-Path $PSScriptRoot 'android\app\src\main\python\index.html')
)

if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
    throw "Primary interface not found: $source"
}

if ($Check) {
    $sourceHash = (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
    $different = @($copies | Where-Object {
        -not (Test-Path -LiteralPath $_ -PathType Leaf) -or
        (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash -ne $sourceHash
    })
    if ($different.Count -gt 0) {
        throw "Interface copies differ from index.html: $($different -join ', ')"
    }
    Write-Output 'All three interface files are identical.'
    exit 0
}

foreach ($copy in $copies) {
    Copy-Item -LiteralPath $source -Destination $copy -Force
}

Write-Output 'Synchronized Android interfaces from index.html.'
