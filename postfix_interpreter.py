from lexer import lex, tableToPrint
from lexer import tableOfSymb, tableOfId, tableOfConst, tableOfLabel, sourceCode
from postfixExpr_translator_02 import postfixTranslator, postfixCode
from stack01 import Stack

stack = Stack()

toView = True

def postfixInterpreter():
    FSuccess = postfixTranslator()
    # чи була успішною трансляція
    if (True,'Translator') == FSuccess:
        print('\nПостфіксний код: \n{0}'.format(postfixCode))
        return postfixProcessing()
    else:
        # Повідомити про факт виявлення помилки
        print('Interpreter: Translator завершив роботу аварійно')
        return False

print('-'*30)

# tableToPrint('All')
# print('\nПочатковий код програми: \n{0}'.format(sourceCode))

# while len(str(postfixCode))==0: pass
# print('\nКод програми у постфіксній формі (ПОЛІЗ): \n{0}'.format(postfixCode))

# lenCode=len(str(postfixCode))
# print('\n---------------Код програми у постфіксній формі (ПОЛІЗ): \n{0}'.format(postfixCode))
def check_name_variables():
    global tableOfSymb
    a, list_used_names = list(tableOfSymb.values()), []
    #print(a)
    for i in range(len(a)):
        if a[i][1] in ('int', 'real', 'boolean'):
            i += 1
            while a[i][1] != ';':
                if a[i][1] != ',':
                    if a[i][1] in list_used_names:
                        failRunTime('зміна вже використовується', a[i][1])
                    else:
                        list_used_names.append(a[i][1])
                i += 1

def processing_JF(instrNum):
    global postfixCode, stack, tableOfLabel
    b = stack.pop()
    if b == ('true', 'boolval'):
        return instrNum+1
    else:
        number = postfixCode[instrNum-1][0][1]
        #print('number', number)
        return tableOfLabel[f'm{int(number)}']


def doJumps(tok, instrNum):
    if tok == 'jump':
        next = processing_JUMP()
    elif tok == 'colon':
        return instrNum+1
    elif tok == 'jf':
        next = processing_JF(instrNum)
    return next

def doForJumps(tok, instrNum):
    if tok == 'jfor':
        b = stack.pop()
        if b == ('true', 'boolval'):
            return instrNum + 1
        else:
            return instrNum + 6
    elif tok == 'jfor_condition':
        b = stack.pop()
        if b == ('false', 'boolval'):
            return tableOfLabel['LOOP_END']+1
        else:
            return instrNum + 1
    elif tok == 'loop_end':
        return tableOfLabel['m1']


def input_output(tok):
    global announcement_variable
    if tok == 'out':
        out_v = stack.pop()
        value = tableOfId[out_v[0]][2]
        if value == 'val_undef':
            failRunTime('неініціалізована змінна при виводі', out_v[0])
        else:
            print(f'PRINT: {out_v[0]} =', tableOfId[out_v[0]][2])
    elif tok == 'input':
        out_v = stack.pop()
        type_var = announcement_variable[out_v[0]]
        try:
            value = input(f'Enter a variable value: {type_var} {out_v[0]} = ')
            if type_var == 'int':
                if value.rfind('.'):
                    value = int(float(value))
                else:
                    value = int(value)
            elif type_var == 'real':
                value = float(value)
            elif type_var == 'boolean':
                #if value != 'true' and value != 'false':
                #    failRunTime('введення не відповідного типу змінної', type_var)
                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                else:
                    value = bool(float(value))
                value = str(value).lower()
            index = tableOfId[out_v[0]][0]
            tableOfId[out_v[0]] = (index, type_var, value)
        except ValueError as e:
            failRunTime('введення не відповідного типу змінної', type_var)
        


