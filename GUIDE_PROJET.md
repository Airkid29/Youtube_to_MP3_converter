# Guide du projet YouTube → MP3 — de A à Z

Ce document explique tout le projet en détail, y compris les concepts techniques comme FFmpeg.

---

## 1. C'est quoi le projet ?

Le projet permet de **télécharger une vidéo YouTube** et d'en **extraire uniquement la piste audio** pour la sauvegarder en **fichier MP3**.

**Exemple :** Tu donnes le lien d'un clip musical YouTube → tu obtiens un fichier MP3 que tu peux écouter sans vidéo.

---

## 2. Vue d'ensemble du flux

```
[Lien YouTube]  →  yt-dlp (télécharge la vidéo)  →  FFmpeg (convertit en MP3)  →  [Fichier .mp3]
```

1. **yt-dlp** : va chercher la vidéo sur YouTube et la télécharge (souvent en format WebM ou M4A).
2. **FFmpeg** : prend ce fichier audio/vidéo et le convertit en MP3.

---

## 3. Les acteurs principaux

### 3.1 yt-dlp

- **Rôle :** Télécharger des vidéos (ou l'audio) depuis YouTube et d'autres sites.
- **Pourquoi yt-dlp ?** YouTube ne propose pas de bouton "Télécharger". yt-dlp sait parler à YouTube pour récupérer le flux vidéo/audio.
- **En bref :** C'est une bibliothèque Python qui sait "décoder" YouTube et télécharger le contenu.

### 3.2 FFmpeg

- **Rôle :** Outil pour manipuler vidéo et audio : conversion de formats, extraction de la piste audio, etc.
- **Pourquoi FFmpeg ?** YouTube fournit souvent du WebM ou M4A. Le MP3 est un format plus universel (lecteurs, voitures, etc.). FFmpeg fait cette conversion.
- **C'est quoi exactement ?** Un programme en ligne de commande (ffmpeg.exe, ffprobe.exe) utilisé par des millions d'applications (OBS, VLC, etc.).
- **Où le trouve-t-on ?** Soit déjà installé sur ton PC (via winget), soit le projet le télécharge automatiquement dans un dossier `ffmpeg/` du projet.

---

## 4. Structure des fichiers du projet

```
mp3_py/
├── main.py           # Script principal : lance le téléchargement
├── ffmpeg_setup.py   # Détecte ou télécharge FFmpeg
├── requirements.txt  # Liste des bibliothèques Python à installer
├── README.md         # Instructions rapides
├── GUIDE_PROJET.md   # Ce guide
├── downloads/        # Dossier où sont enregistrés les MP3 (créé automatiquement)
└── ffmpeg/           # Dossier avec FFmpeg (créé si téléchargé automatiquement)
```

---

## 5. Explication fichier par fichier

### 5.1 `main.py` — Le script principal

**Rôle :** Point d'entrée. Demande l'URL YouTube, vérifie que FFmpeg est dispo, lance le téléchargement.

**Fonctions importantes :**

| Fonction | Rôle |
|----------|------|
| `get_ydl_opts()` | Configure yt-dlp : quel format télécharger (audio), comment convertir (MP3), où enregistrer. |
| `download()` | Appelle yt-dlp pour télécharger puis convertir. |
| `main()` | Récupère l'URL (clavier ou argument), vérifie FFmpeg, appelle `download()`. |

**Options yt-dlp utilisées :**

- `format: "bestaudio/best"` : prend la meilleure qualité audio disponible.
- `postprocessors` : après le téléchargement, on utilise FFmpeg pour extraire l'audio en MP3 (192 kbps).
- `outtmpl` : nom du fichier de sortie (ex. : `%(title)s.%(ext)s` = titre de la vidéo + extension).

---

### 5.2 `ffmpeg_setup.py` — Gestion de FFmpeg

**Rôle :** S'assurer qu'on a FFmpeg quelque part avant de lancer yt-dlp.

**Ordre de recherche :**

1. **FFmpeg local** : le dossier `ffmpeg/bin/` du projet contient déjà ffmpeg.exe et ffprobe.exe.
2. **FFmpeg système** : ffmpeg est installé sur le PC (par ex. via `winget install FFmpeg`) et accessible dans le PATH.
3. **Téléchargement auto** (Windows uniquement) : si rien n'est trouvé, le script télécharge FFmpeg depuis GitHub (yt-dlp/FFmpeg-Builds) et le met dans `ffmpeg/`.

**Fonctions importantes :**

| Fonction | Rôle |
|----------|------|
| `find_ffmpeg()` | Cherche FFmpeg dans le projet ou le PATH. |
| `has_system_ffmpeg()` | Indique si ffmpeg et ffprobe sont dans le PATH. |
| `download_ffmpeg()` | Télécharge le zip FFmpeg pour Windows 64 bits, l'extrait dans le projet. |
| `get_ffmpeg_location()` | Combine tout : trouve FFmpeg, ou le télécharge si nécessaire, et retourne le chemin à donner à yt-dlp. |

---

### 5.3 `requirements.txt`

Liste des bibliothèques Python à installer :

- **yt-dlp** : pour télécharger depuis YouTube.
- **requests** : pour le téléchargement HTTP (utilisé pour télécharger FFmpeg automatiquement).

Installation : `pip install -r requirements.txt`

---

## 6. Enchaînement technique (détaillé)

1. Tu lances `python main.py` et tu colles une URL YouTube.
2. `main.py` appelle `get_ffmpeg_location()` pour s'assurer qu'on a FFmpeg.
3. yt-dlp récupère les métadonnées de la vidéo (titre, formats disponibles).
4. yt-dlp télécharge le flux audio (souvent en WebM ou M4A).
5. yt-dlp appelle FFmpeg en arrière-plan pour convertir ce fichier en MP3.
6. Le fichier MP3 est enregistré dans `downloads/`.

---

## 7. Concepts utiles

### Formats audio / vidéo

- **WebM, M4A** : formats que YouTube envoie souvent pour l'audio.
- **MP3** : format très répandu, compatible partout.
- **Conversion** : FFmpeg lit le fichier source (ex. WebM) et le réécrit en MP3.

### Le PATH

- Le **PATH** est une variable système qui liste les dossiers où Windows cherche les programmes.
- Si `ffmpeg` est dans le PATH, on peut taper `ffmpeg` dans un terminal et ça fonctionne.
- Le projet peut soit utiliser FFmpeg du PATH, soit un FFmpeg local dans `ffmpeg/`.

### Postprocessors (yt-dlp)

- Un **postprocessor** s'exécute après le téléchargement.
- Ici, on utilise `FFmpegExtractAudio` : il prend le fichier téléchargé et en extrait la piste audio en MP3.

---

## 8. FAQ rapide

**Q : Pourquoi FFmpeg n'est pas dans requirements.txt ?**  
R : FFmpeg n'est pas une bibliothèque Python. C'est un programme externe (exe). On le télécharge en binaire ou on l'installe séparément.

**Q : D'où vient le MP3 si YouTube envoie du WebM ?**  
R : FFmpeg fait la conversion. Il décode le WebM, garde uniquement l'audio, et le réencode en MP3.

**Q : Le dossier ffmpeg/ est gros ?**  
R : Oui, environ 200 Mo. Il est ignoré par Git (.gitignore) car on peut le régénérer.

**Q : Ça marche sur Mac ou Linux ?**  
R : Oui. Sur Mac/Linux, il faut installer FFmpeg soi-même (brew, apt, etc.). Le téléchargement auto ne concerne que Windows.

---

## 9. Résumé en une phrase

> **yt-dlp** télécharge l’audio depuis YouTube, puis **FFmpeg** le convertit en MP3 et le sauvegarde dans `downloads/`.
