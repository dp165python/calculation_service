import operator

def get_operation(sign):
    operators = {
        '+':operator.add,
        '-':operator.sub,
        '*':operator.mul,
    }
    return operators.get(sign)

print(get_operation('+')(2,3))