announcement_variable = {}
def postfixProcessing():
    global stack, postfixCode, announcement_variable, maxNumb
    maxNumb=len(postfixCode)
    instrNum = 0
    check_name_variables()
    try:
        while instrNum < maxNumb:
            lex,tok = postfixCode[instrNum]
            # перевірка чи була об'явлена змінна ident
            if lex in ('r1', 'r2'): announcement_variable[lex] = 'int'
            if tok == 'ident':
                for numLine, value in tableOfSymb.items():
                    if lex == value[1] and value[-1] == tableOfId[lex][0]:
                        check_announcement = [ i for i in list(tableOfSymb.values()) if i[0] == value[0] ]
                        announcement = False
                        for j in check_announcement: 
                            if j[1] in ('int', 'real', 'boolean'):
                                announcement = True
                                announcement_variable[lex] = j[1]
                                break
                        if not announcement:
                            failRunTime('змінна не була оголошена', lex)
                        break
            ###
            if tok in ('int','real','ident', 'boolval'): # boolean !!!
                stack.push((lex,tok))
                nextNum = instrNum + 1
            elif tok in ('jf', 'colon'):
                nextNum = doJumps(tok, instrNum)
            elif tok in ('jfor', 'jfor_condition', 'loop_end'):
                nextNum = doForJumps(tok, instrNum)
            elif tok in ('out', 'input'):
                input_output(tok)
                nextNum = instrNum + 1
            else: 
                doIt(lex,tok)
                nextNum = instrNum + 1
            #if toView: configToPrint(instrNum+1, lex, tok, maxNumb)
            instrNum = nextNum
        configToPrint(maxNumb, lex, tok, maxNumb)
        return True
    except SystemExit as e:
        # Повідомити про факт виявлення помилки
        print('RunTime: Аварійне завершення програми з кодом {0}'.format(e))
    return True

def configToPrint(step,lex,tok,maxN):
    if step == 1:
        print('='*30+'\nInterpreter run\n')
        tableToPrint('All')
    '''
    print('\nКрок інтерпретації: {0}'.format(step))
    if tok in ('int','real'):
        print('Лексема: {0} у таблиці констант: {1}'.format((lex,tok),lex + ':' +str(tableOfConst[lex])))
    elif tok in ('ident'):
        print('Лексема: {0} у таблиці ідентифікаторів: {1}'.format((lex,tok),lex + ':' +str(tableOfId[lex])))
    else:
        print('Лексема: {0}'.format((lex,tok)))

    print('postfixCode={0}'.format(postfixCode)) 
    stack.print()
    '''
    if  step == maxN: 
        for Tbl in ('Id','Const', 'Label'): # 'Label'
            tableToPrint(Tbl)

    return True


