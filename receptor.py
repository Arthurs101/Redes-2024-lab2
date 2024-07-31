import math

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
hammingDecoding(input('Enter a bit message for the Hamming decoding: '))
crc32Decoding(input('Enter a bit message for the crc32 detection: '))
# message = input("Enter a bit message of any length: ")
# encodedMessage = hammingEncoding(message)
# decodedMessage = hammingDecoding(encodedMessage)
# print(encodedMessage)
# print(decodedMessage)
# message = input("enter bit message: ")
# print(f'Message corrected is: {hammingDecoding(message)}')