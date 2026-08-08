def string_info(s):
    upper = 0
    lower = 0

    for ch in s:
        if ch.isupper():
            upper += 1
        elif ch.islower():
            lower += 1

    print("Length =", len(s))
    print("Uppercase =", upper)
    print("Lowercase =", lower)


text = input("Enter a string: ")

string_info(text)
