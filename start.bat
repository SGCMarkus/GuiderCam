git pull origin master
@echo off
for /F "tokens=*" %%g in ('type python_install_path') do (set pythonEnv=%%g)
set pythonPath="%pythonEnv%\python.exe"
@echo on
%pythonPath% Cams.py