def swap(a, b):
    a, b = b, a
    return a, b


x = int(input("Enter first number: "))
y = int(input("Enter second number: "))

x, y = swap(x, y)

print("After swapping:")
print("First number =", x)
print("Second number =", y)
