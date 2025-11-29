# src/modern_ciphers.py

# --- Import seguro das bibliotecas criptográficas ---
try:
    from Crypto.Cipher import DES, AES
    from Crypto.Util.Padding import pad, unpad
    CRYPTO_NS = "Crypto"
except Exception:
    try:
        from Cryptodome.Cipher import DES, AES
        from Cryptodome.Util.Padding import pad, unpad
        CRYPTO_NS = "Cryptodome"
    except Exception:
        DES = AES = pad = unpad = None
        CRYPTO_NS = None


# CIFRAS MODERNAS (DES e AES) — ECB padrão

def des_encrypt(data, key_text):
    """
    Cifra dados usando DES.
    """
    if DES is None:
        raise ImportError("Biblioteca criptográfica não disponível")
    
    key = key_text.encode('utf-8')[:8].ljust(8, b'\0')
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(pad(data, 8))


def des_decrypt(data, key_text):
    """
    Decifra dados usando DES.
    """
    if DES is None:
        raise ImportError("Biblioteca criptográfica não disponível")
    
    key = key_text.encode('utf-8')[:8].ljust(8, b'\0')
    cipher = DES.new(key, DES.MODE_ECB)
    return unpad(cipher.decrypt(data), 8)


def aes_encrypt(data, key_text):
    """
    Cifra dados usando AES.
    """
    if AES is None:
        raise ImportError("Biblioteca criptográfica não disponível")
    
    kb = key_text.encode('utf-8')
    if len(kb) not in (16, 24, 32):
        kb = kb[:32].ljust(32, b'\0')
    cipher = AES.new(kb, AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))


def aes_decrypt(data, key_text):
    """
    Decifra dados usando AES.
    """
    if AES is None:
        raise ImportError("Biblioteca criptográfica não disponível")
    
    kb = key_text.encode('utf-8')
    if len(kb) not in (16, 24, 32):
        kb = kb[:32].ljust(32, b'\0')
    cipher = AES.new(kb, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)


def get_crypto_backend():
    """
    Retorna informações sobre o backend criptográfico ativo.
    """
    return CRYPTO_NS or "NENHUM"
