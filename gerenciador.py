import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ===============================
# CONFIGURAÇÕES GERAIS
# ===============================
ctk.set_appearance_mode("light")  # "dark" se preferir
ctk.set_default_color_theme("blue")

# ===============================
# BANCO DE DADOS
# ===============================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("financeiro.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def inserir(self, tipo, descricao, valor):
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cursor.execute("INSERT INTO transacoes (tipo, descricao, valor, data) VALUES (?, ?, ?, ?)",
                            (tipo, descricao, valor, data))
        self.conn.commit()

    def deletar(self, transacao_id):
        self.cursor.execute("DELETE FROM transacoes WHERE id = ?", (transacao_id,))
        self.conn.commit()

    def buscar_todas(self):
        self.cursor.execute("SELECT * FROM transacoes ORDER BY id DESC")
        return self.cursor.fetchall()

    def calcular_saldo(self):
        self.cursor.execute("SELECT tipo, valor FROM transacoes")
        transacoes = self.cursor.fetchall()
        saldo = 0
        for tipo, valor in transacoes:
            if tipo == "Receita":
                saldo += valor
            else:
                saldo -= valor
        return saldo


# ===============================
# INTERFACE
# ===============================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciador de Despesas Pessoais")
        self.geometry("700x500")
        self.db = Database()

        # Frames
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(fill="x", pady=10)

        self.frame_mid = ctk.CTkFrame(self)
        self.frame_mid.pack(fill="x", pady=10)

        self.frame_bottom = ctk.CTkFrame(self)
        self.frame_bottom.pack(fill="both", expand=True, pady=10)

        # Label Saldo
        self.saldo_label = ctk.CTkLabel(self.frame_top, text="", font=("Arial", 20, "bold"))
        self.saldo_label.pack(pady=5)
        self.atualizar_saldo()

        # Inputs
        self.tipo_var = ctk.StringVar(value="Receita")
        self.option_tipo = ctk.CTkOptionMenu(self.frame_mid, values=["Receita", "Despesa"], variable=self.tipo_var)
        self.option_tipo.grid(row=0, column=0, padx=5, pady=5)

        self.entry_desc = ctk.CTkEntry(self.frame_mid, placeholder_text="Descrição")
        self.entry_desc.grid(row=0, column=1, padx=5, pady=5)

        self.entry_valor = ctk.CTkEntry(self.frame_mid, placeholder_text="Valor (R$)")
        self.entry_valor.grid(row=0, column=2, padx=5, pady=5)

        self.btn_add = ctk.CTkButton(self.frame_mid, text="Adicionar", command=self.adicionar_transacao)
        self.btn_add.grid(row=0, column=3, padx=5, pady=5)

        self.btn_del = ctk.CTkButton(self.frame_mid, text="Excluir Selecionado", fg_color="red", command=self.excluir_transacao)
        self.btn_del.grid(row=0, column=4, padx=5, pady=5)

        # Treeview (Histórico)
        colunas = ("ID", "Tipo", "Descrição", "Valor", "Data")
        self.tree = ttk.Treeview(self.frame_bottom, columns=colunas, show="headings", height=12)
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.atualizar_lista()

    def atualizar_saldo(self):
        saldo = self.db.calcular_saldo()
        cor = "green" if saldo >= 0 else "red"
        self.saldo_label.configure(text=f"💰 Saldo Atual: R$ {saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
                                   text_color=cor)

    def atualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for transacao in self.db.buscar_todas():
            id_, tipo, desc, valor, data = transacao
            valor_formatado = f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            self.tree.insert("", "end", values=(id_, tipo, desc, valor_formatado, data))

    def adicionar_transacao(self):
        tipo = self.tipo_var.get()
        desc = self.entry_desc.get()
        try:
            valor = float(self.entry_valor.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Digite um valor válido!")
            return

        if desc.strip() == "":
            messagebox.showwarning("Atenção", "Descrição não pode estar vazia.")
            return

        self.db.inserir(tipo, desc, valor)
        self.atualizar_lista()
        self.atualizar_saldo()
        self.entry_desc.delete(0, "end")
        self.entry_valor.delete(0, "end")

    def excluir_transacao(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione uma transação para excluir.")
            return
        transacao_id = self.tree.item(item)["values"][0]
        self.db.deletar(transacao_id)
        self.atualizar_lista()
        self.atualizar_saldo()


# ===============================
# RODAR APP
# ===============================
if __name__ == "__main__":
    app = App()
    app.mainloop()
