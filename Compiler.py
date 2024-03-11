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
            return (Dchar, "relOperator", line)    #else return <
    elif (schar == ">"):   #same logic like the less and less equal
        Dchar = schar
        schar = input_file.read(1) 
        if (schar == "="):
            Dchar = Dchar + schar
            return (Dchar, "relOperator", line)  #return >=
        else:     
            return (Dchar, "relOperator", line)   #return >
    elif (schar == "="):
        Dchar = schar
        schar= input_file.read(1)
        if(schar== "="):
            Dchar=Dchar + schar 
            return (Dchar, "relOperator", line) #return ==
        else:
            input_file.seek(input_file.tell() - 1)
            return (Dchar, "assignment", line) #return =
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
                    return(0,0,0)
                else:
                    print("Comment section not closed, comment starts at line " + str(line))
                    eof=True
                    return(0,0,0)
        else:
            print ("error" + schar +  " at line " + str(line))
            sys.exit(0)
    else:
        print ("Invalid Character \"" + schar + "\" at line " + str(line))
        sys.exit(0)

# Syntax Analyzer
def syntax_analyzer():
    global token
    token = get_token()
    program()
    print("Compilation successfully completed")  

def get_token():
    global index
    global all_ts
    index += 1
    if (index == len(all_t)):
    #    print("DEBUG: End Token ")                                  # For Debugging Purposes
        return (Token("",0,0))
    #print("DEBUG: Examining Token : " + str(all_ts[index]))     # For Debugging Purposes
    return (all_t[index])

def error(typeOfError):
    global line 
    global token
    errors = {
        "validId": "A valid id was expected at line ",
        "plusOrMinus": "A \"+\" or \"-\" was expected at line ",
        "mulOrDiv": "A \"*\" or \"/\" was expected at line ",
        "asgnSym": "The \":=\" was expected at line ",
        "closeCurBracket": "Curly bracket hasn't closed at line ",
        "openCurBracket": "Curly bracket expected at line ",
        "closeSqBracket": "Square bracket hasn't closed at line ",
        "openSqBracket": "Square bracket expected at line ",
        "closeParentheses": "Parentheses hasn't closed at line ",
        "openParentheses": "Parentheses expected at line ",
        "numExprId": "Number/(Expression)/ID expected at line ",
        "defaultNotFound": "Default case not found around line ",
        "programKeywordNF": "\"program\" keyword not found at line ",
        "dotExpected": "A \".\" was expected at line ",
        "eofExpected": "Characters found after \".\", line ",
        "relOpExpected": "One of the =, <=, >=, >, <, <> symbols are expected at line ",
        "semicolonExpected": "A \";\" was expected at line ",
        "invalidFuncName": "Invalid function name at line ",
        "invalidProcName": "Invalid procedure name at line "
    }
    print(errors[typeOfError] + str(token.line_number))
    sys.exit()

def addoperator():
    global token
    if (token.recognized_string == "+"):
        token = get_token()
    elif (token.recognized_string == "-"):
        token = get_token()
    else:
        error("plusOrMinus") # +, -
        
def assignStat():
    global token
    if (token.family == "id"):
        eplace = ""
        x = token.recognized_string
        token = get_token()
    else: 
        error("validId") # not an id, is (another family)

def blockstatements():
    global token
    statement()
    while (token.recognized_string == ";"):
        token = get_token()
        statement()

def declarations():
    global token
    while (token.recognized_string == "declare"):
        token = get_token()
        varlist()
        if (token.recognized_string == ";"):
            token = get_token()
        else:
            error("semicolonExpected") # ";" expected but something else came

def elsepart():
    global token
    if (token.recognized_string == "else"):
        token = get_token()
        statements()

def ifStat():
    global token
    token = get_token() # consume if
    if (token.recognized_string == "("):
        token = get_token()
        if (token.recognized_string == ")"):
            token = get_token()
            statements()
        else:
            error("closeParentheses")
    else:
        error("openParentheses")
    
def inputStat():
    global token
    idplace = ""
    token = get_token() # consume input
    if (token.recognized_string == "("):
        token = get_token()
        if (token.family == "id"):
            idplace = token.recognized_string
            token = get_token()
            if (token.recognized_string == ")"):
                token = get_token()
            else:
                error("closeParentheses") # ) expected
        else:
            error("validId") # a valid id expected
    else:
        error("openParentheses") # ( expected

def muloperator():
    global token
    if (token.recognized_string == "*"):
        token = get_token()
    elif (token.recognized_string == "/"):
        token = get_token()
    else:
        error("mulOrDiv") # *, /

def optionalSign():
    global token
    global index
    if (token.recognized_string == "+" or token.recognized_string == "-"):
        addoperator()

