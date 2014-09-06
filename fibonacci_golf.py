def fibgolf(type,num):
    values, coefficients = {
        "fibonacci": ([0, 1], [1, 1]),
        "tribonacci": ([0, 1, 1], [1, 1, 1]),
        "lucas": ([2, 1], [1, 1]),
        "jacobsthal": ([0, 1], [1, 2]),
        "pell": ([0, 1], [1, 2]),
        "perrin": ([3, 0, 2], [0, 1, 1]),
        "padovan": ([0, 1, 1], [0, 1, 1])
    }[type]
    while len(values) <= num:
        values.append(sum([a*b for a, b in zip(coefficients, values[::-1])]))

    return values[num]
