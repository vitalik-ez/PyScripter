from lexer import lex
from lexer import tableOfSymb #, tableOfVar, tableOfConst


lex()
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('-'*30)

# номер рядка таблиці розбору/лексем/символів ПРОГРАМИ tableOfSymb
numRow=1    

# довжина таблиці символів програми 
# він же - номер останнього запису
len_tableOfSymb=len(tableOfSymb)
print(('len_tableOfSymb',len_tableOfSymb))

# Функція для розбору за правилом
# Program = StatementList
# читає таблицю розбору tableOfSymb
def parseProgram():
    try:
        # перевірити синтаксичну коректність списку інструкцій StatementList
        parseStatementList()
        # повідомити про синтаксичну коректність програми
        print('Parser: Синтаксичний аналіз завершився успішно')
        return True
    except SystemExit as e:
        if f"{e}" == '100':
             print('Parser: Синтаксичний аналіз завершився успішно')
        else:
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
        print(indent+'parseToken: В рядку {0} токен {1}'.format(numLine,(lexeme,token)))
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
    if numRow > len_tableOfSymb :
            failParse('Програма завершена',numRow)
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
    elif str == 'Програма завершена':
        exit(100)


          
# Функція для розбору за правилом для StatementList 
# StatementList = Statement  { Statement }
# викликає функцію parseStatement() доти,
# доки parseStatement() повертає True
def parseStatementList():
        print('parseStatementList():')
        while parseStatement():
                pass
        return True


def parseStatement():
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    print('\tparseStatement():')
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
    elif (lex, tok) == ('end','keyword'):
            return False

    else: 
        # жодна з інструкцій не відповідає 
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій',(numLine,lex,tok,'ident або if'))
        return False


def parsePrint():
    global numRow
    print('\t'*3 + ' parsePrint():')
    numRow += 1
    numLine, lex, tok = getSymb()
    if lex=='(':
        print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
        parseIdentList()
        numLine, lex, tok = getSymb()
        if lex == ')':
            print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
            numRow += 1
            numLine, lex, tok = getSymb()
            if lex == ';':
                print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
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
    print('\t'*4+'parse IdentList()')
    while True:
        numRow += 1
        print('\t'*5+'parse Ident()')
        numLine, lex, tok = getSymb()
        parseToken(lex, 'ident', '\t'*6)
        numLine, lex, tok = getSymb()
        if lex != ',':
            break


