import Crypto.Util.number as cu

def findSeed(size, M):
    x = cu.getRandomNBitInteger(int(size/2))
    while not(cu.GCD(x,M)==1):
        x = cu.getRandomNBitInteger(int(size/2))
    return x

def bbs(N):
    p = 0
    while (p % 4 != 3):
        p = cu.getPrime(512)
    q = 0
    while (q % 4 != 3):
        q = cu.getPrime(512)
    M = p * q
    x = findSeed(512, M)
    key = 0b0
    for i in range(N):
        x = x * x % M
        key = key | (x & 0b1 << i)
    return key

def ex3():
    print(bin(int(bbs(128))))

def ex4():
    i = cu.bytes_to_long(bytearray(input("Input something\n").encode()))
    key = bbs(128)
    cyphered = i ^ key
    print("Cyphered: " + str(bin(cyphered)))
    decyphered = cyphered ^ key
    print("Decyphered: " + str(cu.long_to_bytes(decyphered).decode()))


print("ex3: ")
ex3()
print("\nex4: ")
ex4()



