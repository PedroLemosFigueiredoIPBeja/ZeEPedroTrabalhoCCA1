# src/classical_ciphers.py

# CIFRAS CLÁSSICAS (Vigenère e ~)

def vigenere_encrypt(text, key, table):
    """
    Cifra texto usando a cifra de Vigenère.
    """
    table = table.strip()
    res = []
    key_seq = (key * ((len(text)//len(key)) + 1))[:len(text)]
    for t, k in zip(text, key_seq):
        if t in table and k in table:
            i = (table.index(t) + table.index(k)) % len(table)
            res.append(table[i])
        else:
            res.append(t)
    return ''.join(res)


def vigenere_decrypt(cipher, key, table):
    """
    Decifra texto usando a cifra de Vigenère.
    """
    table = table.strip()
    res = []
    key_seq = (key * ((len(cipher)//len(key)) + 1))[:len(cipher)]
    for c, k in zip(cipher, key_seq):
        if c in table and k in table:
            i = (table.index(c) - table.index(k)) % len(table)
            res.append(table[i])
        else:
            res.append(c)
    return ''.join(res)


# PLAYFAIR — versão corrigida

def playfair_matrix(table_text):
    """
    Cria a matriz 5x5 para a cifra PlayFair.
    """
    s = ''.join(ch for ch in table_text.upper() if ch.isalpha())
    s = s.replace('J', 'I')
    seen = set()
    s = ''.join([c for c in s if not (c in seen or seen.add(c))])
    if len(s) < 25:
        raise ValueError("Tabela PlayFair precisa de pelo menos 25 letras distintas (A–Z, sem J).")
    s = s[:25]
    return [list(s[i:i+5]) for i in range(0, 25, 5)]


def playfair_pos(matrix, ch):
    """
    Encontra a posição de um caractere na matriz PlayFair.
    """
    ch = ch.upper()
    if ch == 'J':
        ch = 'I'
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    return None


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


def playfair_encrypt(text, table_text):
    """
    Cifra texto usando a cifra PlayFair.
    """
    matrix = playfair_matrix(table_text)
    pairs = playfair_prepare(text)
    out = []
    for pair in pairs:
        a, b = pair[0], pair[1]
        pa = playfair_pos(matrix, a)
        pb = playfair_pos(matrix, b)
        if not pa or not pb:
            out.append(a + b)
            continue
        ra, ca = pa
        rb, cb = pb
        if ra == rb:
            out.append(matrix[ra][(ca + 1) % 5] + matrix[rb][(cb + 1) % 5])
        elif ca == cb:
            out.append(matrix[(ra + 1) % 5][ca] + matrix[(rb + 1) % 5][cb])
        else:
            out.append(matrix[ra][cb] + matrix[rb][ca])
    return ''.join(out)


def playfair_decrypt(cipher, table_text):
    """
    Decifra texto usando a cifra PlayFair.
    """
    matrix = playfair_matrix(table_text)
    c = ''.join([ch for ch in cipher.upper() if ch.isalpha()])
    pairs = [c[i:i + 2] for i in range(0, len(c), 2)]
    out = []
    for pair in pairs:
        if len(pair) < 2:
            continue
        a, b = pair[0], pair[1]
        pa = playfair_pos(matrix, a)
        pb = playfair_pos(matrix, b)
        if not pa or not pb:
            out.append(a + b)
            continue
        ra, ca = pa
        rb, cb = pb
        if ra == rb:
            out.append(matrix[ra][(ca - 1) % 5] + matrix[rb][(cb - 1) % 5])
        elif ca == cb:
            out.append(matrix[(ra - 1) % 5][ca] + matrix[(rb - 1) % 5][cb])
        else:
            out.append(matrix[ra][cb] + matrix[rb][ca])
    return ''.join(out)
