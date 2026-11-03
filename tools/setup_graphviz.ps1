# Vendos Graphviz portable vetëm brenda projektit; pa ndryshuar instalimin e sistemit.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$downloadDirectory = Join-Path $projectRoot '.tools/downloads'
$installDirectory = Join-Path $projectRoot '.tools/graphviz'
$archivePath = Join-Path $downloadDirectory 'graphviz.zip'
$checksumPath = Join-Path $downloadDirectory 'graphviz.zip.sha256'
$releaseUrl = 'https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/16.1.0/windows_10_cmake_Release_Graphviz-16.1.0-win64.zip'
New-Item -ItemType Directory -Force -Path $downloadDirectory | Out-Null
Invoke-WebRequest -Uri $releaseUrl -OutFile $archivePath
Invoke-WebRequest -Uri ($releaseUrl + '.sha256') -OutFile $checksumPath
$expectedChecksum = ((Get-Content -LiteralPath $checksumPath -Raw).Trim() -split '\s+')[0].ToLower()
$actualChecksum = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLower()
if ($expectedChecksum -ne $actualChecksum)
{
    throw 'Graphviz SHA256 nuk përputhet; arkivi nuk do të ekzekutohet.'
}
Expand-Archive -LiteralPath $archivePath -DestinationPath $installDirectory -Force
$dotPath = Get-ChildItem -LiteralPath $installDirectory -Filter dot.exe -Recurse | Select-Object -First 1 -ExpandProperty FullName
if (-not $dotPath)
{
    throw 'Arkivi nuk përmban dot.exe.'
}
& $dotPath -V
Write-Output ('Graphviz u vendos te: ' + $dotPath)
