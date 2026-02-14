# YouTube → MP3

Projet académique : extraction audio des vidéos YouTube et conversion en MP3.

## Prérequis

1. **Python 3.8+**
2. **FFmpeg** — requis pour la conversion en MP3

### Installer FFmpeg (Windows)

- Télécharger depuis : https://ffmpeg.org/download.html  
- Ou avec **winget** : `winget install FFmpeg`
- Ou avec **Chocolatey** : `choco install ffmpeg`
- Ajouter FFmpeg au PATH système

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

**Mode interactif** — au lancement, un menu propose les options suivantes :
```bash
python main.py
```

| Option | Description |
|--------|-------------|
| 1 | Telecharger une video (format MP4) |
| 2 | Telecharger une playlist (MP3) |
| 3 | Telecharger une video et convertir en MP3 |
| 0 | Quitter |

**En ligne de commande** :
```bash
python main.py <mode> <url> [dossier]
# mode : 1 (video MP4), 2 (playlist MP3), 3 (video MP3)
python main.py 3 "https://www.youtube.com/watch?v=VIDEO_ID"
python main.py 1 "https://youtu.be/..." "videos"
```

Les fichiers sont enregistres dans `downloads/` par defaut.

## Structure du projet

```
mp3_py/
├── main.py           # Script principal
├── requirements.txt  # Dépendances
├── README.md
└── downloads/        # MP3 générés (créé automatiquement)
```
