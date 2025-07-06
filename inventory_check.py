import tkinter as tk
import csv
import os

def main():
    root = tk.Tk()
    root.title("Inventory Check")
    root.configure(bg='white')
    root.geometry("800x600")

    frame = tk.Frame(root, bg='white')
    frame.pack(pady=30)

    listbox = tk.Listbox(frame, font=("Arial", 14), width=60, height=25)
    listbox.pack()

    txt_path = 'estoque.txt'
    if os.path.exists(txt_path):
        with open(txt_path, newline='', encoding='latin1') as txtfile:
            reader = csv.reader(txtfile)
            for row in reader:
                if len(row) == 3:
                    nome, valor, quantidade = row
                    listbox.insert(tk.END, f"Nome: {nome} | Valor: {valor} | Quantidade: {quantidade}")
                else:
                    listbox.insert(tk.END, ', '.join(row))
    else:
        listbox.insert(tk.END, 'Arquivo estoque.txt não encontrado.')

    root.mainloop()

if __name__ == "__main__":
    main()

# Arquivo feito por Thiago Chemello. @sudothi on github.