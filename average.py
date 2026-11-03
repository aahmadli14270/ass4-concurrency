import sys
from pathlib import Path
from PIL import Image


def weight(offset, block_size):
    from_near = offset
    from_far = block_size - 1 - offset
    if from_far < from_near:
        from_near = from_far
    return from_near + 1


def main():
    if len(sys.argv) != 4:
        raise SystemExit(1)

    src = Path(sys.argv[1])
    mode = sys.argv[3]
    try:
        square = int(sys.argv[2])
    except ValueError:
        print("square size must be a positive integer")
        raise SystemExit(1)
    if square < 1:
        print("square size must be a positive integer")
        raise SystemExit(1)
    if mode not in ("S", "M"):
        print("processing mode must be S or M")
        raise SystemExit(1)
    if mode == "M":
        print("multi-threaded mode is not implemented yet")
        raise SystemExit(1)
    if src.suffix.lower() not in (".jpg", ".jpeg"):
        print("file must be a jpg")
        raise SystemExit(1)

    image = Image.open(src).convert("RGB")
    width, height = image.size
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

    dst = Path(__file__).resolve().parent / "averaged.jpeg"
    image.save(dst, "JPEG", quality=95)
    print(f"wrote {dst.name} ({width}x{height}, square {square}, mode {mode})")


if __name__ == "__main__":
    main()
