import Crypto.Util.number as cu
import math

H = [0x6a09e667,  0xbb67ae85,  0x3c6ef372,  0xa54ff53a,  0x510e527f,0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
K = [0x428a2f98,  0x71374491,  0xb5c0fbcf,  0xe9b5dba5,  0x3956c25b,  0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe,  0x9bdc06a7,  0xc19bf174,  0xe49b69c1,  0xefbe4786,  0x0fc19dc6,  0x240ca1cc, 0x2de92c6f,  0x4a7484aa,  0x5cb0a9dc,  0x76f988da,  0x983e5152,0xa831c66d,  0xb00327c8, 0xbf597fc7,  0xc6e00bf3,  0xd5a79147,  0x06ca6351,  0x14292967,  0x27b70a85,  0x2e1b2138, 0x4d2c6dfc,  0x53380d13,  0x650a7354,  0x766a0abb,  0x81c2c92e,  0x92722c85,  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 0x19a4c116,  0x1e376c08,  0x2748774c,  0x34b0bcb5,  0x391c0cb3,  0x4ed8aa4a,  0x5b9cca4f, 0x682e6ff3,  0x748f82ee,  0x78a5636f,  0x84c87814,  0x8cc70208,  0x90befffa,  0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

def parseUint32(a):
    n = 0
    for i in range(4):
        n = (n << 8) + a[i]
    return n

def RotateRight(aa, nn):
    aa = aa & 0xFFFFFFFF
    return ((aa >> nn) | (aa << (32 - nn))) & 0xFFFFFFFF

def S(x, a, b, c):
    return RotateRight(x, a) ^ RotateRight(x, b) ^ RotateRight(x, c)

def s(x, a, b, c):
    return RotateRight(x, a) ^ RotateRight(x, b) ^ (x >> c)

def Maj(a, b, c):
    return (a & b) ^ (a & c) ^ (b & c)

def Ch(a, b, c):
    return (a & b) ^ (~a & c)

def pad(m, n):
    tmp = (len(m) * 8) & 0xFFFFFFFFFFFFFFFF
    m.append(0x80)
    while (len(m) % n) != (n - 8):
        m.append(0x00)
    m = (cu.bytes_to_long(m) << 64) | tmp
    return cu.long_to_bytes(m)

def sha256(M):
    M = pad(M,64)
    i = 0
    tmp = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    while i < len(M):
        W = []
        for j in range(16):
            W.append(parseUint32(M[(math.floor(i/64)*64 + j*4):(math.floor(i/64)*64 + j*4 + 4)]))
        for j in range(16, 64):
            W.append((W[j-16]+W[j-7]+s(W[j-15], 7, 18, 3)+s(W[j-2], 17, 19, 10)) & 0xFFFFFFFF)
        for j in range(8):
            tmp[j] = H[j]
        for j in range(64):
            t1 = (K[j] + W[j] + S(tmp[4], 6, 11, 25) + Ch(tmp[4], tmp[5], tmp[6]) + tmp[7]) & 0xFFFFFFFF
            t2 = (Maj(tmp[0], tmp[1], tmp[2]) + S(tmp[0], 2, 13, 22)) & 0xFFFFFFFF
            for k in range(7,0,-1):
                tmp[k] = tmp[k - 1]
            tmp[0] = (t1 + t2) & 0xFFFFFFFF
            tmp[4] = (tmp[4] + t1) & 0xFFFFFFFF
        for j in range(8):
            H[j] = (H[j] + tmp[j]) & 0xFFFFFFFF
        i = i + 64
    ret = 0
    for i in range(8):
        ret = (ret << 32) + H[i]
    return ret

print(hex(sha256(bytearray(input("Input something\n").encode()))))