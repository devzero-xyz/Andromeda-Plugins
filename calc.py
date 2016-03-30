import irc.client as irclib
from utils import add_cmd
import utils

from fractions import Fraction
from decimal import Decimal
import math, re

import sys
sys.setrecursionlimit(20000) #Totally safe BTW (Not being sarcastic)

name = "calc"
commands = ["calc"]

def asin2(x):
    return math.degrees(math.asin(x))
def acos2(x):
    return math.degrees(math.acos(x))
def atan2(x):
    return math.degrees(math.atan(x))
def asinh2(x):
    return math.degrees(math.asinh(x))
def acosh2(x):
    return math.degrees(math.acosh(x))
def atanh2(x):
    return math.degrees(math.atanh(x))
    
def sin2(x):
    return math.sin(math.radians(x))
def cos2(x):
    return math.cos(math.radians(x))
def tan2(x):
    return math.tan(math.radians(x))
def sinh2(x):
    return math.sinh(math.radians(x))
def cosh2(x):
    return math.cosh(math.radians(x))
def tanh2(x):
    return math.tanh(math.radians(x))




constants = {
    "pi":"3.1415926535897932384626433",
    "K":"9000000000",
    "E":"2.7182818284590452353602874713527",
    "G":"6.67408 * 10**-11",
    "e_charge":"1.60217662*10**-19", #Elementary charge
    "phi":"1.61803398874989484820458683436563811",
    
    "mprot":"1.6726219 * 10**-27", #Masses in kg
    "mneut":"1.674929 * 10**-27",
    "melec":"9.109390 * 10**-31",
    
}

def fact(n):
    try:
        if n < 0:
            raise ArithmeticError("You cannot have negative factorial.")
        elif n==0 or n==1:
            return 1
        return n*fact(n-1)
    except: raise ArithmeticError("Factorial too large.")

def double_fact(n):
    try:
        if n < 0:
            return 1
        elif n==0 or n==1:
            return 1
        return n*double_fact(n-2)
    except: raise ArithmeticError("Factorial too large.")
    
def phraseMath(m,modes=""):
    if "the meaning of life" in m:
        return 42
    elif "my ass" in m:
        return ":C"
    elif "windows" in m:
        return 0
    
    modes = modes.split(",")
    display = "NORMAL"; trig = "DEG"; truncate = 25
    if "SCI" in modes:
        display = "SCI"
    elif "FRACT" in modes:
        display = "FRACT"
    if "DEG" in modes:
        trig = "DEG"
    
    #Replace constants
    for c in constants:
        m = m.replace(c,"{}".format(constants[c]))
        
    m = m.replace("^","**")
    m = m.replace("_","").replace("import","")
    
    #Change double factorials, ie 5!! -> double_fact(5)
    p = re.compile('(-?\d+)!!'); subst = "double_fact(\1)"
    m = re.sub(p, subst, m)
    #Change factorials, ie 5! -> fact(5)
    p = re.compile('(-?\d+)!'); subst = "fact(\1)"
    m = re.sub(p, subst, m)
    
    m = m.replace("||"," or ").replace("|"," or ")
    m = m.replace("&&"," and ").replace("&"," and ")

    #AND WIKIPEDIA https://en.wikipedia.org/wiki/List_of_mathematical_symbols_by_subject combinatorics
    #Also npr and stuff
    
    #Converts e notation, ie 2e9 to 2 * 10**9, because errors and stuff
    p = re.compile('([:]?\d*\.\d+|\d+)e([-+]?)([-+]?\d*\.\d+|\d+)'); subst = "\1 * 10**\2\3"
    m = re.sub(p, subst, m)
    
    #Fixes functions
    p = re.compile('(sin\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(cos\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(tan\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(asin\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(acos\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(atan\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(sinh\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(cosh\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(tanh\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(asinh\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(acosh\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(atanh\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)

    p = re.compile('(pow\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(abs\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(sqrt\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(log\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(ceil\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(floor\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(exp\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(log10\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(degrees\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(deg\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(radians\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)
    p = re.compile('(rad\([^)]*\))'); subst = "Decimal(\1)"; m = re.sub(p, subst, m)

    #Converts all remaining numbers into decimals
    p = re.compile('([:]?\d*\.\d+|\d+)'); subst = "Decimal(\1)"
    m = re.sub(p, subst, m)

    safe_dict = {}
    if trig == "DEG":
        safe_dict["sin"] = sin2
        safe_dict["cos"] = cos2
        safe_dict["tan"] = tan2
        safe_dict["asin"] = asin2
        safe_dict["acos"] = acos2
        safe_dict["atan"] = atan2
        
        safe_dict["sinh"] = sinh2
        safe_dict["cosh"] = cosh2
        safe_dict["tanh"] = tanh2
        safe_dict["asinh"] = asinh2
        safe_dict["acosh"] = acosh2
        safe_dict["atanh"] = atanh2
    else:
        safe_dict["sin"] = math.sin
        safe_dict["cos"] = math.cos
        safe_dict["tan"] = math.tan
        safe_dict["asin"] = math.asin
        safe_dict["acos"] = math.acos
        safe_dict["atan"] = math.atan
        
        safe_dict["sinh"] = math.sinh
        safe_dict["cosh"] = math.cosh
        safe_dict["tanh"] = math.tanh
        safe_dict["asinh"] = math.asinh
        safe_dict["acosh"] = math.acosh
        safe_dict["atanh"] = math.atanh
    
    safe_dict["pow"] = math.pow
    safe_dict["sqrt"] = math.sqrt
    safe_dict["abs"] = abs
    safe_dict["log"] = math.log
    safe_dict["fact"] = fact
    safe_dict["factorial"] = fact
    safe_dict["double_fact"] = double_fact
    safe_dict["ceil"] = math.ceil
    safe_dict["floor"] = math.floor
    safe_dict["exp"] = math.exp
    safe_dict["log10"] = math.log10
    
    safe_dict["deg"] = math.degrees
    safe_dict["rad"] = math.radians
    safe_dict["degrees"] = math.degrees
    safe_dict["radians"] = math.radians
    
    safe_dict["Decimal"] = Decimal
    safe_dict["Fraction"] = Fraction

    result = eval(m, {"__builtins__": None}, safe_dict)
    
    if display == "SCI":
        try: return '%.{}E'.format(truncate) % result
        except: return result
    elif display == "FRACT":
        try: return Fraction(result)
        except: return result
    return result

@add_cmd
def calc(irc, event, args):
    if len(args) > 0:
        text = " ".join(args)
        """Calculates math"""
        try:
            options = text.split(" ")[-1]
            if "DEG" in options or "SCI" in options or "FRACT" in options or "RAD" in options:
                text = text.replace(options,"")
            result = phraseMath(text, options)
            returned = "\x02Answer: \x0f" + str(result)[:350]
            if len(str(result)) > 350:
                returned = returned + "..."
            irc.reply(event,  returned)
        except ZeroDivisionError:
            irc.reply(event,  "\x02\x034Error: \x0fCannot divide by zero.")
        except OverflowError:
            irc.reply(event,  "\x02\x034Error: \x0fNumber overflowed.")
        except ArithmeticError:
            irc.reply(event,  "\x02\x034Error: \x0fNumber undefined or too large.")
        except ValueError:
            irc.reply(event,  "\x02\x034Error: \x0fMath Domain Error.")
        except Exception as e:
            irc.reply(event,  "\x02\x034Error: \x0fCould not understand input.")
            

