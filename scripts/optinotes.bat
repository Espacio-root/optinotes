@echo off
setlocal enabledelayedexpansion

set "script_directory=%~dp0"
set "project_path=!script_directory:~0,-1!"

set "venv_path=%project_path%\venv"
set "script_path=%project_path%\src\python_script.py"

call "%venv_path%\Scripts\activate"

python "%script_path%" %*
