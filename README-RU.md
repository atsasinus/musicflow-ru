# MusicFlow-RU

MusicFlow-RU — русскоязычная версия интерфейса MusicFlow для Windows и Android. Цель форка — сделать приложение удобным для русскоязычных пользователей, сохранив существующие функции и структуру проекта.

## Отличия от оригинала

- Пользовательские подписи, подсказки, обучение, уведомления и сообщения приложения переведены на русский язык.
- Для HTML-интерфейса установлен язык `ru`.
- Название Android-приложения — MusicFlow-RU.
- Корневой `index.html` остаётся основным источником интерфейса. Команда `.\sync-interface.ps1` копирует его в Android-папки, а `.\sync-interface.ps1 -Check` проверяет идентичность всех трёх файлов.

Поиск, сетевые запросы, обработка аудио и работа очереди сохранены без изменений. Сортировка названий в интерфейсе использует русскую локаль.

## Windows и Android

В Windows интерфейс из корневого `index.html` обслуживает Flask-сервер `app.py`. Android-версия использует тот же веб-интерфейс внутри WebView, Python-сервер `app_mobile.py` через Chaquopy и Kotlin-код для системных функций Android. Общий интерфейс можно менять в одном HTML-файле, но приложение не состоит только из HTML: выбор папок, уведомления, фоновая загрузка и доступ к хранилищу зависят от платформы.

Корневой `index.html` — основной источник интерфейса. После его изменения запустите `sync-interface.ps1`, чтобы обновить обе копии для Android.

## Запуск Windows-версии из исходников

Из корня проекта создайте виртуальное окружение, установите зависимости и запустите сервер:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app.py
```

Откройте `http://127.0.0.1:5090`. Для сборки Windows EXE установите зависимости сборки и запустите `build_exe.bat`:

```powershell
.\.venv\Scripts\python -m pip install -r requirements-build.txt
.\build_exe.bat
```

EXE-файл появится в `dist\MusicFlow-RU.exe`. После настройки окружения запускать приложение можно через `Lancer MusicFlow.bat`.

## Сборка Debug APK в Windows

Нужны:

- JDK 17;
- Android SDK с платформой API 36 и необходимыми Android Build Tools;
- Python 3.13 для Chaquopy;
- доступ к сети для загрузки Gradle и зависимостей при первой сборке.

Укажите `JAVA_HOME` на JDK 17 и `ANDROID_HOME` на каталог Android SDK. Укажите путь к Python 3.13 в `CHAQUOPY_PYTHON`.

Для локальной сборки можно задать переменные только в текущем окне PowerShell:

```powershell
$env:JAVA_HOME = 'C:\путь\к\JDK 17'
$env:ANDROID_HOME = "$env:LOCALAPPDATA\Android\Sdk"
$env:CHAQUOPY_PYTHON = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
$env:Path = "$env:JAVA_HOME\bin;$env:ANDROID_HOME\platform-tools;$env:Path"
```

Из каталога `android` выполните:

```powershell
.\gradlew.bat assembleDebug
```

Готовый файл появится по пути `android\app\build\outputs\apk\debug\app-debug.apk`.

Для Release-сборки можно указать внешний файл настроек подписи через переменную `MUSICFLOW_SIGNING_PROPERTIES` или параметр `-PmusicflowSigningProperties=...`. Файл настроек подписи и ключи не следует добавлять в репозиторий. Для локальной Debug-сборки отдельный ключ не нужен.

## Синхронизация HTML

После редактирования корневого `index.html` из корня проекта выполните:

```powershell
.\sync-interface.ps1
.\sync-interface.ps1 -Check
```

## Благодарность и лицензия

Спасибо автору оригинального MusicFlow за разработку приложения: [captentv1/musicflow](https://github.com/captentv1/musicflow).

MusicFlow-RU сохраняет лицензию [GPL-3.0](LICENSE) и уведомления об авторстве оригинального проекта.
