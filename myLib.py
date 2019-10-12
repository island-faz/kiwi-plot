#!/usr/bin/env python

"""myLib.py: some functions."""

__author__      = "Amine BOURHIME"
__copyright__   = "Copyright 2018, kiwi-Plot Project"
__version__     = "1.0.1"
__email__       = "bourhime_amine@hotmail.fr"
__date__        = "7/12/2018"

import math

def is_number(str):
    try:
        Number = float(str) - 0
        return True
    except:
        return False

def add2(a, b):
    return a + b

def sub2(a, b):
    return a - b

def div2(a, b):
    try:
        return a / b
    except:
        return None

def mul2(a, b):
    return a * b

def mod2(a, b):
    try:
        return a % b
    except:
        return None

def pow2(a, b):
    try:
        tmp = a ** b
        if (is_number(tmp)):
            return tmp
    except:
        return None
#    return -(math.sqrt(tmp.imag ** 2 + tmp.real ** 2))

def mullNeg(a):
    return -a

def myCos(a):
    return math.cos(a)

def mySin(a):
    return math.sin(a)

def myTan(a):
    try:
        return math.tan(a)
    except:
        return None

def myExp(a):
    try:
        return math.exp(a)
    except:
        return None

def mySqrt(a):
    try:
        return math.sqrt(a)
    except:
        return None

def mullPlus(a):
    return a

def myAbs(a):
    return math.fabs(a)

def myLog(a):
    try:
        return math.log(a)
    except:
        return None

def myAcos(a):
    try:
        return math.acos(a)
    except:
        return None

def myAsin(a):
    try:
        return math.asin(a)
    except:
        return None

def myAtan(a):
    try:
        return math.atan(a)
    except:
        return None

def myAcosh(a):
    try:
        return math.acosh(a)
    except:
        return None

def myAsinh(a):
    try:
        return math.asinh(a)
    except:
        return None

def myAtanh(a):
    try:
        return math.atanh(a)
    except:
        return None

def myCosh(a):
    try:
        return math.cosh(a)
    except:
        return None

def mySinh(a):
    try:
        return math.sinh(a)
    except:
        return None

def myTanh(a):
    try:
        return math.tanh(a)
    except:
        return None

def myGamma(a):
    try:
        return math.gamma(a)
    except:
        return None

def myLgamma(a):
    try:
        return math.lgamma(a)
    except:
        return None

def myErf(a):
    return math.erf(a)

def myErfc(a):
    return math.erfc(a)