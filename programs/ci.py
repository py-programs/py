def annual_ci(p, r, t):
    amount = p * (1 + r / 100) ** t
    return amount - p

def half_yearly_ci(p, r, t):
    amount = p * (1 + r / 200) ** (2 * t)
    return amount - p

def quarterly_ci(p, r, t):
    amount = p * (1 + r / 400) ** (4 * t)
    return amount - p


print("1. Compound Interest Annually")
print("2. Compound Interest Half-Yearly")
print("3. Compound Interest Quarterly")

choice = int(input("Enter your choice: "))

p = float(input("Enter principal: "))
r = float(input("Enter rate: "))
t = float(input("Enter time in years: "))

if choice == 1:
    print("Compound Interest =", annual_ci(p, r, t))

elif choice == 2:
    print("Compound Interest =", half_yearly_ci(p, r, t))

elif choice == 3:
    print("Compound Interest =", quarterly_ci(p, r, t))

else:
    print("Invalid choice")
