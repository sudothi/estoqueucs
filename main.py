import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import subprocess

class LoadingToArchiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Truck Stock")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")

        self.label = tk.Label(root, bg="white")
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.archive_image = Image.open("icons/archive.png").convert("RGBA")
        self.archive_image = self.archive_image.resize((100, 100), Image.LANCZOS)
        self.fade_alpha = 0

        self.start_fade_in_archive()

    def start_fade_in_archive(self):
        self.fade_alpha = 1
        self.fade_in_step()

    def fade_in_step(self):
        if self.fade_alpha <= 255:
            transparent = Image.new("RGBA", self.archive_image.size, (255, 255, 255, 0))
            faded = Image.blend(transparent, self.archive_image, self.fade_alpha / 255)

            self.tk_archive = ImageTk.PhotoImage(faded)
            self.label.configure(image=self.tk_archive)
            self.fade_alpha += 10
            self.root.after(50, self.fade_in_step)
        else:
            self.root.after(5000, self.show_blank_screen)

    def show_blank_screen(self):
        self.label.place_forget() 
        self.root.configure(bg='white')  

        main_frame = tk.Frame(self.root, bg='white')
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        buttons_info = [
            ("icons/add.png", "add or remove obj", self.open_add_or_remove_obj),
            ("icons/archive.png", "inventory check", self.open_inventory_check),
            ("icons/dollar.png", "sale", self.open_sale)
        ]
        self.button_images = []  
        for i, (icon_path, label_text, callback) in enumerate(buttons_info):
            btn_frame = tk.Frame(main_frame, bg='white')
            btn_frame.grid(row=0, column=i, padx=40)


            size = (90, 90)
            radius = 20
            bg_color = (255, 255, 255, 255)
            border_color = (0, 0, 0, 255)
            rounded = Image.new('RGBA', size, (0, 0, 0, 0))
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius, fill=255)
            draw_rounded = ImageDraw.Draw(rounded)
            draw_rounded.rounded_rectangle([0, 0, size[0]-1, size[1]-1], radius, fill=bg_color, outline=border_color, width=2)
            rounded.putalpha(mask)


            icon = Image.open(icon_path).resize((64, 64), Image.LANCZOS)
            rounded.paste(icon, ((size[0]-64)//2, (size[1]-64)//2), icon)

            tk_img = ImageTk.PhotoImage(rounded)
            self.button_images.append(tk_img)

            btn = tk.Button(
                btn_frame,
                image=tk_img,
                width=90, height=90,
                relief='flat', borderwidth=0,
                bg='white', activebackground='white',
                highlightthickness=0,
                command=callback if callback else None
            )
            btn.pack()

            lbl = tk.Label(btn_frame, text=label_text, bg='white', font=("Arial", 10))
            lbl.pack(pady=(8,0))

    def open_add_or_remove_obj(self):
        subprocess.Popen(['python', 'add_or_remove_obj.py'])

    def open_inventory_check(self):
        subprocess.Popen(['python', 'inventory_check.py'])

    def open_sale(self):
        subprocess.Popen(['python', 'sale.py'])

if __name__ == "__main__":
    root = tk.Tk()
    app = LoadingToArchiveApp(root)
    root.mainloop()

# Arquivo feito por Thiago Chemello. @sudothi on github.
