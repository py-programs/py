def largest_digit(n):
    largest = 0

    while n > 0:
        digit = n % 10
        if digit > largest:
            largest = digit
        n //= 10

    return largest

num = int(input("Enter a number: "))

print("Largest digit =", largest_digit(num))
