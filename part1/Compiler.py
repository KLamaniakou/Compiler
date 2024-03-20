#KONSTANTINOS-DIONISIOS LAMANIAKOU AM:5110
#IOANNIS TSOXLAS AM:4993
import sys
#class token from 27-MANIS-Handbook-on-Compiler-Design-and-Development Page:41
class Token:
    def __init__(self, recognized_string, family, line_number): 
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number
#lex funcion
def lex():
    global line
    global eof
    schar = input_file.read(1)
    Dchar=""
    if (schar == ""):  #Check the end of file
        eof = True     #End of File flag to true
        return (0, 0, 0) #return 0 
    while (schar == " " or schar == "\t" or schar == "\n"):
        if (schar == "\n"): #return
            line = line + 1 #go to the new line
        schar = input_file.read(1) #go to the next char
    if (schar.isalpha()): #if is char
        Char_counter = 1  #count the character to check later the range
        Dchar = schar     #save the first char
        schar = input_file.read(1) #read the second
        while (schar.isalpha() or schar.isdigit()):  #after 1 char we can have numbers
            Char_counter += 1  #counter++
            if (Char_counter <= 30): #check the range
                Dchar = Dchar + schar #put it with others
                schar = input_file.read(1) #read the next
            else:                      #else is out of range                  
                print ("Identifier over range you can use <= 30 characters")
                sys.exit(0)
        if(schar.isalpha()==False or schar.isdigit()==False):
            input_file.seek(input_file.tell() - 1)
        if (Dchar in keywords):   #check the word if its in the keywords
            return (Dchar, "keyword", line) 
        return (Dchar, "identifier", line)    
    elif (schar.isdigit()):  
        Dchar= schar #first digit
        schar = input_file.read(1) #second char
        while (schar.isdigit()):  #check if second char is number
            Dchar= Dchar+ schar   #Save the char and put it at the end
            schar = input_file.read(1)  #read the next char  
        if(schar.isdigit() == False):
            input_file.seek(input_file.tell() - 1)
        if (int(Dchar) <= -32767 or int(Dchar) >= 32767): #CHECK THE RANGE
            print ("Number is out of range.Keep the range between -32767 and 32767")
            sys.exit(0)
        return (Dchar, "number", line)
    elif (schar == "+" or schar == "-"): #check for add operator
        Dchar = schar
        return (Dchar, "addOperator", line)   
    elif (schar == "*" or schar == "%"): #check for mul operator
        Dchar = schar
        return (Dchar, "mulOperator", line)
    elif(schar=="/"):   #check for double /
        Dchar = schar
        schar = input_file.read(1)  
        if (schar == "/"): #if the second character is "/"
            Dchar = Dchar + schar
            return (Dchar, "mulOperator", line) 
        else:  #else is error we dont have one /
            input_file.seek(input_file.tell() - 1)
            print ("Character / not found after /, for assignment use '//', at line " + str(line)) 
            sys.exit(0)
    elif (schar == "<"): #check for rel operator "less"
        Dchar = schar
        schar = input_file.read(1)   #read the next char to check for less equal "<="
        if (schar == "="):   #if second char is "="
            Dchar = Dchar + schar
            return (Dchar, "relOperator", line)   #then return <=
        else:
            input_file.seek(input_file.tell() - 1)
            return (Dchar, "relOperator", line)   
    elif (schar == "!"): 
        Dchar = schar
        schar = input_file.read(1)   
        if (schar == "="):  
            Dchar = Dchar + schar
            return (Dchar, "relOperator", line) 
        else:
            input_file.seek(input_file.tell() - 1)
            return (Dchar, "relOperator", line)    
    elif (schar == ">"):   #same logic like the less and less equal
        Dchar = schar
        schar = input_file.read(1) 
        if (schar == "="):
            Dchar = Dchar + schar
            return (Dchar, "relOperator", line)  #return >=
        else:
            input_file.seek(input_file.tell() - 1)     
            return (Dchar, "relOperator", line)   #return >
    elif (schar == "="):
        Dchar = schar
        schar= input_file.read(1)
        if(schar== "="):
            Dchar=Dchar + schar 
            return (Dchar, "relOperator", line) #return ==
        else:
            input_file.seek(input_file.tell() - 1)
            return (Dchar, "relOperator", line) #return =
    elif (schar == "," or schar == ":"):  #check for delimiter
        Dchar = schar
        return (Dchar, "delimiter", line) 
    elif (schar == "(" or schar == ")"): #check for group symbol
        Dchar = schar
        return (Dchar, "groupSymbol", line)  
    elif (schar == "#"): #here we check and for the comments and for groups symbols
        Dchar = schar
        schar=input_file.read(1)
        if(schar == "{" or schar == "}"):
            Dchar=Dchar+schar
            return (Dchar, "groupSymbol", line) 
        elif(schar == "#"):
            Dchar = schar     #save the first char
            schar = input_file.read(1) #read the second
            while (schar != "#"):  #after 1 char we can have numbers
                Dchar = Dchar + schar #put it with others
                if(Dchar in keywords):
                    return (Dchar, "keyword", line)
                schar = input_file.read(1) #read the next
            schar = input_file.read(1) #read the next
            if (schar=="#"):
                return(0,0,0)
            if(schar == " " or schar == "\t" or schar == "\n"):
                input_file.seek(input_file.tell() - 1)
            else:
                if(schar == "#"):
                    return (0, 0, 0)
                else:
                    print("Comment section not closed, comment starts at line " + str(line))
                    eof=True
                    return (0, 0, 0)
        elif (schar.isalpha()): #if is char
            Char_counter = 1  #count the character to check later the range
            Dchar = schar     #save the first char
            schar = input_file.read(1) #read the second
            while (schar.isalpha()):  #after 1 char we can have numbers
                Char_counter += 1  #counter++
                if (Char_counter <= 4): #check the range
                    Dchar = Dchar + schar #put it with others
                    schar = input_file.read(1) #read the next
                else:                      #else is out of range                  
                    print ("wrong declarasion")
                    sys.exit(0)
            if(schar.isalpha()==False or schar.isdigit()==False):
                input_file.seek(input_file.tell() - 1)
            if (Dchar in keywords):   #check the word if its in the keywords
                return ("#"+Dchar, "keyword", line) 
        else:
            print ("error " + schar +  " at line " + str(line))
            sys.exit(0)
    else:
        print ("Invalid Character \"" + schar + "\" at line " + str(line))
        sys.exit(0)

