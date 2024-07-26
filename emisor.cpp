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

uint32_t crc32(const std::string& data) {
    const uint32_t POLY = 0x04C11DB7; // CRC32 polynomial
    uint32_t crc = 0xFFFFFFFF;
    for (char bit : data) {
        crc ^= (bit == '1' ? 1 : 0) << 31;
        for (int i = 0; i < 8; ++i) {
            if (crc & 0x80000000) {
                crc = (crc << 1) ^ POLY;
            } else {
                crc <<= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFF;
}

std::string uint32ToBinaryString(uint32_t value) {
    std::string result;
    for (int i = 31; i >= 0; --i) {
        result += (value & (1 << i)) ? '1' : '0';
    }
    return result;
}


// Función para calcular el código Hamming (7,4)
string hamming74(const string &data) {
    int n = data.length();
    vector<int> bits(n+3);
    for (int i = 0; i < n; ++i) {
        bits[i] = data[i] - '0'; // char a entero
    }
    
    // Parity calculation
    bits[6]=bits[0]^bits[2]^bits[4];
    bits[5]=bits[0]^bits[1]^bits[4];
    bits[3]=bits[0]^bits[1]^bits[2];

    string hamming_code = to_string(bits[0]) + to_string(bits[1]) + to_string(bits[2]) +
                      to_string(bits[3]) + to_string(bits[4]) + to_string(bits[5]) + to_string(bits[6]);
    return hamming_code;
}

// Función para codificar una cadena de bits usando el código Hamming y CRC32 Checksum
void encode(const string &input) {
    string hamming_encoded = hamming74(input);
    uint32_t crc = crc32(input);
    std::string crcBinaryString = uint32ToBinaryString(crc);
    std::string output = input + crcBinaryString;
    cout << "Hamming encoded: " << hamming_encoded << endl;
    cout << "CRC32 Checksum: " << output << endl;
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
