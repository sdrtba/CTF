from PIL import Image


def decode(img_path: str):
    img = Image.open(img_path)
    img = img.crop((70, 70, 230, 230))
    img.show()

    for j in range(0, img.height, 10):
        text = ""
        for i in range(0, img.width, 10):
            color = img.getpixel((i + 3, j + 3))
            if color == (0, 0, 0):
                text += "1"
            else:
                text += "0"
        print(chr(int(text[:8], 2)), end="")
        print(chr(int(text[9:], 2)), end="")


if __name__ == "__main__":
    img = "qr.png"
    decode(img)
