import os
import shutil
import sys
import time
from pathlib import Path

import whisper


def _ensure_ffmpeg_in_path() -> None:
	if shutil.which("ffmpeg"):
		print("[OK] ffmpeg found in PATH", flush=True)
		return

	print("[..] ffmpeg not found, using imageio-ffmpeg...", flush=True)

	try:
		import imageio_ffmpeg

		ffmpeg_exe = Path(imageio_ffmpeg.get_ffmpeg_exe())
	except Exception as exc:  # pragma: no cover
		raise RuntimeError(
			"ffmpeg tidak ditemukan. Install ffmpeg (dan pastikan ada di PATH), "
			"atau jalankan: pip install imageio-ffmpeg"
		) from exc

	# imageio-ffmpeg menyimpan binary dengan nama versi (bukan ffmpeg.exe).
	# Whisper memanggil executable bernama "ffmpeg", jadi kita buat alias ffmpeg.exe.
	if ffmpeg_exe.name.lower() != "ffmpeg.exe":
		ffmpeg_alias = ffmpeg_exe.with_name("ffmpeg.exe")
		if not ffmpeg_alias.exists():
			shutil.copyfile(ffmpeg_exe, ffmpeg_alias)
		ffmpeg_exe = ffmpeg_alias

	os.environ["PATH"] = str(ffmpeg_exe.parent) + os.pathsep + os.environ.get("PATH", "")
	print(f"[OK] ffmpeg available at: {ffmpeg_exe}", flush=True)


def main() -> None:
	print("[..] Starting speech_to_text", flush=True)
	print(f"[..] Python: {sys.executable}", flush=True)
	_ensure_ffmpeg_in_path()

	audio_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("audio/part A.mpeg")
	if not audio_path.exists():
		raise FileNotFoundError(f"File audio tidak ditemukan: {audio_path.resolve()}")
	print(f"[..] Input audio: {audio_path}", flush=True)

	start = time.perf_counter()
	print("[..] Loading model: base", flush=True)
	model = whisper.load_model("base")
	print(f"[OK] Model loaded in {time.perf_counter() - start:.1f}s", flush=True)

	start = time.perf_counter()
	print("[..] Transcribing (this may take a while)...", flush=True)
	result = model.transcribe(str(audio_path), fp16=False)
	print(f"[OK] Transcription finished in {time.perf_counter() - start:.1f}s", flush=True)

	text = result["text"].strip()
	print(text)

	output_dir = Path("result")
	output_dir.mkdir(parents=True, exist_ok=True)
	output_path = output_dir / f"{audio_path.stem}.txt"
	output_path.write_text(text + "\n", encoding="utf-8")
	print(f"\n[OK] Saved: {output_path.resolve()}", flush=True)


if __name__ == "__main__":
	main()