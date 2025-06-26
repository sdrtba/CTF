import subprocess
import random
from pathlib import Path
import time
from PIL import Image
import sys

COLOR_MAP = {
    "R": (255, 0, 0),  # Red
    "G": (0, 255, 0),  # Green
    "B": (0, 0, 255),  # Blue
    "W": (255, 255, 255),  # White
    "O": (255, 165, 0),  # Orange
    "P": (128, 0, 128),  # Purple
}


def generate_password_and_image(out_dir: Path, layer: int) -> str | Path:
    """
    Генерирует пароль из символов RGBOYP и создаёт соответствующее изображение 180x30.
    :param length: Длина пароля (шагов).
    :param out_dir: Каталог для сохранения изображения.
    :param layer: Номер слоя для имени файла.
    :return: пароль и путь к созданному изображению.
    """
    chars = list(COLOR_MAP.keys())
    random.shuffle(chars)
    pwd = "".join(_ for _ in chars)
    img = Image.new("RGB", (6 * 30, 30))
    for idx, c in enumerate(pwd):
        x0 = idx * 30
        for x in range(x0, x0 + 30):
            for y in range(30):
                img.putpixel((x, y), COLOR_MAP[c])
    img_path = out_dir / f"layer_{layer}.png"
    img.save(img_path)
    return pwd, img_path


def nest_rar_archives_with_images(
    flag: str,
    layers: int,
    rar_path: Path,
):
    with open("flag.txt", "w") as f:
        f.write(flag)

    prev_archive = None
    prev_image = None
    out_dir = Path.cwd()

    for i in range(1, layers + 1):
        # Генерируем пароль и изображение для текущего слоя
        pwd, img_path = generate_password_and_image(out_dir, i)
        archive_name = out_dir / f"layer_{i}.rar"

        if i == 1:
            to_archive = ["flag.txt"]
            print(f"[Layer {1}] Архивация flag.txt")
        else:
            to_archive = [prev_archive, prev_image]
            print(
                f"[Layer {i}] Архивация {', '.join(p.name for p in to_archive)} → '{archive_name.name}', пароль: {pwd}"
            )

        cmd = [str(rar_path), "a", "-ep1", f"-hp{pwd}", str(archive_name)] + [
            str(p) for p in to_archive
        ]

        try:
            subprocess.run(cmd, capture_output=True, text=True, check=True)
        except FileNotFoundError:
            print("❌ Не удалось запустить Rar.exe. Проверьте путь.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"❌ Ошибка архивации на слое {i}:")
            print(e.stderr or e.stdout)
            sys.exit(1)

        # Удаляем предыдущие файлы, чтобы оставить только текущие
        if prev_archive and prev_archive.exists():
            prev_archive.unlink()
        if prev_image and prev_image.exists():
            prev_image.unlink()

        # Обновляем ссылки для следующего шага
        prev_archive = archive_name
        prev_image = img_path

    print(f"Финальный архив: {prev_archive}")

    # Создаём финальный архив Archive.rar без пароля
    final_archive = out_dir / "Archive.rar"
    cmd_final = [
        str(rar_path),
        "a",  # add
        "-ep1",  # без путей
        final_archive.name,
        prev_archive.name,
        prev_image.name,
    ]
    try:
        subprocess.run(
            cmd_final, cwd=out_dir, capture_output=True, text=True, check=True
        )
        print(f"Создан финальный архив без пароля: {final_archive}")
    except subprocess.CalledProcessError as e:
        print("❌ Ошибка при создании Archive.rar:")
        print(e.stderr or e.stdout)
        sys.exit(1)

    # Удаляем
    for file in [out_dir / i for i in ["flag.txt", prev_archive.name, prev_image.name]]:
        if file.exists():
            file.unlink()
            print(f"Удалён файл {file}")


if __name__ == "__main__":
    flag = r"flag{iNf1n1Ty_1$_N0T_THe_limi7}"
    rar_path = r"C:\Program Files\WinRAR\Rar.exe"
    layers = 500

    nest_rar_archives_with_images(flag, layers, rar_path)
