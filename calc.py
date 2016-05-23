#Calc plugin by Bowserinator

from utils import *
import utils

name = "calc"
cmds = ["calc"]

@add_cmd
def calc(irc, event, args):
    """<math>
    
    Compute a mathamatical equation, accepts TRIG, factorial.
    Use SCI, FRACT and DIGIT=<prec> to change display modes and set precision.
    By Bowserinator (No remove citation!)
    """
    
    result = phraseTextMath(args)
    irc.reply(event, result)
    return
    
from decimal import Decimal
import decimal, fractions
import math, re

constants = {
    "E":"2.718281828459045235360287471352662497757247093699959574966967627724076630353547594571382178",
    "pi":"3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679",
    "K":"9000000000",
    "G":"6.67408 * 10**-11",
    "e_charge":"1.60217662*10**-19", #Elementary charge
    "phi":"1.61803398874989484820458683436563811",
    
    "mprot":"1.6726219 * 10**-27", #Masses in kg
    "mneut":"1.674929 * 10**-27",
    "melec":"9.109390 * 10**-31",
    "c":"299792458",
}

class number(object):
    def __init__(self):
        self.Number = Number

class constant(object):
    def __init__(self):
        self.constants = constants

constant = constant()

#http://people.math.sc.edu/girardi/m142/handouts/10sTaylorPolySeries.pdf
from decimal import Decimal
import math
class ComparasionError(Exception):
    pass

