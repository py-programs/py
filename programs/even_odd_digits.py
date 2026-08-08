def sum_digits(n, choice):
    total = 0

    while n > 0:
        digit = n % 10

        if choice == "even" and digit % 2 == 0:
            total += digit
        elif choice == "odd" and digit % 2 != 0:
            total += digit

        n //= 10

    return total


num = int(input("Enter a number: "))
choice = input("Enter even or odd: ").lower()

print("Sum =", sum_digits(num, choice))
