"""
Détection et téléchargement automatique de FFmpeg pour Windows.
"""

import os
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

# Dossier local pour FFmpeg (dans le projet)
PROJECT_DIR = Path(__file__).resolve().parent
FFMPEG_DIR = PROJECT_DIR / "ffmpeg"
FFMPEG_BIN = FFMPEG_DIR / "bin"
FFMPEG_URL = "https://github.com/yt-dlp/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"


def find_ffmpeg() -> str | None:
    """
    Retourne le chemin vers le dossier contenant ffmpeg/ffprobe, ou None.
    None avec ffmpeg dans PATH = yt-dlp utilisera le PATH.
    """
    # 1. Vérifier le dossier local du projet
    if FFMPEG_BIN.exists() and (FFMPEG_BIN / "ffmpeg.exe").exists():
        return str(FFMPEG_BIN)
    
    # 2. Vérifier le PATH système
    if shutil.which("ffmpeg") and shutil.which("ffprobe"):
        return None  # yt-dlp utilisera le PATH
    
    return None


def download_ffmpeg() -> bool:
    """Télécharge FFmpeg depuis yt-dlp/FFmpeg-Builds (Windows 64-bit uniquement)."""
    if platform.system() != "Windows" or platform.machine() not in ("AMD64", "x86_64"):
        return False
    
    if not requests:
        return False
    
    print("Telechargement de FFmpeg... (environ 200 Mo, une seule fois)")
    
    try:
        r = requests.get(FFMPEG_URL, stream=True, timeout=30)
        r.raise_for_status()
        
        zip_path = PROJECT_DIR / "ffmpeg.zip"
        with open(zip_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Nettoyer l'ancien dossier
        if FFMPEG_DIR.exists():
            shutil.rmtree(FFMPEG_DIR)
        
        # Extraire
        with zipfile.ZipFile(zip_path, "r") as z:
            # Le zip contient un dossier ffmpeg-master-latest-win64-gpl avec bin/ à l'intérieur
            for name in z.namelist():
                z.extract(name, PROJECT_DIR)
        
        zip_path.unlink()
        
        # Le zip extrait un dossier ffmpeg-*-win64-gpl/ avec bin/ à l'intérieur
        extracted = [f for f in PROJECT_DIR.iterdir() if f.is_dir() and f.name.startswith("ffmpeg-")]
        for folder in extracted:
            inner_bin = folder / "bin"
            if inner_bin.exists() and (inner_bin / "ffmpeg.exe").exists():
                FFMPEG_BIN.mkdir(parents=True, exist_ok=True)
                for exe in inner_bin.iterdir():
                    shutil.copy2(exe, FFMPEG_BIN / exe.name)
                shutil.rmtree(folder)
                return True
        
        return (FFMPEG_BIN / "ffmpeg.exe").exists()
        
    except Exception as e:
        print(f"Erreur: {e}")
        return False


def has_system_ffmpeg() -> bool:
    """Vérifie si ffmpeg et ffprobe sont dans le PATH."""
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def get_ffmpeg_location() -> str | None:
    """
    Retourne le chemin FFmpeg à utiliser pour yt-dlp, ou None pour utiliser le PATH.
    Télécharge automatiquement si nécessaire (Windows).
    """
    location = find_ffmpeg()
    if location:
        return location
    if has_system_ffmpeg():
        return None  # yt-dlp utilisera le PATH
    
    # Essayer de télécharger sur Windows
    if platform.system() == "Windows" and download_ffmpeg():
        return str(FFMPEG_BIN)
    
    return None