class Number(object):
    def __init__(self,positive,imaginary="0.0"):
        self.real = Decimal(positive)
        self.imaginary = Decimal(imaginary)
    
    def phase(self): #Returns "angle" in radians
        return math.atan2(self.imaginary, self.real)
    def polar(self): #Converts to polar
        return (abs(self), self.phase())
    def toRect(self,r,phi):
        return Number(r) * Number(math.cos(phi) , math.sin(phi))
        
    def exp(self): #Returns e**x
        e = Decimal(constant.constants["E"])
        if self.imaginary == 0:
            return Number(e**(self.real),0)
        return Number(e**(self.real) * Decimal(math.cos(self.imaginary)), e**(self.real) * Decimal(math.sin(self.imaginary)))
    def conj(self):
        return Number(self.real,-self.imaginary)
        
    def floor(self):
        return Number(self.real.to_integral(), self.imaginary.to_integral())
        
    def ceil(self):
        return Number(math.ceil(self.real),math.ceil(self.imaginary))
        
    #Trig and log/log10/ln
    #http://mathonweb.com/help_ebook/html/complex_funcs.htm
    def ln(self):
        if self.imaginary == 0:
            try: return Number(math.log(self.real))
            except: pass
        p = self.polar()
        return Number(math.log(p[0]), p[1])
        
    def log(self,x=10):
        if self.imaginary == 0:
            try: return Number(math.log(self.real,x))
            except: pass
        p = self.polar()
        return Number(math.log(p[0],x), p[1])
        
    def log10(self):
        if self.imaginary == 0:
            return Number(math.log10(self.real))
        return Number(self.ln() / Number(math.log(10)))
        
    def sin(self):
        if self.imaginary == 0:
            return Number(math.sin(self.real))
        try: return Number(math.sin(self.real) * math.cosh(self.imaginary), math.cos(self.real) * math.sinh(self.imaginary))
        except: return Number("inf")
        
    def cos(self):
        if self.imaginary == 0:
            return Number(math.cos(self.real))
        try: return Number(math.cos(self.real) * math.cosh(self.imaginary), -math.sin(self.real) * math.sinh(self.imaginary))
        except: return Number("inf")
    
    def tan(self):
        try: return self.sin() / self.cos()
        except: return Number("inf")
        
    def acos(self):
        if self.imaginary == 0:
            return Number(math.acos(self))
        A = Number(((Decimal(1) + self.real)**Decimal(2) + self.imaginary**Decimal(2))**Decimal(0.5) - ((Decimal(1) - self.real)**Decimal(0.5) + self.imaginary**Decimal(2))**Decimal(0.5)) / Number(2)
        B = Number(((Decimal(1) + self.real)**Decimal(2) + self.imaginary**Decimal(2))**Decimal(0.5) + ((Decimal(1) - self.real)**Decimal(0.5) + self.imaginary**Decimal(2))**Decimal(0.5)) / Number(2)
        return Number(A.acos(), -(B+(B*B - Number(1))**Number(0.5)).ln() )
        
    def asin(self):
        if self.imaginary == 0:
            return Number(math.asin(self))
        A = Number(((Decimal(1) + self.real)**Decimal(2) + self.imaginary**Decimal(2))**Decimal(0.5) - ((Decimal(1) - self.real)**Decimal(0.5) + self.imaginary**Decimal(2))**Decimal(0.5)) / Number(2)
        B = Number(((Decimal(1) + self.real)**Decimal(2) + self.imaginary**Decimal(2))**Decimal(0.5) + ((Decimal(1) - self.real)**Decimal(0.5) + self.imaginary**Decimal(2))**Decimal(0.5)) / Number(2)
        return Number(A.asin(), (B+(B*B - Number(1))**Number(0.5)).ln() )
    
    def atan(self):
        result = (Number(0,1)+self) / (Number(0,1) - self)
        return Number(0,0.5) * result.ln()
        
    def cosh(self):
        if self.imaginary == 0:
            return Number(math.cosh(self.real))
        try: return Number(math.cosh(self.real) * math.cos(self.imaginary), math.sinh(self.real) * math.sin(self.imaginary))
        except: return Number("inf")
        
    def sinh(self):
        if self.imaginary == 0:
            return Number(math.sinh(self.real))
        try: return Number(math.sinh(self.real) * math.cos(self.imaginary), math.cosh(self.real) * math.sin(self.imaginary))
        except: return Number("inf")
        
    def tanh(self):
        try: return self.sinh() / self.cosh()
        except: return Number("inf")
        
    def acosh(self):
        returned = self + (self*self - Number(1))**0.5
        return returned.ln()
        
    def asinh(self):
        returned = self + (self*self + Number(1))**0.5
        return returned.ln()
    def atanh(self):
        a = (Number(1)+self).ln() - (Number(1)-self).ln()
        return Number(0.5) * a
        
    #Builtin functions
    def __str__(self):
        if self.imaginary == 0:
            return str(self.real)
        return (str(self.real)+"+"+str(self.imaginary)+"i").replace("+-","-")
        
    def __abs__(self):
        return (self.real**2 + self.imaginary**2).sqrt()
    def __add__(self,other):
        return Number(self.real+other.real, self.imaginary+other.imaginary)
    def __sub__(self,other):
        return Number(self.real-other.real, self.imaginary-other.imaginary)
    def __mul__(self,other):
        if self.imaginary == 0 and other.imaginary == 0:
            return Number(self.real*other.real,"0")
        return Number( self.real*other.real - self.imaginary*other.imaginary,self.real*other.imaginary + self.imaginary*other.real )
    def __div__(self,other):
        if self.imaginary == 0 and other.imaginary == 0:
            return Number(self.real/other.real,"0")
        a = (self.real*other.real + self.imaginary*other.imaginary)/(other.real*other.real + other.imaginary*other.imaginary)
        b = (self.imaginary*other.real - self.real*other.imaginary)/(other.real*other.real + other.imaginary*other.imaginary)
        return Number(a,b)
    def __truediv__(self,other):
        if self.imaginary == 0 and other.imaginary == 0:
            return Number(self.real/other.real,"0")
        a = (self.real*other.real + self.imaginary*other.imaginary)/(other.real*other.real + other.imaginary*other.imaginary)
        b = (self.imaginary*other.real - self.real*other.imaginary)/(other.real*other.real + other.imaginary*other.imaginary)
        return Number(a,b)
    def __neg__(self):
        return Number(-self.real,-self.imaginary)
    def __pos__(self):
        return Number(self.real,self.imaginary)
    def __inverse__(self):
        return Number(1)/self
    def __mod__(self,other):#a%b = a + b * ciel(-a/b) 
        return self+ other* ((-self/other).ceil())
    def __pow__(self,other):
        if other.imaginary == 0:
            polar = self.polar()
            return self.toRect(Decimal(polar[0])**other.real, Decimal(polar[1])*other.real)
        elif other.real == 0:
            a = Number(self.real); b = Number(self.imaginary)
            c = Number(other.real); d = Number(other.imaginary)
            x = (-d * (b/a).atan()).exp() * ((a*a+b*b).ln() * d / Number(2)).cos() 
            y = Number(0,1) * (-d * (b/a).atan()).exp() * ((a*a+b*b).ln() * d / Number(2)).sin()
            return x+y

        b = other.real; c = other.imaginary
        #a^(b+c) = a^b * a^ci
        return self**(Number(b)) * self**(Number(0,1) * Number(c))
  
    def __complex__(self):
        return complex(float(self.real),float(self.imaginary))
    def __int__(self):
        return int(self.real)
    def __float__(self):
        return float(self.real)
    
    #Comparasions
    def __lt__(self,other): #>
        if self.imaginary != 0 or other.imaginary != 0:
            raise ComparasionError("Complex comparasion is not supported")
        return self.real < other.real
        
    def __le__(self,other): #>=
        if self.imaginary != 0 or other.imaginary != 0:
            raise ComparasionError("Complex comparasion is not supported")
        return self.real <= other.real
        
    def __eq__(self,other): #==
        if self.real == other.real and self.imaginary == other.imaginary:
            return True
        return False
    def __ne__(self,other): #!=
        return not self.__eq__(other)
        
    def __gt__(self,other): #<
        if self.imaginary != 0 or other.imaginary != 0:
            raise ComparasionError("Complex comparasion is not supported")
        return self.real > other.real
        
    def __ge__(self,other): #<=
        if self.imaginary != 0 or other.imaginary != 0:
            raise ComparasionError("Complex comparasion is not supported")
        return self.real >= other.real
    
