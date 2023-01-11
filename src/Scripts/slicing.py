import bitarray
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("string")
args = parser.parse_args()
message = args.string

def remplissage(m) :
    a = bitarray.bitarray()
    a.frombytes(m.encode('utf-8'))
    l = len(a.tolist())
    a.append(1)
    k = 0
    while (l + 1 + k) % 512 != 448:
        a.append(0)
        k += 1
    binaryl = bin(l)[2:]
    if (len(binaryl) < 64) :
        k2 = 64 - len(binaryl)
        for i in range(k2) :
            a.append(0)
    for j in binaryl :
        a.append(int(j))
    l2 = a.tolist()
    return l2

def decouppage(l) :
    n = len(l) // 512
    sortie = []
    for i in range(n):
        u32liste = []
        for j in range(16) :
            u32array = []
            u32 = 0
            for h in range(32):
                u32array.append(l[i*512 + j*32 + h])
            for z in range(32) :
                u32 += (2**(31-z))*u32array[z]
            u32liste.append(u32)
        sortie.append(u32liste)
    return sortie


def traitement(m) :
    a = remplissage(m)
    return decouppage(a)

def Conversion_hexa(u32array) :
    a = bitarray.bitarray()
    for u32 in u32array :
        b = bitarray.bitarray()
        u32_bytes = u32.to_bytes(4,  byteorder='big')
        b.frombytes(u32_bytes)
        a += b
    binary = a.to01()
    sortie_hexa = hex(int(binary, 2))
    return sortie_hexa

def hexa_hash_to_u32(hexa) :
    bits = ''
    u32_array = []
    for num in hexa :
        if num == '0':
            bits += '0000'
        elif num == '1':
            bits += '0001'
        elif num == '2':
            bits += '0010'
        elif num == '3':
            bits += '0011'
        elif num == '4':
            bits += '0100'
        elif num == '5':
            bits += '0101'
        elif num == '6':
            bits += '0111'
        elif num == '7':
            bits += '0111'
        elif num == '8':
            bits += '1000'
        elif num == '9':
            bits += '1001'
        elif num == 'a':
            bits += '1010'
        elif num == 'b':
            bits += '1011'
        elif num == 'c':
            bits += '1100'
        elif num == 'd':
            bits += '1101'
        elif num == 'e':
            bits += '1110'
        elif num == 'f':
            bits += '1111'
    k = len(bits)//32
    for i in range(k):
        u32 = 0
        for j in range(32):
            u32+= int(bits[32*i +j])*(2**j)
        u32_array.append(u32)
    return u32_array

def to_string(array):
    counter = 0
    string = ''
    for liste in array :
        for u32 in liste :
            counter+=1
            string += str(u32)
            string += str(' ')
    number = int(counter/16)
    zokfile = 'get_hash' + str(number) + '.zok'
    return [string, zokfile]

liste = remplissage(message)
tableau = decouppage(liste)
sortie = to_string(tableau)
print(sortie)