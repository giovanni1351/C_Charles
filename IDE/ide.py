import os
import re
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING, NoReturn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from lexic.lexer import Lexer
from lexic.parser import Parser, ParserError

if TYPE_CHECKING:
    from lexic.token_lexico import Token
    from lexic.tree import Tree


class Redirector:
    def __init__(self, text_widget: tk.Text) -> None:
        self.text_widget = text_widget

    def write(self, msg: str) -> None:
        self.text_widget.config(state="normal")
        self.text_widget.insert(tk.END, msg)
        self.text_widget.see(tk.END)
        self.text_widget.config(state="disabled")

    def flush(self) -> None:
        pass


class Ide:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("IDE para C-Charles")
        self.root.geometry("900x700")

        menu = tk.Menu(self.root)
        menu.add_command(label="Abrir", command=self.abrir_arquivo)
        menu.add_command(label="Salvar", command=self.salvar_arquivo)
        menu.add_command(label="Executar", command=self.executar)

        self.root.config(menu=menu)

        nav_frame = tk.Frame(self.root, bg="#2d2d2d", height=40)
        nav_frame.pack(fill="x")

        btn_editor = tk.Button(
            nav_frame, text="Editor", command=lambda: self.mostrar_pagina("editor")
        )
        btn_tokens = tk.Button(
            nav_frame, text="Tokens", command=lambda: self.mostrar_pagina("tokens")
        )
        btn_arvore = tk.Button(
            nav_frame, text="Árvore", command=lambda: self.mostrar_pagina("arvore")
        )
        btn_traducao = tk.Button(
            nav_frame, text="Tradução", command=lambda: self.mostrar_pagina("traducao")
        )

        btn_editor.pack(side="left", padx=5, pady=5)
        btn_tokens.pack(side="left", padx=5, pady=5)
        btn_arvore.pack(side="left", padx=5, pady=5)
        btn_traducao.pack(side="left", padx=5, pady=5)

        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.page_editor = tk.Frame(self.container)

        self.frame_editor = tk.Frame(self.page_editor)
        self.frame_editor.pack(fill="both", expand=True)

        self.numeros = tk.Text(
            self.frame_editor,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background="#f0f0f0",
            state="disabled",
            font=("Consolas", 12),
        )
        self.numeros.pack(side="left", fill="y")

        self.texto = tk.Text(
            self.frame_editor, wrap="none", undo=True, font=("Consolas", 12)
        )
        self.texto.pack(fill="both", expand=True)

        tk.Label(
            self.page_editor,
            text="Saída do compilador:",
            anchor="w",
            font=("Consolas", 10, "bold"),
        ).pack(fill="x")

        self.saida = tk.Text(
            self.page_editor,
            height=10,
            bg="#111",
            fg="#0f0",
            font=("Consolas", 11),
            state="disabled",
        )

        sys.stdout = Redirector(self.saida)
        sys.stderr = Redirector(self.saida)

        self.saida.pack(fill="x")

        self.texto.bind("<KeyRelease>", self.atualizar_linhas)
        self.texto.bind("<ButtonRelease>", self.atualizar_linhas)
        self.texto.bind("<KeyRelease>", self.highlight, add="+")

        self.texto.tag_config("palavras_chave", foreground="#0077aa")
        self.texto.tag_config("string", foreground="#aa5500")

        self.page_tokens = tk.Frame(self.container)
        tk.Label(
            self.page_tokens, text="Lista de Tokens", font=("Consolas", 12, "bold")
        ).pack()

        self.tokens_text = tk.Text(self.page_tokens, font=("Consolas", 12))
        self.tokens_text.pack(fill="both", expand=True)

        self.page_arvore = tk.Frame(self.container)
        tk.Label(
            self.page_arvore, text="Árvore Sintática", font=("Consolas", 12, "bold")
        ).pack()

        self.arvore_text = tk.Text(self.page_arvore, font=("Consolas", 12))
        self.arvore_text.pack(fill="both", expand=True)

        self.page_traducao = tk.Frame(self.container)
        tk.Label(
            self.page_traducao, text="Tradução em Pascal", font=("Consolas", 12, "bold")
        ).pack()

        self.traducao_text = tk.Text(self.page_traducao, font=("Consolas", 12))
        self.traducao_text.pack(fill="both", expand=True)

        self.paginas = {
            "editor": self.page_editor,
            "tokens": self.page_tokens,
            "arvore": self.page_arvore,
            "traducao": self.page_traducao,
        }

        self.mostrar_pagina("editor")

        if not self.texto.get("1.0", tk.END).strip():
            self.processa_modelo()

        self.atualizar_linhas()

    def mostrar_pagina(self, nome_pagina: str) -> None:
        for pagina in self.paginas.values():
            pagina.pack_forget()
        self.paginas[nome_pagina].pack(fill="both", expand=True)

    def executar(self) -> None:
        self.saida.config(state="normal")
        self.saida.delete("1.0", tk.END)

        codigo = self.texto.get("1.0", tk.END)

        lexer: Lexer = Lexer(codigo)
        tokens: list[Token] = lexer.get_token()
        parser = Parser(tokens)

        self.tokens_text.delete("1.0", tk.END)

        for token in tokens:
            self.tokens_text.insert(tk.END, f"{token}\n")
        try:
            arvore: Tree = parser.main()
        except ParserError as error:
            print(f"Erro de parse: {error}")
            return
        arvore_str: str = arvore.root.get_tree()

        conteudo = self.saida.get("1.0", tk.END).strip()

        if conteudo == "Sintaticamente correto":
            self.saida.config(state="normal")
            self.saida.delete("1.0", tk.END)

            # Alerta de Gambiarra
            # Alterar para apenas escrever no arquivo quando tiver a string de traduçãp
            arvore.print_code(declaracoes=parser.declaracoes)
            with open("traducao.pas", "w", encoding="utf-8") as arquivo:
                conteudo = self.saida.get("1.0", tk.END)
                arquivo.write(conteudo)

            self.traducao_text.delete("1.0", tk.END)
            self.traducao_text.insert(tk.END, conteudo)

            self.saida.config(state="normal")
            self.saida.delete("1.0", tk.END)

            os.system("fpc traducao.pas")  # noqa: S605, S607
            os.system("traducao.exe")  # noqa: S605, S607

            try:
                compilacao = subprocess.run(
                    ["fpc", "traducao.pas"],  # noqa: S607
                    text=True,
                    capture_output=True,
                )

                if compilacao.returncode == 0:
                    execucao = subprocess.run(  # noqa: S603
                        ["./traducao.exe" if os.name != "nt" else "traducao.exe"],
                        text=True,
                        capture_output=True,
                    )
                    self.mostrar_saida(execucao.stdout)
                    self.mostrar_saida(execucao.stderr)
                else:
                    self.mostrar_saida("Erro na compilação do pascal.\n")
            except FileNotFoundError:
                self.mostrar_saida("Sem FPC.\n")

        self.arvore_text.delete("1.0", tk.END)
        self.arvore_text.insert(tk.END, arvore_str)

    def abrir_arquivo(self) -> None:
        caminho = filedialog.askopenfilename(
            filetypes=[("Arquivos C-Charles", "*.ccr"), ("Todos os arquivos", "*.*")]
        )
        if caminho:
            with open(caminho, encoding="utf-8") as arquivo:
                conteudo = arquivo.read()
                self.texto.delete("1.0", tk.END)
                self.texto.insert("1.0", conteudo)

    def mostrar_saida(self, texto: str) -> None:
        if texto.strip():
            self.saida.config(state="normal")
            self.saida.insert(tk.END, texto)
            self.saida.see(tk.END)
            self.saida.config(state="disabled")

    def salvar_arquivo(self) -> None:
        caminho = filedialog.asksaveasfilename(
            defaultextension=".ccr", filetypes=[("Arquivos C-Charles", "*.ccr")]
        )

        if caminho:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                conteudo = self.texto.get("1.0", tk.END)
                arquivo.write(conteudo)
            messagebox.showinfo(title="Salvar", message="Arquivo salvo com sucesso!")  # pyright: ignore[reportUnknownMemberType]

    def atualizar_linhas(self, event: tk.Event | None = None) -> None:
        self.numeros.config(state="normal")
        self.numeros.delete("1.0", "end")

        total_linhas = int(self.texto.index("end-1c").split(".")[0])
        linhas = "\n".join(str(i) for i in range(1, total_linhas + 1))

        self.numeros.insert("1.0", linhas)
        self.numeros.config(state="disabled")

    def highlight(self, event: tk.Event | None = None) -> None:
        self.texto.tag_remove("palavras_chave", "1.0", "end")
        self.texto.tag_remove("string", "1.0", "end")
        self.texto.tag_remove("comentarios", "1.0", "end")

        codigo = self.texto.get("1.0", "end-1c")
        palavras_chave = (
            r"\b(string|boolean|float|int|for|while|if|else|else if|input|console)\b"
        )
        strings = r"(\".*?\"|\'.*?\')"

        for match in re.finditer(palavras_chave, codigo, re.MULTILINE):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"

            self.texto.tag_add("palavras_chave", start, end)

        for match in re.finditer(strings, codigo, re.MULTILINE):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"

            self.texto.tag_add("string", start, end)

    def processa_modelo(self) -> None:
        with open("modelo.ccr", encoding="utf-8") as arquivo:
            codigo_modelo = arquivo.read()

        self.texto.insert("1.0", codigo_modelo)
        self.highlight()

    def run(self) -> NoReturn:
        self.root.mainloop()
        exit()


if __name__ == "__main__":
    ide = Ide()
    ide.run()
