@echo off
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH
    pause
    exit /b
)

echo Ensuring pip is installed...
python -m ensurepip --upgrade

echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing requirements
python -m pip install -r requirements.txt

echo Setup complete. You can now run the scripts with run.bat
pause