# Syntax Analyzer
def syntax_analyzer():
    global token
    token = get_token()
    startRule()
    print("Compilation successfully completed")  

def get_token():
    global index
    global all_ts
    index += 1
    if (index == len(all_t)):
        return (Token("",0,0))
    return (all_t[index])

def startRule():
    def_main_part()
    call_main_part()

def def_main_part():
    global token
    declarations()
    def_main_function()
    while token.recognized_string=="def":
        def_main_function()

def def_main_function():
    global token
    if token.recognized_string=="def":
        token = get_token()
        if token.family == "identifier":
            token = get_token()
            if token.recognized_string == "(":
                token = get_token()
                id_list()
                if token.recognized_string==")":
                    token = get_token()
                    if token.recognized_string == ":":
                        token = get_token()
                        if token.recognized_string==0:
                            token=get_token()
                        if token.recognized_string == "#{":
                            token=get_token()
                            declarations()
                            while token.recognized_string == "def":
                                def_main_function()
                            declarations() 
                            statements()
                            if token.recognized_string == "#}":
                                token=get_token()
                            else:
                                print("Error,the program does not have #} after #{ at main function in line",token.line_number)
                                exit(-1)
                        else:
                            print("Error,the program does not have #{ after main function in line",token.line_number)
                            exit(-1)
                    else:
                        print("Error,the program does not have : after main function in line",token.line_number)
                        exit(-1)
                else:
                    print("Error,the program does not have a ) after ( at main function in line",token.line_number)
                    exit(-1)
            else:
                print("Error,the program does not have ( after main function in line",token.line_number)
                exit(-1)
        else:
            print("Error,the program does not have a name for main function in line",token.line_number)
            exit(-1)
    else:
        print("Error,the program doesnt start with def  at main function in line", token.line_number)
        exit(-1)

def declarations():
    global token
    while token.recognized_string == "#int" or token.recognized_string =="global":
        declaration_line()

def declaration_line():
    global token
    if token.recognized_string == "#int" or token.recognized_string =="global":
        token = get_token()
        id_list()

def id_list():
    global token
    if token.family == "identifier":
        line=token.line_number
        token = get_token()
        while token.recognized_string == ",":
            token = get_token()
            if token.family == "identifier":
                token = get_token()
            else:
                print("Error,there is not identifier after , in line",token.line_number)
                exit(-1)
        if token.family == "identifier" and token.line_number==line:
            print("Error,there is not , between arguments in line",token.line_number)

def statement():
    global token
    if token.family == "identifier" or token.recognized_string == "print" or token.recognized_string == "return":
        simple_statement()
    elif token.recognized_string == "if" or token.recognized_string == "while":
        structured_statement()

