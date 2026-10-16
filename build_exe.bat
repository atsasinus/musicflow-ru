@echo off
setlocal
cd /d "%~dp0"
.venv\Scripts\python -m PyInstaller --noconfirm --onefile --name MusicFlow-RU --add-data "index.html;." --collect-data imageio_ffmpeg --collect-binaries imageio_ffmpeg --collect-data selenium --collect-submodules yt_dlp --collect-data yt_dlp_ejs --hidden-import truststore app.py > build_exe.log 2>&1
if errorlevel 1 (
    echo EXE_KO>> build_exe.log
    exit /b 1
)
echo EXE_OK>> build_exe.log
exit /b 0
