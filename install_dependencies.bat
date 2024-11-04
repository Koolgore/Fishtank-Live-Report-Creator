@echo off
echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing dependencies from requirements.txt...
python -m pip install -r requirements.txt

if %errorlevel% == 0 (
    echo All dependencies have been successfully installed.
) else (
    echo An error occurred while installing dependencies.
)

pause
