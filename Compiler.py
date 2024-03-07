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
            else:                      #else is out of range                  poy eiani to chat?
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

#syntax analyzer
def syntax_analyzer():
    global token
    token = all_t.get_token()
    all_t.program()
    print('compilation successfully completed')

#Main 
def main():
    while (not eof):
        t= lex()                                                
        new_token = Token(t[0],t[1],t[2]) 
        all_t.append(new_token)
    syntax_analyzer

#DEFINES
line = 1
all_t=[]
eof= False
keywords={"main","def","#def",
            "#int","global",
            "if","elif","else",
            "while",    
            "print",
            "return",
            "input","int",
            "not","or","not"}
file="C:/Users/kostas/Documents/sxolh kwsta/Compiler/test.txt"
input_file = open(file, "r")
main()