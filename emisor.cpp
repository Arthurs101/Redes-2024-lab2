// codigo en C++ para el emisor
// Arturo Argueta
// Diego Alonzo
//emplea el uso de bit de paridad

#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <algorithm>

using namespace std;

// Función para calcular el CRC32 Checksum
uint32_t crc32(const string &data) {
    uint32_t crc = 0xFFFFFFFF;
    for (char c : data) {
        crc ^= static_cast<uint32_t>(c);
        for (int i = 0; i < 8; ++i) {
            if (crc & 1) {
                crc = (crc >> 1) ^ 0xEDB88320;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFF;
}

// Función para calcular el código Hamming (7,4)
string hamming74(const string &data) {
    int n = data.length();
    vector<int> bits(n);
    for (int i = 0; i < n; ++i) {
        bits[i] = data[i] - '0';
    }

    int r1 = bits[0] ^ bits[1] ^ bits[3];
    int r2 = bits[0] ^ bits[2] ^ bits[3];
    int r3 = bits[1] ^ bits[2] ^ bits[3];

    string hamming_code = data + to_string(r1) + to_string(r2) + to_string(r3);
    return hamming_code;
}

// Función para codificar una cadena de bits usando el código Hamming y CRC32 Checksum
void encode(const string &input) {
    string hamming_encoded = hamming74(input);
    uint32_t crc = crc32(input);

    cout << "Hamming encoded: " << hamming_encoded << endl;
    cout << "CRC32 Checksum: " << bitset<32>(crc) << endl;
}

int main() {
    string bit_string;
    cout << "Enter a bit string: ";
    cin >> bit_string;

    // Validar que la entrada sea una cadena de bits
    if (!all_of(bit_string.begin(), bit_string.end(), [](char c) { return c == '0' || c == '1'; })) {
        cerr << "Invalid input. Please enter a valid bit string." << endl;
        return 1;
    }

    // Validar que la longitud de la entrada sea válida para Hamming (7,4)
    if (bit_string.length() != 4) {
        cerr << "Invalid input length for Hamming (7,4). Please enter a 4-bit string." << endl;
        return 1;
    }

    encode(bit_string);

    return 0;
}
