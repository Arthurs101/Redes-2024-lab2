# Arturo Argueta 
# Diego Alonzo
import math
# def xOrOp(xorarray):
    
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
    if j!=0:
        print(f'There is an error in the position {len(message)-j}')
        message = list(message)
        message[len(message)-j] = str((int(message[len(message)-j])+1)%2)
        message = "".join(message)
    return message

def crc32(data: bytes) -> int:
    POLYNOMIAL = 0xEDB88320
    crc = 0xFFFFFFFF

    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLYNOMIAL
            else:
                crc >>= 1

    return crc ^ 0xFFFFFFFF

def verify_crc32(message_with_checksum: str) -> bool:
    if len(message_with_checksum) <= 32:
        print("Entrada inválida: el mensaje es muy corto para incluir tanto el mensaje como el checksum.")
        return False

    # Dividir el mensaje y el checksum recibido
    message = message_with_checksum[:-32]
    received_checksum_str = message_with_checksum[-32:]

    # Convertir el checksum recibido de cadena binaria a entero
    received_checksum = int(received_checksum_str, 2)

    # Convertir el mensaje de cadena binaria a bytes
    message_bytes = int(message, 2).to_bytes((len(message) + 7) // 8, byteorder='big')

    # Calcular el CRC32 del mensaje
    calculated_checksum = crc32(message_bytes)

    # Imprimir información de depuración
    print(f"Checksum recibido: {received_checksum_str} (int: {received_checksum})")
    print(f"Checksum calculado: {calculated_checksum:032b} (int: {calculated_checksum})")

    return calculated_checksum == received_checksum
# result = verify_crc32('10101010101010101011010100000011010001110010101011001')
# print(f'Valido: {str(result)}')
# crc32Decoding('11010000','1001')
# crc32Decoding('01001011100','1011')
# crc32Decoding('10101100','11011')
# crc32Decoding('10110101111001011100100100100000')
# message = input("Enter a bit message of any length: ")
# encodedMessage = hammingEncoding(message)
# decodedMessage = hammingDecoding(encodedMessage)
# print(encodedMessage)
# print(decodedMessage)
# message = input("enter bit message: ")
# print(f'Message corrected is: {hammingDecoding(message)}')


