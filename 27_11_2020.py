import Crypto.Util.number as cu
import hashlib as hl
import math
import random

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

def RSAEncode (m, e, n):
    return pow(m, e, n)

def RSADecode (c, d, n):
    return cu.long_to_bytes(pow(c, d, n))

def RSAOAEPciphering (msg, n, e):
    BEM = OAEPEncoding(msg)
    if (BEM == "Error"):
        print("Error encoding")
        exit()
    C = RSAEncode (BEM, e, n)
    return cu.long_to_bytes(C)

def RSAOAEPdeciphering (cipher, n, d):
    C = cu.bytes_to_long(cipher)
    BC = RSADecode(C, d, n)
    return OAEPDecoding(cu.bytes_to_long(BC))



# ex1

def generateRSAKEM(n, e):
    hLen = 32
    k = 255
    RAND = 0
    while RAND <= 1 or RAND >= n:
        len = random.randint(1, k - 2 * hLen - 2 + 1)
        RAND = cu.getRandomNBitInteger(len)
    BRAND = cu.long_to_bytes(RAND)
    BKEY = hl.sha256(BRAND).digest()
    return [RSAOAEPciphering(BRAND, n, e), BKEY]

def receiveRSAKEM(cryptogram, n, d):
    KEY = RSAOAEPdeciphering(cryptogram, n, d)
    h = hl.sha256(KEY).digest()
    return h

p = cu.getPrime(1536)
q = cu.getPrime(512)
n = p * q
f = (p - 1) * (q - 1)
e = cu.getRandomNBitInteger(128)
while e <= 1 or e >= f or cu.GCD(f, e) != 1:
    e = cu.getRandomNBitInteger(128)
d = cu.inverse(e, f)
ret = generateRSAKEM(n, e)
cipher = ret[0]
BKEY = ret[1]
key = receiveRSAKEM(cipher, n, d)
if BKEY == key:
    print("Keys correspond")
else:
    print("Keys do not correspond")



# ex2

def createEMSAPSS(msg):
    hLen = 32
    sLen = 32
    emLen = 255
    if emLen < hLen + sLen + 2:
        return "Error"
    mHash = hl.sha256(msg).digest()
    if len(mHash) != hLen:
        return "Error"
    salt = cu.getRandomNBitInteger(sLen*8)
    M = ((salt << hLen*8) + cu.bytes_to_long(mHash)) << 64
    if len(cu.long_to_bytes(M)) != 8 + hLen + sLen:
        return "Error"
    H = hl.sha256(cu.long_to_bytes(M)).digest()
    if len(H) != hLen:
        return "Error"
    DB = ((salt << 8) + 0x01) << ((emLen - sLen - hLen - 2)*8)
    if len(cu.long_to_bytes(DB)) != emLen - hLen - 1:
        return "Error"
    dbMask = mgf1(H, emLen - hLen - 1)
    maskedDB = DB ^ cu.bytes_to_long(dbMask)
    return (((0xbc << (hLen * 8)) + cu.bytes_to_long(H)) << (len(cu.long_to_bytes(maskedDB)) * 8)) + maskedDB

def verifyEMSAPSS(msg, EM):
    hLen = 32
    sLen = 32
    emLen = 255
    if emLen < hLen + sLen + 2:
        return "Error1"
    mHash = hl.sha256(msg).digest()
    if len(mHash) != hLen:
        return "Error2"
    MSB = EM >> ((emLen - 1) * 8)
    if MSB != 0xbc:
        return "Error3"
    maskedDB = EM - ((EM >> ((emLen - hLen - 1) * 8)) << ((emLen - hLen - 1) * 8))
    H = (EM - ((EM >> ((emLen - 1) * 8)) << ((emLen - 1) * 8)) - maskedDB) >> ((emLen - hLen - 1) * 8)
    dbMask = mgf1(cu.long_to_bytes(H), emLen - hLen - 1)
    DB = maskedDB ^ cu.bytes_to_long(dbMask)
    if (DB - ((DB >> ((emLen - hLen - sLen - 2) * 8)) << ((emLen - hLen - sLen - 2) * 8))) != 0:
        return "Error4"
    if ((DB - ((DB >> ((emLen - hLen - sLen - 1) * 8)) << ((emLen - hLen - sLen - 1) * 8))) >> ((emLen - hLen - sLen - 2) * 8)) != 0x01:
        return "Error5"
    salt = DB >> ((len(cu.long_to_bytes(DB)) - sLen) * 8)
    M = ((salt << hLen * 8) + cu.bytes_to_long(mHash)) << 64
    H2 = hl.sha256(cu.long_to_bytes(M)).digest()
    if len(H2) != hLen:
        return "Error6"
    if H == H2:
        return "Error7"
    return "Verified"

msg = input("Input something\n")
signature = createEMSAPSS(bytearray(msg.encode()))
if signature == "Error":
    print("Error creating signature")
else:
    message = verifyEMSAPSS(bytearray(msg.encode()), signature)
    if message == "Error":
        print("Error verifying signature")
    else:
        print(message)



# ex3

def createRSAPSS(msg, n, d):
    EM = createEMSAPSS(msg)
    EM = pow(EM, d, n)
    return cu.long_to_bytes(EM)

def verifyRSAPSS(msg, signature, n, e):
    EM = cu.bytes_to_long(signature)
    EM = pow(EM, e, n)
    return verifyEMSAPSS(msg, EM)

p = cu.getPrime(1536)
q = cu.getPrime(512)
n = p * q
f = (p - 1) * (q - 1)
e = cu.getRandomNBitInteger(128)
while e <= 1 or e >= f or cu.GCD(f, e) != 1:
    e = cu.getRandomNBitInteger(128)
d = cu.inverse(e, f)
msg = input("Input something\n")
signature = createRSAPSS(bytearray(msg.encode()), n, d)
if signature == "Error":
    print("Error creating signature")
else:
    message = verifyRSAPSS(bytearray(msg.encode()), signature, n, e)
    if message == "Error":
        print("Error verifying signature")
    else:
        print(message)
