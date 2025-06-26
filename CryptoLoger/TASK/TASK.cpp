#include <iostream>
#include <string>
#include <vector>
#include <cstdint>

static constexpr uint8_t XOR_KEY = 0x5A;

static constexpr uint8_t enc_flag[] = { 0x3C, 0x36, 0x3B, 0x3D, 0x21, 0x23, 0x6A, 0x2F, 0x05,
0x6E, 0x28, 0x69, 0x05, 0x3C, 0x6B, 0x28, 0x69, 0x3E, 0x27 };
static constexpr uint8_t enc_c1[] = { 0x6a, 0x62, 0x60, 0x6e, 0x6c };
static constexpr uint8_t enc_c2[] = { 0x6b, 0x6b, 0x75, 0x6a, 0x63, 0x75, 0x68, 0x6a, 0x6a, 0x6b };
static constexpr uint8_t enc_c3[] = { 0x10, 0x35, 0x32, 0x34, 0x1e, 0x35, 0x3f };
static constexpr uint8_t enc_c4[] = {
    0x08, 0x3f, 0x38, 0x35, 0x35, 0x2e, 0x7a, 0x33, 0x29,
    0x7a, 0x37, 0x23, 0x7a, 0x2e, 0x35, 0x35, 0x36
};

std::string decrypt(const uint8_t* data, size_t len) {
    std::string out;
    out.reserve(len);
    for (size_t i = 0; i < len; ++i) {
        out.push_back(char(data[i] ^ XOR_KEY));
    }
    return out;
}

int main() {
    const std::string flag = decrypt(enc_flag, sizeof(enc_flag));
    const std::string c1 = decrypt(enc_c1, sizeof(enc_c1));
    const std::string c2 = decrypt(enc_c2, sizeof(enc_c2));
    const std::string c3 = decrypt(enc_c3, sizeof(enc_c3));
    const std::string c4 = decrypt(enc_c4, sizeof(enc_c4));

    std::string s1, s2, s3, s4;
    std::cout << "Time (HH:MM): ";
    std::getline(std::cin, s1);
    std::cout << "Date (dd/mm/YYYY): ";
    std::getline(std::cin, s2);
    std::cout << "Hostname: ";
    std::getline(std::cin, s3);
    std::cout << "Note: ";
    std::getline(std::cin, s4);

    if (s1 == c1 && s2 == c2 && s3 == c3 && s4 == c4) {
        std::cout << flag;
    }
    else {
        std::cout << "WRONG\n";
    }

    return 0;
}
