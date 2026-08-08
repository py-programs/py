def ci(p, r, t):
    amount = p * (1 + r / 100) ** t
    return amount - p

p = float(input("Enter Principal: "))
r = float(input("Enter Rate: "))
t = float(input("Enter Time: "))

print("Compound Interest =", ci(p, r, t))
