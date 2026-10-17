@echo off
setlocal
cd /d "%~dp0"

rem Use JDK 17 for this build process without changing Windows-wide settings.
if defined JAVA_HOME (
    if not exist "%JAVA_HOME%\bin\javac.exe" set "JAVA_HOME="
    if defined JAVA_HOME (
        "%JAVA_HOME%\bin\javac.exe" -version 2>&1 | findstr /b /c:"javac 17." >nul
        if errorlevel 1 set "JAVA_HOME="
    )
)
if not defined JAVA_HOME (
    for /d %%J in ("%ProgramFiles%\Eclipse Adoptium\jdk-17*" "%ProgramFiles%\Java\jdk-17*" "%ProgramFiles%\Microsoft\jdk-17*") do (
        if exist "%%~fJ\bin\javac.exe" set "JAVA_HOME=%%~fJ"
    )
)
if not defined JAVA_HOME (
    echo JDK 17 not found. Set JAVA_HOME to a JDK 17 installation.
    exit /b 1
)
set "PATH=%JAVA_HOME%\bin;%PATH%"

if not defined ANDROID_HOME if defined ANDROID_SDK_ROOT set "ANDROID_HOME=%ANDROID_SDK_ROOT%"
if not defined ANDROID_HOME if exist "%LOCALAPPDATA%\Android\Sdk\platforms\android-36\android.jar" set "ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk"
if not defined ANDROID_HOME (
    echo Android SDK not found. Install Android SDK Platform 36 and set ANDROID_HOME.
    exit /b 1
)
if not exist "%ANDROID_HOME%\platforms\android-36\android.jar" (
    echo Android SDK Platform 36 not found under "%ANDROID_HOME%".
    exit /b 1
)
set "PATH=%ANDROID_HOME%\platform-tools;%PATH%"

if not defined CHAQUOPY_PYTHON (
    for /d %%P in ("%LOCALAPPDATA%\Programs\Python\Python313*") do (
        if exist "%%~fP\python.exe" set "CHAQUOPY_PYTHON=%%~fP\python.exe"
    )
)
if not defined CHAQUOPY_PYTHON (
    echo Python 3.13 not found. Set CHAQUOPY_PYTHON to python.exe.
    exit /b 1
)
if not exist "%CHAQUOPY_PYTHON%" (
    echo CHAQUOPY_PYTHON does not point to an executable: "%CHAQUOPY_PYTHON%"
    exit /b 1
)
for /f "tokens=2" %%V in ('"%CHAQUOPY_PYTHON%" --version 2^>^&1') do set "PYTHON_VERSION=%%V"
if not "%PYTHON_VERSION:~0,4%"=="3.13" (
    echo Python 3.13 required by Chaquopy. Found "%PYTHON_VERSION%".
    exit /b 1
)

call .\gradlew.bat assembleDebug --no-daemon
exit /b %ERRORLEVEL%
