def npr_to_inr(npr):
    rate = 1.60
    return npr / rate

def inr_to_npr(inr):
    rate = 1.60
    return inr * rate

print("1. NPR to INR")
print("2. INR to NPR")

choice = int(input("Enter your choice: "))

if choice == 1:
    npr = float(input("Enter amount in NPR: "))
    print("Amount in INR =", npr_to_inr(npr))

elif choice == 2:
    inr = float(input("Enter amount in INR: "))
    print("Amount in NPR =", inr_to_npr(inr))

else:
    print("Invalid choice")
