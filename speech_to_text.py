import os
import shutil
from pathlib import Path

import whisper


def _ensure_ffmpeg_in_path() -> None:
	if shutil.which("ffmpeg"):
		return

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


def main() -> None:
	_ensure_ffmpeg_in_path()

	audio_path = Path("part A.mpeg")
	if not audio_path.exists():
		raise FileNotFoundError(f"File audio tidak ditemukan: {audio_path.resolve()}")

	model = whisper.load_model("base")
	result = model.transcribe(str(audio_path), fp16=False)

	print(result["text"].strip())


if __name__ == "__main__":
	main()