number = number()


import sys
sys.setrecursionlimit(20000)

def log(n,x):return n.log(x)
def phase(n):return n.phase()
def exp(n):return n.exp()
def floor(n):return n.floor()
def ceil(n):return n.ceil()
def ln(n):return n.ln()
def log10(n):return n.log10()

def sin(n):return n.sin()
def cos(n):return n.cos()
def tan(n):return n.tan()
def asin(n):return n.asin()
def acos(n):return n.acos()
def atan(n):return n.atan()
def sqrt(n): return n**number.Number(0.5)

def sinh(n):return n.sinh()
def cosh(n):return n.cosh()
def tanh(n):return n.tanh()
def asinh(n):return n.asinh()
def acosh(n):return n.acosh()
def atanh(n):return n.atanh()

def radian(n):
    return n * number.Number(constant.constants["pi"]) / number.Number(180)
def degree(n):
    return n * number.Number(180) / number.Number(constant.constants["pi"])
    
def factorial(n):
    if n.imaginary != 0:
        raise ArithmeticError("You cannot have imaginary factorial.")
    if n < number.Number(0): raise ArithmeticError("You cannot have negative factorial.")
    if n < number.Number(2): return number.Number(1)
    return n * factorial(n - number.Number(1))
    
def double_fact(n):
    if n.imaginary != 0:
        raise ArithmeticError("You cannot have imaginary factorial.")
    if n < number.Number(0): raise ArithmeticError("You cannot have negative factorial.")
    if n < number.Number(2): return number.Number(1)
    return n * (double_fact(n-number.Number(2)))
    
