import Crypto.Util.number as cu
import hashlib as hl
import math


# Ex2

def RSAEncode (m, e, n):
    return pow(m, e, n)

def RSADecode (c, d, n):
    return pow(c, d, n)
"""
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
"""

# Ex3

def msgf1 (msg, len):
    num = cu.bytes_to_long(msg)
    output = 0b0
    for i in range(math.ceil(len/32)-1):
        temp = hl.sha256(cu.long_to_bytes((num << i.bit_length()) + i))
        output = (output << temp.digest_size) + cu.bytes_to_long(temp.digest())
    return cu.long_to_bytes(output >> (output.bit_length() - len))

print(msgf1(bytearray(input("Input something\n").encode()), 56))
"""
def MGF(m, len):
    hlen = 32
    mNumber = cu.bytes_to_long(m)
    output = 0
    for i in range(0, len//hlen-1):
        tmp = hl.sha256(mNumber << i.bit_length() + i).digest()
        output = output << tmp.bit_length() + tmp
    return cu.long_to_bytes(mNumber >> (mNumber.bit_length() - len))


def ex3():
    expectingLength = 56
    msg = bytearray("r".encode())
    masked = MGF(msg, expectingLength)
    print("Expected bits length: " + str(expectingLength) + ". Actual bits length: " + str(cu.bytes_to_long(masked).bit_length()))
    print("Masked with MGF: " + str(masked))

ex3()
"""
