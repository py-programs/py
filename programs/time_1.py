def convert_days(days):
    years = days // 365
    days = days % 365

    months = days // 30
    days = days % 30

    return years, months, days


d = int(input("Enter number of days: "))

y, m, d = convert_days(d)

print("Years =", y)
print("Months =", m)
print("Days =", d)
