@echo off
setlocal

reg add HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR /v Start /t REG_DWORD /d 3 /f >nul 2>&1  

REM Change the value of the Start key to 3 to unblock USB storage devices