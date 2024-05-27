def fib(x):
#{
    global counterFunctionCalls
    counterFunctionCalls = counterFunctionCalls + 1
    if x<0:
        return -1
    elif x==0 or x==1:
        return 1
    else:
        return fib(x-1)+fib(x-2)
#}

#def main
    fib(5)