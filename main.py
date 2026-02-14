"""
YouTube to MP3 - Extrait l'audio des vidéos YouTube et le convertit en MP3.

"""

import os
import sys

try:
    import yt_dlp
except ImportError:
    print("Erreur: yt-dlp n'est pas installe.")
    print("   Execute: pip install -r requirements.txt")
    sys.exit(1)

from ffmpeg_setup import get_ffmpeg_location, has_system_ffmpeg

OUTPUT_DIR = "downloads"


def get_ydl_opts(output_path: str, ffmpeg_location: str | None = None) -> dict:
    """Options pour yt-dlp : extrait l'audio et convertit en MP3."""
    opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "quiet": False,
        "no_warnings": False,
    }
    if ffmpeg_location:
        opts["ffmpeg_location"] = ffmpeg_location
    return opts


def download(url: str, output_path: str = OUTPUT_DIR, ffmpeg_location: str | None = None) -> bool:
    """
    Télécharge une vidéo YouTube et la convertit en MP3.
    
    Args:
        url: Lien YouTube (ou playlist)
        output_path: Dossier de destination
    
    Returns:
        True si succès, False sinon
    """
    os.makedirs(output_path, exist_ok=True)
    
    opts = get_ydl_opts(output_path, ffmpeg_location)
    
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"Erreur de telechargement: {e}")
        return False
    except Exception as e:
        print(f"Erreur: {e}")
        return False


def main():
    print("=" * 50)
    print("  YouTube -> MP3 ")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        output = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_DIR
    else:
        url = input("\nColler l'URL YouTube: ").strip()
        output = OUTPUT_DIR
    
    if not url:
        print("Aucune URL fournie.")
        sys.exit(1)
    
    ffmpeg_loc = get_ffmpeg_location()
    if ffmpeg_loc is None and not has_system_ffmpeg():
        print("\nFFmpeg introuvable.")
        print("   Sur Windows : winget install FFmpeg")
        print("   Ou relance le script pour tenter un telechargement automatique.")
        sys.exit(1)
    
    print("\nTelechargement en cours...")
    print(f"   Dossier: {os.path.abspath(output)}\n")
    
    if download(url, output, ffmpeg_loc):
        print(f"\nTermine ! Fichiers dans: {os.path.abspath(output)}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
