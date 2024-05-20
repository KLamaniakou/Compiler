#KONSTANTINOS-DIONISIOS LAMANIAKOU AM:5110
#IOANNIS TSOXLAS AM:4993
import sys
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
file = open('endiamesos.int','w')
file2 = open('symbol_table.sym','w') 
final_file = open('final_file.asm','w')
#class token from 27-MANIS-Handbook-on-Compiler-Design-and-Development Page:41
class Token:
    def __init__(self, recognized_string, family, line_number): 
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number
class Entity():
    def __init__(self):
        self.name = ''			#we initialize our class entity with the name and datatype(variable,function,parameter,temporaryvariable)
        self.datatype = ''
        self.variable = self.Variable() #we create 4 objects from the classes who inherit the name and datatype from entity
        self.function = self.Function()
        self.parameter = self.Parameter()
        self.temporaryVariable = self.TemporaryVariable()

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
#endiamesos_kwdikas
fullist = []
fullist2 = []
quadlabel = 1
counter = -1
isArgument = True

def nextQuad():
    global fullist
    global quadlabel
    return quadlabel

def genQuad(op,x,y,z):
    global fullist
    global fullist2
    global quadlabel
    my_list = []
    my_list = [nextQuad()]
    my_list.insert(1,str(op))
    my_list.insert(2,str(x))
    my_list.insert(3,str(y))
    my_list.insert(4,str(z))
    fullist += [my_list]
    fullist2 += [my_list]
    quadlabel = quadlabel + 1
    return my_list

def new_temp():
    global fullist
    global counter
    counter += 1
    entity = Entity()
    entity_assign(entity,"T" + str(counter),"TEMPORARYVARIABLE",calculate_offset())
    add_entity(entity)

    return "T" + str(counter)

def empty_list():
    return []

def makeList(label):
    return [label]

def merge(list1,list2):
    return list1 +list2


def backPatch(list,z):
    global fullist
    list.sort()
    y = 0
    count = 0
    for i in list:
        for j in fullist[y:]:
            if j[0] == i:
                j[4] = str(z)
                count += 1
                y = count
                break
            else:
                count += 1
        count = 0
        
def write_Quads(x):
    global fullist
    for i in range(len(fullist)):
        z = fullist[i]
        for y in z:
            if y == z[0]:
                x.write(str(y) + ": ")
            else:
                x.write(str(y) + " ")
        x.write('\n')

#pianakas_symbolwn
list_of_scopes = []
class Scope():
    def __init__(self):
        self.name = ''						
        self.entityList = []
        self.nestingLevel = 0

class Entity():
    def __init__(self):
        self.name = ''			
        self.datatype = ''
        self.variable = self.Variable() 
        self.function = self.Function()
        self.parameter = self.Parameter()
        self.temporaryVariable = self.TemporaryVariable()


    class Variable:
        def __init__(self):
            self.offset = 0  


    class Function:
        def __init__(self):
            self.startingQuad = 0  
            self.frameLength = 0 
            self.argumentList = []  
            self.nestingLevel = 0


    class Parameter:
        def __init__(self):
            self.offset = 0  


    class TemporaryVariable:
        def __init__(self):
            self.offset = 0  



class Argument():
    def __init__(self):
        self.name = ''		
        self.datatype = 'INT'


def add_entity(entity):
    global list_of_scopes
    list_of_scopes[-1].entityList = list_of_scopes[-1].entityList + [entity]

count = 0
def nestingLevel_assign(scope):
    global count
    scope.nestingLevel = count

def add_argument(argument):
    global list_of_scopes
    list_of_scopes[-1].entityList[-1].function.argumentList = list_of_scopes[-1].entityList[-1].function.argumentList + [argument]

def add_scope(name):
    global list_of_scopes
    global count

    nextScope = Scope()
    nextScope.name = name
    if len(list_of_scopes) >= 1:
        count += 1
        nestingLevel_assign(nextScope)

    list_of_scopes.append(nextScope)


def delete_scope():
    global list_of_scopes
    global count
    count = 0
    for i in range(len(list_of_scopes[-1].entityList)):
        list_of_scopes[-1].entityList.pop()
    del list_of_scopes[-1]


