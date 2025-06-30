import random
from PIL import Image

size = 10
black = Image.new("RGB", (size, size), (0, 0, 0))


def paste_block(img: Image.Image, block: Image.Image, x: int, y: int):
    pattern = [
        "1111111",
        "1000001",
        "1011101",
        "1011101",
        "1011101",
        "1000001",
        "1111111",
    ]
    for i in range(7):
        for j in range(7):
            if pattern[i][j] == "1":
                img.paste(
                    block,
                    (
                        x + j * size,
                        y + i * size,
                        x + (j + 1) * size,
                        y + (i + 1) * size,
                    ),
                )


def paste_random(
    img: Image.Image, block: Image.Image, x: int, y: int, width: int, height: int
):
    for i in range(width // size):
        for j in range(height // size):
            if random.randint(0, 1):
                img.paste(
                    block,
                    (
                        x + i * size,
                        y + j * size,
                        x + (i + 1) * size,
                        y + (j + 1) * size,
                    ),
                )


def build(flag: str):
    bins = [bin(ord(i)).replace("0b", "").zfill(8) for i in flag]

    bins_len = len(bins)
    width = size * bins_len // 2
    height = size * bins_len // 2

    img = Image.new("RGB", (width, height), (255, 255, 255))

    index = 0
    for i in bins:
        for j in range(8):
            if i[j] == "1":
                x = index * size % width
                y = index * size // width * size
                img.paste(black, (x, y, x + size, y + size))
            index += 1

    b_size = 7 * size
    qr = Image.new("RGB", (width + b_size * 2, height + b_size * 2), (255, 255, 255))
    qr.paste(img, (b_size, b_size))

    paste_block(qr, black, 0, 0)
    paste_block(qr, black, width + b_size, 0)
    paste_block(qr, black, 0, height + b_size)

    paste_random(qr, black, 0, b_size + size, b_size - size, b_size * 2)
    paste_random(qr, black, b_size + size, 0, b_size * 2, b_size - size)
    paste_random(
        qr, black, b_size + width + size, b_size + size, b_size - size, b_size * 2 + 10
    )
    paste_random(
        qr,
        black,
        b_size + size,
        b_size + width + size,
        b_size + width - size,
        b_size - size,
    )

    qr.save("image.png")


if __name__ == "__main__":
    flag = "flag{3v3Ry7h1nG_1s_mUch_$1mPl3r}"

    build(flag)
