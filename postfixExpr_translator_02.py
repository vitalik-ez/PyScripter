from lexer import lex
from lexer import tableOfSymb, tableOfId, tableOfConst, sourceCode, tableToPrint, tableOfIdToPrint, tableOfConstToPrint
import lexer

lex()

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow=1    

# довжина таблиці символів програми 
# він же - номер останнього запису
len_tableOfSymb=len(tableOfSymb)

toView = False

# Список для зберігання ПОЛІЗу - 
# коду у постфіксній формі
postfixCode = []

def postfixTranslator():
    # чи був успішним лексичний розбір
    if (True,'Lexer') == lexer.FSuccess:

        #print('-'*30)
        #tableToPrint('All')
        #tableOfIdToPrint()
        #tableOfConstToPrint()

        #print('tableOfSymb:{0}'.format(tableOfSymb))
        #print('-'*30)
        #print(('len_tableOfSymb',len_tableOfSymb))

        return parseProgram()

# Функція для розбору за правилом
# Program = StatementList
# читає таблицю розбору tableOfSymb
def parseProgram():
    try:
        # перевірити синтаксичну коректність списку інструкцій StatementList
        parseStatementList()
        # повідомити про синтаксичну коректність програми
        print('Translator: Переклад у ПОЛІЗ та синтаксичний аналіз завершились успішно')
        FSuccess = (True,'Translator')
        return FSuccess
    except SystemExit as e:
        FSuccess = (False,'Translator')
        # Повідомити про факт виявлення помилки
        print('Parser: Аварійне завершення програми з кодом {0}'.format(e))

            
# Функція перевіряє, чи у поточному рядку таблиці розбору
# зустрілась вказана лексема lexeme з токеном token
# параметр indent - відступ при виведенні у консоль
def parseToken(lexeme,token,indent):
    # доступ до поточного рядка таблиці розбору
    global numRow
    
    # якщо всі записи таблиці розбору прочитані,
    # а парсер ще не знайшов якусь лексему
    if numRow > len_tableOfSymb :
        failParse('неочікуваний кінець програми',(lexeme,token,numRow))
        
    # прочитати з таблиці розбору 
    # номер рядка програми, лексему та її токен
    numLine, lex, tok = getSymb()   
    # тепер поточним буде наступний рядок таблиці розбору
    numRow += 1
        
    # чи збігаються лексема та токен таблиці розбору з заданими 
    if (lex, tok) == (lexeme,token):
        # вивести у консоль номер рядка програми та лексему і токен
        #print(indent+'parseToken: В рядку {0} токен {1}'.format(numLine,(lexeme,token)))
        return True
    else:
        # згенерувати помилку та інформацію про те, що 
        # лексема та токен таблиці розбору (lex,tok) відрізняються від
        # очікуваних (lexeme,token)
        failParse('невідповідність токенів',(numLine,lex,tok,lexeme,token))
        return False


# Прочитати з таблиці розбору поточний запис
# Повертає номер рядка програми, лексему та її токен
def getSymb():
    if numRow > len_tableOfSymb:
        return 'endOfProgram'
            #failParse('getSymb(): неочікуваний кінець програми',numRow)
    # таблиця розбору реалізована у формі словника (dictionary)
    # tableOfSymb[numRow]={numRow: (numLine, lexeme, token, indexOfVarOrConst)
    numLine, lexeme, token, _ = tableOfSymb[numRow] 
    return numLine, lexeme, token        


# Обробити помилки
# вивести поточну інформацію та діагностичне повідомлення 
def failParse(str,tuple):
    if str == 'неочікуваний кінець програми':
        (lexeme,token,numRow)=tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format((lexeme,token),numRow))
        exit(1001)
    if str == 'getSymb(): неочікуваний кінець програми':
        numRow=tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {0}. \n\t Останній запис - {1}'.format(numRow,tableOfSymb[numRow-1]))
        exit(1002)
    elif str == 'невідповідність токенів':
        (numLine,lexeme,token,lex,tok)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - ({3},{4}).'.format(numLine,lexeme,token,lex,tok))
        exit(1)
    elif str == 'невідповідність інструкцій':
        (numLine,lex,tok,expected)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
        exit(2)
    elif str == 'невідповідність у Expression.Factor':
        (numLine,lex,tok,expected)=tuple
        print('Parser ERROR: \n\t В рядку {0} неочікуваний елемент ({1},{2}). \n\t Очікувався - {3}.'.format(numLine,lex,tok,expected))
        exit(3)
    elif str == 'неочікуваний кінець програми endOfProgram':
        (numRow, lexeme)=tuple
        print('Parser ERROR: \n\t Неочікуваний кінець програми - в таблиці символів (розбору) немає запису з номером {1}. \n\t Очікувалось - {0}'.format(lexeme,numRow))
        exit(1003)
    #elif str == 'Програма завершена':
    #    exit(100)


          
