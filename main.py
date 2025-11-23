import matplotlib.pyplot as plt
import numpy as np


def fit_pewpew():
    print("##### Curve Fitting #####")
    print("Modelling: y = f(x)")

    print("\nHow many data points:")
    n = int(input("> "))

    xs = []
    ys = []

    print("\nEnter data as: x y")
    print("Example: projectile_cm angle_deg")
    for i in range(n):
        line = input(f"Point {i + 1}: ")
        a_str, d_str = line.split()
        xs.append(float(a_str))
        ys.append(float(d_str))

    xs = np.array(xs, dtype=float)
    ys = np.array(ys, dtype=float)

    degree = int(input("\nPolynomial degree (1-3 recommended): "))

    # Fit polynomial: ys = p(xs).
    coeffs = np.polyfit(xs, ys, degree)
    poly = np.poly1d(coeffs)

    # Plot.
    # Create smooth range for curve.
    x_curve = np.linspace(xs.min(), xs.max(), 300)
    y_curve = poly(x_curve)
    plt.scatter(xs, ys, color="red", label="Data Points")
    plt.plot(x_curve, y_curve, color="blue", label=f"Polynomial (deg={degree})")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Curve Fit: y = f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()

    # coeffs is [c_deg, ..., c2, c1, c0] (highest degree first).
    print("\nFitted coefficients (highest power first):")
    for i, c in enumerate(coeffs):
        power = degree - i
        print(f"  a_{power} = {c:.8f}")

    print("\nPolynomial form (y in meters):")
    terms = []
    for i, c in enumerate(coeffs):
        p = degree - i
        if p == 0:
            terms.append(f"{c:.8f}")
        elif p == 1:
            terms.append(f"{c:.8f} * x")
        else:
            terms.append(f"{c:.8f} * pow(x, {p})")
    print("  y ~= " + " + ".join(terms))

    print("\n##### Arduino function (copy-paste) #####\n")
    print("float y_from_x(float x) {")
    print("    // Polynomial approximation generated from Python")
    print("    float y = ", end="")

    # Format nicely for C++.
    expr_terms = []
    for i, c in enumerate(coeffs):
        p = degree - i
        if p == 0:
            expr_terms.append(f"{c:.8f}f")
        elif p == 1:
            expr_terms.append(f"{c:.8f}f * x")
        elif p == 2:
            expr_terms.append(f"{c:.8f}f * x * x")
        elif p == 3:
            expr_terms.append(f"{c:.8f}f * x * x * x")
        else:
            expr_terms.append(f"{c:.8f}f * pow(x, {p})")

    print(" + ".join(expr_terms) + ";")
    print("    return y;")
    print("}")
    print("\n// Call y_from_x(x).")


if __name__ == "__main__":
    fit_pewpew()