def doIt(lex,tok):
    global stack, postfixCode, tableOfId, tableOfConst, announcement_variable, maxNumb
    exec_typing = lambda type_var, var: exec(f'temporary = {type_var}({var})', globals())
    if (lex,tok) == ('=', 'assign_op'):
        # зняти з вершини стека запис (правий операнд = число)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека ідентифікатор (лівий операнд)
        (lexL,tokL) = stack.pop()

        if tokR == 'ident':
            if tableOfId[lexR][1] == 'type_undef':
                failRunTime('неініціалізована змінна',(lexR,tableOfId[lexR],(lexL,tokL),lex,(lexR,tokR)))
        
        #if tokR == 'boolval':
        #    lexR = str(lexR)[0].upper() + str(lexR)[1:]
        #print(lexR, tokR)
        if announcement_variable[lexL] == 'boolean' and tokR == 'boolval':
            tableOfId[lexL] = (tableOfId[lexL][0],  tableOfConst[lexR][1], tableOfConst[lexR][2])
        else:
            if tokR == 'ident':
                tokR = tableOfId[lexR][1]
                lexR = tableOfId[lexR][2]

            if announcement_variable[lexL] != tokR:
                if announcement_variable[lexL] == 'real':
                    type_var = 'float'
                elif announcement_variable[lexL] == 'boolean':
                    type_var = 'bool'
                else:
                    type_var = announcement_variable[lexL]

                ###
                if lexR in ('true', 'false'):
                    lexR = str(lexR)[0].upper() + str(lexR)[1:]
                ###
                exec_typing(type_var, lexR)
                lexR = temporary
                ###
                if lexR in (True, False):
                    lexR = str(lexR)[0].lower() + str(lexR)[1:]
                ###
                toTableOfConst(lexR, announcement_variable[lexL])
                tableOfId[lexL] = (tableOfId[lexL][0],  tableOfConst[str(lexR)][1], tableOfConst[str(lexR)][2])
            else:
            # виконати операцію:
            # оновлюємо запис у таблиці ідентифікаторів
            # ідентифікатор/змінна  
            # (index не змінюється, 
            # тип - як у константи,  
            # значення - як у константи)
                tableOfId[lexL] = (tableOfId[lexL][0],  tableOfConst[lexR][1], tableOfConst[lexR][2])
    elif tok in ('add_op','mult_op', 'exp_op'):
        #print(lex)
        # зняти з вершини стека запис (правий операнд)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека запис (лівий операнд)
        (lexL,tokL) = stack.pop()
        #print('Left', (lexL,tokL))
        #print('Right', (lexR,tokR))

        #if (tokL,tokR) in (('int','real'),('real','int')):
        #    failRunTime('невідповідність типів',((lexL,tokL),lex,(lexR,tokR)))
        #else:
        processing_add_mult_op((lexL,tokL),lex,(lexR,tokR))
            # stack.push()
        #    pass

    elif tok == 'NEG':
        (lexR,tokR) = stack.pop()
        if tokR == 'ident':
            if tableOfId[lexR][1] == 'type_undef':
                failRunTime('неініціалізована змінна',(lexR,tableOfId[lexR],(lexL,tokL),lex,(lexR,tokR)))
            else:
                valR,tokR = (tableOfId[lexR][2],tableOfId[lexR][1])
        else:
            valR = tableOfConst[lexR][2]
        
        valR = -1 * valR
        stack.push((str(valR),tokR))
        toTableOfConst(valR,tokR)

    elif tok == 'PLS':
        pass
    elif tok == 'rel_op':
        # зняти з вершини стека запис (правий операнд)
        (lexR,tokR) = stack.pop()
        # зняти з вершини стека запис (лівий операнд)
        (lexL,tokL) = stack.pop()
        #if (tokL,tokR) in (('int','real'),('real','int')):
        #    failRunTime('невідповідність типів',((lexL,tokL),lex,(lexR,tokR)))
        #else:
        processing_add_mult_op((lexL,tokL),lex,(lexR,tokR))
    return True


def processing_add_mult_op(ltL,lex,ltR): 
    global stack, postfixCode, tableOfId, tableOfConst
    lexL,tokL = ltL
    lexR,tokR = ltR
    if tokL == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        #print(tableOfSymb)
        if tableOfId[lexL][1] == 'type_undef':
            failRunTime('неініціалізована змінна',(lexL,tableOfId[lexL],(lexL,tokL),lex,(lexR,tokR)))
        else:
            valL,tokL = (tableOfId[lexL][2],tableOfId[lexL][1])
    else:
        valL = tableOfConst[lexL][2]
    if tokR == 'ident':
        # print(('===========',tokL , tableOfId[lexL][1]))
        # tokL = tableOfId[lexL][1]
        if tableOfId[lexR][1] == 'type_undef':
            failRunTime('неініціалізована змінна',(lexR,tableOfId[lexR],(lexL,tokL),lex,(lexR,tokR)))
        else:
            valR,tokR = (tableOfId[lexR][2],tableOfId[lexR][1])
    else:
        valR = tableOfConst[lexR][2]
    # if :
        # print(('lexL',lexL,tableOfConst))
        # valL = tableOfConst[lexL][2]
        # valR = tableOfConst[lexR][2]
    getValue((valL,lexL,tokL),lex,(valR,lexR,tokR))

