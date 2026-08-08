def check_equal(s1, s2):
    if s1 == s2:
        return "Equal"
    else:
        return "Not Equal"


str1 = input("Enter first string: ")
str2 = input("Enter second string: ")

print(check_equal(str1, str2))
