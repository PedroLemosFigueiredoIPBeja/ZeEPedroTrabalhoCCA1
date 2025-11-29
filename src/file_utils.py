from pathlib import Path

def read_key_text(path: str) -> str:
    """
    Lê o ficheiro de chave removendo BOM, \r, \n e espaços laterais.
    Garante compatibilidade com UTF-8 e ISO-8859-1.
    """
    try:
        return Path(path).read_text(encoding='utf-8-sig').replace('\r', '').strip()
    except UnicodeDecodeError:
        # fallback para ficheiros gravados em ISO-8859-1 (ANSI)
        return Path(path).read_text(encoding='latin-1').replace('\r', '').strip()

def safe_write_text(file_path: str, content: str) -> bool:
    """
    Escreve texto de forma segura, tratando possíveis erros de encoding.
    """
    try:
        Path(file_path).write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Erro ao escrever arquivo: {e}")
        return False

def safe_write_bytes(file_path: str, data: bytes) -> bool:
    """
    Escreve dados binários de forma segura.
    """
    try:
        Path(file_path).write_bytes(data)
        return True
    except Exception as e:
        print(f"Erro ao escrever arquivo binário: {e}")
        return False
