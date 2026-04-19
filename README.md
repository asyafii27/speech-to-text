# Speech to Text (Whisper) – Setup & Run (Windows)

Project ini menjalankan **speech-to-text** menggunakan **OpenAI Whisper** (Python).

## Prasyarat

- Windows
- Python **3.10+** (disarankan 3.10)

> Catatan: Whisper membutuhkan `ffmpeg` untuk membaca audio/video.
> README ini memakai `imageio-ffmpeg` agar **tidak perlu install ffmpeg manual**.

## 1) Buat virtual environment

Jalankan dari folder project `E:/Back End/phyton`.

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

## 2) Install library yang dibutuhkan

Pakai Python dari venv agar paket terpasang ke environment yang benar.

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

## 3) Jalankan program

File utama: `speech_to_text.py`

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

Output akan menampilkan teks hasil transkripsi.

## Input audio

Secara default, script membaca file:

- `part A.mpeg`

Jika ingin ganti file, ubah nilai `audio_path` di `speech_to_text.py`.

## Troubleshooting

### 1) Error `ModuleNotFoundError: No module named 'whisper'`

Biasanya karena Anda menjalankan Python yang **bukan** dari `.venv`.
Pastikan run memakai:

- PowerShell: `& .\.venv\Scripts\python.exe speech_to_text.py`
- Git Bash: `./.venv/Scripts/python.exe speech_to_text.py`

### 2) Salah install paket `whisper`

Nama import-nya memang `whisper`, tapi paket yang benar adalah:

- `openai-whisper`

Jika terlanjur menginstall paket `whisper` lain, hapus lalu install yang benar:

```bash
./.venv/Scripts/python.exe -m pip uninstall -y whisper
./.venv/Scripts/python.exe -m pip install -U openai-whisper
```

### 3) Error terkait `ffmpeg` / `WinError 2`

Whisper perlu `ffmpeg`.
Kalau Anda sudah install `imageio-ffmpeg` dan memakai script versi terbaru di repo ini, seharusnya `ffmpeg` otomatis bisa dipakai.

Jika masih error, pastikan perintah run memakai python dari venv (lihat langkah Run di atas).
