def check(n):
    if n <= 1:
        print("Neither Prime nor Composite")
    else:
        count = 0

        for i in range(1, n + 1):
            if n % i == 0:
                count += 1

        if count == 2:
            print("Prime")
        else:
            print("Composite")


n = int(input("Enter a number: "))
check(n)
