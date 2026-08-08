# Salary Tax Calculator

salary = float(input("Enter your annual salary (Rs.): "))

# Example progressive tax rates
if salary <= 500000:
    tax = salary * 0.01
elif salary <= 700000:
    tax = 5000 + (salary - 500000) * 0.10
elif salary <= 1000000:
    tax = 25000 + (salary - 700000) * 0.20
elif salary <= 2000000:
    tax = 85000 + (salary - 1000000) * 0.30
else:
    tax = 385000 + (salary - 2000000) * 0.36

after_tax = salary - tax

print("\n----- Salary Tax Calculation -----")
print(f"Annual Salary : Rs. {salary:,.2f}")
print(f"Tax           : Rs. {tax:,.2f}")
print(f"After Tax     : Rs. {after_tax:,.2f}")
print(f"Monthly After Tax: Rs. {after_tax / 12:,.2f}")
