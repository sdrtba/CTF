import socket
import re
from string import ascii_lowercase, ascii_uppercase
import enchant

eng_dict = enchant.Dict("en_US")

HOST = "127.0.0.1"
PORT = 31337


def recv_until(sock, terminator=b"> "):
    """
    Читает из сокета до появления терминатора (по умолчанию b'> ').
    Возвращает накопленный буфер.
    """
    buf = b""
    while terminator not in buf:
        chunk = sock.recv(1024)
        if not chunk:
            break
        buf += chunk
    return buf


def extract_challenge(msg: str) -> str:
    """
    Ищет в msg блок:
        Repeat this text:
        <payload>
    и возвращает payload без лишних пробелов.
    """
    m = re.search(r"Restore the text:\s*([^\r\n]+)", msg)
    return m.group(1).strip() if m else None


def is_meaningful(text: str, threshold: float = 0.4) -> bool:
    tokens = re.findall(r"[A-Za-z']+", text)
    if not tokens:
        return False

    known = sum(1 for tok in tokens if eng_dict.check(tok))
    ratio = known / len(tokens)

    return ratio >= threshold


def decode(msg: str) -> str:
    text = ""
    for i in range(1, 26):
        for c in msg:
            if c in ascii_lowercase:
                idx = (ascii_lowercase.index(c) - i) % 26
                text += ascii_lowercase[idx]
            elif c in ascii_uppercase:
                idx = (ascii_uppercase.index(c) - i) % 26
                text += ascii_uppercase[idx]
            else:
                text += c

        if is_meaningful(text):
            return text

        text = ""

    return text


def main():
    sock = socket.socket()
    sock.connect((HOST, PORT))

    while True:
        block = recv_until(sock).decode()
        print(block, end="")

        if "flag" in block:
            break

        chall = extract_challenge(block)
        if not chall:
            continue
        print(f"[challenge] {chall!r}")

        text = decode(chall)
        print(text)

        sock.sendall(text.encode() + b"\n")

    sock.close()


if __name__ == "__main__":
    main()
