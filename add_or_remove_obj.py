import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import csv
import os

ARQUIVO_ESTOQUE = 'estoque.txt'

def carregar_estoque():
    estoque = []
    if os.path.exists(ARQUIVO_ESTOQUE):
        with open(ARQUIVO_ESTOQUE, newline='', encoding='latin1') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) == 3:
                    estoque.append({'nome': row[0], 'preco': row[1], 'quantidade': row[2]})
    return estoque

def salvar_estoque(estoque):
    with open(ARQUIVO_ESTOQUE, 'w', newline='', encoding='latin1') as f:
        writer = csv.writer(f)
        for item in estoque:
            writer.writerow([item['nome'], item['preco'], item['quantidade']])

class EstoqueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adicionar ou Remover Objeto")
        self.root.configure(bg='white')
        self.root.geometry("800x600")

        def create_rounded_box_image(size, radius, bg_color, border_color):
            img = Image.new('RGBA', size, (0,0,0,0))
            draw = ImageDraw.Draw(img)
            draw.rounded_rectangle([0,0,size[0]-1,size[1]-1], radius, fill=bg_color, outline=border_color, width=2)
            return img

        nome_canvas = tk.Canvas(root, width=370, height=48, bg='white', highlightthickness=0)
        nome_canvas.pack(pady=10)
        nome_bg = create_rounded_box_image((370, 48), 18, (255,255,255,255), (0,0,0,255))
        self.nome_bg_img = ImageTk.PhotoImage(nome_bg)
        nome_canvas.create_image(0, 0, anchor='nw', image=self.nome_bg_img)
        tk.Label(nome_canvas, text="Nome:", font=("Arial", 12), bg='white').place(x=20, y=12)
        self.nome_entry = tk.Entry(nome_canvas, font=("Arial", 12), bd=0, relief='flat', bg='white', highlightthickness=0)
        self.nome_entry.place(x=80, y=10, width=270, height=28)

        preco_canvas = tk.Canvas(root, width=200, height=48, bg='white', highlightthickness=0)
        preco_canvas.pack(pady=10)
        preco_bg = create_rounded_box_image((200, 48), 18, (255,255,255,255), (0,0,0,255))
        self.preco_bg_img = ImageTk.PhotoImage(preco_bg)
        preco_canvas.create_image(0, 0, anchor='nw', image=self.preco_bg_img)
        tk.Label(preco_canvas, text="Preço:", font=("Arial", 12), bg='white').place(x=15, y=12)
        self.preco_entry = tk.Entry(preco_canvas, font=("Arial", 12), bd=0, relief='flat', bg='white', highlightthickness=0)
        self.preco_entry.place(x=70, y=10, width=110, height=28)

        qtd_canvas = tk.Canvas(root, width=170, height=48, bg='white', highlightthickness=0)
        qtd_canvas.pack(pady=10)
        qtd_bg = create_rounded_box_image((170, 48), 18, (255,255,255,255), (0,0,0,255))
        self.qtd_bg_img = ImageTk.PhotoImage(qtd_bg)
        qtd_canvas.create_image(0, 0, anchor='nw', image=self.qtd_bg_img)
        tk.Label(qtd_canvas, text="Quantidade:", font=("Arial", 12), bg='white').place(x=10, y=12)
        self.qtd_entry = tk.Entry(qtd_canvas, font=("Arial", 12), bd=0, relief='flat', bg='white', highlightthickness=0)
        self.qtd_entry.place(x=100, y=10, width=55, height=28)

        btn_frame = tk.Frame(root, bg='white')
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Adicionar", font=("Arial", 12), command=self.adicionar, width=12).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Remover", font=("Arial", 12), command=self.remover, width=12).pack(side=tk.LEFT, padx=10)

        estoque_canvas = tk.Canvas(root, width=700, height=220, bg='white', highlightthickness=0)
        estoque_canvas.pack(pady=20)
        estoque_bg = create_rounded_box_image((700, 220), 18, (255,255,255,255), (0,0,0,255))
        self.estoque_bg_img = ImageTk.PhotoImage(estoque_bg)
        estoque_canvas.create_image(0, 0, anchor='nw', image=self.estoque_bg_img)

        scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        self.estoque_listbox = tk.Listbox(
            root, font=("Arial", 12), width=60, height=9, bd=0, relief='flat',
            highlightthickness=0, bg='white', yscrollcommand=scrollbar.set
        )
        estoque_canvas.create_window(16, 16, anchor='nw', window=self.estoque_listbox, width=668, height=188)
        scrollbar.config(command=self.estoque_listbox.yview)
        estoque_canvas.create_window(684, 16, anchor='nw', window=scrollbar, height=188)

        self.atualizar_estoque()

    def atualizar_estoque(self):
        self.estoque_listbox.delete(0, tk.END)
        self.estoque = carregar_estoque()
        for item in self.estoque:
            self.estoque_listbox.insert(
                tk.END,
                f"Nome: {item['nome']} | Preço: {item['preco']} | Quantidade: {item['quantidade']}"
            )

    def adicionar(self):
        nome = self.nome_entry.get().strip()
        preco = self.preco_entry.get().strip().replace(',', '.')
        qtd = self.qtd_entry.get().strip()
        if not nome or not preco or not qtd:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return
        try:
            preco = float(preco)
            qtd = int(qtd)
        except ValueError:
            messagebox.showwarning("Valor inválido", "Preço deve ser número e quantidade deve ser inteiro.")
            return
        for item in self.estoque:
            if item['nome'].lower() == nome.lower():
                item['preco'] = str(preco)
                item['quantidade'] = str(int(item['quantidade']) + qtd)
                break
        else:
            self.estoque.append({'nome': nome, 'preco': str(preco), 'quantidade': str(qtd)})
        salvar_estoque(self.estoque)
        self.atualizar_estoque()
        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.qtd_entry.delete(0, tk.END)

    def remover(self):
        nome = self.nome_entry.get().strip()
        qtd = self.qtd_entry.get().strip()
        if not nome or not qtd:
            messagebox.showwarning("Campos obrigatórios", "Preencha o nome e a quantidade para remover.")
            return
        try:
            qtd = int(qtd)
        except ValueError:
            messagebox.showwarning("Valor inválido", "Quantidade deve ser inteiro.")
            return
        for item in self.estoque:
            if item['nome'].lower() == nome.lower():
                nova_qtd = int(item['quantidade']) - qtd
                if nova_qtd > 0:
                    item['quantidade'] = str(nova_qtd)
                else:
                    self.estoque.remove(item)
                salvar_estoque(self.estoque)
                self.atualizar_estoque()
                self.nome_entry.delete(0, tk.END)
                self.preco_entry.delete(0, tk.END)
                self.qtd_entry.delete(0, tk.END)
                return
        messagebox.showwarning("Produto não encontrado", "Produto não encontrado no estoque.")

def main():
    root = tk.Tk()
    app = EstoqueApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Arquivo feito por Thiago Chemello. @sudothi on github.