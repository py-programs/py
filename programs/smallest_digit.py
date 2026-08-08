def smallest_digit(n):
    smallest = 9

    while n > 0:
        digit = n % 10
        if digit < smallest:
            smallest = digit
        n //= 10

    return smallest

num = int(input("Enter a number: "))

print("Smallest digit =", smallest_digit(num))
