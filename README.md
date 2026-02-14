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

**Mode interactif** (l’URL sera demandée) :
```bash
python main.py
```

**En ligne de commande** :
```bash
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

**Avec dossier de sortie personnalisé** :
```bash
python main.py "https://youtube.com/..." "mon_dossier"
```

Les fichiers MP3 sont enregistrés dans le dossier `downloads/` par défaut.

## Structure du projet

```
mp3_py/
├── main.py           # Script principal
├── requirements.txt  # Dépendances
├── README.md
└── downloads/        # MP3 générés (créé automatiquement)
```
