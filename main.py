"""
YouTube Downloader - Telechargement de videos et playlists YouTube.
Modes : video (MP4), playlist (MP3), video -> MP3
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

# Modes disponibles
MODE_VIDEO = "1"      # Vidéo en MP4
MODE_PLAYLIST = "2"   # Playlist en MP3
MODE_MP3 = "3"        # Vidéo unique en MP3


def get_ydl_opts_mp3(output_path: str, ffmpeg_location: str | None = None, playlist: bool = False) -> dict:
    """Options pour extraire l'audio et convertir en MP3."""
    outtmpl = os.path.join(output_path, "%(playlist_index)s - %(title)s.%(ext)s" if playlist else "%(title)s.%(ext)s")
    opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": outtmpl,
        "quiet": False,
        "no_warnings": False,
    }
    if ffmpeg_location:
        opts["ffmpeg_location"] = ffmpeg_location
    return opts


def get_ydl_opts_video(output_path: str, ffmpeg_location: str | None = None) -> dict:
    """Options pour telecharger la video en MP4."""
    opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "quiet": False,
        "no_warnings": False,
    }
    if ffmpeg_location:
        opts["ffmpeg_location"] = ffmpeg_location
    return opts


def download(url: str, mode: str, output_path: str = OUTPUT_DIR, ffmpeg_location: str | None = None) -> bool:
    """
    Telecharge selon le mode choisi.
    
    Args:
        url: Lien YouTube (video ou playlist)
        mode: "1" video MP4, "2" playlist MP3, "3" video MP3
        output_path: Dossier de destination
        ffmpeg_location: Chemin vers FFmpeg (ou None pour PATH)
    """
    os.makedirs(output_path, exist_ok=True)
    
    if mode == MODE_VIDEO:
        opts = get_ydl_opts_video(output_path, ffmpeg_location)
    else:
        opts = get_ydl_opts_mp3(output_path, ffmpeg_location, playlist=(mode == MODE_PLAYLIST))
    
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


def show_menu() -> tuple[str, str]:
    """Affiche le menu et retourne (mode, url)."""
    print("\n" + "=" * 50)
    print("  YouTube Downloader")
    print("=" * 50)
    print("\n  Choisir une option :")
    print("    1 - Telecharger une video (format MP4)")
    print("    2 - Telecharger une playlist (MP3)")
    print("    3 - Telecharger une video et convertir en MP3")
    print("    0 - Quitter")
    print()
    
    choice = input("Votre choix (1/2/3/0) : ").strip()
    
    if choice == "0":
        print("Au revoir.")
        sys.exit(0)
    
    if choice not in (MODE_VIDEO, MODE_PLAYLIST, MODE_MP3):
        print("Choix invalide.")
        sys.exit(1)
    
    url = input("\nColler l'URL YouTube : ").strip()
    if not url:
        print("Aucune URL fournie.")
        sys.exit(1)
    
    return choice, url


def main():
    if len(sys.argv) >= 3:
        # Mode CLI : python main.py <mode> <url>
        mode = sys.argv[1]
        url = sys.argv[2]
        output = sys.argv[3] if len(sys.argv) > 3 else OUTPUT_DIR
        if mode not in (MODE_VIDEO, MODE_PLAYLIST, MODE_MP3):
            print("Mode invalide. Utilisez 1, 2 ou 3.")
            sys.exit(1)
    else:
        mode, url = show_menu()
        output = OUTPUT_DIR
    
    ffmpeg_loc = get_ffmpeg_location()
    if ffmpeg_loc is None and not has_system_ffmpeg():
        print("\nFFmpeg introuvable.")
        print("   Sur Windows : winget install FFmpeg")
        print("   Ou relance le script pour tenter un telechargement automatique.")
        sys.exit(1)
    
    labels = {MODE_VIDEO: "Video MP4", MODE_PLAYLIST: "Playlist MP3", MODE_MP3: "Video -> MP3"}
    print(f"\nTelechargement ({labels[mode]}) en cours...")
    print(f"   Dossier: {os.path.abspath(output)}\n")
    
    if download(url, mode, output, ffmpeg_loc):
        print(f"\nTermine ! Fichiers dans: {os.path.abspath(output)}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
