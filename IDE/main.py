import tkinter as tk


class Ide:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("IDE para C-Charles")
        self.root.geometry("800x600")

        menu = tk.Menu(root)

        menu.add_command(label="Executar", command=self.executar)

        root.config(menu=menu)

        self.texto = tk.Text(root, wrap="none", undo=True, font=("Consolas", 12))
        self.texto.pack(fill="both", expand=True)

    def executar(self) -> None:
        codigo = self.texto.get("1.0", tk.END)

        with open("codigo.ccr", "w", encoding="utf-8") as arquivo:
            arquivo.write(codigo)

if __name__ == "__main__":
    root = tk.Tk()
    ide = Ide(root)
    root.mainloop()