def statements():
    global token
    if token.recognized_string==0:
        token=get_token()
    declarations()        
    statement()
    while token.recognized_string == "def":
        def_main_function()
    if token.recognized_string==0:
        token=get_token()
    declarations()
    statement()
    while token.family == "identifier" or token.recognized_string == "print" or token.recognized_string == "return" or token.recognized_string == "if"  or token.recognized_string == "while":
        if token.recognized_string==0:
            token=get_token()
        statement() 

def simple_statement():
    global token
    if token.family =="identifier":
        assignment_stat()
    elif token.recognized_string == "print":
        print_stat()
    elif token.recognized_string == "return":
        return_stat()

def structured_statement():
    global token    
    if token.recognized_string == "if":
        if_stat()
    elif token.recognized_string == "while":
        while_stat()

def assignment_stat():
    global token
    if token.family == "identifier":
        token=get_token()
        if token.recognized_string =="(":
            token=get_token()
            statement()
            if token.recognized_string ==")":
                token=get_token()
        elif token.recognized_string =="=":
            token=get_token()
            if token.recognized_string =="int":
                token=get_token()
                if token.recognized_string =="(":
                    token=get_token()
                    if token.recognized_string =="input":
                        token=get_token()
                        if token.recognized_string =="(":
                            token=get_token()
                            if token.recognized_string ==")":
                                token=get_token()
                                if token.recognized_string ==")":
                                    token=get_token()
                                else:
                                    print("Error,there is not ) after int( in line", token.line_number)
                                    exit(-1)
                            else:
                                print("Error,there is not ) after input( in line", token.line_number)
                                exit(-1)
                        else:
                            print("Error,there is not ( after input in line",token.line_number)
                            exit(-1)
                    else:
                        print("Error,there is not input after ( in line",token.line_number)
                        exit(-1)
                else:
                    print("Error,there is not ( after int in line",token.line_number)
                    exit(-1)
            else:
                expression()
        else:
            print("Error, there is not = for assignment statement in line",token.line_number)
            exit(-1)
    else:
        print("Error,there is not an identifier for assignment in line",token.line_number)
        exit(-1)

def print_stat():
    global token
    if token.recognized_string =="print":
        token=get_token()
        expression()
    else:
        print("Error,there is not print in line",token.line_number)
        exit(-1)

def return_stat():
    global token
    if token.recognized_string =="return":
        token=get_token()
        expression()
    else:
        print("Error,there is not return in line",token.line_number)
        exit(-1)

def if_stat():
    global token
    if token.recognized_string == "if":
        token=get_token()
        condition()
        if token.recognized_string == ":":
            token=get_token()
            if token.recognized_string == "#{":
                token=get_token()
                statements()
                if token.recognized_string == "#}":
                    token=get_token()
                    elif_stat()
                    if token.recognized_string == "else":
                        token=get_token()
                        if token.recognized_string == ":":
                            token=get_token()
                            if token.recognized_string == "#{":
                                token=get_token()
                                statements()
                                if token.recognized_string == "#}":
                                    token=get_token()
                                else:
                                    print("Error there is not #} after else: #{ in line", token.line_number)
                                    exit(-1)
                            else:
                                statement()
                        else:
                            print("Error,there is not : after else in line",token.line_number)
                            exit(-1)
                else:
                    print("Error there is not #} after if #{ in line", token.line_number)
                    exit(-1)
            else:
                statement()
                elif_stat()
                if token.recognized_string == "else":
                    token=get_token()
                    if token.recognized_string == ":":
                        token=get_token()
                        if token.recognized_string == "#{":
                            token=get_token()
                            statements()
                            if token.recognized_string == "#}":
                                token=get_token()
                            else:
                                print("Error there is not #} after else: #{ in line", token.line_number)
                                exit(-1)
                        else:
                            statement()
                    else:
                        print("Error,there is not : after else in line",token.line_number)
                        exit(-1)
        else:
            print("Error,there is not : after if in line",token.line_number)
            exit(-1)
    else:
        print("Error,there is not if in line",token.line_number)
        exit(-1)
def elif_stat():
    global token
    if token.recognized_string =="elif":
        token=get_token()
        condition()
        if token.recognized_string ==":":
            token=get_token()
            if token.recognized_string == "#{":
                token=get_token()
                statements()
                if token.recognized_string == "#}":
                    token=get_token()
                else:
                    print("Error there is not #} after else: #{ in line", token.line_number)
                    exit(-1)
            else:
                statement()