def calculate_offset():
    global list_of_scopes
    offset = 12

    if len(list_of_scopes[-1].entityList) >= 1:
        for i in range( len(list_of_scopes[-1].entityList)):
            if list_of_scopes[-1].entityList[i].datatype == 'VARIABLE' or list_of_scopes[-1].entityList[i].datatype == 'TEMPORARYVARIABLE' \
                    or list_of_scopes[-1].entityList[i].datatype == 'PARAMETER':
                offset += 4
    return offset


def calculate_framelength():
    global list_of_scopes
    list_of_scopes[-2].entityList[-1].function.frameLength = calculate_offset()


def calculate_startingQuad():
    global list_of_scopes
    list_of_scopes[-2].entityList[-1].function.startingQuad = nextQuad()

def find_entity(x):
    global list_of_scopes
    if len(list_of_scopes) > 0:
        for j in range(len(list_of_scopes)-1,-1,-1):
            for i in list_of_scopes[j].entityList:
                if i.name == x:
                    return(list_of_scopes[j],i)
        print("There is not entity with  name : " + str(x))
        exit()

def entity_assign(en,name1,type1,offset1):
    en.name = name1
    en.datatype = type1
    if en.datatype == "PARAMETER":
        en.parameter.offset = offset1
    elif en.datatype == "VARIABLE":
        en.variable.offset = offset1
    elif en.datatype == "TEMPORARYVARIABLE":
        en.temporaryVariable.offset = offset1


def add_parameters():
    global list_of_scopes

    for i in list_of_scopes[-2].entityList[-1].function.argumentList:
        entity = Entity()
        entity_assign(entity,i.name,"PARAMETER",calculate_offset())
        add_entity(entity)

def show_symbols(file):
    global list_of_scopes
    file.write("-------------------------------------------------------------------------------------------------")
    file.write("\n")
    for i in list_of_scopes:
        file.write("\n")
        file.write("Scope: " + str(i.name) + " " + "nestingLevel: " + str(i.nestingLevel))
        for j in i.entityList:
            file.write("\n")
            file.write("     Entity: " + str(j.name) + " " + str(j.datatype))
            file.write("\n")
            if j.datatype == "VARIABLE":
                file.write("     Offset is :" + str(j.variable.offset))
                file.write("\n")
            elif j.datatype == "PARAMETER":
                file.write("     Offset is :" + str(j.parameter.offset))
                file.write("\n")
            elif j.datatype == "TEMPORARYVARIABLE":
                file.write("     Offset is :" + str(j.temporaryVariable.offset))
                file.write("\n")
            elif j.datatype == "FUNCTION":
                file.write("     Framelength of " + str(j.name) + " is : " + str(j.function.frameLength))
                file.write("\n")
                file.write("     StartingQuad of " + str(j.name) + " is : " + str(j.function.startingQuad))
                file.write("\n")
                for k in j.function.argumentList:
                    file.write("         Argument: " + str(k.name) + " " + str(k.datatype))
                    file.write("\n")
def gnlvcode(y):
    global list_of_scopes
    (my_scope, my_entity) = find_entity(y)
    n = list_of_scopes[-1].nestingLevel - my_scope.nestingLevel - 1
    final_file.write('lw t0,-4(sp)\n')
    while n > 0:
        final_file.write('lw t0,-4(t0)\n')
        n = n - 1
    if my_entity.datatype == 'VARIABLE':
        my_offset = my_entity.variable.offset
        final_file.write('addi t0,t0,-%d\n' % my_offset)
    elif my_entity.datatype == 'PARAMETER':
        my_offset = my_entity.parameter.offset
        final_file.write('addi t0,t0,-%d\n' % my_offset)



def loadvr(v,r):
    if v.isdigit():
        final_file.write('li t%s,%s\n' % (r,v))
    else:
        (my_scope,my_entity) = find_entity(v)
        if my_scope.nestingLevel == 0:
            if my_entity.datatype == "VARIABLE":
                final_file.write('lw t%s,-%d(gp)\n' % (r, my_entity.variable.offset))
            elif my_entity.datatype == "TEMPORARYVARIABLE":
                final_file.write('lw t%s,-%d(gp)\n' % (r, my_entity.temporaryVariable.offset))

        elif my_scope.nestingLevel == list_of_scopes[-1].nestingLevel:
            if my_entity.datatype == "VARIABLE":
                final_file.write('lw t%s,-%d(sp)\n' % (r, my_entity.variable.offset))
            elif my_entity.datatype == "TEMPORARYVARIABLE":
                final_file.write('lw t%s,-%d(sp)\n' % (r, my_entity.temporaryVariable.offset))
            elif my_entity.datatype == "PARAMETER":
                final_file.write('lw t%s,-%d(sp)\n' % (r, my_entity.parameter.offset))

        elif my_scope.nestingLevel < list_of_scopes[-1].nestingLevel:
            if my_entity.datatype == "VARIABLE":
                gnlvcode(v)
                final_file.write('lw t%s,(t0)\n' % r)
            elif my_entity.datatype == "PARAMETER":
                gnlvcode(v)
                final_file.write('lw t%s,(t0)\n' % r)

