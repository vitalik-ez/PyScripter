 	
# Таблиця лексем мови
tableOfLanguageTokens = {'int':'keyword', 'real':'keyword', 'boolean':'keyword',
						 'input':'keyword', 'print':'keyword',
						 'for':'keyword', 'to':'keyword', 'do':'keyword', 'end':'keyword',
						 'if':'keyword','then':'keyword','fi':'keyword',
						 'true': 'boolval', 'false': 'boolval',
						 '=':'assign_op',
						 '-':'add_op', '+':'add_op',
						 '*':'mult_op', '/':'mult_op', '//':'mult_op',
						 '**':'exp_op',
						 '<':'rel_op', '<=':'rel_op', '>':'rel_op', '>=':'rel_op', '==':'rel_op', '!=':'rel_op',
						 '(':'brackets_op', ')':'brackets_op',
						 '.':'punct', ',':'punct',  ';':'punct',
						 ' ':'ws', '\t':'ws', 
						 '\n':'eol', '\r\n':'eol',
						 }
# Решту токенів визначаємо не за лексемою, а за заключним станом
tableIdentFloatInt = {2:'ident', 6:'real', 10:'real', 11:'int'}

# Діаграма станів
#               Q                                   q0          F
# M = ({0,1,2,4,5,6,9,11,12,13,14,101,102}, Σ,  δ , 0 , {2,6,9,12,13,14,101,102})

# δ - state-transition_function
stf={(0, 'ws'):0,
	 (0,'Letter'):1,  (1,'Letter'):1, (1,'Digit'):1, (1,'other'):2,
     (0,'Digit'):3, (3,'Digit'):3, (3,'other'):11, (3,'e'):7,
     (3,'dot'):4, (4,'Digit'):5, (5,'Digit'):5, (5,'other'):6, (5,'e'):7,
     (7,'+'):8 , (7,'-'):8, (7,''):8, (8,'Digit'):9, (9,'Digit'):9, (9,'other'):10, 
	 (0,'='):12, (12,'='):12.1, (12,'other'):12.2,
     (0, 'Punctuation'):13,
     (0, 'eol'):14,
     (0, 'arithmetic'):15, (0, '*'):16, (16, '*'):15, (16, 'other'):18,
     (0, '/'):17, (17, '/'):15, (17, 'other'):18,
     (0, 'relation_operator'):19, (19, '='):20, (19, 'other'):21,
     (0, 'other'):101,  
}


initState = 0   # q0 - стартовий стан
F={2, 6, 10, 11, 12.1, 12.2, 13, 14, 15, 101, 18, 20, 21}
Fstar={2, 6, 10, 11, 12.2, 18, 21}   # зірочка
Ferror={101}# обробка помилок


tableOfId={}   # Таблиця ідентифікаторів
tableOfConst={} # Таблиця констант
tableOfSymb={}  # Таблиця символів програми (таблиця розбору)


state=initState # поточний стан

f = open('test.my_lang', 'r')
sourceCode=f.read()
f.close()

# FSuccess - ознака успішності розбору
FSuccess = (True,'Lexer')

lenCode=len(sourceCode)-1       # номер останнього символа у файлі з кодом програми
numLine=1                       # лексичний аналіз починаємо з першого рядка
numChar=-1                      # з першого символа (в Python'і нумерація - з 0)
char=''                         # ще не брали жодного символа
lexeme=''                       # ще не починали розпізнавати лексеми


def lex():
	global state,numLine,char,lexeme,numChar,FSuccess
	try:
		while numChar<lenCode:
			char=nextChar()		
			classCh=classOfChar(char, state)		 
			state=nextState(state,classCh)
			if (is_final(state)): 			
				processing()				
				# if state in Ferror:	    
					# break					
			elif state==initState:lexeme=''
			else: lexeme+=char		
		print('Lexer: Лексичний аналіз завершено успішно')
	except KeyError as e:
		FSuccess = (False,'Lexer')
		print('Lexer: у рядку', numLine,'неочікуваний символ', char)
		print('Lexer: Аварійне завершення програми')
	except SystemExit as e:
		# Встановити ознаку неуспішності
		FSuccess = (False,'Lexer')
		# Повідомити про факт виявлення помилки
		print('Lexer: Аварійне завершення програми з кодом {0}'.format(e))

