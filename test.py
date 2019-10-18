with open('credits.txt', 'r') as f:
    for c in f:
        print(c)
f.close()

choices = [0, 1]
a = [(x, y) for x in choices for y in choices]
print(a)
