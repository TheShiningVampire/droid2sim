"""Compare existing real/sim frames without rerunning physics."""

import argparse

import imageio.v2 as imageio
import numpy as np
from PIL import Image, ImageDraw

from droid2sim.paths import EPISODE, resolve_output


def compare(out="artifacts/final"):
    output = resolve_output(out)
    real = np.load(EPISODE / "ext1.npy")
    sim = np.load(output / "sim_ext1.npy")
    if real.shape != sim.shape:
        raise ValueError("Real and sim frames must have identical shapes")
    with imageio.get_writer(output / "side_by_side.mp4", fps=15, macro_block_size=1) as writer:
        for index, (real_frame, sim_frame) in enumerate(zip(real, sim)):
            image = Image.fromarray(np.concatenate([real_frame, sim_frame], axis=1))
            draw = ImageDraw.Draw(image)
            draw.text((4, 4), f"REAL {index / 15:.2f}s", fill="red")
            draw.text((324, 4), "SIM", fill="red")
            writer.append_data(np.array(image))

    for camera in ("ext1", "ext2"):
        real_frames = np.load(EPISODE / f"{camera}.npy")
        sim_frames = np.load(output / f"sim_{camera}.npy")
        for label, frame in (
            ("start", 0),
            ("mid", len(real_frames) // 2),
            ("end", len(real_frames) - 1),
        ):
            overlay = Image.blend(
                Image.fromarray(real_frames[frame]), Image.fromarray(sim_frames[frame]), 0.5
            )
            overlay.save(output / f"overlay_{camera}_{label}.png")

    indices = [0, 60, 90, 110, 120, 130, 150, 160, 180]
    sheet = Image.new("RGB", (320 * len(indices), 180 * 3 + 25), "white")
    for column, frame in enumerate(indices):
        overlay = ((real[frame].astype(float) + sim[frame]) / 2).astype("uint8")
        for row, image in enumerate((real[frame], sim[frame], overlay)):
            sheet.paste(Image.fromarray(image), (column * 320, 25 + row * 180))
        ImageDraw.Draw(sheet).text(
            (column * 320 + 3, 3), f"{frame}: real / sim / overlay", fill="black"
        )
    sheet.save(output / "review.jpg")
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="artifacts/final")
    compare(parser.parse_args(argv).out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
