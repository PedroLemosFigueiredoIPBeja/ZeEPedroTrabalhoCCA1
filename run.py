import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import CryptoApp
from tkinter import Tk

if __name__ == "__main__":
    root = Tk()
    app = CryptoApp(root)
    root.mainloop()