def storerv(r,v):
    (my_scope, my_entity) = find_entity(v)
    if my_scope.nestingLevel == 0:
        if my_entity.datatype == "VARIABLE":
            final_file.write('sw t%d,-%d(gp)\n' % (r,my_entity.variable.offset))
        elif my_entity.datatype == "TEMPORARYVARIABLE":
            final_file.write('sw t%d,-%d(gp)\n' % (r, my_entity.temporaryVariable.offset))

    elif my_scope.nestingLevel == list_of_scopes[-1].nestingLevel:
        if my_entity.datatype == "VARIABLE":
            final_file.write('sw t%d,-%d(sp)\n' % (r, my_entity.variable.offset))
        elif my_entity.datatype == "TEMPORARYVARIABLE":
            final_file.write('sw t%d,-%d(sp)\n' % (r, my_entity.temporaryVariable.offset))
        elif my_entity.datatype == "PARAMETER":
            final_file.write('sw t%d,-%d(sp)\n' % (r, my_entity.parameter.offset))

    elif my_scope.nestingLevel < list_of_scopes[-1].nestingLevel:
        if my_entity.datatype == "VARIABLE":
            gnlvcode(v)
            final_file.write('sw t%d,(t0)\n' % r)
        elif my_entity.datatype == "PARAMETER":
            gnlvcode(v)
            final_file.write('sw t%d,(t0)\n' % r)

final_file.write('       \n')
my_count = 0
def generate_final():
    global fullist
    global fullist2
    global my_count
    relop_operators = ['==', '!=', '<', '<=', '>', '>=']
    assembly_operators = ['beq', 'bne', 'blt', 'ble', 'bgt', 'bge']
    numerical_op = ['+', '-', '*', '//']
    assembly_op = ['add', 'sub', 'mul', 'div']
    final_flag = 0
    for i in fullist2:
        final_file.write('L' + str(i[0]) + ': \n')
        if i[1] == "jump":
            final_file.write('j L'+str(i[4])+'\n')
        elif i[1] in relop_operators:
            x = assembly_operators[relop_operators.index(i[1])]
            loadvr(i[2], 1)
            loadvr(i[3], 2)
            final_file.write(x + ' ,t1, t2, L' + i[4] + '\n')
        elif i[1] in numerical_op:
            x = assembly_op[numerical_op.index(i[1])]
            loadvr(i[2], 1)
            loadvr(i[3], 2)
            final_file.write(x + ' ,t1, t1,t2 \n')
            storerv(1, i[4])
        elif i[1] == '=':
            loadvr(i[2], 1)
            storerv(1, i[4])
        elif i[1] == 'retv':
            loadvr(i[2], '1')
            final_file.write('lw t0, -8(sp)\n')
            final_file.write('sw t1, 0(t0)\n')
            final_file.write('lw ra, 0(sp)\n')
            final_file.write('jr ra\n')
        elif i[1] == 'inp':
            final_file.write('li a7,5' + '\n')
            final_file.write('ecall' + '\n')
            final_file.write('mv t1,a0' + '\n')
            storerv(1, i[2])
        elif i[1] == 'out':
            loadvr(i[2], 1)
            final_file.write('mv a0,t1' + '\n')
            final_file.write('li a7,1' + '\n')
            final_file.write('ecall' + '\n')
        elif i[1] == 'halt':
            final_file.write('li a0,0\n')
            final_file.write('li a7,93\n')
            final_file.write('ecall\n')
        elif i[1] == 'begin_block' and list_of_scopes[-1].nestingLevel != 0:
            final_file.write('sw ra,(sp)\n')
        elif i[1] == 'end_block' and list_of_scopes[-1].nestingLevel != 0:
            final_file.write('lw ra,(sp)\n')
            final_file.write('jr ra\n')
        elif i[1] == 'begin_block' and list_of_scopes[-1].nestingLevel == 0:
            final_file.seek(0,0)
            final_file.write('j L%d\n' % i[0])
            final_file.seek(0,2)
            final_file.write('addi sp,sp,%d\n' % calculate_offset())
            final_file.write('mv gp,sp\n')
        elif i[1] == 'par':
            j = fullist.index(i)
            for k in fullist[j:]:
                if k[1] == 'call' and final_flag == 0:
                    (my_scope,my_entity) = find_entity(k[2])
                    final_file.write('addi fp,sp,%d\n' % my_entity.function.frameLength)
                    final_flag = 1
                    break
            if i[3] == 'CV':
                loadvr(i[2],0)
                final_file.write('sw t0, -%d(fp)\n' % (12 + 4 * my_count))
                my_count = my_count + 1
            elif i[3] == 'RET':
                (my_scope, my_entity) = find_entity(i[2])
                final_file.write('addi t0,sp,-%d\n' % my_entity.temporaryVariable.offset)
                final_file.write('sw t0, -8(fp)\n')
        elif i[1] == 'call':
            final_flag = 0
            my_count = 0
            (my_scope,my_entity) = find_entity(i[2])
            if list_of_scopes[-1].nestingLevel < my_entity.function.nestingLevel:
                final_file.write('sw sp,-4(fp)\n')
            elif list_of_scopes[-1].nestingLevel == my_entity.function.nestingLevel:
                final_file.write('lw t0,-4(sp)\n')
                final_file.write('sw t0,-4(fp)\n')
            final_file.write('addi sp,sp,%d\n' % my_entity.function.frameLength)
            final_file.write('jal L%d\n' % my_entity.function.startingQuad)
            final_file.write('addi sp,sp,-%d\n' % my_entity.function.frameLength)


        fullist2 = []

