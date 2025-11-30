charAAsciiCode = 65

def createTable5By5(key: str) -> list[list[str]]:
	currentCharNumber = 0
	numberOfChars = 26
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
	while True:
		try:
			size = int(input('Qual o tamanho da tabela? forneça um número entre 5 e 7: '))
			if(4 < size < 8): 
				break 
			else:
				raise ValueError("wrong value")
		except ValueError:
			print("Por favor forneça um número entre 5 e 7: ")
	return key, size

key, size = askUser()

table = []

if size == 5:
	table = createTable5By5(key)
	pass

with open("tabelaPlayFair.txt", "w") as f:
	for row in table:
		f.write(" ".join(row) + "\n")

