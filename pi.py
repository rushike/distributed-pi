D = 14        # number of digits of working precision
M = 16 ** D
SHIFT = (4 * D)
MASK = M - 1

def S(j, n):
    # Left sum
    s = 0
    k = 0
    while k <= n:
        r = 8*k+j
        s = (s + (pow(16,n-k,r)<<SHIFT)//r) & MASK
        k += 1
    # Right sum
    t = 0
    k = n + 1
    while 1:
        xp = int(16**(n-k) * M)
        newt = t + xp // (8*k+j)
        # Iterate until t no longer changes
        if t == newt:
            break
        else:
            t = newt
        k += 1
    return s + t

def pi(n):
    n -= 1
    x = (4*S(1, n) - 2*S(4, n) - S(5, n) - S(6, n)) & MASK
    return "%014x" % x


def pi_(a, b):
    M = 5
    # S = (a - b) // M + 1
    s = ''
    for i in range(a, b, M):
        s += pi(i)[:M]
    
    return s[:(b - a)]