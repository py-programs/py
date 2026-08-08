def count_all(s):
    letters = 0
    digits = 0
    words = 0

    for ch in s:
        if ch.isalpha():
            letters += 1
        elif ch.isdigit():
            digits += 1

    words = len(s.split())

    return letters, digits, words


text = input("Enter a sentence: ")

l, d, w = count_all(text)

print("Letters =", l)
print("Digits =", d)
print("Words =", w)
