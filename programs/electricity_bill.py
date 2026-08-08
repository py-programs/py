# Nepal Electricity Bill Calculator

def calculate_bill(units, capacity):
    # Minimum/service charge and energy rates
    # Example domestic tariff structure
    if capacity == 5:
        minimum_charge = 30
    elif capacity == 15:
        minimum_charge = 50
    elif capacity == 30:
        minimum_charge = 75
    elif capacity == 60:
        minimum_charge = 125
    else:
        print("Invalid meter capacity!")
        return

    # Progressive energy-charge calculation
    remaining = units
    energy_charge = 0

    # First 20 units
    slab = min(remaining, 20)
    energy_charge += slab * 4
    remaining -= slab

    # 21–30 units
    if remaining > 0:
        slab = min(remaining, 10)
        energy_charge += slab * 6.5
        remaining -= slab

    # 31–50 units
    if remaining > 0:
        slab = min(remaining, 20)
        energy_charge += slab * 8
        remaining -= slab

    # 51–150 units
    if remaining > 0:
        slab = min(remaining, 100)
        energy_charge += slab * 9.5
        remaining -= slab

    # 151–250 units
    if remaining > 0:
        slab = min(remaining, 100)
        energy_charge += slab * 10
        remaining -= slab

    # Above 250 units
    if remaining > 0:
        energy_charge += remaining * 11

    subtotal = minimum_charge + energy_charge

    # VAT (13%)
    vat = subtotal * 0.13

    total = subtotal + vat

    print("\n----- Nepal Electricity Bill -----")
    print(f"Meter Capacity : {capacity} A")
    print(f"Units Consumed : {units}")
    print(f"Energy Charge  : Rs. {energy_charge:.2f}")
    print(f"Minimum Charge : Rs. {minimum_charge:.2f}")
    print(f"VAT (13%)      : Rs. {vat:.2f}")
    print("----------------------------------")
    print(f"TOTAL BILL     : Rs. {total:.2f}")


# User input
units = float(input("Enter units consumed: "))
capacity = int(input("Enter meter capacity (5/15/30/60 A): "))

calculate_bill(units, capacity)
