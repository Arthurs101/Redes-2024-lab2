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

def crcxor(message:list, polinomio:list):
    if len(message)>=len(polinomio) and '1' in message:
        firstOne = 0
        for index in range(0, len(polinomio)):
            message[index] = (str((int(message[index])+int(polinomio[index]))%2))
            if message[index] == '1':
                firstOne = index
        message = crcxor(message[firstOne:],polinomio)
    return message

def crc32Decoding(message:str, polinomio:str='100000100110000010001110110110111'):
    # Apply xor 
    message = list(message)
    polinomio = list(polinomio)
    message = crcxor(message,polinomio)
    print('Error in message '+"".join(message)) if '1' in message else print(f'Message accepted')
    
# crc32Decoding('11010001','1001')
crc32Decoding('10110101111001011100100100100000')
# message = input("Enter a bit message of any length: ")
# encodedMessage = hammingEncoding(message)
# decodedMessage = hammingDecoding(encodedMessage)
# print(encodedMessage)
# print(decodedMessage)
# message = input("enter bit message: ")
# print(f'Message corrected is: {hammingDecoding(message)}')