def parseInput():
    global numRow
    print('\t'*3 + ' parseInput():')
    numRow += 1
    numLine, lex, tok = getSymb()
    if lex=='(':
        print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
        print('\t'*4, 'parseIdent():')
        numRow += 1
        numLine, lex, tok = getSymb()
        if tok == 'ident':
            print('\t'*5 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
            numRow += 1
            numLine, lex, tok = getSymb()
            if lex == ')':
                print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
                numRow += 1
                numLine, lex, tok = getSymb()
                if lex == ';':
                    print('\t'*4 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
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
    print('\t'*3 + ' parseDeclaration():')
    # прочитаємо поточну лексему в таблиці розбору
    numLine, lex, tok = getSymb()
    if tok == 'keyword' and lex in ('real', 'boolean', 'int'):
        print('\t'*4+'parseType()')
        print('\t'*5 + 'parseToken: В рядку {0} токен {1}'.format(numLine, (lex, tok)))
        numRow += 1
        print('\t'*4+'parse IdentList()')
        while True:
            numLine, lex, tok = getSymb()
            print('\t'*5+'parse Ident()')
            parseToken(lex, 'ident', '\t'*6)
            numLine, lex, tok = getSymb()
            if lex == ';':
                parseToken(';', 'punct', '\t'*6)
                break
            parseToken(',', 'punct','\t'*6)
        numLine, lex, tok = getSymb()
        return True if lex in ('int', 'boolean', 'real') else False
    else:
        # жодна з інструкцій не відповідає
        # поточній лексемі у таблиці розбору,
        failParse('невідповідність інструкцій', (numLine, lex, tok, 'int, real, boolean'))
        return False


def parseAssign():
    # номер запису таблиці розбору
    global numRow
    print('\t'*3+'parseAssign():')

    # взяти поточну лексему
    numLine, lex, tok = getSymb()
    # встановити номер нової поточної лексеми
    numRow += 1

    print('\t'*4+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    # якщо була прочитана лексема - '='
    if parseToken('=','assign_op','\t\t\t\t'):
        # розібрати арифметичний вираз
        parseExpression()
        numLine, lex, tok = getSymb()
        if lex == 'to' or parseToken(';', 'punct', '\t\t\t\t'):
            return True
    else: return False    


def parseExpression():
    global numRow
    print('\t'*5+'parseExpression():')
    numLine, lex, tok = getSymb()
    parseTerm()
    F = True
    # продовжувати розбирати Доданки (Term)
    # розділені лексемами '+' або '-'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('add_op'):
            numRow += 1
            print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            parseTerm()
        else:
            F = False
    return True

def parseTerm():
    global numRow
    print('\t'*6+'parseTerm():')
    parseFactor()
    F = True
    # продовжувати розбирати Множники (Factor)
    # розділені лексемами '*' або '/'
    while F:
        numLine, lex, tok = getSymb()
        if tok in ('mult_op') or tok in ('exp_op') : # or tok in ('rel_op')
            numRow += 1
            print('\t'*6+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
            parseFactor()
        else:
            F = False
    return True

def parseFactor():
    global numRow
    print('\t'*7+'parseFactor():')
    numLine, lex, tok = getSymb()
    print('\t'*7+'parseFactor():=============рядок: {0}\t (lex, tok):{1}'.format(numLine,(lex, tok)))
    
    # перша і друга альтернативи для Factor
    # якщо лексема - це константа або ідентифікатор
    if tok in ('int','real','boolean','ident')  or tok in ('boolval'):
            numRow += 1
            print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    
    # третя альтернатива для Factor
    # якщо лексема - це відкриваюча дужка
    elif lex=='(':
        numRow += 1
        parseExpression()
        parseToken(')','brackets_op','\t'*7)
        print('\t'*7+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('невідповідність у Expression.Factor',(numLine,lex,tok,'int, float, ident або \'(\' Expression \')\'')) # rel_op
    return True

# розбір інструкції розгалудження за правилом
# IfStatement = if BoolExpr then Statement else Statement endif
# функція названа parseIf() замість parseIfStatement()
def parseIf():
    global numRow
    _, lex, tok = getSymb()
    if lex=='if' and tok=='keyword':
        print('\t'*3, 'parseIfStatement():')
        numRow += 1
        parseBoolExpr()
        parseToken('then','keyword','\t'*4)
        print('parceDoBlock', '\t'*4)
        parseStatement()
        parseToken('fi','keyword','\t'*4)
        return True
    else: return False

def parseFor():
    global numRow
    _, lex, tok = getSymb()
    if lex=='for' and tok=='keyword':
        print('\t'*3, 'parseForStatement():')
        numRow += 1
        parseIndExpr()
        parseToken('do','keyword','\t'*4)
        print('parceDoBlock', '\t'*4)
        parseStatementList()
        parseToken('end','keyword','\t'*4)
        return True
    else: return False

def parseIndExpr():
    global numRow
    numLine, lex, tok = getSymb()
    if tok == 'ident':    
        parseAssign()
        if parseToken('to','keyword','\t'*4):
            parseExpression()
        return True
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
        print('\t'*5+'в рядку {0} - {1}'.format(numLine,(lex, tok)))
    else:
        failParse('невідповідність інструкцій',(numLine,lex,tok,'rel_op'))
    parseExpression()
    return True    

# запуск парсера
parseProgram()  