# Syntax Analyzer
def syntax_analyzer():
    global token
    global fullist
    token = get_token()
    add_scope('main')
    startRule()
    print("Compilation successfully completed")  

def get_token():
    global index
    global all_t
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
    global  list_of_scopes
    if token.recognized_string=="def":
        token = get_token()
        if token.family == "identifier":
            ID = token.recognized_string
            token = get_token()
            if token.recognized_string == "(":
                token = get_token()
                id_list()
                if token.recognized_string==")":
                    token = get_token()
                    entity = Entity()
                    entity.datatype = 'FUNCTION'  
                    entity.name = ID
                    entity.function.nestingLevel = list_of_scopes[-1].nestingLevel + 1
                    add_entity(entity)
                    if token.recognized_string == ":":
                        token = get_token()
                        if token.recognized_string==0:
                            token=get_token()
                        add_scope(ID)
                        if token.recognized_string == "#{":
                            token=get_token()
                            declarations()
                            while token.recognized_string == "def":
                                def_main_function()
                            calculate_startingQuad()
                            genQuad('begin_block',ID, '_', '_')
                            declarations() 
                            statements()
                            if token.recognized_string == "#}":
                                calculate_framelength()
                                genQuad('end_block', ID, '_', '_')
                                show_symbols(file2)
                                generate_final()
                                token=get_token()
                                delete_scope()
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
    global isArgument
    if token.recognized_string == "#int" or token.recognized_string =="global":
        token = get_token()
        isArgument = False
        id_list()

def id_list():
    global token
    global  isArgument
    if token.family == "identifier":
        ID = token.recognized_string
        token = get_token()
        if isArgument == True:  
            argument = Argument()
            argument.name = ID
            add_argument(argument) 
        else: 
            entity = Entity()
            entity_assign(entity,ID,"VARIABLE",calculate_offset()) 
            add_entity(entity) 
        while token.recognized_string == ",":
            token = get_token()
            ID = token.recognized_string
            if token.family == "identifier":
                token = get_token()
                if isArgument == True:  
                    argument = Argument()
                    argument.name = ID
                    add_argument(argument) 
                else:
                    entity = Entity() 
                    entity_assign(entity, ID, "VARIABLE", calculate_offset())
                    add_entity(entity) 
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
        idplace = token.recognized_string
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
                genQuad('inp', idplace, '_', '_')
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
                Eplace = expression()
                genQuad('=', Eplace, '_', idplace)
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
        if token.recognized_string=="(":
            Eplace = expression()
            genQuad('out', Eplace, '_', '_')
            if token.recognized_string ==")":
                token=get_token()
        else:
            print(" ( was expected",token.line_number)
    else:
        print("Error,there is not print in line",token.line_number)
        exit(-1)

