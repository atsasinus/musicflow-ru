# MusicFlow-RU

[English](README-EN.md) · [Русский](README-RU.md)

MusicFlow-RU is a Russian-localized fork of [MusicFlow](https://github.com/captentv1/musicflow) for Windows and Android. It preserves the original app's features and GPL-3.0 license while translating the interface, tips, notifications, and user-facing messages into Russian.

## Features

- Search for songs and artists, browse discographies, and discover charts and playlists.
- Download tracks and playlists with a queue, duplicate detection, and pause/resume controls.
- Save audio as MP3, FLAC, WAV, Opus, or AAC, with metadata, cover art, and lyrics.
- Manage a local music library, edit tags, and check audio files.
- Use the same web interface on Windows and Android, with platform-specific features supplied by each app.

## How it works

On Windows, the Flask server in `app.py` serves the web interface from the root `index.html`. On Android, a Kotlin app displays that interface in a WebView; Python server code runs through Chaquopy, while Kotlin handles Android system features.

The root `index.html` is the canonical interface file. After editing it, run `sync-interface.ps1` from the project root to update both Android copies. Run `sync-interface.ps1 -Check` to confirm all three copies match.

## Windows

### Run from source

From the project root, create a virtual environment and install the app dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5090> in a browser. You can also start the source version with `Lancer MusicFlow.bat` after setting up `.venv`.

### Build or run the Windows EXE

Install the build dependencies and run the packaging script:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\build_exe.bat
```

PyInstaller creates `dist\MusicFlow-RU.exe`. The one-file executable includes its Python runtime and opens the local app in the default browser. The generated `dist` folder and the virtual environment are excluded from Git; build a local copy with the commands above.

## Android

To build a Debug APK on Windows, install or configure:

- JDK 17;
- Android SDK Platform API 36 and the required Android Build Tools;
- Python 3.13 for Chaquopy;
- network access for the first Gradle build.

Set `JAVA_HOME` to JDK 17, `ANDROID_HOME` to the Android SDK folder, and `CHAQUOPY_PYTHON` to the Python 3.13 executable. These can be set for the current PowerShell session only:

```powershell
$env:JAVA_HOME = 'C:\path\to\JDK 17'
$env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"
$env:CHAQUOPY_PYTHON = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
$env:Path = "$env:JAVA_HOME\bin;$env:ANDROID_HOME\platform-tools;$env:Path"
```

Then build from the `android` directory:

```powershell
.\gradlew.bat assembleDebug
```

The Debug APK is created at `android\app\build\outputs\apk\debug\app-debug.apk`. For Release builds, provide signing settings and keys outside the repository through `MUSICFLOW_SIGNING_PROPERTIES` or `-PmusicflowSigningProperties=...`. Do not commit signing keys or their configuration.

## Credits, disclaimer, and license

MusicFlow-RU is based on [captentv1/musicflow](https://github.com/captentv1/musicflow). The original project and its authors retain their credit.

This software is intended for personal use. Follow copyright law and the terms of service of any sources you use, and download only content you are allowed to copy. MusicFlow-RU is not affiliated with music or video services whose names appear in the app.

This project is distributed under the [GPL-3.0](LICENSE) license.
