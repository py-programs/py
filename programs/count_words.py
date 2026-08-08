def count_words(s):
    count = 0

    for word in s.split():
        count += 1

    return count


text = input("Enter a sentence: ")

print("Number of words =", count_words(text))
