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

    # Lê o arquivo CSV e preenche a lista
    csv_path = 'inventory.csv'
    if os.path.exists(csv_path):
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                listbox.insert(tk.END, ', '.join(row))
    else:
        listbox.insert(tk.END, 'Arquivo inventory.csv não encontrado.')

    root.mainloop()

if __name__ == "__main__":
    main()
