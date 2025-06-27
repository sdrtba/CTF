from PIL import Image
from apng import APNG
import os
import sys
import shutil


def clear(objects: list[str]):
    for obj in objects:
        if os.path.exists(obj):
            os.remove(obj)
            print(f"[✔] Удалён: {obj}")
        else:
            print(f"[!] Не найден для удаления: {obj}")


def make_apng(frames: list[str], output_path: str, delay: int = 100):
    apng = APNG()
    for f in frames:
        apng.append_file(f, delay=delay)
    apng.save(output_path)
    print(f"[✔] APNG собран: {output_path}")


def embed(frames: list[str], output_dir: str, chars_dir: str, flag: str):
    new_frames = []
    for i in range(len(flag)):
        new_frame = embed_bit_plane(frames[i], f"{chars_dir}/{flag[i]}.png", output_dir)
        new_frames.append(new_frame)

    return new_frames


def embed_bit_plane(container_path: str, secret_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # Загружаем и приводим к RGBA
    cont = Image.open(container_path).convert("RGBA")
    sec = Image.open(secret_path).convert("RGBA")

    w_cont, h_cont = cont.size
    w_sec, h_sec = sec.size

    if w_sec > w_cont or h_sec > h_cont:
        sys.exit("Ошибка: секретное изображение превышает размер контейнера.")

    cont_px = cont.load()
    sec_px = sec.load()

    # Встраиваем побитово: берём старший бит (bit7) каждого синего канала секрета
    # и записываем его в младший бит (bit0) синего канала контейнера.
    for y in range(h_sec):
        for x in range(w_sec):
            r_c, g_c, b_c, a_c = cont_px[x, y]
            _, _, b_s, a_s = sec_px[x, y]

            # if a_s == 0:
            #    a_s = 255

            # выделяем бит 7 из секрета (0 или 1)
            secret_bit = (a_s & 0x80) >> 7

            # сбрасываем младший бит контейнера и ставим туда secret_bit
            a_new = (a_c & ~1) | secret_bit

            cont_px[x, y] = (r_c, g_c, b_c, a_new)

    output = os.path.join(output_dir, container_path.replace("frames\\", ""))
    cont.save(output, "PNG")
    print(f"[✔] Секрет спрятан в bit-plane 0 синего канала:\n    {output}")

    return output


def resize(paths: list[str], size: tuple[int] = (128, 128), output_dir: str = None):
    for src in paths:
        # Проверяем расширение
        if not src.lower().endswith(".png"):
            print(f"[!] Пропускаем не-PNG: {src}")
            continue

        # Открываем
        img = Image.open(src).convert("RGBA")
        # Принудительный ресайз
        img_resized = img.resize(size, Image.LANCZOS)

        # Формируем путь вывода
        base, name = os.path.split(src)
        name_noext, _ = os.path.splitext(name)
        out_folder = output_dir or base
        os.makedirs(out_folder, exist_ok=True)
        dest = os.path.join(out_folder, f"{name_noext}.png")

        # Сохраняем
        img_resized.save(dest, "PNG")
        print(f"[✔] {src} → {dest}")


def extract_frames(gif_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    frames = []
    with Image.open(gif_path) as img:
        frame = 0
        try:
            while True:
                frame_path = os.path.join(output_dir, f"frame_{frame:03d}.png")
                frames.append(frame_path)
                img.convert("RGBA").save(frame_path)
                print(f"[+] Сохранён кадр {frame} → {frame_path}")
                frame += 1
                img.seek(frame)  # переходим к следующему кадру
        except EOFError:
            print(f"[✔] Извлечено {frame} кадра(ов).")

    return frames


if __name__ == "__main__":
    gif_file = "input.gif"
    flag = "flag{Z0d1ac_$3nds_gr33t1ng$}"
    frames_dir = "frames"
    new_frames_dir = "new_frames"
    chars_dir = "chars"

    frames = extract_frames(gif_file, frames_dir)
    resize(frames)
    new_frames = embed(frames, new_frames_dir, chars_dir, flag)
    make_apng(new_frames, "output.gif")

    # test
    extract_frames("output.gif", "test")

    # clear
    for dir in [frames_dir, new_frames_dir, "test"]:
        shutil.rmtree(dir)
