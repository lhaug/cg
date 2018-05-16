def int2bin4(i):
    s = [0, 0, 0, 0]
    for x in range(0,4):
        if i == 0:
            s[x] = 0
        s[x] = i % 2
        i = int(i) / int(2)
    return s

print(int2bin4(5))