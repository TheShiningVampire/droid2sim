"""Create GitHub-friendly GIFs from the five existing videos; no new simulation."""

import json
import shutil
import subprocess

from droid2sim.paths import ROOT


def main():
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        import imageio_ffmpeg

        ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    output = ROOT / "docs/media"
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    for iteration in range(1, 6):
        source = ROOT / f"artifacts/iteration{iteration}/side_by_side.mp4"
        target = output / f"iteration-{iteration}.gif"
        filters = (
            "fps=10,scale=640:-1:flags=lanczos,split[a][b];"
            "[a]palettegen=max_colors=128:stats_mode=diff[p];"
            "[b][p]paletteuse=dither=bayer:bayer_scale=3"
        )
        subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                str(source),
                "-filter_complex",
                filters,
                "-loop",
                "0",
                str(target),
            ],
            check=True,
        )
        result = json.loads((source.parent / "success.json").read_text())
        manifest.append(
            {
                "iteration": iteration,
                "success": result["success"],
                "source": str(source.relative_to(ROOT)),
                "gif": str(target.relative_to(ROOT)),
                "bytes": target.stat().st_size,
                "fps": 10,
                "note": "Full recorded duration, real exterior1 | sim exterior1, no speed change",
            }
        )
        print(f"{target.relative_to(ROOT)}: {target.stat().st_size:,} bytes", flush=True)
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    main()
