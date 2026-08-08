def convert_string(s, choice):
    if choice == 1:
        return s.upper()
    elif choice == 2:
        return s.lower()
    else:
        return "Invalid choice"


text = input("Enter a string: ")

print("1. Uppercase")
print("2. Lowercase")

choice = int(input("Enter your choice: "))

print("Result =", convert_string(text, choice))