# Функція для розбору за правилом для StatementList 
# StatementList = Statement  { Statement }
# викликає функцію parseStatement() доти,
# доки parseStatement() повертає True
def parseStatementList(fiStatement=None, endStatement=None):
    #print('parseStatementList():')
    while parseStatement(fiStatement, endStatement):
        pass
    return True


def parseStatement(fiStatement, endStatement):
    # прочитаємо поточну лексему в таблиці розбору
    values = getSymb()
    if values != 'endOfProgram':
        numLine, lex, tok = values
        #print('\tparseStatement():')
        # якщо токен - ідентифікатор
        # обробити інструкцію присвоювання
        if lex in ('int','real','boolean') and tok == ('keyword'):
            parseDeclaration()
            return True
        elif tok == 'ident':    
            parseAssign()      
            return True
        elif lex == 'input':    
            parseInput()       
            return True
        elif lex == 'print':    
            parsePrint()       
            return True
        # якщо лексема - ключове слово 'if'
        # обробити інструкцію розгалудження
        elif (lex, tok) == ('if','keyword'):
            parseIf()
            return True 

        elif (lex, tok) == ('for','keyword'):
            parseFor()
            return True 

        # тут - ознака того, що всі інструкції були коректно 
        # розібрані і була знайдена остання лексема програми.
        # тому parseStatement() має завершити роботу

        # parseStatement() має завершити роботу в ifStatement
        elif fiStatement == True and (lex, tok) == ('fi','keyword'):
            return False
        elif endStatement == True and (lex, tok) == ('end','keyword'):
            return False
        else: 
            #print('here!')
            #if numRow == len_tableOfSymb:
            #    return False
            # жодна з інструкцій не відповідає 
            # поточній лексемі у таблиці розбору,
            if fiStatement:
                failParse('невідповідність інструкцій',(numLine,lex,tok,'fi'))
            elif endStatement:
                failParse('невідповідність інструкцій',(numLine,lex,tok,'end'))
            else:
                failParse('невідповідність інструкцій',(numLine,lex,tok,'ident або if (fi) або for (end)'))
            return False
    else:
        print('endOfProgram')
        return False

    


def parsePrint():
    global numRow
    #print('\t'*3 + ' parsePrint():')
    numRow += 1
    numLine, lex, tok = getSymb()
    if lex=='(':
        #print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
        parseIdentList()
        numLine, lex, tok = getSymb()
        if lex == ')':
            #print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
            numRow += 1
            numLine, lex, tok = getSymb()
            if lex == ';':
                #print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
                numRow += 1
                return True
            else:
                failParse('невідповідність інструкцій',(numLine,lex,tok,';'))
        else:
            failParse('невідповідність інструкцій',(numLine,lex,tok,')'))

    else:
        failParse('невідповідність інструкцій',(numLine,lex,tok,'('))
    return False

def parseIdentList():
    global numRow
    #print('\t'*4+'parse IdentList()')
    while True:
        numRow += 1
        #print('\t'*5+'parse Ident()')
        numLine, lex, tok = getSymb()
        parseToken(lex, 'ident', '\t'*6)
        numLine, lex, tok = getSymb()
        if lex != ',':
            break


