charAAsciiCode = 65
def createViginereTable() -> list[str]:
    currentCharNumber = 0
    currentLine = 0
    currentRow = 0
    currentChar = ''
    numberOfChars = 26
    table = []
    for line in range(numberOfChars):
        table.append([])
        for column in range(numberOfChars):
            currentCharNumber = line + column
            if currentCharNumber >= numberOfChars:
                currentChar = chr(currentCharNumber + charAAsciiCode - numberOfChars)
            else:
                currentChar = chr(currentCharNumber + charAAsciiCode)
            table[line].append(currentChar)
            continue
        continue
    return table

grid = createViginereTable()
with open('vigenere_table_output.txt', 'w') as f:
    for row in grid:
        f.write(" ".join(row) + "\n")


print(createViginereTable())

