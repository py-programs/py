import math

def perimeter(radius):
    return 2 * math.pi * radius

r = float(input("Enter the radius of the circle: "))

p = perimeter(r)

print("Perimeter of the circle =", p)
