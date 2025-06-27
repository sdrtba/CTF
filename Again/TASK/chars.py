from PIL import Image
import os


def make_background_transparent(
    paths: list[str], output_dir: str = None, white_threshold: int = 130
):
    """
    Для каждого PNG-файла из списка заменяет почти белый фон на прозрачный,
    оставляя чёрные символы нетронутыми.

    :param paths:           список путей к входным PNG (чёрные символы на белом фоне)
    :param output_dir:      папка для сохранённых результатов (по умолчанию — рядом с исходником)
    :param white_threshold: граница «бело-цвета» в 0–255 (по умолчанию 250)
    """
    for src in paths:
        if not src.lower().endswith(".png"):
            print(f"[!] Пропускаем не-PNG: {src}")
            continue

        # Открываем изображение и приводим к RGBA
        img = Image.open(src).convert("RGBA")
        pixels = img.getdata()

        new_data = []
        for r, g, b, a in pixels:
            # Если цвет близок к белому, делаем пиксель прозрачным
            if r >= white_threshold and g >= white_threshold and b >= white_threshold:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append((r, g, b, a))

        img.putdata(new_data)

        # Подготавливаем путь сохранения
        base, name = os.path.split(src)
        name_noext, _ = os.path.splitext(name)
        out_folder = output_dir or base
        os.makedirs(out_folder, exist_ok=True)
        dest = os.path.join(out_folder, f"{name_noext}.png")

        # Сохраняем результат
        img.save(dest, "PNG")
        print(f"[✔] Обработано: {src} → {dest}")


if __name__ == "__main__":
    frames = ["chars\\" + i for i in os.listdir("chars")]
    make_background_transparent(frames, "nc")
