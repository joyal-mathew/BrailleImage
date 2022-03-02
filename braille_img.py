from PIL import Image
from argparse import ArgumentParser

braille_W = 2
braille_H = 4
PXLS_MASK = [ 1, 8, 2, 16, 4, 32, 64, 128 ]


def braille_pxls_convert(pxls):
    return chr(0x2800 + sum(a * b for a, b in zip(pxls, PXLS_MASK)))


def braille_img_convert(img, scale=1, invert=False):
    w, h = img.size
    w = int(w * scale) // braille_W * braille_W
    h = int(h * scale) // braille_H * braille_H

    img = img.resize((w, h)).convert(mode="1")

    out = ""
    delim = ""

    for y in range(0, h, braille_H):
        out += delim
        delim = "\n"
        for x in range(0, w, braille_W):
            pxls = []

            for dy in range(0, braille_H):
                for dx in range(0, braille_W):
                    pxls.append((img.getpixel((x + dx, y + dy)) and 1) ^ invert)

            out += braille_pxls_convert(pxls)

    return out


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("input_path", type=str, help="Path to the input image")
    parser.add_argument("output_path", type=str, help="Path to output the text to")
    parser.add_argument("--scale", type=float, default=1, help="Scaling of the output (1 pixel is 1 braille dot)")
    parser.add_argument("--invert", action="store_true", default=False, help="If passed, braille dots are treated as black pixels instead of white")

    args = parser.parse_args()

    with open(args.output_path, "w", encoding="utf-8") as f:
        f.write(braille_img_convert(
            Image.open(args.input_path),
            scale=args.scale,
            invert=args.invert,
        ))
