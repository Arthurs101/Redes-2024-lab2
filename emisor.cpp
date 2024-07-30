#include <iostream>
#include <string>
#include <vector>
#include <bitset>
#include <algorithm>
#include <cstring>
#include <netinet/in.h>
#include <sys/socket.h>
#include <unistd.h>
#include <random>

using namespace std;

struct Message {
    char hamming_code_l[8] = {0};
    char hamming_code_r[8] = {0};
    char crc32_code[37] = {0};
};

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

// Function to calculate Hamming (7,4) code
string hamming74(const string &data) {
    int n = data.length();
    vector<int> bits(n + 3);
    for (int i = 0; i < n; ++i) {
        bits[i] = data[i] - '0'; // char to int
    }
    
    // Parity calculation
    bits[6] = bits[0] ^ bits[2] ^ bits[4];
    bits[5] = bits[0] ^ bits[1] ^ bits[4];
    bits[3] = bits[0] ^ bits[1] ^ bits[2];

    string hamming_code = to_string(bits[0]) + to_string(bits[1]) + to_string(bits[2]) +
                          to_string(bits[3]) + to_string(bits[4]) + to_string(bits[5]) + to_string(bits[6]);
    return hamming_code;
}

// Function to encode a bit string using Hamming and CRC32
Message encode(const string &input) {
    // hamming left & right
    string leftP = input.substr(0, 4);  // fixed length 4
    string rightP = input.substr(4, 4); // fixed length 4
    string hamming_encoded_l = hamming74(leftP);
    string hamming_encoded_r = hamming74(rightP);
    // crc
    uint32_t crc = crc32(input);
    std::string crcBinaryString = uint32ToBinaryString(crc);
    std::string output = input + crcBinaryString;
    // print changes
    cout << "Hamming encoded left: " << hamming_encoded_l << endl << "Hamming encoded right: " << hamming_encoded_r << endl;
    cout << "CRC32 Checksum: " << output << endl;
    Message newM;
    // left hamming
    strncpy(newM.hamming_code_l, hamming_encoded_l.c_str(), sizeof(newM.hamming_code_l) - 1);
    newM.hamming_code_l[sizeof(newM.hamming_code_l) - 1] = '\0';
    // right hamming
    strncpy(newM.hamming_code_r, hamming_encoded_r.c_str(), sizeof(newM.hamming_code_r) - 1);
    newM.hamming_code_r[sizeof(newM.hamming_code_r) - 1] = '\0';
    // crc32
    strncpy(newM.crc32_code, output.c_str(), sizeof(newM.crc32_code) - 1);
    newM.crc32_code[sizeof(newM.crc32_code) - 1] = '\0';
    return newM;
}

Message applyNoise(Message mess){
    // Seed with a real random value, if available
    std::random_device rd;
    // Use the default_random_engine and the uniform_real_distribution
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<> dist(0.0, 1.0);
    // Generate a random number between 0 and 1
    double random_number = dist(eng);
    // Apply Noise Hamming
    int position;
    cout << random_number << endl;
    // Apply Noise CRC32 & Hamming
    if (random_number > 0.7) {
        // left hamming
        position = dist(eng) * (sizeof(mess.hamming_code_l) - 1);
        mess.hamming_code_l[position] = (mess.hamming_code_l[position] == '0' ? '1' : '0');
        cout << "Applied noise in hamming code left, position: " << position << endl;
        // right hamming
        position = dist(eng) * (sizeof(mess.hamming_code_r) - 1);
        mess.hamming_code_r[position] = (mess.hamming_code_r[position] == '0' ? '1' : '0');
        cout << "Applied noise in hamming code right, position: " << position << endl;
        // crc32
        position = dist(eng) * (sizeof(mess.crc32_code) - 1);
        mess.crc32_code[position] = (mess.crc32_code[position] == '0' ? '1' : '0');
        cout << "Applied noise in crc32 code, position: " << position << endl;
    }
    return mess;
}

// encode character
string charEncoding(char character){
    int asciiValue = (int)character;
    string binary = std::bitset<8>(asciiValue).to_string(); // to binary
    return binary;
}

int main() {
    // Application Layer
    char character;
    cout << "Enter a character: ";
    cin >> character;
    // Presentation Layer
    string bit_string = charEncoding(character);
    cout << "Encoded bit string: " << bit_string << endl;
    // Validate that the input is a bit string
    if (!all_of(bit_string.begin(), bit_string.end(), [](char c) { return c == '0' || c == '1'; })) {
        cerr << "Invalid input. Please enter a valid bit string." << endl;
        return 1;
    }
    // Connection Layer
    Message newM = encode(bit_string);
    
    // Noise layer
    Message finalMessage = applyNoise(newM);

    // creating socket 
    int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket < 0) {
        cerr << "Socket creation error" << endl;
        return 1;
    }

    // specifying address 
    sockaddr_in serverAddress; 
    serverAddress.sin_family = AF_INET; 
    serverAddress.sin_port = htons(65432); 
    serverAddress.sin_addr.s_addr = INADDR_ANY; 

    // sending connection request 
    if (connect(clientSocket, (struct sockaddr*)&serverAddress, sizeof(serverAddress)) < 0) {
        cerr << "Connection failed" << endl;
        return 1;
    }
    // sending data 
    // Transmission Layer
    if (send(clientSocket, &finalMessage, sizeof(finalMessage), 0) < 0) {
        perror("Send failed");
        return 1;
    }

    // closing socket 
    close(clientSocket); 
    return 0;
}
