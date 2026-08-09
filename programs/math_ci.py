import math

def solve_discrete_future_value(P, r, n, t):
    """A = P * (1 + r/n)**(n*t)"""
    return P * (1 + r/n)**(n*t)

def solve_discrete_present_value(A, r, n, t):
    """P = A / (1 + r/n)**(n*t)"""
    return A / (1 + r/n)**(n*t)

def solve_discrete_time(A, P, r, n):
    """t = ln(A/P) / (n * ln(1 + r/n))"""
    if A <= 0 or P <= 0:
        raise ValueError("A and P must be positive.")
    if r == 0:
        raise ValueError("Rate is zero – time is undefined (A equals P for any t).")
    return math.log(A/P) / (n * math.log(1 + r/n))

def solve_discrete_rate(A, P, n, t, tol=1e-10, max_iter=100):
    """Solve for r using Newton's method. f(r) = P(1+r/n)^(nt) - A = 0"""
    if P <= 0 or t <= 0 or n <= 0:
        raise ValueError("P, t, n must be positive.")
    if A <= 0:
        raise ValueError("A must be positive.")

    # Initial guess: use simple interest approximation or just 0.05
    r = 0.05
    for _ in range(max_iter):
        base = 1 + r/n
        f = P * base**(n*t) - A
        # derivative: P * n*t * base**(n*t - 1) * (1/n) = P * t * base**(n*t - 1)
        df = P * t * base**(n*t - 1)
        if df == 0:
            break
        r_new = r - f / df
        if r_new < -1:  # r can't be <= -100% realistically, cap for stability
            r_new = -0.999
        if abs(r_new - r) < tol:
            return r_new
        r = r_new
    raise ValueError("Rate did not converge. Try different initial values or check inputs.")

def solve_discrete_compounding_frequency(A, P, r, t, tol=1e-10, max_iter=100):
    """Solve for n using Newton's method. f(n) = P(1+r/n)^(nt) - A = 0 (n > 0)"""
    if P <= 0 or t <= 0:
        raise ValueError("P and t must be positive.")
    if A <= 0:
        raise ValueError("A must be positive.")
    if r == 0:
        # With zero rate, any n yields A = P. Return a conventional value.
        return 1.0

    # Initial guess
    n = 1.0
    for _ in range(max_iter):
        base = 1 + r/n
        f = P * base**(n*t) - A
        # derivative df/dn = P * base**(n*t) * [ t * ln(base) - (r*t)/(n + r) ]
        # Derived from logarithmic differentiation.
        ln_base = math.log(base)
        term = t * ln_base - (r * t) / (n + r)
        df = P * base**(n*t) * term
        if df == 0:
            break
        n_new = n - f / df
        if n_new <= 0:
            n_new = 1e-6  # keep positive
        if abs(n_new - n) < tol:
            return n_new
        n = n_new
    raise ValueError("Compounding frequency did not converge. Check your inputs.")

# ---------- Continuous Compounding ----------
def continuous_future_value(P, r, t):
    return P * math.exp(r * t)

def continuous_present_value(A, r, t):
    return A * math.exp(-r * t)

def continuous_time(A, P, r):
    if A <= 0 or P <= 0:
        raise ValueError("A and P must be positive.")
    if r == 0:
        raise ValueError("Rate is zero – time undefined.")
    return math.log(A/P) / r

def continuous_rate(A, P, t):
    if A <= 0 or P <= 0 or t <= 0:
        raise ValueError("A, P, t must be positive.")
    return math.log(A/P) / t

def get_positive_float(prompt):
    """Keep asking until a positive number is entered."""
    while True:
        try:
            val = float(input(prompt))
            if val > 0:
                return val
            print("Please enter a positive number.")
        except ValueError:
            print("Invalid number. Try again.")

def get_non_negative_float(prompt):
    """Allow zero as well."""
    while True:
        try:
            val = float(input(prompt))
            if val >= 0:
                return val
            print("Please enter a number >= 0.")
        except ValueError:
            print("Invalid number. Try again.")

