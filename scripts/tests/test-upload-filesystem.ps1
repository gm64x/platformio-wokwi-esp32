$ErrorActionPreference = "Stop"

$scriptsDir = Split-Path -Parent $PSScriptRoot
$projectRoot = Split-Path -Parent $scriptsDir
$wrapperPath = Join-Path $scriptsDir "upload-filesystem.ps1"
$tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("pio-wrapper-test-" + [guid]::NewGuid().ToString("N"))
$outputPath = Join-Path $tempDir "pio-output.txt"
$fakePioPath = Join-Path $tempDir "pio.cmd"

New-Item -ItemType Directory -Path $tempDir | Out-Null
@'
@echo off
>"%PIO_TEST_OUTPUT%" echo %CD%
>>"%PIO_TEST_OUTPUT%" echo %*
if not defined PIO_TEST_EXIT_CODE exit /b 0
exit /b %PIO_TEST_EXIT_CODE%
'@ | Set-Content -LiteralPath $fakePioPath -Encoding Ascii

$oldPath = $env:PATH
$oldOutput = $env:PIO_TEST_OUTPUT
$oldExitCode = $env:PIO_TEST_EXIT_CODE
$oldLocation = Get-Location

try {
  $env:PATH = "$tempDir;$oldPath"
  $env:PIO_TEST_OUTPUT = $outputPath
  $env:PIO_TEST_EXIT_CODE = "0"
  Set-Location -LiteralPath $tempDir

  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $wrapperPath
  $successExitCode = $LASTEXITCODE
  if ($successExitCode -ne 0) {
    throw "Expected successful upload wrapper run, got exit code $successExitCode"
  }

  $actual = Get-Content -LiteralPath $outputPath
  if ($actual.Count -lt 2) {
    throw "The pio stub did not record its working directory and arguments"
  }
  if ($actual[0] -ine $projectRoot) {
    throw "Expected project root '$projectRoot', got '$($actual[0])'"
  }
  if ($actual[1] -ne "run -t uploadfs") {
    throw "Unexpected pio arguments: '$($actual[1])'"
  }

  $env:PIO_TEST_EXIT_CODE = "17"
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $wrapperPath
  $failureExitCode = $LASTEXITCODE
  if ($failureExitCode -ne 17) {
    throw "Expected the wrapper to propagate exit code 17, got $failureExitCode"
  }

  Write-Output "Windows uploader wrapper tests passed"
}
finally {
  Set-Location -LiteralPath $oldLocation
  $env:PATH = $oldPath

  if ($null -eq $oldOutput) {
    Remove-Item Env:PIO_TEST_OUTPUT -ErrorAction SilentlyContinue
  } else {
    $env:PIO_TEST_OUTPUT = $oldOutput
  }

  if ($null -eq $oldExitCode) {
    Remove-Item Env:PIO_TEST_EXIT_CODE -ErrorAction SilentlyContinue
  } else {
    $env:PIO_TEST_EXIT_CODE = $oldExitCode
  }

  Remove-Item -LiteralPath $tempDir -Recurse -Force -ErrorAction SilentlyContinue
}
