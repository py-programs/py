def display_vowels(s):
    for ch in s:
        if ch.lower() in "aeiou":
            print(ch, end=" ")

text = input("Enter a string: ")

print("Vowels are:", end=" ")
display_vowels(text)
