@echo off

set "CURRENT_DIR=%~dp0"

cd /d "%CURRENT_DIR%"
call .\_install.bat

cd /d "%CURRENT_DIR%"
call .\_fix.bat

pause