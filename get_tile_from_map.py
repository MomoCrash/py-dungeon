
x0 = 112  # position en x de l'origine en pixels
y = 32  # position en y de l'origine en pixels
nb = 4  # nombre de tuiles 16x16 aligné horizontalement vers la droite

ret = []

for i in range(nb):
    for height in range(2):
        for width in range(2):
            ret.append((int((x0 + i * 16 + width * 8) / 8), int((y + height * 8) / 8)))

for i in range(0, len(ret), 4):
    print(f"{ret[i]}, {ret[i + 1]}, {ret[i + 2]}, {ret[i + 3]}, ")
