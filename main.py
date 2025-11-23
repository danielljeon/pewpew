import numpy as np


def fit_pewpew():
    print("##### Curve Fitting #####")
    print("Modelling: distance_m = f(variable)")

    print("\nHow many data points:")
    n = int(input("> "))

    variables = []
    distances = []

    print("\nEnter data as: variable distance_m")
    print("Example: 30 5.2")
    for i in range(n):
        line = input(f"Point {i + 1}: ")
        a_str, d_str = line.split()
        variables.append(float(a_str))
        distances.append(float(d_str))

    variables = np.array(variables, dtype=float)
    distances = np.array(distances, dtype=float)

    degree = int(input("\nPolynomial degree (1-3 recommended): "))

    # Fit polynomial: distances = p(variables).
    coeffs = np.polyfit(variables, distances, degree)

    # coeffs is [c_deg, ..., c2, c1, c0] (highest degree first).
    print("\nFitted coefficients (highest power first):")
    for i, c in enumerate(coeffs):
        power = degree - i
        print(f"  a_{power} = {c:.8f}")

    print("\nPolynomial form (distance in meters):")
    terms = []
    for i, c in enumerate(coeffs):
        p = degree - i
        if p == 0:
            terms.append(f"{c:.8f}")
        elif p == 1:
            terms.append(f"{c:.8f} * variable")
        else:
            terms.append(f"{c:.8f} * pow(variable, {p})")
    print("  distance_m ~= " + " + ".join(terms))

    print("\n##### Arduino function (copy-paste) #####\n")
    print("float distance_from_variable(float variable) {")
    print("    // Polynomial approximation generated from Python")
    print("    // distance_m = ", end="")

    # Format nicely for C++.
    expr_terms = []
    for i, c in enumerate(coeffs):
        p = degree - i
        if p == 0:
            expr_terms.append(f"{c:.8f}f")
        elif p == 1:
            expr_terms.append(f"{c:.8f}f * variable")
        elif p == 2:
            expr_terms.append(f"{c:.8f}f * variable * variable")
        elif p == 3:
            expr_terms.append(f"{c:.8f}f * variable * variable * variable")
        else:
            expr_terms.append(f"{c:.8f}f * pow(variable, {p})")

    print(" + ".join(expr_terms) + ";")
    print("}")
    print("\n// Call distance_from_variable(variable).")


if __name__ == "__main__":
    fit_pewpew()
