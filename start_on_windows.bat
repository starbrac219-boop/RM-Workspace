@echo off
REM RM Workspace — starts dashboard + scheduler when Windows/your PC starts.
REM Put a shortcut to this file in: Win+R -> shell:startup
cd /d %~dp0
start "RM Dashboard" /min python run.py dashboard
python run.py schedule
