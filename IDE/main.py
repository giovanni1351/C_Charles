import os
import sys
import tkinter as tk
from typing import NoReturn

sys.path.append(os.path.join(os.path.basename(__file__), "..", "src"))
from lexic.lexer import Lexer
from lexic.parser import Parser
from lexic.token_lexico import Token

print(os.path.basename(__file__))


class Ide:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("IDE para C-Charles")
        self.root.geometry("800x600")

        menu = tk.Menu(self.root)

        menu.add_command(label="Executar", command=self.executar)

        self.root.config(menu=menu)

        self.texto = tk.Text(self.root, wrap="none", undo=True, font=("Consolas", 12))
        self.texto.pack(fill="both", expand=True)

    def executar(self) -> None:
        codigo = self.texto.get("1.0", tk.END)
        lexer: Lexer = Lexer(codigo)
        tokens: list[Token] = lexer.get_token()
        for token in tokens:
            print(token)
        parser = Parser(tokens)
        with open("codigo.ccr", "w", encoding="utf-8") as arquivo:
            arquivo.write(codigo)
        with open("arvore.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write(parser.main().root.get_tree())

    def run(self) -> NoReturn:
        self.root.mainloop()
        exit()


if __name__ == "__main__":
    ide = Ide()
    ide.run()
