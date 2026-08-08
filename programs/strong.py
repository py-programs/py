def strong(n):
    original = n
    total = 0

    while n > 0:
        digit = n % 10

        fact = 1
        for i in range(1, digit + 1):
            fact *= i

        total += fact
        n //= 10

    return total == original


num = int(input("Enter a number: "))

if strong(num):
    print("Strong number")
else:
    print("Not a Strong number")
