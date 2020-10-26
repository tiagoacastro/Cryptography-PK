def EA(a, b):
    r = b % a
    prev = r
    while(r != 0):
        b = a
        a = r
        prev = r
        r = b % a
    return prev

print(EA(22, 59))
print(EA(7, 15))
print(EA(49, 101))
print(EA(66, 123))

print('---')

def EEA(a, b):
    max = b
    x1 = 0
    x2 = 1
    y1 = 0
    y2 = 0
    r = 1
    c = 0
    while r != 0:
        d = b // a
        r = b % a
        b = a
        a = r
        if c >= 2:
            x = (x1 - y1*x2) % max
            x1 = x2
            x2 = x
        y1 = y2
        y2 = d
        c += 1
    x = (x1 - y1 * x2) % max
    return x

print(EEA(22, 59))
print(EEA(7, 15))
print(EEA(49, 101))
print(EEA(66, 123))

print('---')

def FLT(a, b):
    return pow(a, b-2) % b

print(EEA(22, 59))
print(EEA(7, 15))
print(EEA(49, 101))
print(EEA(66, 123))

print('---')

def BMA(a, b):
    r = 1
    while b != 0:
        if b % 2 == 1:
            r = r * a
        a = pow(a, 2)
        b = b >> 1
    return r

print(BMA(5, 10))
print(BMA(3, 15))
print(BMA(16, 5))
print(BMA(2, 17))

