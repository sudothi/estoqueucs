import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import csv
import os

class SaleCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sale Cart")
        self.root.configure(bg='white')
        self.root.geometry("1000x600")

        self.items = []
        self.total = 0.0

        entry_canvas = tk.Canvas(root, width=370, height=48, bg='white', highlightthickness=0)
        entry_canvas.pack(pady=20)
        entry_bg = self.create_rounded_box_image((370, 48), 18, (255,255,255,255), (0,0,0,255))
        self.entry_bg_img = ImageTk.PhotoImage(entry_bg)
        entry_canvas.create_image(0, 0, anchor='nw', image=self.entry_bg_img)
        self.entry = tk.Entry(root, font=("Arial", 14), bd=0, relief='flat', bg='white', highlightthickness=0)
        entry_window = entry_canvas.create_window(16, 8, anchor='nw', window=self.entry, width=330, height=32)

        qty_canvas = tk.Canvas(root, width=110, height=48, bg='white', highlightthickness=0)
        qty_canvas.place(x=200, y=20)
        qty_bg = self.create_rounded_box_image((110, 48), 18, (255,255,255,255), (0,0,0,255))
        self.qty_bg_img = ImageTk.PhotoImage(qty_bg)
        qty_canvas.create_image(0, 0, anchor='nw', image=self.qty_bg_img)
        qty_label = tk.Label(qty_canvas, text="Qtd:", font=("Arial", 12), bg='white')
        qty_label.place(x=10, y=12)
        self.qty_entry = tk.Entry(qty_canvas, font=("Arial", 14), bd=0, relief='flat', bg='white', highlightthickness=0, width=5)
        self.qty_entry.place(x=50, y=10, width=45, height=28)
        self.qty_entry.insert(0, "1")

        btn_frame = tk.Frame(root, bg='white')
        btn_frame.pack(pady=10)

        self.add_img = self.create_rounded_button_image((60, 60), 15, (255,255,255,255), (0,0,0,255), 'icons/mais.png')
        add_btn = tk.Button(
            btn_frame, image=self.add_img, width=60, height=60,
            relief='flat', borderwidth=0, bg='white', activebackground='white',
            highlightthickness=0, command=self.add_item
        )
        add_btn.grid(row=0, column=0, padx=15)
        add_lbl = tk.Label(btn_frame, text="Adicionar", bg='white', font=("Arial", 10))
        add_lbl.grid(row=1, column=0, pady=(8,0))

        self.remove_img = self.create_rounded_button_image((60, 60), 15, (255,255,255,255), (0,0,0,255), 'icons/menos.png')
        remove_btn = tk.Button(
            btn_frame, image=self.remove_img, width=60, height=60,
            relief='flat', borderwidth=0, bg='white', activebackground='white',
            highlightthickness=0, command=self.remove_item
        )
        remove_btn.grid(row=0, column=1, padx=15)
        remove_lbl = tk.Label(btn_frame, text="Remover", bg='white', font=("Arial", 10))
        remove_lbl.grid(row=1, column=1, pady=(8,0))

        self.finalize_img = self.create_rounded_button_image((60, 60), 15, (255,255,255,255), (0,0,0,255), 'icons/finalizar.png')
        finalize_btn = tk.Button(
            btn_frame, image=self.finalize_img, width=60, height=60,
            relief='flat', borderwidth=0, bg='white', activebackground='white',
            highlightthickness=0, command=self.finalize_cart
        )
        finalize_btn.grid(row=0, column=2, padx=15)
        finalize_lbl = tk.Label(btn_frame, text="Finalizar", bg='white', font=("Arial", 10))
        finalize_lbl.grid(row=1, column=2, pady=(8,0))

        listbox_canvas = tk.Canvas(root, width=700, height=340, bg='white', highlightthickness=0)
        listbox_canvas.pack(pady=20)
        listbox_bg = self.create_rounded_box_image((700, 340), 18, (255,255,255,255), (0,0,0,255))
        self.listbox_bg_img = ImageTk.PhotoImage(listbox_bg)
        listbox_canvas.create_image(0, 0, anchor='nw', image=self.listbox_bg_img)
        self.listbox = tk.Listbox(root, font=("Arial", 14), width=60, height=15, bd=0, relief='flat', highlightthickness=0, bg='white')
        listbox_window = listbox_canvas.create_window(16, 16, anchor='nw', window=self.listbox, width=668, height=308)

        self.total_label = tk.Label(root, text="Total: R$ 0.00", font=("Arial", 16), bg='white')
        self.total_label.pack(pady=10)

    def create_rounded_button_image(self, size, radius, bg_color, border_color, icon_path=None, text=None):
        rounded = Image.new('RGBA', size, (0, 0, 0, 0))
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius, fill=255)
        draw_rounded = ImageDraw.Draw(rounded)
        draw_rounded.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius, fill=bg_color, outline=border_color, width=2)
        rounded.putalpha(mask)
        if icon_path:
            icon = Image.open(icon_path).resize((36, 36), Image.LANCZOS)
            rounded.paste(icon, ((size[0]-36)//2, (size[1]-36)//2), icon)
        elif text:
            draw_text = ImageDraw.Draw(rounded)
            draw_text.text((size[0]//2, size[1]//2), text, fill=(0,0,0,255), anchor="mm", align="center")
        return ImageTk.PhotoImage(rounded)

    def create_rounded_box_image(self, size, radius, bg_color, border_color):
        from PIL import ImageDraw
        img = Image.new('RGBA', size, (0,0,0,0))
        draw = ImageDraw.Draw(img)
        draw.rounded_rectangle([0,0,size[0]-1,size[1]-1], radius, fill=bg_color, outline=border_color, width=2)
        return img

    def add_item(self):
        nome_produto = self.entry.get().strip()
        try:
            quantidade = int(self.qty_entry.get())
        except ValueError:
            messagebox.showwarning("Quantidade", "Digite uma quantidade válida.")
            return
        if not nome_produto or quantidade <= 0:
            return
        estoque = self.ler_estoque()
        for produto in estoque:
            if produto['nome'].lower() == nome_produto.lower():
                estoque_disp = int(produto['quantidade'])
                if estoque_disp >= quantidade:
                    for item in self.items:
                        if item['nome'].lower() == nome_produto.lower():
                            if estoque_disp >= item['quantidade'] + quantidade:
                                item['quantidade'] += quantidade
                                break
                            else:
                                messagebox.showwarning("Estoque", "Quantidade acima do disponível.")
                                return
                    else:
                        self.items.append({
                            'nome': produto['nome'],
                            'valor': float(produto['valor'].replace(',','.')),
                            'quantidade': quantidade
                        })
                    self.atualizar_listbox()
                    self.entry.delete(0, tk.END)
                    self.qty_entry.delete(0, tk.END)
                    self.qty_entry.insert(0, "1")
                    return
                else:
                    messagebox.showwarning("Estoque", "Produto sem estoque suficiente.")
                    return
        messagebox.showwarning("Produto", "Produto não encontrado no estoque.")

    def remove_item(self):
        selected_item_index = self.listbox.curselection()
        if selected_item_index:
            idx = selected_item_index[0]
            item = self.items[idx]
            if item['quantidade'] > 1:
                item['quantidade'] -= 1
            else:
                del self.items[idx]
            self.atualizar_listbox()

    def atualizar_listbox(self):
        self.listbox.delete(0, tk.END)
        total = 0.0
        for item in self.items:
            subtotal = item['valor'] * item['quantidade']
            total += subtotal
            self.listbox.insert(tk.END, f"{item['nome']} | R$ {item['valor']:.2f} x {item['quantidade']} = R$ {subtotal:.2f}")
        self.total = total
        self.total_label.config(text=f"Total: R$ {self.total:.2f}")

    def finalize_cart(self):
        if not self.items:
            messagebox.showinfo("Finalizar", "Carrinho vazio!")
            return
        estoque = self.ler_estoque()
        for item in self.items:
            for produto in estoque:
                if produto['nome'].lower() == item['nome'].lower():
                    if int(produto['quantidade']) >= item['quantidade']:
                        produto['quantidade'] = str(int(produto['quantidade']) - item['quantidade'])
                    else:
                        messagebox.showwarning("Estoque", f"Estoque insuficiente para {item['nome']}.")
                        return
        self.salvar_estoque(estoque)
        total = sum(item['valor'] * item['quantidade'] for item in self.items)
        messagebox.showinfo(
            "Finalizar",
            f"Carrinho finalizado e estoque atualizado!\n\nValor total da compra: R$ {total:.2f}"
        )
        self.items.clear()
        self.atualizar_listbox()

    def ler_estoque(self):
        estoque = []
        if os.path.exists('estoque.txt'):
            with open('estoque.txt', newline='', encoding='latin1') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 3:
                        estoque.append({'nome': row[0], 'valor': row[1], 'quantidade': row[2]})
        return estoque

    def salvar_estoque(self, estoque):
        with open('estoque.txt', 'w', newline='', encoding='latin1') as f:
            writer = csv.writer(f)
            for produto in estoque:
                writer.writerow([produto['nome'], produto['valor'], produto['quantidade']])

def main():
    root = tk.Tk()
    app = SaleCartApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# Arquivo feito por Thiago Chemello. @sudothi on github.