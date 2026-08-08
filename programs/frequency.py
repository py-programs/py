def frequency(s, ch):
    count = 0

    for x in s:
        if x == ch:
            count += 1

    return count


text = input("Enter a string: ")
char = input("Enter a character: ")

print("Frequency =", frequency(text, char))
