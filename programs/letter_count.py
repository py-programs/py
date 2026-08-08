def count_letter(s, letter):
    count = 0

    for ch in s:
        if ch.lower() == letter.lower():
            count = count + 1

    return count


text = input("Enter a string: ")
letter = input("Enter a letter: ")

print("The letter", letter, "occurs", count_letter(text, letter), "times.")
