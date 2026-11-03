import sys
from pathlib import Path
from PIL import Image

if len(sys.argv) != 2:
    raise SystemExit(1)

root = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1])
dst = root / "averaged.jpeg"
square = 16


def weight(offset, block_size):
    from_near = offset
    from_far = block_size - 1 - offset
    if from_far < from_near:
        from_near = from_far
    return from_near + 1


image = Image.open(src).convert("RGB")
width, height = image.size
print(width, height)
pixels = image.load()

for y0 in range(0, height, square):
    y1 = min(y0 + square, height)
    block_h = y1 - y0
    for x0 in range(0, width, square):
        x1 = min(x0 + square, width)
        block_w = x1 - x0

        sum_r = 0
        sum_g = 0
        sum_b = 0
        sum_w = 0
        for j in range(block_h):
            weight_y = weight(j, block_h)
            for i in range(block_w):
                w = weight(i, block_w) * weight_y
                r, g, b = pixels[x0 + i, y0 + j]
                sum_r += r * w
                sum_g += g * w
                sum_b += b * w
                sum_w += w

        color = (
            (sum_r + sum_w // 2) // sum_w,
            (sum_g + sum_w // 2) // sum_w,
            (sum_b + sum_w // 2) // sum_w,
        )
        for j in range(block_h):
            for i in range(block_w):
                pixels[x0 + i, y0 + j] = color

image.save(dst, "JPEG", quality=95)
print(f"wrote {dst.name} ({width}x{height}, square {square})")
