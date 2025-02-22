import socket
import struct
import math

incorrectBuffers = 0

def hammingEncoding(message):
    mesLen = len(message)
    newM = []
    xorOp = []
    counter = mesLen-1
    index = 1
    while (index<1000):
        # Parity bit
        if math.log2(index).is_integer():
            newM.append(None)
        else:       
            newM.append(message[counter])
            if int(message[counter]) == 1:
                xorOp.append(bin(len(newM))[2:])
            counter-=1
        if counter==-1:
            break
        index+=1
    resXOR = []
    biggestVal = xorOp[len(xorOp)-1]
    for index in range(0,len(xorOp)):
        dif = (len(biggestVal)-len(xorOp[index]))
        if dif!=0:
            xorOp[index]='0'*dif+xorOp[index]
    for index in range(0,len(biggestVal)):
        value = 0
        for val in xorOp:
            value+=int(val[index])
        # Si es par va a ser 0 si es impar sera 1
        resXOR.append(value%2)
    # print(newM)
    # print(resXOR)
    counter = len(resXOR)-1
    for index in range(1, len(newM)):
        if math.log2(index).is_integer():
            newM[index-1] = str(resXOR[counter])
            counter-=1
    return ''.join(newM)[::-1]

def hammingDecoding(message):
    resXOR = []
    xorOp = []
    biggestNum = bin(len(message))[2:]
    for index in range(len(message)-1,-1,-1):
        if message[index] == '1':
            value = bin(len(message)-index)[2:]
            value = '0'*(len(biggestNum)-len(value))+value
            xorOp.append(value)
    for index in range(0,len(biggestNum)):
        value = 0
        for val in xorOp:
            value+=int(val[index])
        # Si es par va a ser 0 si es impar sera 1
        resXOR.append(str(value%2))
    j = int(''.join(resXOR),2)
    success = False
    if j!=0:
        print(f'There is an error in the position {len(message)-j}')
        message = list(message)
        message[len(message)-j] = str((int(message[len(message)-j])+1)%2)
        message = "".join(message)
        print(f'Corrected message is: {message}')
    else:
        print("There is no error in message")
        success = True
    return [message, success]

def crc32(data): 
    POLY = 0x04C11DB7
    crc = 0xFFFFFFFF
    for bit in data:
        crc ^= (1 if bit == '1' else 0) << 31
        for _ in range(8):
            if crc & 0x80000000:
                crc = (crc << 1) ^ POLY
            else:
                crc <<= 1
            crc &= 0xFFFFFFFF  # Ensure CRC is within 32 bits
    return crc ^ 0xFFFFFFFF

def crc32Decoding(input):
    global incorrectBuffers
    data = input[:-32]
    checksum = format(crc32(data),'032b')
    if input[-32:] == str(checksum):
        print('Correct checksum')
        return True
    else:
        print('Incorrect checksum')
        incorrectBuffers += 1
        return False

# Connection Layer
def getData(data):
    data1 = data.split(b'\x00')
    data1 = [item.decode('utf-8') for item in data1]
    messageData = []
    for index in range(0,len(data1)-1,3):
        # Unpack the received data
        hamming_code_left = data1[index]
        hamming_code_right = data1[index+1]
        crc32_code = data1[index+2]
        print(f"Received Hamming Code Left: {hamming_code_left}\tReceived Hamming Code Right: {hamming_code_right}")
        print(f"Received CRC32 Code: {crc32_code}")
        crc32Success = crc32Decoding(crc32_code)
        hammingSuccessLeft = hammingDecoding(hamming_code_left)
        hammingSuccessRight = hammingDecoding(hamming_code_right)
        print("Checksum failed") if not crc32Success else print("Checksum accepted")
        print(f"Hamming Left must be corrected, this is the new hamming: {hammingSuccessLeft[0]}") if not hammingSuccessLeft[1] else print(f"Accepted Hamming Left: {hammingSuccessLeft[0]}")
        print(f"Hamming Right must be corrected, this is the new hamming: {hammingSuccessRight[0]}") if not hammingSuccessRight[1] else print(f"Accepted Hamming Right: {hammingSuccessRight[0]}")
        messageData.append({"h_message_left": hammingSuccessLeft[0], "h_message_right": hammingSuccessRight[0], "crc_message": crc32_code})  
    return messageData

# Presentation layer
def decodeData(data1):
    hamming = ""
    crc32 = ""
    for data in data1:
        hamming += chr(int(data["h_message_left"][:3] + data["h_message_left"][4] + data["h_message_right"][:3] + data["h_message_right"][4], 2))
        crc32 += chr(int(data["crc_message"][:-32], 2))
    return {"hamming": hamming, "crc32": crc32}

def main():
    HOST = "127.0.0.1"  # IP, capa de Red. 127.0.0.1 es localhost
    PORT = 65432        # Puerto, capa de Transporte
    numberBuffers = 0
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Conexion Entrante del proceso {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Connection layer
                data = getData(data)
                # Presentation layer
                data = decodeData(data)
                # Application Layer
                print(f"Hamming message is: ", data["hamming"])
                print(f"Crc32 message is: ", data["crc32"])
                numberBuffers += 1
    print("Amount of Stream Buffers (Buffers Sended): ",numberBuffers)
    print("Amount of letters with errors: ",incorrectBuffers)

if __name__ == "__main__":
    main()
