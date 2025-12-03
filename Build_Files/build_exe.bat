@echo off
echo Building Stroop Test Executable...
echo This may take several minutes...

REM Change to parent directory where stroop_test.py is located
cd ..

REM Clean up old builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build the executable using Python 3.13 and PyInstaller
"C:\Python313\python.exe" "C:\Users\42077\AppData\Roaming\Python\Python313\site-packages\PyInstaller\__main__.py" --onefile --windowed stroop_test.py

echo.
echo Build completed! Check the 'dist' folder for stroop_test.exe
pause
