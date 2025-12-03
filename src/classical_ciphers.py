# src/classical_ciphers.py

# CIFRAS CLÁSSICAS (Vigenère e ~)

def vigenere_encrypt(text: str, key: str, tableText: str):
    """
    Cifra texto usando a cifra de Vigenère.
    """
    text = text.replace(" ", "").upper()
    key = key.replace(" ", "").upper()
    tableMatrix = [line.split() for line in tableText.strip().split('\n')]
    header = tableMatrix[0]
    result = []

    key_seq = (key * ((len(text)//len(key)) + 1))[:len(text)]

    for t, k in zip(text, key_seq):
        if t in header and k in header:
            # Encontra o index da linha (baseado no char da chave)
            row_idx = header.index(k)
            # Encontra o index da coluna (baseado no char da mensagem)
            col_idx = header.index(t)
            
            # The intersection in the Vigenère Square is the encrypted char
            encrypted_char = tableMatrix[row_idx][col_idx]
            print(encrypted_char)
            result.append(encrypted_char)
        else:
            
            #result.append(t) #to allow non alphabetic characteres uncomment the this line
            pass
    return ''.join(result)


def vigenere_decrypt(cipher: str, key: str, table: str):
    """
    Decifra texto usando a cifra de Vigenère.
    """
    tableMatrix = [line.split() for line in table.strip().split('\n')]
    header = tableMatrix[0]
    key = key.replace(" ", "").upper()

    res = []
    key_seq = (key * ((len(cipher)//len(key)) + 1))[:len(cipher)]

    for c, k in zip(cipher, key_seq):
        if c in header and k in header:
            key_row_idx = header.index(k)
            row = tableMatrix[key_row_idx]
            col_id = row.index(c)
            decryptedChar = header[col_id]
            res.append(decryptedChar)
            pass
        else:
            res.append(c)
    return ''.join(res)


# PLAYFAIR — versão corrigida

def playfair_matrix(table_text: str) -> list[list[str]]:
    """
    Cria a matriz 5x5 para a cifra PlayFair.
    """
    table = []
    for line in table_text.strip().split("\n"):
        row = line.strip().split()
        if row:
            table.append(row)
            pass
        pass
    return table

def findPosition(table: list[list[str]], char: str) -> tuple[int, int]:
    for row in range(len(table)):
        for col in range(len(table[row])):
            if table[row][col] == char.upper():
                return (row, col)
        pass
    raise ValueError("Invalid character: ", char)


def playfair_prepare(text):
    """
    Prepara o texto para cifragem PlayFair.
    """
    t = ''.join([c for c in text.upper() if c.isalpha()])
    t = t.replace('J', 'I')
    pairs = []
    i = 0
    while i < len(t):
        a = t[i]
        b = t[i+1] if i+1 < len(t) else 'X'
        if a == b:
            pairs.append(a + 'X')
            i += 1
        else:
            pairs.append(a + b)
            i += 2
    return pairs

def encryptPair(table: list[list[str]], pair: str) -> str:
    rows = len(table)
    cols = len(table[0]) if table else 0
    print (pair[1])
    row1, col1 = findPosition(table, pair[0])
    row2, col2 = findPosition(table, pair[1])

    if row1 == row2:
        newCol1 = (col1 + 1) % cols
        newCol2 = (col2 + 1) % cols
        return table[row1][newCol1] + table[row2][newCol2]
    elif col1 == col2:
        new_row1 = (row1 + 1) % rows
        new_row2 = (row2 + 1) % rows
        return table[new_row1][col1] + table[new_row2][col2]
    else:
        return table[row1][col2] + table[row2][col1]


def playfair_encrypt(text, table_text):
    """
    Cifra texto usando a cifra PlayFair.
    """
    table = playfair_matrix(table_text)
    pairs = playfair_prepare(text)
    ciphertext = ''

    out = []
    for pair in pairs:
        ciphertext += encryptPair(table, pair)
        pass
    print (ciphertext)
    return ciphertext

def decryptPair(table, pair):
    rows = len(table)
    cols = len(table[0]) if table else 0
    print (pair[1])
    row1, col1 = findPosition(table, pair[0])
    row2, col2 = findPosition(table, pair[1])
    if row1 == row2:
        newCol1 = (col1 - 1) % cols
        newCol2 = (col2 - 1) % cols
        return table[row1][newCol1] + table[row2][newCol2]
    elif col1 == col2:
        new_row1 = (row1 - 1) % rows
        new_row2 = (row2 - 1) % rows
        return table[new_row1][col1] + table[new_row2][col2]
    else:
        return table[row1][col2] + table[row2][col1]

def playfair_decrypt(cipher, table_text):
    """
    Decifra texto usando a cifra PlayFair.
    """
    table = playfair_matrix(table_text)
    pairs = playfair_prepare(cipher)
    ciphertext = ''

    out = []
    for pair in pairs:
        ciphertext += decryptPair(table, pair)
        pass
    print (ciphertext)
    return ciphertext
