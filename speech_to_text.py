import os
import shutil
import sys
import time
from pathlib import Path

import whisper


PAUSE_SECONDS = 1.0  # insert a blank line if silence between segments >= this threshold


def _format_text_with_pauses(segments: list[dict], pause_seconds: float = PAUSE_SECONDS) -> str:
	lines: list[str] = []
	current_parts: list[str] = []
	prev_end: float | None = None

	for seg in segments:
		start = float(seg.get("start", 0.0))
		end = float(seg.get("end", 0.0))
		seg_text = str(seg.get("text", "")).strip()
		if not seg_text:
			prev_end = end
			continue

		if prev_end is not None and (start - prev_end) >= pause_seconds:
			if current_parts:
				lines.append(" ".join(current_parts).strip())
				current_parts = []
			lines.append("")  # blank line for long pause

		current_parts.append(seg_text)
		prev_end = end

	if current_parts:
		lines.append(" ".join(current_parts).strip())

	# Normalize consecutive blank lines
	out_lines: list[str] = []
	prev_blank = False
	for line in lines:
		blank = (line.strip() == "")
		if blank and prev_blank:
			continue
		out_lines.append(line)
		prev_blank = blank

	return "\n".join(out_lines).strip() + "\n"


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

	segments = result.get("segments") or []
	if segments:
		text = _format_text_with_pauses(segments)
	else:
		text = (result.get("text") or "").strip() + "\n"

	print(text.rstrip())

	output_dir = Path("result")
	output_dir.mkdir(parents=True, exist_ok=True)
	output_path = output_dir / f"{audio_path.stem}.txt"
	output_path.write_text(text, encoding="utf-8")
	print(f"\n[OK] Saved: {output_path.resolve()}", flush=True)


if __name__ == "__main__":
	main()