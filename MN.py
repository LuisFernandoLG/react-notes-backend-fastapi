from tabulate import tabulate

data = []

def f(x):
    return (x**3) + (2 * x**2) + (10 * x) - 20

def biseccion( xi, xs, tolerancia):
    if (not(f(xi) < 0 and f(xs) > 0) ):
        return "No se puede"

    old_xm = 0
    error = 100
    while( error >= tolerancia ):
        xm =  (xi + xs) / 2

        error = abs(((xm - old_xm) / xm)) * 100  
        Fxm = f(xi) * f(xm)

        Fxi = f(xi)
        Fxs = f(xs)

        data.append([ xi, xs, Fxi, Fxs, xm , Fxm, error])

        if (Fxm > 0 ):
            xi = xm
        else:
            xs = xm

        old_xm = xm

    print(tabulate(data, tablefmt='fancy_grid',  headers=['xi', 'xs', 'F(xi)', 'F(xs)', 'xm', "Fxm", "error" ], showindex=True))


r = biseccion(1, 2, 0.01)