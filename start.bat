git pull origin master
@echo off
for /F "tokens=*" %%g in ('cat python_install_path') do (set pythonEnv=%%g)
set pythonPath="%pythonEnv%\python.exe"
@echo on
%pythonPath% GuiderCam.py