def getValue(vtL,lex,vtR):
    global stack, postfixCode, tableOfId, tableOfConst
    valL,lexL,tokL = vtL
    valR,lexR,tokR = vtR
    #if (tokL,tokR) in (('int','real'),('real','int')):
    #    print('yes')
    #    failRunTime('невідповідність типів',((lexL,tokL),lex,(lexR,tokR)))

    relatioal_operation = lambda valL, lex, valR: exec(f'temporary = {valL} {lex} {valR}', globals())

    if isinstance(valL, str):
        if valL == 'true':
            valL = True
        elif valL == 'false':
            valL = False
        else:
            valL = float(valL) if valL.rfind('.') else int(varlL)
    elif isinstance(valR, str):
        if valR == 'true':
            valR = True
        elif valR == 'false':
            valR = False
        else:
            valR = float(valR) if valR.rfind('.') else int(varlR)


    if lex == '+':
        value = valL + valR
    elif lex == '-':
        value = valL - valR
    elif lex == '*':
        value = valL * valR
    elif lex == '/' and valR == 0:
        failRunTime('ділення на нуль',((lexL,tokL),lex,(lexR,tokR)))
    elif lex == '/': # and (tokL, tokR) in (('real', 'int'), ('int', 'real'), ('real', 'int'))
        value = valL / valR
        tokL = 'real'
    elif lex == '**':
        print(valR, valL)
        value = valL ** valR
    elif lex == '//':
        value = valL // valR
    elif lex in ('<', '<=', '==', '>=', '>', '!='):
        if valL in ('true', 'false'):
            valL = valL[0].upper() + valL[1:]
        if valR in ('true', 'false'):
            valR = valR[0].upper() + valR[1:]
        relatioal_operation(valL, lex, valR)
        value = str(temporary)[0].lower() + str(temporary)[1:]
        tokL = 'boolval'

    #elif lex == '/' and tokL=='int':
    #    value = int(valL / valR)
    else:
        pass

    ###
    if (tokL, tokR) in (('int', 'real'), ('real', 'int')):
        tokL = 'real'
    ###

    stack.push((str(value),tokL))
    toTableOfConst(value,tokL)

        # tableOfId[lexR] = (tableOfId[lexR][0],  tableOfConst[lexL][1], tableOfConst[lexL][2])

def toTableOfConst(val,tok):
    lexeme = str(val)
    indx1=tableOfConst.get(lexeme)   
    if indx1 is None:
        indx = len(tableOfConst)+1 
        tableOfConst[lexeme]=(indx,tok,val)


def failRunTime(str,tuple):
    if str == 'невідповідність типів':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Типи операндів відрізняються у {0} {1} {2}'.format((lexL,tokL),lex,(lexR,tokR)))
        exit(1)
    elif str == 'неініціалізована змінна':
        (lx,rec,(lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Значення змінної {0}:{1} не визначене. Зустрілось у {2} {3} {4}'.format(lx,rec,(lexL,tokL),lex,(lexR,tokR)))
        exit(2)
    elif str == 'ділення на нуль':
        ((lexL,tokL),lex,(lexR,tokR))=tuple
        print('RunTime ERROR: \n\t Ділення на нуль у {0} {1} {2}. '.format((lexL,tokL),lex,(lexR,tokR)))
        exit(3)
    elif str == 'змінна не була оголошена':
        print('RunTime ERROR: \n\t Змінна {0} не була оголошена'.format(tuple))
        exit(1000)
    elif str == 'зміна вже використовується':
        print('RunTime ERROR: \n\t Змінна {0} вже оголошена'.format(tuple))
        exit(1000)
    elif str == 'неініціалізована змінна при виводі':
        print('RunTime ERROR: \n\t Змінна {0} не ініціалізована (вивід)'.format(tuple))
        exit(1056)
    elif str == 'введення не відповідного типу змінної':
        print('RunTime ERROR: \n\tНевідповідність типу введенного значення.\n\tОчікувався тип {0}'.format(tuple))
        exit(1200)
postfixInterpreter()