def return_stat():
    global token
    if token.recognized_string =="return":
        token=get_token()
        Eplace = expression()
        genQuad('retv', Eplace, '_', '_')
    else:
        print("Error,there is not return in line",token.line_number)
        exit(-1)

def if_stat():
    global token
    global ifList
    Btrue = []
    Bfalse = []
    ifList = []
    if token.recognized_string == "if":
        token=get_token()
        B = condition()
        Btrue = B[0]
        Bfalse = B[1]
        backPatch(Btrue, nextQuad())
        if token.recognized_string == ":":
            token=get_token()
            if token.recognized_string == "#{":
                token=get_token()
                statements()
                ifList = makeList(nextQuad())
                genQuad("jump", "_", "_", "_")
                backPatch(Bfalse, nextQuad())
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
                ifList = makeList(nextQuad())
                genQuad('jump', '_', '_', '_')
                backPatch(Bfalse, nextQuad())
                elif_stat()
                if token.recognized_string == "else":
                    token=get_token()
                    if token.recognized_string == ":":
                        token=get_token()
                        if token.recognized_string == "#{":
                            token=get_token()
                            statements()
                            backPatch(ifList, nextQuad())
                            if token.recognized_string == "#}":
                                token=get_token()
                            else:
                                print("Error there is not #} after else: #{ in line", token.line_number)
                                exit(-1)
                        else:
                            statement()
                            backPatch(ifList, nextQuad())
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
    global ifList
    Btrue = []
    Bfalse = []
    if token.recognized_string =="elif":
        token=get_token()
        B = condition()
        Btrue = B[0]
        Bfalse = B[1]
        backPatch(Btrue, nextQuad())
        if token.recognized_string ==":":
            token=get_token()
            if token.recognized_string == "#{":
                token=get_token()
                statements()
                backPatch(ifList, nextQuad())
                if token.recognized_string == "#}":
                    token=get_token()
                else:
                    print("Error there is not #} after else: #{ in line", token.line_number)
                    exit(-1)
            else:
                statement()
def while_stat():
    global token
    Btrue = []
    Bfalse = []
    if token.recognized_string =="while":
        token=get_token()
        Bquad = nextQuad()
        B = condition()
        Btrue = B[0]
        Bfalse = B[1]
        backPatch(Btrue, nextQuad())
        if token.recognized_string ==":":
            token=get_token()
            if token.recognized_string=="#{":
                token=get_token()
                statements()
                genQuad("jump","_","_",Bquad)
                backPatch(Bfalse,nextQuad())
                if token.recognized_string=="#}":
                    token=get_token()
                else:
                    print("Error there is not #} after while #{ in line", token.line_number)
                    exit(-1)
            else:
                statement()
                genQuad("jump", "_", "_", Bquad)
                backPatch(Bfalse, nextQuad())
        else:
            print("Error,there is not : after while in line", token.line_number)
            exit(-1)
    else:
        print("Error,there is not while in line", token.line_number)
        exit(-1)

def expression():
    global token
    optional_sign()
    T1place = term()
    while token.family =="addOperator":
        add_operator = ADD_OP()
        T2place = term()
        w = new_temp()
        genQuad(add_operator,T1place,T2place,w)
        T1place = w
    Eplace = T1place
    return Eplace

def term():
    global token
    F1place = factor()
    while token.family=="mulOperator":
        mul_operator = MUL_OP()
        F2place = factor()
        w = new_temp()
        genQuad(mul_operator,F1place,F2place,w)
        F1place = w
    Tplace = F1place
    return Tplace

