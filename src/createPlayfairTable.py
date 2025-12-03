charAAsciiCode = 65
char0AsciiCode = 48
charSpaceAsciiCode = 32
numberOfChars = 26

def createTable5By5(key: str) -> list[list[str]]:
	currentCharNumber = 0
	
	table = []
	key = key.upper().replace(" ", "").replace("J", "I")
	alphabet = ""

	for currentCharNumber in range(numberOfChars):
		alphabet = alphabet + chr(currentCharNumber + charAAsciiCode)
		pass
	alphabet = alphabet.replace("J", "")
	
	usedChars = set()

	for char in key:
		if char not in usedChars and char in alphabet:
			usedChars.add(char)
			if len(table) == 0 or len(table[-1]) == 5:
				table.append([])
				pass
			table[-1].append(char)
			pass
		pass

	for char in alphabet:
		if char not in usedChars:
			usedChars.add(char)
			if len(table) == 0 or len(table[-1]) == 5:
				table.append([])
				pass
			table[-1].append(char)
			pass
		pass
	return table

def askUser() -> tuple[str, int]:
	key = input ("Qual a chave a utilizar? ")
	size = 5
	# while True:
	# 	try:
	# 		size = int(input('Qual o tamanho da tabela? forneça um número entre 5 e 7: '))
	# 		if(4 < size < 8): 
	# 			break 
	# 		else:
	# 			raise ValueError("wrong value")
	# 	except ValueError:
	# 		print("Por favor forneça um número entre 5 e 7: ")
	return key, size

# def createTable(key: str, size: int) -> list[list[str]]:
# 	table = []
# 	chars = ''
# 	if(size == 6): key = key.upper().replace(" ", "")
# 	else: chars = chr(charSpaceAsciiCode)

# 	print(len(chars))
	
# 	if 5 < size < 10:
# 		for currentCharNumber in range(10):
# 			chars += chars + chr(char0AsciiCode + currentCharNumber)
# 			pass
# 		for currentCharNumber in range(size * size - 11):
# 			print(len(chars))
# 			if len(chars) < size * size:
# 				chars += chars + chr(charAAsciiCode + currentCharNumber)
# 				if charAAsciiCode + currentCharNumber >= 96:
# 					chars += chars + chr(charAAsciiCode + currentCharNumber + numberOfChars)
# 					pass
# 				pass
# 			pass
# 		pass
# 	elif size < 14:
# 		for currentCharNumber in range(size * size - 1):
# 			chars += chars + chr(charSpaceAsciiCode + currentCharNumber + 1)
	
# 	usedChars = set()	

# 	for char in key:
# 		if char not in usedChars and char in chars:
# 			usedChars.add(char)
# 			if len(table) == 0 or len(table[-1]) == size:
# 				table.append([])
# 				pass
# 			table[-1].append(char)
# 			pass
# 		pass



# 	for char in chars:
# 		if char not in usedChars:
# 			usedChars.add(char)
# 			if len(table) == 0 or len(table[-1]) == size:
# 				table.append([])
# 				pass
# 			table[-1].append(char)
# 			pass
# 		pass
# 	return table

key, size = askUser()

table = []

table = createTable5By5(key)
pass

with open("tabelaPlayFair.txt", "w") as f:
	for row in table:
		f.write(" ".join(row) + "\n")

