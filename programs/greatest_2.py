def greatest(a, b):
    if a > b:
        return a
    else:
        return b

x = float(input("Enter first number: "))
y = float(input("Enter second number: "))

print("Greatest number is:", greatest(x, y))
