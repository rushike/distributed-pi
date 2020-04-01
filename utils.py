import collections
def print_dict(di, p = True):
    # sort = collections.OrderedDict(sorted(di.items()))
    st = ''
    for k in sorted(di.keys()):
        st += str(di[k])
    if p: 
        print("HEX : ", st)
        tofile("hex.txt", st)
        ds = pidecimal(st)
        tofile("dec.txt", str(ds))
        print("DEC : ", ds)
    return st 

def pidecimal(st):
    M = len(st)
    SS = 16 ** M
    d = int("0x" + st, 16)
    d *= (10 ** (M)) 
    d //= (16 ** (M - 1)) 
    return d    

def tofile(fl, st):
    with open(fl, 'w') as f:
        f.write(st)