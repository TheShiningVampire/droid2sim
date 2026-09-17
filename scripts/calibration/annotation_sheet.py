from droid2sim.paths import ROOT as REPO_ROOT
import os

os.chdir(REPO_ROOT)
import numpy as np
from PIL import Image, ImageDraw

for name in ["ext1", "ext2"]:
    a = np.load("data/episode/" + name + ".npy")
    out = Image.new("RGB", (1280, 5 * 400), "white")
    for j, t in enumerate([0, 30, 60, 90, 110, 120, 130, 150, 160, 180]):
        im = Image.fromarray(a[t]).resize((640, 360))
        d = ImageDraw.Draw(im)
        for x in range(0, 320, 20):
            d.line((x * 2, 0, x * 2, 359), fill=(100, 100, 100), width=1)
            d.text((x * 2, 0), str(x), fill="red")
        for y in range(20, 180, 20):
            d.line((0, y * 2, 639, y * 2), fill=(100, 100, 100), width=1)
            d.text((0, y * 2), str(y), fill="red")
        x = (j % 2) * 640
        y = (j // 2) * 400
        out.paste(im, (x, y + 30))
        ImageDraw.Draw(out).text((x + 5, y + 5), f"{name} frame {t}", fill="black")
    out.save("artifacts/annotate_" + name + ".jpg")