def factor():
    global token
    if token.family == "number":
        Fplace = token.recognized_string
        token = get_token()
    elif token.recognized_string == "(":
        token = get_token()
        Eplace = expression()
        if token.recognized_string == ")":
            Fplace = Eplace
            token = get_token()
        else:
            print("Error,there is not ) after ( at factor in line", token.line_number)
            exit(-1)
    elif token.family == "identifier":
        function_name = token.recognized_string
        token = get_token()
        Fplace = idtail(function_name)
    elif token.recognized_string == "-":
        if token.family == "number":
            token = get_token()
    else:
        print("Error,there is not numerical constant or expression or identifier at factor in line", token.line_number)
        exit(-1)
    return Fplace

def idtail(function_name):
    global token
    if token.recognized_string == "(":
        token = get_token()
        actual_par_list()
        w = new_temp()
        genQuad('par', w, 'RET', '_')
        genQuad('call', function_name, '_', '_')
        if token.recognized_string == ")":
            token = get_token()
            return w
        else:
            print("Error ,there is not ) after ( at idtail ",token.line_number)
            exit(-1)
    else:
        return function_name
def actual_par_list():
    global token
    if token.family== "number" or token.recognized_string== "(" or token.family== "identifier":
        Eplace = expression()
        genQuad('par', Eplace, 'CV', '_')
        while token.recognized_string== ",":
            token=get_token()
            Eplace = expression()
            genQuad('par', Eplace, 'CV', '_')

def optional_sign():
    global token
    if token.family== "addOperator":
            ADD_OP()

def ADD_OP():
    global token
    add_operator = token.recognized_string
    if token.recognized_string== "+":
        token=get_token()
    elif token.recognized_string== "-":
        token=get_token()
    return add_operator

def MUL_OP():
    global token
    mull_operator = token.recognized_string
    if token.recognized_string == "*":
        token=get_token()
    elif token.recognized_string == "//":
        token=get_token()
    elif token.recognized_string =="%":
        token=get_token()
    return mull_operator

def condition():
    global token
    Btrue = []
    Bfalse = []
    Q1 = bool_term()
    Q1true = Q1[0]
    Q1false = Q1[1]
    Btrue = Q1true
    Bfalse = Q1false
    while token.recognized_string== "or":
        backPatch(Q1false, nextQuad())
        token=get_token()
        Q2 = bool_term()
        Q2true = Q2[0]
        Q2false = Q2[1]
        Btrue =merge(Q1true,Q2true)
        Bfalse = Q2false
    return Btrue,Bfalse

def bool_term():
    global token
    Btrue = []
    Bfalse = []
    B1 = bool_factor()
    Qtrue = B1[0]
    Qfalse = B1[1]
    Btrue = Qtrue
    Bfalse = Qfalse
    while token.recognized_string== "and":
        backPatch(Qtrue, nextQuad())
        token=get_token()
        B2 = bool_factor()
        Q2true = B2[0]
        Q2false = B2[1]
        Qfalse = merge(Qfalse,Q2false)
        Qtrue = Q2true
        Btrue = Qtrue
        Bfalse = Qfalse
    return Btrue,Bfalse

def bool_factor():
    global token
    Btrue = []
    Bfalse = []
    if token.recognized_string== "not":
        token=get_token()
        if token.recognized_string== "(":
            token=get_token()
            R = condition()
            if token.recognized_string== ")":
                token=get_token()
                Rtrue = R[0]
                Rfalse = R[1]
                Btrue = Rfalse
                Bfalse = Rtrue
            else:
                print("Error,there is not ) after not( at boolfactor in line",token.line_number)
                exit(-1)
        else:
            print("Error,there is not ( after not at boolfactor in line",token.line_number)
            exit(-1)
    elif token.recognized_string== "(":
        token=get_token()
        R = condition()
        if token.recognized_string== ")":
            token=get_token()
            Rtrue = R[0]
            Rfalse = R[1]
            Btrue = Rtrue
            Bfalse = Rfalse
        else:
            print("Error,there is not ) after ( at boolfactor in line",token.line_number)
            exit(-1)
    else:
        E1place = expression()
        rel_operator = REL_OP()
        E2place = expression()
        Rtrue = makeList(nextQuad())
        genQuad(rel_operator, E1place, E2place,"_")
        Rfalse = makeList(nextQuad())
        genQuad("jump","_","_","_")
        Btrue = Rtrue
        Bfalse = Rfalse
    return Btrue,Bfalse

def REL_OP():
    global token
    rel_operator = token.recognized_string
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
    return rel_operator


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
    write_Quads(file)
    file.close()
    file2.close()
    final_file.close()
main()