def processing():
	global state,lexeme,char,numLine,numChar, tableOfSymb
	if state==14:		# \n
		numLine+=1
		state=initState
	if state in (2,6,10,11,12.2):	# keyword, ident, real, int
		token=getToken(state,lexeme)
		if token!='keyword': # не keyword
			index=indexIdConst(state,lexeme)
			print('{0:<3d} {1:<10s} {2:<10s} {3:<2d} '.format(numLine,lexeme,token,index))
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,index)
		else: # якщо keyword
			print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token)) #print(numLine,lexeme,token)
			tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme=''
		numChar=putCharBack(numChar) # зірочка
		state=initState
	if state in (12.1,13, 15): #12:         #  == rel assign_op # in (12,14):  
		lexeme+=char
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme='' 
		state=initState
	if state in (18,):
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token,''))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme=''
		numChar=putCharBack(numChar) # зірочка
		state=initState
	if state in (21,):
		print('yes') 
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token,''))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme=''
		numChar=putCharBack(numChar) # зірочка
		state=initState
	if state in (20,):
		lexeme+=char
		token=getToken(state,lexeme)
		print('{0:<3d} {1:<10s} {2:<10s} '.format(numLine,lexeme,token,''))
		tableOfSymb[len(tableOfSymb)+1] = (numLine,lexeme,token,'')
		lexeme=''
		state=initState
	if state in Ferror:  #(101):  # ERROR
		fail()

def fail():
	global state,numLine,char
	print(numLine)
	if state == 101:
		print('Lexer: у рядку ',numLine,' неочікуваний символ '+char)
		exit(101)
	#if state == 102:
#		print('Lexer: у рядку ',numLine,' очікувався символ =, а не '+char)
#		exit(102)
	
		
def is_final(state):
	if (state in F):
		return True
	else:
		return False

def nextState(state,classCh):
	try:
		return stf[(state,classCh)]
	except KeyError:
		return stf[(state,'other')]

def nextChar():
	global numChar
	numChar+=1
	return sourceCode[numChar]

def putCharBack(numChar):
	return numChar-1

def classOfChar(char, state):
	if char in '.' :
		res="dot"
	elif char != '*' and state == 16:
		res = 'other'
	elif char in "*":
		res='*'
	elif char != '/' and state == 17:
		res = 'other'
	elif char in "/":
		res='/'
	elif char in ',;':
		res="Punctuation"
	elif (char in 'e' and state == 3) or (char in 'e' and state == 5):
		res="e"
	elif char in 'abcdefghijklmnopqrstuvwxyz' :
		res="Letter"
	elif char in "0123456789" :
		res="Digit"
	elif char in " \t" :
		res="ws"
	elif char in "\n" :
		res="eol"
	elif char in "+-" and state == 7:
		res=char
	elif char in "=" and state == 12:
		res='='
	elif char != "=" and state == 12:
		res='other'
	#elif char in "<>" and state == 19:
	#	res='='
	#elif char not in "<>" and state == 19:
	elif char == '=' and state == 19:
		res='='
	elif char != '=' and state == 19:
		res='other'
	elif char in "!<>=":
		res='relation_operator'
	elif char in "+-()" :
		res='arithmetic'
	else: res='символ не належить алфавіту'
	return res

def getToken(state,lexeme):
	try:
		return tableOfLanguageTokens[lexeme]
	except KeyError:
		return tableIdentFloatInt[state]

def indexIdConst(state,lexeme):
	indx=0
	if state==2:
		indx=tableOfId.get(lexeme)
#		token=getToken(state,lexeme)
		if indx is None:
			indx=len(tableOfId)+1
			tableOfId[lexeme]=indx
	if state==6 or state==10: # real
		indx=tableOfConst.get(lexeme)
		if indx is None:
			indx=len(tableOfConst)+1
			tableOfConst[lexeme]=indx
	if state==11: #int
		indx=tableOfConst.get(lexeme)
		if indx is None:
			indx=len(tableOfConst)+1
			tableOfConst[lexeme]=indx
	return indx


# запуск лексичного аналізатора	
lex()

# Таблиці: розбору, ідентифікаторів та констант
print('-'*30)
print('tableOfSymb:{0}'.format(tableOfSymb))
print('tableOfId:{0}'.format(tableOfId))
print('tableOfConst:{0}'.format(tableOfConst))
