#!/usr/bin/env python

"""kiwiCore.py: main functions for kiwiPlot."""

__author__      = "Amine BOURHIME"
__copyright__   = "Copyright 2018, kiwi-Plot Project"
__version__     = "1.0.1"
__email__       = "bourhime_amine@hotmail.fr"
__date__        = "7/12/2018"

try:
    from PIL import ImageFont
except:
    print("please try to install PIL dependency for python")
    exit()

from myLib import *

parseError = None

def calc(left, right, op, _x):
    list = [["+", add2], ["-", sub2], ["/", div2],
            ["*", mul2], ["%", mod2], ["^", pow2]]

    neg = 1
    if (op == "^" and left[0] == '-'):
        left = left[1: len(left)]
        neg = -1

    for item in list:
        if (op == item[0]):
            op2 = item[1]
            break;

    if (is_number(left)):
        left = float(left)
    else:
        left = parse(left, _x)
        if (left == None):
            return None
    if (is_number(right)):
        right = float(right)
    else:
        right = parse(right, _x)
        if (right == None):
            return None
    tmp = op2(left, right)
    if (tmp == None):
        return None
    return  tmp * neg

def calcFunc(exp, func, _x):
    global parseError

    func2 = None
    list = [["+", mullPlus], ["-", mullNeg], ["cos", myCos], ["sin", mySin],
    ["tan", myTan], ["exp", myExp], ["sqrt", mySqrt], ["abs", myAbs],
    ["log", myLog], ["acos", myAcos], ["asin", myAsin], ["atan", myAtan],
    ["acosh", myAcosh], ["asinh", myAsinh], ["atanh", myAtanh], ["cosh", myCosh],
    ["sinh", mySinh], ["tanh", myTanh], ["gamma", myGamma], ["erf", myErf],
    ["erfc", myErfc], ["lgamma", myLgamma]]

    for item in list:
        if (func == item[0]):
            func2 = item[1]
            break;

    if (func2 == None):
        if (func[0] == '+'):
            return (calcFunc(exp, func[1: len(func)], _x))
        elif (func[0] == '-'):
            tmp = calcFunc(exp, func[1: len(func)], _x)
            if is_number(tmp):
                return -tmp
            return None

    if (func2 == None): # Synstax error, bad function (func not defined)
        parseError = ("function '%s' is not defined"%(func))
        return None

    if (is_number(exp)):
        return (func2(float(exp)))
    res = parse(exp, _x)
    if (res == None):
        return None
    return (func2(res))

def is_op(c):
    if (c == '+' or c == '-' or c == '*' or c == '/' or c == '%' or c == '^'):
        return True
    return False

def parse(exp, _x):
    global parseError

    if (len(exp) == 0):
        parseError = ("Empty expression")
        return None
    i = 0
    _len = len(exp)
    parenthesis = 0
    parenthesisFlag = False
    parantehsisIndexStart = 0
    parantehsisIndexEnd = 0
    powerFlag = False
    mulDivIndex = 0
    addSubIndex = 0
    powIndex = 0
    while (i < _len):
        if (exp[i] == '('):
            parenthesis += 1
            if (parenthesisFlag == False):
                parantehsisIndexStart = i
                parenthesisFlag = True
        elif (exp[i] == ')'):
            parenthesis -= 1
            parantehsisIndexEnd = i
        elif (parenthesis == 0 and i > 0 and (exp[i] == '+' or exp[i] == '-')
            and is_op(exp[i - 1]) == False):
            addSubIndex = i
        elif (parenthesis == 0 and (exp[i] == '/' or exp[i] == "*" or exp[i] == '%')):
            mulDivIndex = i
        elif (parenthesis == 0 and exp[i] == '^' and powerFlag == False):
            powIndex = i
            powerFlag = True
        i += 1

    if (parenthesis != 0):
        parseError = "unmatched parentheses"
        return None

    tmpIndex = None
    if (addSubIndex != 0):
        tmpIndex = addSubIndex
    elif (mulDivIndex != 0):
        tmpIndex = mulDivIndex
    elif (powIndex != 0):
        tmpIndex = powIndex

    if (tmpIndex != None):
        left = exp[0:tmpIndex]
        right = exp[tmpIndex+1:_len]
        return calc(left, right, exp[tmpIndex], _x)

    elif (parantehsisIndexEnd != 0):
        if (parantehsisIndexStart != 0):
            return (calcFunc(exp[parantehsisIndexStart+1:parantehsisIndexEnd], exp[0: parantehsisIndexStart], _x))
        else:
            return parse(exp[parantehsisIndexStart+1:parantehsisIndexEnd], _x)

    if (is_number(exp)):
        return float(exp)
    if (exp == "x"):
        return _x
    elif (exp == "pi"):
        return math.pi
    elif (exp == "e"):
        return math.exp(1)
    elif (exp[0] == "-"):
        tmp = parse(exp[1:_len], _x)
        if (tmp != None):
            return mullNeg(tmp)
    elif (exp[0] == "+"):
        return parse(exp[1:_len], _x)
    parseError = ("'%s' is not defined"%(exp))
    return None

def evalExp(exp, _x):
    global parseError

    parseError = None
    _exp = exp.replace(" ", "")
    _exp = _exp.replace("\n", "")
    if (_exp == ""):
        parseError = "Empty expression"
        return False

    _exp = _exp.replace(")(", ")*(")
    _exp = _exp.lower()

    try:
        res = parse(_exp, _x)
    except:
        return None
    if (res != None):
        return (-res)
    if (parseError != None):
        return False # parse Error
    return None # Domaine def Error

