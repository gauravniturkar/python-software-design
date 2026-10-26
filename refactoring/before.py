"""
BEFORE REFACTORING: a real-looking messy function.

It WORKS, but it's hard to read and risky to change:
  - unclear names (t, a, d, r)
  - magic numbers (0.5, 0.8, 50...)
  - deep nesting
  - the same "apply discount" logic repeated
"""


def calc(t, a, d, r):
    # t = ticket type, a = age, d = day, r = is_recliner_seat
    p = 0
    if t == "2d":
        p = 200
        if a < 12:
            p = p * 0.5
        else:
            if a >= 60:
                p = p * 0.8
        if d == "tue":
            p = p - 50
    elif t == "3d":
        p = 300
        if a < 12:
            p = p * 0.5
        else:
            if a >= 60:
                p = p * 0.8
        if d == "tue":
            p = p - 50
    elif t == "imax":
        p = 450
        if a < 12:
            p = p * 0.5
        else:
            if a >= 60:
                p = p * 0.8
    else:
        return -1
    if r:
        p = p + 150
    if p < 0:
        p = 0
    return p


if __name__ == "__main__":
    print(calc("2d", 30, "mon", False))
    print(calc("3d", 8, "tue", True))
    print(calc("imax", 65, "tue", False))
    print(calc("4dx", 30, "mon", False))
