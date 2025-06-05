import random

PRIME = 2**127 - 1  

def polynom(x, coefficients):
    result = 0
    for power, coeff in enumerate(coefficients):
        result += coeff * (x ** power)
    return result % PRIME

def generate_shares(secret, n, k):
    if k > n:
        raise ValueError("Threshold k must be <= number of shares n")

    coeffs = [secret] + [random.randrange(0, PRIME) for _ in range(k-1)]
    shares = []
    for i in range(1, n+1):
        x = i
        y = polynom(x, coeffs)
        shares.append((x, y))
    return shares

def lagrange_interpolation(x, x_s, y_s):
    total = 0
    k = len(x_s)
    for i in range(k):
        xi, yi = x_s[i], y_s[i]
        li = 1
        for j in range(k):
            if i != j:
                xj = x_s[j]
                li *= (x - xj) * pow(xi - xj, -1, PRIME)
                li %= PRIME
        total += yi * li
        total %= PRIME
    return total

def reconstruct_secret(shares):
    x_s, y_s = zip(*shares)
    return lagrange_interpolation(0, x_s, y_s)