def printStat():
    global token
    eplace = ""
    token = get_token() # consume print
    if (token.recognized_string == "("):
        token = get_token()
        if (token.recognized_string == ")"):
            token = get_token()
        else:
            error("closeParentheses") # ) expected
    else:
        error("openParentheses") # ( expected

def program():
    global token
    global main_name
    if (token.recognized_string == "program"):
        token = get_token()
        if (token.family == "id"):
            main_name = token.recognized_string
            token = get_token()
            if (token.recognized_string == "."):
                token = get_token()
                if (token.recognized_string == ""):
                    pass
                else:
                    error("eofExpected")
            else:
                error("dotExpected")
        else:
            error("validId")
    else:
        error("programKeywordNF")

def reloperator():
    global token
    relop = ""
    if (token.recognized_string == "="):
        relop = token.recognized_string
        token = get_token()
    elif (token.recognized_string == "<="):
        relop = token.recognized_string
        token = get_token()
    elif (token.recognized_string == ">="):
        relop = token.recognized_string
        token = get_token()
    elif (token.recognized_string == ">"):
        relop = token.recognized_string
        token = get_token()
    elif (token.recognized_string == "<"):
        relop = token.recognized_string
        token = get_token()
    elif (token.recognized_string == "<>"):
        relop = token.recognized_string
        token = get_token()
    else:
        error("relOpExpected") # =, <=, >=, >, <, <> expected
    return (relop)

def returnStat():
    global token
    global ret
    eplace = ""
    token = get_token() # consume return
    if (token.recognized_string == "("):
        token = get_token()
        if (token.recognized_string == ")"):
            token = get_token()
            ret = True
        else:
            error("closeParentheses") # ) expected
    else:
        error("openParentheses") # ( expected

def statement():
    global token
    global index
    token = get_token()
    if (token.recognized_string == ":="):
        index -= 2
        token = get_token()
        assignStat()
    else:
        index -= 2
        token = get_token()
    if (token.recognized_string == "if"):
        ifStat()
    elif (token.recognized_string == "while"):
        whileStat()
    elif (token.recognized_string == "return"):
        returnStat()
    elif (token.recognized_string == "input"):
        inputStat()
    elif (token.recognized_string == "print"):
        printStat()
    elif (token.recognized_string == "default"):
        token = get_token()
        statement()

def statements():
    global token
    if (token.recognized_string == "{"):
        token = get_token()
        statement()
        while (token.recognized_string == ";"):
            token = get_token()
            statement()
        if (token.recognized_string == "}"):
            token = get_token()
        else: 
            error("closeCurBracket") # } expected
    else:
        statement()
        if (token.recognized_string == ";"):
            token = get_token()
        else: 
            error("semicolonExpected") # ; expected

def subprogram():
    global token
    global label
    global ret
    id = ""
    if (token.recognized_string == "function"):
        token = get_token()
        if (token.family == "id"):
            id = token.recognized_string         
            token = get_token()
            if (token.recognized_string == "("):
                token = get_token()
                if (token.recognized_string == ")"):
                    token = get_token()
                    if (ret == False):
                        print("Function has not return statement")
                        sys.exit(0)
                else:
                    error("closeParentheses") # ")" not found
            else:
                error("openParentheses") # "(" not found
        else: 
            error("invalidFuncName") # a valid function name is expected

def subprograms():
    global token
    while (token.recognized_string == "function"):
        subprogram()

def term():
    global token
    global index
    while (token.recognized_string == "*" or token.recognized_string == "/"):
        operator = token.recognized_string
        muloperator()
        f1place = x
        if (token.recognized_string == ")"):
            token = get_token()
            if (token.recognized_string == ";"):
                index -= 2
                token = get_token()
    eplace = f1place
    if (token.family == "keyword"):  # catch a case where after ")" we get a keyword, so we don"t skip token
        if (token.recognized_string != "and" and token.recognized_string != "or"):
            index -= 2
            token = get_token()
    return (eplace)

def varlist():
    global token
    global variables
    if (token.family == "id"):
        variables.append(token.recognized_string)          
        token = get_token()
        while (token.recognized_string == ","):
            token = get_token()
            variables.append(token.recognized_string)           
            if (token.family == "id"):
                token = get_token()
            else:
                error("validId") # id expected, something else came

def whileStat():
    global token
    token = get_token() # consume while
    if (token.recognized_string == "("):
        if (token.recognized_string == ")"):
            token = get_token()
            statements()
        else:
            error("closeParentheses") # ) expected
    else:
        error("openParentheses") # ( expected
#Main 
def main():
    while (not eof):
        t= lex()       
        print(t[0])                                         
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
            "not","or","not"}
input_file = open(sys.argv[1],"r") 
main()