def product_of_digits(n):
    product = 1

    while n > 0:
        digit = n % 10
        product = product * digit
        n = n // 10

    return product


num = int(input("Enter a number: "))

print("Product of digits =", product_of_digits(num))
