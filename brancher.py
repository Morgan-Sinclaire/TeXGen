import random
import numpy as np
import pandas as pd

# Takes a function that generates a string and an indicator.
# Returns LaTeX around string, as well as indicator
def tex_poly(f):
    expr,indic = f()
    # expr = expr.replace("x^0", "").replace("^1 ", " ")
    # expr = expr.replace("- -", "+ ").replace("+ -", "- ")
    multiline = len(expr) > 100

    s = ''
    s += r"\documentclass{article}"
    s += '\n' + r"\usepackage[utf8]{inputenc}"
    s += '\n' + r"\usepackage{amsmath}"

    if multiline:
        s += '\n' + r"\usepackage{breqn}"

    s += '\n\n' + r"\begin{document}"
    s += '\n\n' + r"\pagenumbering{gobble}" + '\n\n'
    if multiline:
        s += r"\begin{dmath*}"
    else:
        s += r"\begin{equation*}"
    s += '\n' + expr + '\n'
    if multiline:
        s += r"\end{dmath*}"
    else:
        s += r"\end{equation*}"
    s += '\n\n' + r"\end{document}"
    return s,indic



# Creates a polynomial with random exponents, coefficients, and number of terms
# Returns it as a TeX-friendly string
def brancher():
    p = .55
    if random.random() < p:
        sig = np.random.poisson(.223)
        if sig == 0:
            coeff = int(round(random.gauss(0, 10)))
        else:
            coeff = round(random.gauss(0, 10), sig)
        exponent = np.random.poisson(5)
        return str(coeff) + "x^{" + str(exponent) + "}"
    else:
        if random.random() < .5:
            return brancher(p) + " + " + brancher(p)
        else:
            return brancher(p) + " - " + brancher(p)

# Creates a quadratic of the form ax^{2} + bx + c
# Returns it as a TeX-friendly string, as well as the sign of the first coefficient
def quad():
    a,b,c = [(int(random.gauss(0, 10))) for i in range(3)]
    var = "x" #random.choice(("x", "m", "t"))
    expr = "{}{}^{{2}} + {}{} + {}".format(a,var,b,var,c)
    pos = int(a>0)
    return expr,pos

# Returns a random Greek symbol, as well as an index indicating which symbol was picked
# symbols = map(lambda x: x[:-1], "\gamma, \Gamma, \pi, \Pi, \phi, \mu, \Phi,".split())
df = pd.read_csv("greek.csv", header=None)
symbols = []
for i in xrange(df.shape[0]):
    symbols += df.iloc[i,0].split()

def symbol():
    index = random.randrange(len(symbols))
    indic = np.zeros(len(symbols))
    indic[index] = 1
    return symbols[index], indic
