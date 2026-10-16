"""Reliability (PC + Android): diagnostics, versions, cleanup, failure explanations."""
from __future__ import annotations

import json
import re
import time
import urllib.request
from pathlib import Path

_UA = {"User-Agent": "Mozilla/5.0 MusicFlow"}

# Explains a failure from its error message, with a tip.
_RAISONS = [
    (r"only an excerpt|только фрагмент|доступен только фрагмент", "Источник предоставил только фрагмент песни.",
     "Попробуйте выбрать другую версию или найти запись из другого источника."),
    (r"sign in to confirm|not a bot|429|too many requests", "YouTube ограничивает загрузки через это подключение.",
     "Подождите несколько минут или смените сеть (Wi-Fi ↔ 4G), затем нажмите «Повторить ошибки»."),
    (r"age|confirm your age|inappropriate", "Видео YouTube с возрастным ограничением.",
     "Нажмите «Другая версия» или «Версии», чтобы выбрать другое видео."),
    (r"private|unavailable|removed|not available|copyright|blocked", "Видео недоступно (удалено, скрыто или заблокировано в вашей стране).",
     "Приложение попробует найти другое видео. Если это не поможет, нажмите «Версии»."),
    (r"introuvable|not found|no video|no youtube match|no reliable|aucune correspondance|aucune autre|не найдены|не найдено|не найдена", "Песня не найдена на YouTube.",
     "Проверьте название и исполнителя или найдите песню вручную во вкладке «Поиск»."),
    (r"connexion|connection|network|timed out|timeout|getaddrinfo|unreachable|ssl|подключени|соединение|сеть", "Проблема с подключением к интернету.",
     "Повторная попытка начнётся автоматически после восстановления подключения."),
    (r"postprocessing|conversion|ffmpeg|постобработ|преобразован", "Не удалось преобразовать файл.",
     "Попробуйте другой формат в настройках (например, MP3 вместо FLAC или Opus)."),
    (r"espace|storage|no space|disk|недостаточно места|хранилищ", "Недостаточно места на устройстве.",
     "Освободите место или выберите другую папку."),
    (r"permission|denied|accès|нет доступа|отказано в доступе", "Нет доступа к папке назначения.",
     "Выберите папку для загрузки ещё раз."),
]


def expliquer(message: str) -> dict:
    m = (message or "").lower()
    for motif, raison, conseil in _RAISONS:
        if re.search(motif, m):
            return {"raison": raison, "conseil": conseil}
    return {"raison": "Непредвиденная ошибка.", "conseil": "Повторите попытку. Если ошибка появится снова, экспортируйте журнал ошибок (Настройки → Диагностика)."}


def _tester(nom, fonction):
    debut = time.time()
    try:
        detail = fonction() or "Всё работает"
        return {"nom": nom, "ok": True, "detail": str(detail)[:160], "ms": int((time.time() - debut) * 1000)}
    except Exception as exc:
        return {"nom": nom, "ok": False, "detail": str(exc)[:160], "ms": int((time.time() - debut) * 1000)}


def _http_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=_UA), timeout=12) as r:
        return json.loads(r.read().decode("utf-8"))


def _au_moins_un(liste, si_vide="результатов нет"):
    if not liste:
        raise RuntimeError(si_vide)
    return f"Результатов: {len(liste)}"


def diagnostic(search_videos, recherche_spotify, ffmpeg_ok) -> list[dict]:
    """Tests each service used by the app. The search functions are supplied
    by the server (PC or Android) to test exactly what the app uses."""
    tests = [
        ("Интернет", lambda: _http_json("https://api.deezer.com/infos") and "доступен"),
        ("YouTube (поиск)", lambda: _au_moins_un(search_videos("daft punk one more time", limit=2))),
        ("Spotify (поиск)", lambda: _au_moins_un(recherche_spotify("one more time daft punk", 3),
                                                     "Результатов нет; попробуем найти на YouTube")),
        ("Deezer (исполнители и альбомы)", lambda: _http_json("https://api.deezer.com/search?q=daft%20punk&limit=1")["data"][0]["title"]),
        ("iTunes (сведения об альбоме)", lambda: _http_json("https://itunes.apple.com/search?term=daft+punk&entity=song&limit=1")["results"][0]["collectionName"]),
        ("LRCLIB (тексты песен)", lambda: "Всё работает" if _http_json("https://lrclib.net/api/search?q=one%20more%20time%20daft%20punk") else "пусто"),
        ("Преобразование аудио (ffmpeg)", lambda: "Всё работает" if ffmpeg_ok() else (_ for _ in ()).throw(RuntimeError("ffmpeg недоступен"))),
    ]
    return [_tester(n, f) for n, f in tests]


def nettoyer(dossier) -> dict:
    """Deletes leftovers of interrupted downloads (.part, .ytdl, .temp.*, thumbnails)."""
    d = Path(dossier)
    n, octets = 0, 0
    try:
        for f in d.iterdir():
            nom = f.name.lower()
            if f.is_file() and (nom.endswith((".part", ".ytdl", ".webp")) or ".temp." in nom or ".conv." in nom
                                or ".cover." in nom or nom.endswith(".part-frag")):
                try:
                    octets += f.stat().st_size
                    f.unlink()
                    n += 1
                except Exception:
                    pass
    except Exception:
        pass
    return {"fichiers": n, "octets": octets}
