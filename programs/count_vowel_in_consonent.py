def count_vowels_consonants(s):
    vowels = 0
    consonants = 0

    for ch in s:
        if ch.lower() in "aeiou":
            vowels = vowels + 1
        elif ch.isalpha():
            consonants = consonants + 1

    return vowels, consonants


text = input("Enter a string: ")

v, c = count_vowels_consonants(text)

print("Number of vowels =", v)
print("Number of consonants =", c)
