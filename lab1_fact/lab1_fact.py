# Derek McMahon
# dmm7aj
# CS3240
#lab1_fact

def factorial1(n):
    if n < 0:
        raise ValueError("n < 0")
    else:
        if n == 0:
            return 1
        else:
            return n * factorial1(n - 1)


def factorial2(n):
    l = []
    for x in range(0, n):
        l.append(factorial1(x))
    return l


def test_fact1():
    assert 1 == factorial1(0), "factorial(0) didn't yield 1"
    assert 1 == factorial1(1), "factorial(1) didn't yield 1"
    assert 120 == factorial1(5), "factorial(5) didn't yield 1"
    try:
        print("-1! = " + str(factorial1(-1)))
    except ValueError:
        print("Factorial of a negative number is undefined.")


if __name__ == "__main__":
    test_fact1()
