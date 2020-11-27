import Crypto.Util.number as cu
import hashlib as hl
import math



# ex2

def mgf1 (msg, len):
    num = cu.bytes_to_long(msg)
    output = 0
    shift = 0
    for i in range(math.ceil(len / 32)):
        temp = hl.sha256(cu.long_to_bytes((num << 32) + i))
        output = (output << (temp.digest_size * 8)) + cu.bytes_to_long(temp.digest())
        shift = shift + 256
    return cu.long_to_bytes(output >> (shift - len * 8))

def OAEPEncoding (msg):
    hLen = 32
    k = 255
    mLen = len(msg)
    if mLen > k - 2 * hLen - 2:
        return "Error"
    lHash = hl.sha256(bytearray("".encode()))
    PSlen = k - mLen - 2 * hLen - 2
    DB = cu.bytes_to_long(lHash.digest()) << (PSlen * 8)
    DB = (DB << 8) + 1
    DB = (DB << (mLen * 8)) + cu.bytes_to_long(msg)
    if len(cu.long_to_bytes(DB)) != k - hLen - 1:
        return "Error"
    seed = cu.long_to_bytes(cu.getRandomNBitInteger(hLen*8))
    dbMask = mgf1(seed, k - hLen - 1)
    maskedDB = DB ^ cu.bytes_to_long(dbMask)
    seedMask = mgf1(cu.long_to_bytes(maskedDB), hLen)
    maskedSeed = cu.bytes_to_long(seed) ^ cu.bytes_to_long(seedMask)
    EM = (0x00 << (len(cu.long_to_bytes(maskedSeed))*8)) + maskedSeed
    EM = (EM << (len(cu.long_to_bytes(maskedDB))*8)) + maskedDB
    if len(cu.long_to_bytes(EM)) != k - 1:
        return "Error"
    return EM

def OAEPDecoding (cipher):
    hLen = 32
    k = 255
    maskedSeed = (cipher >> (len(cu.long_to_bytes(cipher)) * 8 - hLen*8)) & ((0b1 << (hLen*8))-1)
    maskedDB = cipher & ((0b1 << ((k-hLen-1)*8))-1)
    lHash = hl.sha256(bytearray("".encode()))
    seedMask = mgf1(cu.long_to_bytes(maskedDB), hLen)
    seed = maskedSeed ^ cu.bytes_to_long(seedMask)
    dbMask = mgf1(cu.long_to_bytes(seed), k - hLen - 1)
    DB = maskedDB ^ cu.bytes_to_long(dbMask)
    lHash2 = DB >> (len(cu.long_to_bytes(DB)) * 8 - hLen*8)
    M = cu.long_to_bytes(DB & ((0b1 << (len(cu.long_to_bytes(DB)) - hLen) * 8) - 1))
    if (cu.bytes_to_long(M) >> (len(M)-1)) == 0:
        return "Error"
    M = cu.long_to_bytes(cu.bytes_to_long(M) - (1 << (len(M)*8-8)))
    if lHash2 != cu.bytes_to_long(lHash.digest()):
        return "Error"
    return M

cryptogram = OAEPEncoding(bytearray(input("Input something\n").encode()))
if (cryptogram == "Error"):
    print("Error encoding")
else:
    message = OAEPDecoding(cryptogram)
    if (message == "Error"):
        print("Error decoding")
    else:
        print(str(message.decode()))



# ex3

def RSAEncode (m, e, n):
    return pow(m, e, n)

def RSADecode (c, d, n):
    return cu.long_to_bytes(pow(c, d, n))

def RSAOAEPciphering (msg, n, e):
    BEM = OAEPEncoding(bytearray(msg.encode()))
    if (BEM == "Error"):
        print("Error encoding")
        exit()
    C = RSAEncode (BEM, e, n)
    return cu.long_to_bytes(C)

def RSAOAEPdeciphering (cipher, n, d):
    C = cu.bytes_to_long(cipher)
    BC = RSADecode(C, d, n)
    return OAEPDecoding(cu.bytes_to_long(BC))

p = cu.getPrime(1536)
q = cu.getPrime(512)
n = p * q
f = (p - 1) * (q - 1)
e = cu.getRandomNBitInteger(128)
while e <= 1 or e >= f or cu.GCD(f, e) != 1:
    e = cu.getRandomNBitInteger(128)
d = cu.inverse(e, f)
cipher = RSAOAEPciphering(input("Input something\n"), n, e)
message = RSAOAEPdeciphering(cipher, n, d)
print(str(message.decode()))