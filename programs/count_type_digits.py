def count_even_odd(n):
    even = 0
    odd = 0

    while n > 0:
        digit = n % 10

        if digit % 2 == 0:
            even += 1
        else:
            odd += 1

        n //= 10

    return even, odd


num = int(input("Enter a number: "))

e, o = count_even_odd(num)

print("Even digits =", e)
print("Odd digits =", o)
