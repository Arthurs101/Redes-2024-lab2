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
        crc ^= static_cast<uint32_t>(c); // char a bits ( 8 bits)
        for (int i = 0; i < 8; ++i) { //operar sobre los 8 bits que representan el caracter
            if (crc & 1) { 
                /*  Si el bit menos significativo (crc & 1) es 1, 
               se desplaza crc un bit a la derecha (crc >> 1) 
               y se aplica XOR con el polinomio 0xEDB88320. */ 
                crc = (crc >> 1) ^ 0xEDB88320; 
            } else {
                /* de lo contrario, solo moverlo 1 a la derecha*/
                crc >>= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFF; // xor con -1 en hexadecimal, para invertir los bits
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

    cout << "Hamming encoded: " << hamming_encoded << endl;
    cout << "CRC32 Checksum: " << input<<bitset<32>(crc) << endl;
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
