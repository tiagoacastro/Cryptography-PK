import Crypto.Util.number as cu
import hashlib as hl
import math
import random


# Ex2

def RSAEncode (m, e, n):
    return pow(m, e, n)

def RSADecode (c, d, n):
    return pow(c, d, n)

p = cu.getPrime(2048)
q = cu.getPrime(1024)
n = p*q
f = (p - 1) * (q - 1)
e = random.randint(1, f)
while e <= 1 or e >= f or cu.GCD(f, e) != 1:
    e = cu.getRandomNBitInteger(128)
d = cu.inverse(e, f)

cryptogram = RSAEncode(cu.bytes_to_long(bytearray(input("Input something\n").encode())), e, n)
decoded = cu.long_to_bytes(RSADecode(cryptogram, d, n)).decode()
print(str(decoded))


# Ex3

def msgf1 (msg, len):
    num = cu.bytes_to_long(msg)
    output = 0b0
    for i in range(math.ceil(len/32)-1):
        temp = hl.sha256(cu.long_to_bytes((num << i.bit_length()) + i))
        output = (output << temp.digest_size) + cu.bytes_to_long(temp.digest())
    return cu.long_to_bytes(output >> (output.bit_length() - len))

print(msgf1(bytearray(input("Input something\n").encode()), 56))
