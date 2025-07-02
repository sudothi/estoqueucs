import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

# Oque vai ser colocado aqui eh o codigo do produto, e quando clicar no botao finalizar ele vai remover a quantidade de itens do estoque, nao esta finalizado falta mudar algumas coisas

class SaleCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sale Cart")
        self.root.configure(bg='white')
        self.root.geometry("1000x600")

        self.items = []

        entry_canvas = tk.Canvas(root, width=320, height=48, bg='white', highlightthickness=0)
        entry_canvas.pack(pady=20)
        entry_bg = self.create_rounded_box_image((320, 48), 18, (255,255,255,255), (0,0,0,255))
        self.entry_bg_img = ImageTk.PhotoImage(entry_bg)
        entry_canvas.create_image(0, 0, anchor='nw', image=self.entry_bg_img)
        self.entry = tk.Entry(root, font=("Arial", 14), bd=0, relief='flat', bg='white', highlightthickness=0)
        entry_window = entry_canvas.create_window(16, 8, anchor='nw', window=self.entry, width=288, height=32)

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
        item = self.entry.get().strip()
        if item:
            self.items.append(item)
            self.listbox.insert(tk.END, item)
            self.entry.delete(0, tk.END)

    def remove_item(self):
        selected_item_index = self.listbox.curselection()
        if selected_item_index:
            self.listbox.delete(selected_item_index)
            del self.items[selected_item_index[0]]

    def finalize_cart(self):
        tk.messagebox.showinfo("Finalizar", "Carrinho finalizado!")

def main():
    root = tk.Tk()
    app = SaleCartApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