def parseInput():
    global numRow
    #print('\t'*3 + ' parseInput():')
    numRow += 1
    numLine, lex, tok = getSymb()
    if lex=='(':
        #print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
        #print('\t'*4, 'parseIdent():')
        numRow += 1
        numLine, lex, tok = getSymb()
        if tok == 'ident':
            #print('\t'*5 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
            numRow += 1
            numLine, lex, tok = getSymb()
            if lex == ')':
                #print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
                numRow += 1
                numLine, lex, tok = getSymb()
                if lex == ';':
                    #print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
                    numRow += 1
                    return True
                else:
                    failParse('невідповідність інструкцій',(numLine,lex,tok,';'))
            else:
                failParse('невідповідність інструкцій',(numLine,lex,tok,')'))
        else:
            failParse('невідповідність інструкцій',(numLine,lex,tok,'ident'))
    else:
        failParse('невідповідність інструкцій',(numLine,lex,tok,'('))
    return False


def parseDeclaration():
    global numRow
    #print('\t'*3 + ' parseDeclaration():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    if tok == 'keyword' and lex in ('real', 'boolean', 'int'):
        #print('\t'*4+'parseType()')
        #print('\t'*5 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        #print('\t'*4+'parse IdentList()')
        while True:
            values = getSymb()
            if values == 'endOfProgram':
                failParse('неочікуваний кінець програми endOfProgram', (numLine, 'ident'))
                return False
            numLine, lex, tok = values
            #print('\t'*5+'parse Ident()')
            parseToken(lex, 'ident', '\t'*6)
            values = getSymb()
            if values == 'endOfProgram':
                failParse('неочікуваний кінець програми endOfProgram', (numLine, ';'))
                return False
            numLine, lex, tok = values
            if lex == ';':
                parseToken(';', 'punct', '\t'*6)
                break
            parseToken(',', 'punct','\t'*6)
        return True
        #numLine, lex, tok = getSymb()
        #values = getSymb()
        #print("values", values)
        #if values != 'endOfProgram':
        #    numLine, lex, tok = values
        #    return True if lex in ('int', 'boolean', 'real') else False
        #else:
        #    return False
    else:
        # жодна з інструкцій не відповідає
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'int, real, boolean'))
        return False

# виводить у консоль інформацію про 
# перебіг трансляції
def configToPrint(lex,numRow):
    stage = '\nКрок трансляції\n'
    stage += 'лексема: \'{0}\'\n'
    stage += 'tableOfSymb[{1}] = {2}\n'
    stage += 'postfixCode = {3}\n'
    # tpl = (lex,numRow,str(tableOfSymb[numRow]),str(postfixCode))
    print(stage.format(lex,numRow,str(tableOfSymb[numRow]),str(postfixCode)))


def parseAssign(IndExpr=None):
    # номер запису таблиці розбору
    global numRow, postfixCode
    #print('\t'*3+'parseAssign():')

    # взяти поточну лексему
    numLine, lex, tok = getSymb()

    # починаємо трансляцію інструкції присвоювання за означенням:
    postfixCode.append((lex, tok))     # Трансляція   
                                # ПОЛІЗ ідентифікатора - ідентифікатор

    if toView: configToPrint(lex,numRow)

    # встановити номер нової поточної лексеми
    numRow += 1

    current_row = numRow
    #print('\t'*4+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # якщо була прочитана лексема - '='
    if parseToken('=','assign_op','\t\t\t\t'):
        # розібрати арифметичний вираз
        parseExpression()
        numLine, lex, tok = getSymb()
        if tok in ('rel_op') and IndExpr == None:
            #print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))

            # Трансляція 
            postfixCode.append((lex, 'rel_op'))  
            if toView: configToPrint('=',current_row)
            ###

            numRow += 1
            parseExpression()
            if parseToken(';','punct', '\t\t\t\t'):
                # ERROR !!!!!!!!!! rel_op
                postfixCode.append(('=', 'assign_op'))# Трансляція   
                                    # Бінарний оператор  '='
                                    # додається після своїх операндів
                if toView: configToPrint('=',current_row)
                return True
        elif lex == 'to' or parseToken(';', 'punct', '\t\t\t\t'):
            postfixCode.append(('=', 'assign_op'))# Трансляція   
                                    # Бінарний оператор  '='
                                    # додається після своїх операндів
            if toView: configToPrint('=',current_row)
            return True

        else:
            return False
       
    else: return False    


def parseExpression():
    global numRow, postfixCode
    #print('\t'*5+'parseExpression():')
    numLine, lex, tok = getSymb()
    parseTerm()
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            #print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            current_row = numRow
            parseTerm()
            postfixCode.append((lex, tok)) # lex - бінарний оператор  '+' чи '-'
            if toView: configToPrint(lex,current_row)
        else:
            F = False
    return True