def while_stat():
    global token
    if token.recognized_string =="while":
        token=get_token()
        condition()
        if token.recognized_string ==":":
            token=get_token()
            if token.recognized_string=="#{":
                token=get_token()
                statements()
                if token.recognized_string=="#}":
                    token=get_token()
                else:
                    print("Error there is not #} after while #{ in line", token.line_number)
                    exit(-1)
            else:
                statement()
        else:
            print("Error,there is not : after while in line", token.line_number)
            exit(-1)
    else:
        print("Error,there is not while in line", token.line_number)
        exit(-1)

def expression():
    global token
    term()
    while token.family =="addOperator":
        ADD_OP()
        term()

def term():
    global token
    factor()
    while token.family=="mulOperator":
        MUL_OP()
        factor()

def factor():
    global token
    if token.family == "number":
        token = get_token()
    elif token.recognized_string == "(":
        token = get_token()
        expression()
        if token.recognized_string == ")":
                token = get_token()
        else:
            print("Error,there is not ) after ( at factor in line", token.line_number)
            exit(-1)
    elif token.family == "identifier":
        token = get_token()
        idtail(token.recognized_string)
    elif token.recognized_string == "-":
        if token.family == "number":
            token = get_token()
    else:
        print("Error,there is not numerical constant or expression or identifier at factor in line", token.line_number)
        exit(-1)

def idtail(function_name):
    global token
    if token.recognized_string == "(":
        token = get_token()
        actual_par_list()
        if token.recognized_string == ")":
            token = get_token()
        else:
            print("Error ,there is not ) after ( at idtail ",token.line_number)
            exit(-1)
    else:
        return function_name
def actual_par_list():
    global token
    if token.family== "number" or token.recognized_string== "(" or token.family== "identifier":
        expression()
        while token.recognized_string== ",":
            token=get_token()
            expression()

def optional_sign():
    global token
    if token.family== "addOperator":
            ADD_OP()

def ADD_OP():
    global token
    if token.recognized_string== "+":
        token=get_token()
    elif token.recognized_string== "-":
        token=get_token()

def MUL_OP():
    global token
    if token.recognized_string == "*":
        token=get_token()
    elif token.recognized_string == "//":
        token=get_token()
    elif token.recognized_string =="%":
        token=get_token()

def condition():
    global token
    bool_term()
    while token.recognized_string== "or":
        token=get_token()
        bool_term()

def bool_term():
    global token
    bool_factor()
    while token.recognized_string== "and":
        token=get_token()
        bool_factor()

def bool_factor():
    global token
    if token.recognized_string== "not":
        token=get_token()
        if token.family== "(":
            token=get_token()
            condition()
            if token.recognized_string== ")":
                token=get_token()
            else:
                print("Error,there is not ) after not( at boolfactor in line",token.line_number)
                exit(-1)
        else:
            print("Error,there is not ( after not at boolfactor in line",token.line_number)
            exit(-1)
    elif token.recognized_string== "(":
        token=get_token()
        condition()
        if token.recognized_string== ")":
            token=get_token()
        else:
            print("Error,there is not ) after ( at boolfactor in line",token.line_number)
            exit(-1)
    else:
        expression()
        REL_OP()
        expression()

def REL_OP():
    global token
    if token.recognized_string== "==":
        token=get_token()
    elif token.recognized_string== "!=":
        token=get_token()
    elif token.recognized_string== "<":
        token=get_token()
    elif token.recognized_string== "<=":
        token=get_token()
    elif token.recognized_string== ">":
        token=get_token()
    elif token.recognized_string== ">=":
        token=get_token()
    else:
        print("Error,there is not == or != or > or >= or < or <= in line", token.line_number)
        exit(-1)

def call_main_part():
    global token
    if token.recognized_string == "#def":
        token = get_token()
        if token.recognized_string == "main":
            token = get_token()
            declarations()
            statements()
        else:
            print("Error,there is not main at call_main_part in line",token.line_number)
            exit(-1)
    else:
        print("Error,there is not #def at call_main_part in line",token.line_number)
        exit(-1)
#Main 
def main():
    while (not eof):
        t= lex()                                             
        new_token = Token(t[0],t[1],t[2]) 
        all_t.append(new_token)
    syntax_analyzer()

#DEFINES
line = 1
all_t=[]
index = -1
token = 0
eof= False
keywords={"main","def","#def",
            "#int","global",
            "if","elif","else",
            "while",    
            "print",
            "return",
            "input","int",
            "and","or","not"}
input_file = open(sys.argv[1],"r") 
main()