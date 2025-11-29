# src/main.py - VERSÃO MELHORADA
import tkinter as tk
from tkinter import (
    Tk, StringVar, ttk, filedialog, messagebox, scrolledtext, END
)
from pathlib import Path
import os

# Importações dos módulos locais
from classical_ciphers import (
    vigenere_encrypt, vigenere_decrypt,
    playfair_encrypt, playfair_decrypt
)
from modern_ciphers import (
    des_encrypt, des_decrypt,
    aes_encrypt, aes_decrypt,
    get_crypto_backend
)
from file_utils import read_key_text


class CryptoApp:
    def __init__(self, root):
        self.root = root
        root.title("CryptoSuite Pro - Sistema de Criptografia")
        root.configure(bg='#f0f0f0')

        # --- Dimensões e centralização da janela ---
        win_width = 800
        win_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (win_width // 2)
        y = (screen_height // 2) - (win_height // 2)
        root.geometry(f"{win_width}x{win_height}+{x}+{y}")

        # --- Impede redimensionamento ---
        root.resizable(True, True)

        # --- Cabeçalho profissional ---
        header_frame = ttk.Frame(root)
        header_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(header_frame, text="🛡️ CryptoSuite Pro", 
                 font=("Segoe UI", 20, "bold"), foreground="#2c3e50").pack(pady=5)
        ttk.Label(header_frame, text="Sistema Profissional de Criptografia - Vigenère · PlayFair · DES · AES", 
                 font=("Segoe UI", 10), foreground="#7f8c8d").pack(pady=2)

        # --- Abas principais ---
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)

        # --- Log inferior ---
        log_frame = ttk.Frame(root)
        log_frame.pack(fill='x', padx=10, pady=(5,10))
        
        ttk.Label(log_frame, text="Log do Sistema:", font=("Segoe UI", 9, "bold")).pack(anchor='w')
        self.log = scrolledtext.ScrolledText(log_frame, height=6, state='disabled', font=("Consolas", 9))
        self.log.pack(fill='x', pady=2)

        # --- Inicializa as abas das cifras ---
        self._vigenere_tab()
        self._playfair_tab()
        self._des_tab()
        self._aes_tab()

        # --- Mostra backend ativo ---
        backend = get_crypto_backend()
        self._log(f"✅ Sistema inicializado - Backend criptográfico: {backend}")

    def _log(self, msg):
        """Adiciona mensagem ao log."""
        self.log.config(state='normal')
        self.log.insert(END, msg + "\n")
        self.log.see(END)
        self.log.config(state='disabled')

    def _create_file_selector(self, frame, row, label, var, filetypes=None):
        """Cria um seletor de arquivo padronizado."""
        if filetypes is None:
            filetypes = [("Ficheiros de texto", "*.txt"), ("Todos os ficheiros", "*.*")]
            
        ttk.Label(frame, text=label, font=("Segoe UI", 9)).grid(row=row, column=0, sticky='w', pady=3)
        entry = ttk.Entry(frame, textvariable=var, width=60, font=("Segoe UI", 9))
        entry.grid(row=row, column=1, padx=5, pady=3, sticky='ew')
        ttk.Button(frame, text="📁 Procurar", 
                  command=lambda: var.set(filedialog.askopenfilename(filetypes=filetypes)),
                  width=12).grid(row=row, column=2, padx=5, pady=3)
        return entry

    def _show_preview(self, file_path, operation):
        """Mostra preview do conteúdo do arquivo."""
        try:
            if file_path and Path(file_path).exists():
                content = Path(file_path).read_text()[:100]  # Primeiros 100 caracteres
                preview = f"\n📄 Preview ({operation}): {content}..."
                if len(content) >= 100:
                    preview += " [...]"
                self._log(preview)
        except Exception:
            pass

    # ABA VIGENÈRE MELHORADA
    def _vigenere_tab(self):
        frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(frame, text="🔐 Vigenère")

        # Configurar grid
        frame.columnconfigure(1, weight=1)

        table, key, file_ = StringVar(), StringVar(), StringVar()
        result_text = StringVar(value="Resultado aparecerá aqui...")

        # Seletores de arquivo
        self._create_file_selector(frame, 0, "Tabela de caracteres:", table)
        self._create_file_selector(frame, 1, "Ficheiro da chave:", key)
        self._create_file_selector(frame, 2, "Ficheiro da mensagem:", file_)

        # Área de resultado
        ttk.Label(frame, text="Resultado:", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, sticky='w', pady=(15,5))
        result_entry = ttk.Entry(frame, textvariable=result_text, width=70, font=("Segoe UI", 9), state='readonly')
        result_entry.grid(row=3, column=1, columnspan=2, sticky='ew', pady=(15,5), padx=5)

        # Botões de ação
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=15)

        ttk.Button(btn_frame, text="🔒 Cifrar", command=lambda: self._vigenere_encrypt(table, key, file_, result_text),
                  style="Accent.TButton").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔓 Decifrar", command=lambda: self._vigenere_decrypt(table, key, file_, result_text),
                  style="Accent.TButton").pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🧹 Limpar", command=lambda: self._clear_vigenere(table, key, file_, result_text)).pack(side='left', padx=5)

    def _vigenere_encrypt(self, table, key, file_, result_text):
        try:
            if not all([table.get(), key.get(), file.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            table_t = Path(table.get()).read_text()
            key_t = Path(key.get()).read_text().strip()
            msg = Path(file_.get()).read_text()
            
            self._log("🔄 Iniciando cifragem Vigenère...")
            out = vigenere_encrypt(msg, key_t, table_t)
            
            # Salvar resultado
            out_path = file_.get() + ".vigenere.enc"
            Path(out_path).write_text(out)
            
            result_text.set(f"✅ Mensagem cifrada: '{out[:30]}...'")
            self._log(f"✅ Cifragem Vigenère concluída: {os.path.basename(out_path)}")
            self._show_preview(out_path, "Cifrado")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na cifragem: {str(e)}")
            self._log(f"❌ Erro Vigenère: {e}")

    def _vigenere_decrypt(self, table, key, file_, result_text):
        try:
            if not all([table.get(), key.get(), file.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            table_t = Path(table.get()).read_text()
            key_t = Path(key.get()).read_text().strip()
            msg = Path(file_.get()).read_text()
            
            self._log("🔄 Iniciando decifragem Vigenère...")
            out = vigenere_decrypt(msg, key_t, table_t)
            
            # Salvar resultado
            out_path = file_.get() + ".vigenere.dec"
            Path(out_path).write_text(out)
            
            result_text.set(f"✅ Mensagem decifrada: '{out[:30]}...'")
            self._log(f"✅ Decifragem Vigenère concluída: {os.path.basename(out_path)}")
            self._show_preview(out_path, "Decifrado")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na decifragem: {str(e)}")
            self._log(f"❌ Erro Vigenère: {e}")

    def _clear_vigenere(self, table, key, file_, result_text):
        table.set("")
        key.set("")
        file_.set("")
        result_text.set("Resultado aparecerá aqui...")
        self._log("🧹 Campos Vigenère limpos")

    # ABA PLAYFAIR MELHORADA
    def _playfair_tab(self):
        frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(frame, text="🔐 PlayFair")

        frame.columnconfigure(1, weight=1)

        table, file_ = StringVar(), StringVar()
        result_text = StringVar(value="Resultado aparecerá aqui...")

        self._create_file_selector(frame, 0, "Tabela PlayFair:", table)
        self._create_file_selector(frame, 1, "Ficheiro da mensagem:", file_)

        ttk.Label(frame, text="Resultado:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=(15,5))
        result_entry = ttk.Entry(frame, textvariable=result_text, width=70, font=("Segoe UI", 9), state='readonly')
        result_entry.grid(row=2, column=1, columnspan=2, sticky='ew', pady=(15,5), padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=15)

        ttk.Button(btn_frame, text="🔒 Cifrar", 
                  command=lambda: self._playfair_encrypt(table, file_, result_text)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔓 Decifrar", 
                  command=lambda: self._playfair_decrypt(table, file_, result_text)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🧹 Limpar", 
                  command=lambda: self._clear_playfair(table, file_, result_text)).pack(side='left', padx=5)

    def _playfair_encrypt(self, table, file_, result_text):
        try:
            if not all([table.get(), file_.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            t = Path(table.get()).read_text()
            msg = Path(file_.get()).read_text()
            
            self._log("🔄 Iniciando cifragem PlayFair...")
            out = playfair_encrypt(msg, t)
            
            out_path = file_.get() + ".playfair.enc"
            Path(out_path).write_text(out)
            
            result_text.set(f"✅ Texto cifrado: '{out}'")
            self._log(f"✅ Cifragem PlayFair concluída: {os.path.basename(out_path)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na cifragem: {str(e)}")
            self._log(f"❌ Erro PlayFair: {e}")

    def _playfair_decrypt(self, table, file_, result_text):
        try:
            if not all([table.get(), file_.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            t = Path(table.get()).read_text()
            msg = Path(file_.get()).read_text()
            
            self._log("🔄 Iniciando decifragem PlayFair...")
            out = playfair_decrypt(msg, t)
            
            out_path = file_.get() + ".playfair.dec"
            Path(out_path).write_text(out)
            
            result_text.set(f"✅ Texto decifrado: '{out}'")
            self._log(f"✅ Decifragem PlayFair concluída: {os.path.basename(out_path)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na decifragem: {str(e)}")
            self._log(f"❌ Erro PlayFair: {e}")

    def _clear_playfair(self, table, file_, result_text):
        table.set("")
        file_.set("")
        result_text.set("Resultado aparecerá aqui...")
        self._log("🧹 Campos PlayFair limpos")

    # ABA DES MELHORADA
    def _des_tab(self):
        frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(frame, text="🔒 DES")

        frame.columnconfigure(1, weight=1)

        key, file_ = StringVar(), StringVar()
        result_text = StringVar(value="Resultado aparecerá aqui...")

        self._create_file_selector(frame, 0, "Ficheiro da chave:", key)
        self._create_file_selector(frame, 1, "Ficheiro para processar:", file_, 
                                 [("Todos os ficheiros", "*.*")])

        ttk.Label(frame, text="Resultado:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=(15,5))
        result_entry = ttk.Entry(frame, textvariable=result_text, width=70, font=("Segoe UI", 9), state='readonly')
        result_entry.grid(row=2, column=1, columnspan=2, sticky='ew', pady=(15,5), padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=15)

        ttk.Button(btn_frame, text="🔒 Cifrar", 
                  command=lambda: self._des_encrypt(key, file_, result_text)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔓 Decifrar", 
                  command=lambda: self._des_decrypt(key, file_, result_text)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🧹 Limpar", 
                  command=lambda: self._clear_des(key, file_, result_text)).pack(side='left', padx=5)

    def _des_encrypt(self, key, file_, result_text):
        try:
            if not all([key.get(), file_.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            k = Path(key.get()).read_text().strip()
            data = Path(file_.get()).read_bytes()
            
            self._log("🔄 Iniciando cifragem DES...")
            out = des_encrypt(data, k)
            
            out_path = file_.get() + ".des.enc"
            Path(out_path).write_bytes(out)
            
            result_text.set(f"✅ Ficheiro cifrado: {os.path.basename(out_path)}")
            self._log(f"✅ Cifragem DES concluída: {os.path.basename(out_path)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na cifragem DES: {str(e)}")
            self._log(f"❌ Erro DES: {e}")

    def _des_decrypt(self, key, file_, result_text):
        try:
            if not all([key.get(), file_.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            k = read_key_text(key.get())
            data = Path(file_.get()).read_bytes()
            
            self._log("🔄 Iniciando decifragem DES...")
            out = des_decrypt(data, k)
            
            out_path = file_.get() + ".des.dec"

            # Tenta gravar como texto UTF-8
            try:
                text = out.decode('utf-8')
                Path(out_path).write_text(text, encoding='utf-8')
                result_text.set(f"✅ Texto decifrado: '{text[:30]}...'")
                self._log(f"✅ Decifragem DES concluída (texto): {os.path.basename(out_path)}")
            except UnicodeDecodeError:
                Path(out_path).write_bytes(out)
                result_text.set(f"✅ Ficheiro binário decifrado: {os.path.basename(out_path)}")
                self._log(f"✅ Decifragem DES concluída (binário): {os.path.basename(out_path)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na decifragem DES: {str(e)}")
            self._log(f"❌ Erro DES: {e}")

    def _clear_des(self, key, file_, result_text):
        key.set("")
        file_.set("")
        result_text.set("Resultado aparecerá aqui...")
        self._log("🧹 Campos DES limpos")

    # ABA AES MELHORADA
    def _aes_tab(self):
        frame = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(frame, text="🔒 AES")

        frame.columnconfigure(1, weight=1)

        key, file_ = StringVar(), StringVar()
        result_text = StringVar(value="Resultado aparecerá aqui...")

        self._create_file_selector(frame, 0, "Ficheiro da chave:", key)
        self._create_file_selector(frame, 1, "Ficheiro para processar:", file_, 
                                 [("Todos os ficheiros", "*.*")])

        ttk.Label(frame, text="Resultado:", font=("Segoe UI", 10, "bold")).grid(row=2, column=0, sticky='w', pady=(15,5))
        result_entry = ttk.Entry(frame, textvariable=result_text, width=70, font=("Segoe UI", 9), state='readonly')
        result_entry.grid(row=2, column=1, columnspan=2, sticky='ew', pady=(15,5), padx=5)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=15)

        ttk.Button(btn_frame, text="🔒 Cifrar", 
                  command=lambda: self._aes_encrypt(key, file_, result_text)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🔓 Decifrar", 
                  command=lambda: self._aes_decrypt(key, file_, result_text)).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="🧹 Limpar", 
                  command=lambda: self._clear_aes(key, file_, result_text)).pack(side='left', padx=5)

    def _aes_encrypt(self, key, file_, result_text):
        try:
            if not all([key.get(), file_.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            k = Path(key.get()).read_text().strip()
            data = Path(file_.get()).read_bytes()
            
            self._log("🔄 Iniciando cifragem AES...")
            out = aes_encrypt(data, k)
            
            out_path = file_.get() + ".aes.enc"
            Path(out_path).write_bytes(out)
            
            result_text.set(f"✅ Ficheiro cifrado: {os.path.basename(out_path)}")
            self._log(f"✅ Cifragem AES concluída: {os.path.basename(out_path)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na cifragem AES: {str(e)}")
            self._log(f"❌ Erro AES: {e}")

    def _aes_decrypt(self, key, file_, result_text):
        try:
            if not all([key.get(), file_.get()]):
                messagebox.showwarning("Aviso", "Selecione todos os ficheiros necessários!")
                return

            k = read_key_text(key.get())
            data = Path(file_.get()).read_bytes()
            
            self._log("🔄 Iniciando decifragem AES...")
            out = aes_decrypt(data, k)
            
            out_path = file_.get() + ".aes.dec"

            # Tenta gravar como texto UTF-8
            try:
                text = out.decode('utf-8')
                Path(out_path).write_text(text, encoding='utf-8')
                result_text.set(f"✅ Texto decifrado: '{text[:30]}...'")
                self._log(f"✅ Decifragem AES concluída (texto): {os.path.basename(out_path)}")
            except UnicodeDecodeError:
                Path(out_path).write_bytes(out)
                result_text.set(f"✅ Ficheiro binário decifrado: {os.path.basename(out_path)}")
                self._log(f"✅ Decifragem AES concluída (binário): {os.path.basename(out_path)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na decifragem AES: {str(e)}")
            self._log(f"❌ Erro AES: {e}")

    def _clear_aes(self, key, file_, result_text):
        key.set("")
        file_.set("")
        result_text.set("Resultado aparecerá aqui...")
        self._log("🧹 Campos AES limpos")


# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    root = Tk()
    
    # Configurar estilo moderno
    style = ttk.Style()
    style.theme_use('clam')
    
    app = CryptoApp(root)
    root.mainloop()