def computeEquation(m,modes=""):
    if "the meaning of life" in m: return number.Number(42)
    
    #Replace the constants
    for c in constant.constants:
        m = m.replace(c,constant.constants[c])
    m = m.replace("^","**")
    m = m.replace("_","").replace("import","").replace("decode","").replace("encode","").replace("open","")
    
    #Change double factorials, ie 5!! -> double_fact(5)
    p = re.compile('(-?\d+)!!'); subst = "double_fact(\1)"; m = re.sub(p, subst, m)
    p = re.compile('\((.?)\)!!'); subst = "double_fact(\1)"; m = re.sub(p, subst, m)
    #Change factorials, ie 5! -> fact(5)
    p = re.compile('(-?\d+)!'); subst = "factorial(\1)"; m = re.sub(p, subst, m)
    p = re.compile('\((.?)\)!'); subst = "factorial(\1)"; m = re.sub(p, subst, m)
    
    m = m.replace("||"," or ").replace("|"," or ")
    m = m.replace("&&"," and ").replace("&"," and ")
    
    #Converts e notation, ie 2e9 to 2 * 10**9, because errors and stuff
    p = re.compile('([:]?\d*\.\d+|\d+)e([-+]?)([-+]?\d*\.\d+|\d+)'); subst = "\1 * 10**\2\3"
    m = re.sub(p, subst, m)
    
    m = m.replace("\x01","").replace("\x0f","").replace("\x02","")
    #Converts all remaining numbers into numbers
    p = re.compile('([:]?\d*\.\d+|\d+)'); subst = "number.Number('\1')"
    m = re.sub(p, subst, m)
    
    #Fix up i
    m = m.replace(")i",")*number.Number(0,1)")
    m = m.replace('in','@')
    p = re.compile('(?<![a-zA-Z])i'); subst = "number.Number(0,1)"
    m = re.sub(p, subst, m)
    m = m.replace("@","in")
    
    safe_dict = {}
    safe_dict["sin"] = sin
    safe_dict["cos"] = cos
    safe_dict["tan"] = tan
    safe_dict["asin"] = asin
    safe_dict["acos"] = acos
    safe_dict["atan"] = atan
    
    safe_dict["sinh"] = sinh
    safe_dict["cosh"] = cosh
    safe_dict["tanh"] = tanh
    safe_dict["asinh"] = asinh
    safe_dict["acosh"] = acosh
    safe_dict["atanh"] = atanh
    
    safe_dict["sqrt"] = sqrt
    safe_dict["abs"] = abs
    safe_dict["log"] = log10
    safe_dict["fact"] = factorial
    safe_dict["factorial"] = factorial
    safe_dict["double_fact"] = double_fact
    safe_dict["ceil"] = ceil
    safe_dict["floor"] = floor
    safe_dict["exp"] = exp
    safe_dict["log10"] = log10
    
    safe_dict["deg"] = degree
    safe_dict["rad"] = radian
    safe_dict["degrees"] = degree
    safe_dict["radians"] = radian
    safe_dict["number"] = number
    m = m.replace("\x01","").replace("\x0f","").replace("\x02","")
    result = eval(m, {"__builtins__": None}, safe_dict)
    return result
    
def phraseTextMath(text,user="",hostmask="",extra={}):
    text = " ".join(text)
    text = text.replace("\x01","").replace("\x0f","").replace("\x02","")
    showPrec = 5
    showMode = "NONE"
    for i in ["SCI","FRACT"]:
        if i in text:
            showMode = i; text = text.replace(i,"")
    r2 = re.findall("TRUNCT=([:]?\d*\.\d+|\d+)",text)
    for r in r2: showPrec = int(float(r)); text = text.replace("TRUNCT="+r,"")
    r2 = re.findall("DIGIT=([:]?\d*\.\d+|\d+)",text)
    for r in r2: showPrec = int(float(r)); text = text.replace("DIGIT="+r,"")
    if showPrec > 100 and hostmask != "unaffiliated/bowserinator":
        return "The max precision is 100 digits."
    try:
        decimal.getcontext().prec = 100
        decimal.getcontext().Emax = 500000
        decimal.getcontext().Emin = -500000
        
        text = computeEquation(text)
        if type(text) in (tuple,list):
            text = '['+', '.join( [ (format(a.real, '.{}f'.format(showPrec)) + "+" + format(a.imaginary, '.{}f'.format(showPrec)) + "i").replace("+-","-") for a in text])+']'
        elif type(text) == dict:
            return "Sorry dictionaries are currently not supported."
        else: 
            if showMode == "FRACT":
                text = "\x02Answer: \x0f" + (str(fractions.Fraction(float(text.real))) + "+" + str(fractions.Fraction(float(text.imaginary)))+ "i").replace("+-","-")
            elif showMode == "SCI":
                text = "\x02Answer: \x0f" + (str(float(text.real)) + "+" + str(float(text.imaginary))+ "i").replace("+-","-")
            elif showPrec == -1:
                text = "\x02Answer: \x0f" + str(text)
            else: text = "\x02Answer: \x0f" + (format(text.real, '.{}f'.format(showPrec)) + "+" + format(text.imaginary, '.{}f'.format(showPrec)) + "i").replace("+-","-") 
        text = text.replace('number.Number','')
        returned = text[:700]
        if len(text) > 700: returned = returned + "..."
        return returned
    except ZeroDivisionError:
        return "\x02\x034Error: \x0fCannot divide by zero."
    except OverflowError:
        return "\x02\x034Error: \x0fNumber overflowed."
    except ArithmeticError as e:
        return "\x02\x034Error: \x0f{0}".format(e)
    except ValueError:
        return "\x02\x034Error: \x0fMath Domain Error."
    except Exception as e:
        return "\x02\x034Error: \x0fCould not understand input."
    
