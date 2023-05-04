a = 0
b = 10
rect = 1000000
dx = (b - a) / rect
x = 0
area = 0
for i in range(rect):
    area += (x ** 4 + x ** 2 - x + 7)
    x += dx
area *= dx
print(area)
