import os
import re
import sys
import tkinter as tk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Src')))  # noqa: Q000

from main import Main


class Ide:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("IDE para C-Charles")
        self.root.geometry("800x600")

        menu = tk.Menu(root)
        menu.add_command(label="Executar", command=self.executar)
        root.config(menu=menu)

        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(fill="both", expand=True)

        self.frame_editor = tk.Frame(self.frame_principal)
        self.frame_editor.pack(fill="both", expand=True)

        self.numeros = tk.Text(self.frame_editor, width=4, padx=4, takefocus=0, border=0, background="#f0f0f0", state="disabled", font=("Consolas", 12))  # noqa: E501
        self.numeros.pack(side="left", fill="y")

        self.texto = tk.Text(self.frame_editor, wrap="none", undo=True, font=("Consolas", 12))  # noqa: E501
        self.texto.pack(fill="both", expand=True)

        tk.Label(self.frame_principal, text="Saída do compilador:", anchor="w", font=("Consolas", 10, "bold")).pack(fill="x")  # noqa: E501

        self.saida = tk.Text(self.frame_principal, height=10, bg="#111", fg="#0f0", font=("Consolas", 11), state="disabled")  # noqa: E501
        self.saida.pack(fill="x")

        self.texto.bind("<KeyRelease>", self.atualizar_linhas)
        self.texto.bind("<ButtonRelease>", self.atualizar_linhas)
        self.texto.bind("<KeyRelease>", self.highlight, add="+")

        self.texto.tag_config("palavras_chave", foreground="#0077aa")
        self.texto.tag_config("string", foreground="#aa5500")

        self.atualizar_linhas()

    def atualizar_linhas(self, event: tk.Event = None) -> None:  # noqa: RUF013
        self.numeros.config(state="normal")
        self.numeros.delete("1.0", "end")

        total_linhas = int(self.texto.index("end-1c").split(".")[0])
        linhas = "\n".join(str(i) for i in range(1, total_linhas + 1))
        self.numeros.insert("1.0", linhas)

        self.numeros.config(state="disabled")

    def highlight(self, event: tk.Event = None) -> None:  # noqa: RUF013
        self.texto.tag_remove("palavras_chave", "1.0", "end")
        self.texto.tag_remove("string", "1.0", "end")
        self.texto.tag_remove("comentarios", "1.0", "end")

        codigo = self.texto.get("1.0", "end-1c")

        palavras_chave = r"\b(string|boolean|float|int|for|while|if|else|else if|input|console)\b"  # noqa: E501
        strings = r"(\".*?\"|\'.*?\')"

        for match in re.finditer(palavras_chave, codigo, re.MULTILINE):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.texto.tag_add("palavras_chave", start, end)

        for match in re.finditer(strings, codigo, re.MULTILINE):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.texto.tag_add("string", start, end)

    def executar(self) -> None:
        codigo = self.texto.get("1.0", tk.END)
        with open("codigo.ccr", "w", encoding="utf-8") as arquivo:
            arquivo.write(codigo)

        Main()

        with open("arquivo.ccr", encoding="utf-8") as arq:
            resultado = arq.read()

        self.saida.config(state="normal")
        self.saida.delete("1.0", tk.END)
        self.saida.insert(tk.END, resultado)
        self.saida.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    ide = Ide(root)
    root.mainloop()
