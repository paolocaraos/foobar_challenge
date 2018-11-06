def answer(digest):
    
    digest[0] = int(findMessage(digest[0]))

    for x in range(1, 16):
        digest[x] = digest[x] ^ digest[x - 1]
        digest[x] = int(findMessage(digest[x]))
    return digest

#Since we know that digest ranges from 0 - 256 and
#maps to message which ranges from 0 - 256,
#there must exist some T such that (x + T*256) % 129 == 0
def findMessage(x):
    T = 0
    while (x + T*256) % 129 != 0:
        T += 1
    return (x + T*256) / 129
    

print(answer([255, 129, 3, 129, 7, 129, 3, 129, 15, 129, 3, 129, 7, 129, 3, 129]))
print(answer([0, 129, 5, 141, 25, 137, 61, 149, 113, 145, 53, 157, 233, 185, 109, 165]))