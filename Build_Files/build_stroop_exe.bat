@echo off
echo ============================================
echo    BUILDING STROOP TEST EXECUTABLE
echo ============================================
echo This will take several minutes...
echo.

REM Clean up old builds
echo Cleaning up old files...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul

REM Build the executable
echo.
echo Building executable with PyInstaller...
echo This may take 5-10 minutes...
echo.

"C:\Python313\python.exe" "C:\Users\42077\AppData\Roaming\Python\Python313\site-packages\PyInstaller\__main__.py" --onefile --windowed --clean stroop_test.py

echo.
echo ============================================
if exist "dist\stroop_test.exe" (
    echo ✅ SUCCESS! Executable created successfully!
    echo 📁 Location: dist\stroop_test.exe
    echo 🎯 File size:
    for %%A in ("dist\stroop_test.exe") do echo    %%~zA bytes
) else (
    echo ❌ ERROR: Executable was not created!
    echo Please check the error messages above.
)
echo ============================================
echo.
pause
