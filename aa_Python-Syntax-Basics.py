#Print statements
print("Applesauce")
print(1, 2, 3, sep=' < ') #OUTPUT: 1 < 2 < 3



#Functions
def least_difference(a, b, c):
    """Return the smallest difference between any two numbers
    among a, b and c.
    
    >>> least_difference(1, 5, -5)
    4
    """ #<< "docstring", text that shows when using help() for a function
    diff1 = abs(a - b)
    diff2 = abs(b - c)
    diff3 = abs(a - c)
    return min(diff1, diff2, diff3)

print(least_difference(527, 78, 639))

def greet(who="Colin"):
    print("Hello,", who)
    
greet() #OUTPUT(default): Hello, Collin
greet(who="Kaggle") #OUTPUT: Hello, Kaggle
# (In this case, we don't need to specify the name of the argument, because it's unambiguous.)
greet("world") #Hello, world


#Functions within Functions
def mult_by_five(x):
    return 5 * x

def call(fn, arg):
    """Call fn on arg"""
    return fn(arg)

def squared_call(fn, arg):
    """Call fn on the result of calling fn on arg"""
    return fn(fn(arg))

print(
    call(mult_by_five, 1),
    squared_call(mult_by_five, 1), 
    sep='\n', # '\n' is the newline character - it starts a new line
)


# Splitting & Joining Strings
datestr = "1998-11-04"
year, month, day = datestr.split('-')
print("Year: ", year)
print("Month: ", month)
print("Day: ", day)

print('/'.join([month, day, year]))


#Help/Quick Documentation
help(round)
help(least_difference)
