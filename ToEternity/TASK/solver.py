import os
from PIL import Image
import subprocess

rar_path = r"C:\Program Files\WinRAR\Rar.exe"


def get_color(pixel):
    if pixel == (255, 0, 0):
        return "R"
    elif pixel == (0, 255, 0):
        return "G"
    elif pixel == (0, 0, 255):
        return "B"
    elif pixel == (255, 255, 255):
        return "W"
    elif pixel == (255, 165, 0):
        return "O"
    elif pixel == (128, 0, 128):
        return "P"


def get_psswd(image_path):
    image = Image.open(image_path)

    width, height = image.size

    s = ""
    for x in range(0, width - 1):
        pixel = image.getpixel((x, 10))
        next_pixel = image.getpixel((x + 1, 10))
        if pixel != next_pixel:
            s += get_color(pixel)
    s += get_color(pixel)
    print(s)

    return s


def get_rar_file():
    current_directory = os.getcwd()
    rar_files = [
        file for file in os.listdir(current_directory) if file.endswith(".rar")
    ]

    if rar_files:
        print("Найденные RAR-файлы:")
        for rar_file in rar_files:
            print(rar_file)
            return rar_file
    else:
        print("RAR-файлы не найдены.")


def get_img_file():
    current_directory = os.getcwd()
    png_files = [
        file for file in os.listdir(current_directory) if file.endswith(".png")
    ]

    if png_files:
        print("Найденные PNG-файлы:")
        for png_file in png_files:
            print(png_file)
            return png_file
    else:
        print("PNG-файлы не найдены.")


def extract(rar_file, psswd):
    command = [
        rar_path,  # путь к Rar.exe
        "x",  # extract
        rar_file,  # .rar-файл
        f"-p{psswd}",  # пароль
        "-y",  # авто-«да» на запросы
    ]

    print(" ".join(command))

    try:
        # Выполняем команду через subprocess
        result = subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        print("Разархивация завершена.")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка: {e.stderr}")
        return False


def main():
    rar_file = get_rar_file()
    img_file = get_img_file()
    psswd = get_psswd(img_file)

    success = extract(rar_file, psswd)

    if success:
        os.remove(rar_file)
        os.remove(img_file)


if __name__ == "__main__":
    while True:
        main()
