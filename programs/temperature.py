def c_to_f(c):
    return (c * 9/5) + 32

def c_to_k(c):
    return c + 273.15

def f_to_c(f):
    return (f - 32) * 5/9

def f_to_k(f):
    return (f - 32) * 5/9 + 273.15

def k_to_c(k):
    return k - 273.15

def k_to_f(k):
    return (k - 273.15) * 9/5 + 32


print("Temperature Conversion")
print("1. Celsius to Fahrenheit")
print("2. Celsius to Kelvin")
print("3. Fahrenheit to Celsius")
print("4. Fahrenheit to Kelvin")
print("5. Kelvin to Celsius")
print("6. Kelvin to Fahrenheit")

choice = int(input("Enter your choice: "))
temp = float(input("Enter temperature: "))

if choice == 1:
    print("Temperature in Fahrenheit =", c_to_f(temp))

elif choice == 2:
    print("Temperature in Kelvin =", c_to_k(temp))

elif choice == 3:
    print("Temperature in Celsius =", f_to_c(temp))

elif choice == 4:
    print("Temperature in Kelvin =", f_to_k(temp))

elif choice == 5:
    print("Temperature in Celsius =", k_to_c(temp))

elif choice == 6:
    print("Temperature in Fahrenheit =", k_to_f(temp))

else:
    print("Invalid choice")
