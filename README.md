# Speech to Text (Whisper) — Setup & Run (Windows)

This project performs **speech-to-text** using **OpenAI Whisper** (Python).

## Prerequisites

- Windows
- Python **3.10+** (3.10 recommended)

> Note: Whisper requires `ffmpeg` to decode audio/video.
> This repo uses `imageio-ffmpeg` so you **don't need to install ffmpeg manually**.

## 1) Create a virtual environment

Run these commands from the project folder `E:/Back End/phyton`.

### PowerShell

```powershell
cd "E:/Back End/phyton"
py -3.10 -m venv .venv
```

### Git Bash

```bash
cd "/e/Back End/phyton"
python -m venv .venv
```

## 2) Install required libraries

Use the venv's Python so packages are installed into the correct environment.

### PowerShell

```powershell
cd "E:/Back End/phyton"
& .\.venv\Scripts\python.exe -m pip install -U pip
& .\.venv\Scripts\python.exe -m pip install -U openai-whisper imageio-ffmpeg
```

### Git Bash

```bash
cd "/e/Back End/phyton"
./.venv/Scripts/python.exe -m pip install -U pip
./.venv/Scripts/python.exe -m pip install -U openai-whisper imageio-ffmpeg
```

## 3) Run the program

Main file: `speech_to_text.py`

### PowerShell

```powershell
cd "E:/Back End/phyton"
& .\.venv\Scripts\python.exe speech_to_text.py
```

### Git Bash

```bash
cd "/e/Back End/phyton"
./.venv/Scripts/python.exe speech_to_text.py
```

The output will print the transcription text.

## Text output (.txt)

Each run saves the transcription as:

- `result/<audio-name>.txt`

Example: if the input is `part A.mpeg`, the output will be `result/part A.txt`.

## Run with a different audio file

You can pass an audio path as an argument.

### PowerShell

```powershell
& .\.venv\Scripts\python.exe speech_to_text.py "path\\to\\audio.mp3"
```

### Git Bash

```bash
./.venv/Scripts/python.exe speech_to_text.py "path/to/audio.mp3"
```

## Audio input

By default, the script reads:

- `part A.mpeg`

To change it, update `audio_path` in `speech_to_text.py` (or pass a file path argument).

## Troubleshooting

### 1) `ModuleNotFoundError: No module named 'whisper'`

This usually happens when you're running a Python interpreter **outside** `.venv`.
Make sure you run with:

- PowerShell: `& .\.venv\Scripts\python.exe speech_to_text.py`
- Git Bash: `./.venv/Scripts/python.exe speech_to_text.py`

### 2) Installing the wrong `whisper` package

The import name is `whisper`, but the correct package is:

- `openai-whisper`

If you accidentally installed another `whisper` package, remove it and install the right one:

```bash
./.venv/Scripts/python.exe -m pip uninstall -y whisper
./.venv/Scripts/python.exe -m pip install -U openai-whisper
```

### 3) `ffmpeg` / `WinError 2` errors

Whisper needs `ffmpeg`.
If you installed `imageio-ffmpeg` and are using the latest script in this repo, `ffmpeg` should be handled automatically.

If it still fails, verify you're running with the venv Python (see the Run section above).