def draw_grid(draw, rangeX, rangeY, W, H):
    scaleX = (W) / (rangeX[1] - rangeX[0])
    scaleY = (H) / (rangeY[1] - rangeY[0])

    rgb = (211, 211, 211)

    tmp_l = 10 ** (len(str(rangeX[1] - rangeX[0] - 1)) - 1)

    j = rangeX[0]
    while (j < rangeX[1]):
        tmp = scaleX * (j - rangeX[0])
        if (j % tmp_l == 0):
            draw.line((tmp, 0, tmp, H), rgb)
            j += tmp_l
        else:
            j += 1

    tmp_l = 10 ** (len(str(rangeY[1] - rangeY[0] - 1)) - 1)

    j = rangeY[0]
    k = rangeY[1]
    while (j < rangeY[1]):
        tmp = scaleY * (j - rangeY[0])
        if (k % tmp_l == 0):
            draw.line((0, tmp, W, tmp), rgb)
            j += tmp_l
            k -= tmp_l
        else:
            j += 1
            k -= 1            

def draw_thick_marks(draw, rangeX, rangeY, W, H):
    scaleX = (W) / (rangeX[1] - rangeX[0])
    scaleY = (H) / (rangeY[1] - rangeY[0])

    j = rangeX[0]
    rgb = (0, 0, 0)
    thickMarkLen = 10
    tmp_l = 10 ** (len(str(rangeX[1] - rangeX[0] - 1)) - 1)
    while (j < rangeX[1]):
        tmp = scaleX * (j - rangeX[0])
        tmp2 = (scaleY / 2) * (rangeY[1] + rangeY[0])
        tmp3 = H / 2
        tmp4 = W / 2
        if (j % tmp_l == 0):
            draw.line((tmp, tmp3 - thickMarkLen + tmp2, tmp, tmp3 + thickMarkLen + tmp2), rgb)
            _str = str(j)
            draw.text((tmp - (5*len(_str))//2, tmp3 + thickMarkLen + tmp2), _str, fill=(255,0,0))
            j += tmp_l
        else:
            j += 1

    j = rangeY[0]
    k = rangeY[1]
    tmp_l = 10 ** (len(str(rangeY[1] - rangeY[0] - 1)) - 1)
    while (j < rangeY[1]):
        tmp = scaleY * (j - rangeY[0])
        tmp2 = (scaleX / 2) * (rangeX[1] + rangeX[0])
        if (k % tmp_l == 0):
            draw.line((W/2 - thickMarkLen - tmp2, tmp, W/2 + thickMarkLen - tmp2, tmp), rgb)
            _str = str(k)
            draw.text((W/2 - thickMarkLen - tmp2 - (10*len(_str)), tmp - 5), _str, fill=(255,0,0))
            j += tmp_l
            k -= tmp_l
        else:
            j += 1
            k -= 1

def draw_axis(draw, rangeX, rangeY, W, H):
    rgb = (0, 0, 0)

    scaleX = (W) / (rangeX[1] - rangeX[0])
    scaleY = (H) / (rangeY[1] - rangeY[0])

    tmp = scaleX * (-rangeX[0])
    draw.line((tmp, 0, tmp, H), rgb)

    tmp = scaleY * rangeY[1]
    draw.line((0, tmp, W, tmp), rgb)

def plot_function(draw, _exp, rangeX, rangeY, pointsNbr, W, H, plot_points):
    global parseError

    inc = (rangeX[1] - rangeX[0]) / pointsNbr

    scaleX = (W) / (rangeX[1] - rangeX[0])
    scaleY = (H) / (rangeY[1] - rangeY[0])

    rgb = (0, 0, 0)

    deltaX = W/(rangeX[1] - rangeX[0])
    tmp = H/(rangeY[1] - rangeY[0])

    tmp_ex = deltaX * -rangeX[0]
    tmp_ey = tmp * -rangeY[0]

    i = rangeX[0]

    x1 = i * scaleX + tmp_ex
    y1 = evalExp(_exp, i)

    if (type(y1) is bool and y1 == False):
        return
    elif (y1 != None):
        y1 *= scaleY
        y1 = H + y1 - tmp_ey

    draw_grid(draw, rangeX, rangeY, W, H)
    draw_thick_marks(draw, rangeX, rangeY, W, H)
    draw_axis(draw, rangeX, rangeY, W, H)

    tmp_v = H - tmp_ey

    i += inc
    while (i <= rangeX[1]):
        x2 = i * scaleX + tmp_ex
        y2 = evalExp(_exp, i)
        if (y2 != None):
            y2 *= scaleY
            y2 += tmp_v
        if (y1 != None and y2 != None and y2 - y1 < H and y1 - y2 < H):
            if (plot_points):
                draw.ellipse((x1 - 2, y1 - 1, x1 - 2 + 4, y1 + 4 - 1), fill="red", outline ='red')
            draw.line((x1, y1, x2, y2), fill=(0,0,255))
        x1,y1 = x2,y2
        i = float('%.10f' % (i + inc))
    try:
        fnt = ImageFont.truetype("arial.ttf", 12)
        draw.text((10,10), _exp, font=fnt, fill=(255,0,0))
    except:
        pass