def main():
    print("===== ADVANCED COMPOUND INTEREST CALCULATOR =====")
    while True:
        print("\nChoose calculation type:")
        print("  1. Discrete compounding – Future Value (A)")
        print("  2. Discrete compounding – Present Value (P)")
        print("  3. Discrete compounding – Interest Rate (r)")
        print("  4. Discrete compounding – Time (t)")
        print("  5. Discrete compounding – Compounding Frequency (n)")
        print("  6. Continuous compounding – Future Value (A)")
        print("  7. Continuous compounding – Present Value (P)")
        print("  8. Continuous compounding – Interest Rate (r)")
        print("  9. Continuous compounding – Time (t)")
        print("  0. Exit")

        choice = input("Your choice: ").strip()
        if choice == '0':
            print("Goodbye!")
            break

        try:
            if choice == '1':
                P = get_positive_float("Principal (P): ")
                r_pct = get_non_negative_float("Annual rate in % (e.g., 5): ")
                n = get_positive_float("Compounding periods per year (n): ")
                t = get_positive_float("Time in years (t): ")
                r = r_pct / 100
                A = solve_discrete_future_value(P, r, n, t)
                print(f"Future Value A = {A:.2f}")

            elif choice == '2':
                A = get_positive_float("Future value (A): ")
                r_pct = get_non_negative_float("Annual rate in %: ")
                n = get_positive_float("n: ")
                t = get_positive_float("t: ")
                r = r_pct / 100
                P = solve_discrete_present_value(A, r, n, t)
                print(f"Present Value P = {P:.2f}")

            elif choice == '3':
                P = get_positive_float("Principal (P): ")
                A = get_positive_float("Future value (A): ")
                n = get_positive_float("n: ")
                t = get_positive_float("t: ")
                if A <= P:
                    print("Warning: A should be > P for a positive rate (unless rate can be negative).")
                r = solve_discrete_rate(A, P, n, t)
                r_pct = r * 100
                print(f"Annual interest rate = {r_pct:.4f}%")

            elif choice == '4':
                P = get_positive_float("P: ")
                A = get_positive_float("A: ")
                r_pct = get_non_negative_float("Rate in %: ")
                n = get_positive_float("n: ")
                r = r_pct / 100
                t = solve_discrete_time(A, P, r, n)
                print(f"Time t = {t:.6f} years")

            elif choice == '5':
                P = get_positive_float("P: ")
                A = get_positive_float("A: ")
                r_pct = get_non_negative_float("Rate in %: ")
                t = get_positive_float("t: ")
                r = r_pct / 100
                n = solve_discrete_compounding_frequency(A, P, r, t)
                print(f"Compounding frequency n = {n:.4f} times per year")
                # Suggest common frequencies
                common = {1: 'annually', 2: 'semi-annually', 4: 'quarterly', 12: 'monthly', 365: 'daily'}
                closest = min(common.keys(), key=lambda k: abs(k - n))
                if abs(closest - n) < 0.1:
                    print(f"(Closest standard: {closest} – {common[closest]})")

            elif choice == '6':
                P = get_positive_float("P: ")
                r_pct = get_non_negative_float("Rate in %: ")
                t = get_positive_float("t: ")
                r = r_pct / 100
                A = continuous_future_value(P, r, t)
                print(f"Future value (continuous) A = {A:.2f}")

            elif choice == '7':
                A = get_positive_float("A: ")
                r_pct = get_non_negative_float("Rate in %: ")
                t = get_positive_float("t: ")
                r = r_pct / 100
                P = continuous_present_value(A, r, t)
                print(f"Present value (continuous) P = {P:.2f}")

            elif choice == '8':
                P = get_positive_float("P: ")
                A = get_positive_float("A: ")
                t = get_positive_float("t: ")
                r = continuous_rate(A, P, t)
                r_pct = r * 100
                print(f"Continuous rate = {r_pct:.4f}%")

            elif choice == '9':
                P = get_positive_float("P: ")
                A = get_positive_float("A: ")
                r_pct = get_non_negative_float("Rate in %: ")
                r = r_pct / 100
                t = continuous_time(A, P, r)
                print(f"Time (continuous) t = {t:.6f} years")

            else:
                print("Invalid choice. Please select 0-9.")
        except ValueError as e:
            print(f"Calculation error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
