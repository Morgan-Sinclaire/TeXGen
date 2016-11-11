import random
import numpy as np


def tex_poly(p):
    b = brancher(p)
    # print b + "\n\n\n\n\n"
    b = b.replace("x^0", "").replace("^1 ", " ")
    b = b.replace("- -", "+ ").replace("+ -", "+ ")
    multiline = len(b) > 100

    s = ''
    s += r"\documentclass{article}"
    s += '\n' + r"\usepackage[utf8]{inputenc}"
    s += '\n' + r"\usepackage{amsmath}"

    if multiline:
        s += '\n' + r"\usepackage{breqn}"

    s += '\n\n' + r"\begin{document}" + '\n\n'
    if multiline:
        s += r"\begin{dmath*}"
    else:
        s += r"\begin{equation*}"
    s += '\n' + b + '\n'
    if multiline:
        s += r"\end{dmath*}"
    else:
        s += r"\end{equation*}"
    s += '\n\n' + r"\end{document}"

    return s


def brancher(p):
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
