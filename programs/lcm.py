def lcm(a, b):
    m = max(a, b)
    while True:
        if m % a == 0 and m % b == 0:
            return m
        m += 1

x = int(input("Enter first number: "))
y = int(input("Enter second number: "))

print("LCM =", lcm(x, y))
