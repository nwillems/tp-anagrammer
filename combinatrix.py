
from collections import Counter

def subtract_string(op1, op2):
    res = op1 # Possibly more thourough copy?
    for char in op2:
        idx = res.index(char)
        res = res[:idx] + res[idx+1:]
    return res

def subtract2(op1, op2):
    remaining = Counter(op2)
    out = []
    for char in op1:
        if remaining[char]:
            remaining[char] -= 1
        else:
            out.append(char)
    return "".join(out)

def tests():
    import timeit

    print("Subtract_string, test cases:")
    print("sub({}, {}) = {}".format("abe", "ab", subtract_string("abe", "ab")))
    print("sub({}, {}) = {}".format(
        "poultry outwits ants", "trustpilot", 
        subtract_string("poultry outwits ants", "trustpilot")))
    print("sub({}, {}) = {}".format("abe", "ab", subtract2("abe", "ab")))
    print("sub({}, {}) = {}".format(
        "poultry outwits ants", "trustpilot", 
        subtract2("poultry outwits ants", "trustpilot")))

    t0 = timeit.timeit(lambda: subtract_string("poultry outwits ants", "trustpilot"), number=10000)
    t1 = timeit.timeit(lambda: subtract2("poultry outwits ants", "trustpilot"), number=10000)
    print(t0)
    print(t1)

def main():
    pass

if __name__ == "__main__":
    tests()