def parseTerm():
    global numRow
    #print('\t'*6+'parseTerm():')
    parseFactor()
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        values = getSymb()
        if values == 'endOfProgram':
            failParse('неочікуваний кінець програми endOfProgram', (numRow, ';'))
            return False
        numLine, lex, tok = values
        if tok in ('mult_op') or tok in ('exp_op') : # or tok in ('rel_op')
            numRow += 1
            #print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            current_row = numRow
            parseFactor()

            postfixCode.append((lex, tok)) # lex - бінарний оператор  '*' чи '/'
            if toView: configToPrint(lex,current_row)
        else:
            F = False
    return True

def parseFactor():
    global numRow
    #print('\t'*7+'parseFactor():')
    values = getSymb()
    if values == 'endOfProgram':
        failParse('неочікуваний кінець програми endOfProgram', (numRow, 'ident або int, real, boolean'))
        return False
    numLine, lex, tok = values
    #print('\t'*7+'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine,(lex, tok)))
    
    # для - мінуса перед значенням
    unary = None
    if tok == 'add_op':
        unary = (lex, 'NEG') if lex == '-' else (lex, 'PLS')# Трансляція мінус - або плюс + до змінної
        #if lex == '-':
        #    postfixCode.append((lex, 'NEG'))      
        #else:
        #    postfixCode.append((lex, 'PLS')) 
        numRow += 1
        values = getSymb()
        if values == 'endOfProgram':
            failParse('неочікуваний кінець програми endOfProgram', (numRow, 'ident або int, real, boolean'))
            return False
        numLine, lex, tok = values  
    ### 

    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('int','real','boolval','ident'): 
        postfixCode.append((lex, tok))      # Трансляція
                                # ПОЛІЗ константи або ідентифікатора 
                                # відповідна константа або ідентифікатор
        if toView: configToPrint(lex,numRow)
        # + -
        if unary is not None:
            postfixCode.append(unary) 
        ###

        numRow += 1
        #print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    
    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex=='(':
        numRow += 1
        parseExpression()
        parseToken(')','brackets_op','\t'*7)
        #print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
        # + -
        if unary is not None:
            postfixCode.append(unary) 
        ###
    else:
        failParse('невідповідність у Expression.Factor',(numLine,lex,tok,'int, float, ident або \'(\' Expression \')\'')) # rel_op
    return True

# розбір інструкції розгалудження за правилом
# IfStatement = if BoolExpr then Statement else Statement endif
# функція названа parseIf() замість parseIfStatement()
def parseIf():
    global numRow
    numLine, lex, tok = getSymb()
    if lex=='if' and tok=='keyword':
        #print('\t'*3, 'parseIfStatement():')
        numRow += 1
        parseBoolExpr()
        parseToken('then','keyword','\t'*4)
        #print('parceDoBlock', '\t'*4)
        parseStatementList(fiStatement=True)
        parseToken('fi','keyword','\t'*4)
    else: return False

def parseFor():
    global numRow
    _, lex, tok = getSymb()
    if lex=='for' and tok=='keyword':
        #print('\t'*3, 'parseForStatement():')
        numRow += 1
        parseIndExpr()
        parseToken('do','keyword','\t'*4)
        #print('parceDoBlock', '\t'*4)
        parseStatementList(endStatement=True)
        parseToken('end','keyword','\t'*4)
        return True
    else: return False

def parseIndExpr():
    global numRow
    numLine, lex, tok = getSymb()
    if tok == 'ident':    
        parseAssign(IndExpr=True)
        if parseToken('to','keyword','\t'*4):
            parseExpression()
            return True
        else:
            return False
    else: 
        # жодна з інструкцій не відповідає 
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій',(numLine,lex,tok,'ident'))
        return False

# розбір логічного виразу за правиллом
# BoolExpr = Expression ('='|'<='|'>='|'<'|'>'|'<>') Expression
def parseBoolExpr():
    global numRow
    parseExpression()
    numLine, lex, tok = getSymb()
    if tok in ('rel_op'):
        numRow += 1
        #print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('невідповідність інструкцій',(numLine,lex,tok,'rel_op'))
    parseExpression()
    return True    

# запуск парсера
#postfixTranslator()  