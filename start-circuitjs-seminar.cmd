@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$link = (Get-Content -LiteralPath (Join-Path '%~dp0' 'simulation\roundabout-final-link.txt') -Raw).Trim(); Start-Process $link"
endlocal
