def perfect(n):
    s = 0
    for i in range(1, n):
        if n % i == 0:
            s += i

    if s == n:
        return True
    else:
        return False

num = int(input("Enter a number: "))

if perfect(num):
    print("Perfect number")
else:
    print("Not a perfect number")
