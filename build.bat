@echo off
REM Build script for Windows

echo Building AI Meeting Summarizer...

REM Clean previous builds
if exist dist rmdir /s /q dist

REM Build for Windows
call npm run build

echo Build complete! Check the dist folder for the installer.
pause

