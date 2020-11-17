import Crypto.Util.number as cu
import hashlib as hl
import math


# Ex2

def RSAEncode (m, e, n):
    return pow(m, e, n)

def RSADecode (c, d, n):
    return cu.long_to_bytes(pow(c, d, n))

p = cu.getPrime(1536)
q = cu.getPrime(512)
n = p*q
f = (p - 1) * (q - 1)
e = cu.getRandomNBitInteger(128)
while e <= 1 or e >= f or cu.GCD(f, e) != 1:
    e = cu.getRandomNBitInteger(128)
d = cu.inverse(e, f)

cryptogram = RSAEncode(cu.bytes_to_long(bytearray(input("Input something\n").encode())), e, n)
decoded = RSADecode(cryptogram, d, n).decode()
print(str(decoded))


# Ex3

def mgf1 (msg, len):
    num = cu.bytes_to_long(msg)
    output = 0
    shift = 0
    for i in range(math.ceil(len / 32)):
        temp = hl.sha256(cu.long_to_bytes((num << 32) + i))
        output = (output << (temp.digest_size * 8)) + cu.bytes_to_long(temp.digest())
        shift = shift + 256
    return cu.long_to_bytes(output >> (shift - len * 8))

print(mgf1(bytearray(input("Input something\n").encode()), 56))
