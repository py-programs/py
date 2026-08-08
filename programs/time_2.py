def convert_seconds(seconds):
    hours = seconds // 3600
    seconds = seconds % 3600

    minutes = seconds // 60
    seconds = seconds % 60

    return hours, minutes, seconds


s = int(input("Enter seconds: "))

h, m, s = convert_seconds(s)

print("Hours =", h)
print("Minutes =", m)
print("Seconds =", s)
