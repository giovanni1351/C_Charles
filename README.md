# Como rodar?

O projeto é feito utilizando o gerenciador de pacotes UV, para rodar como o esperado é necessário ter instalado em sua maquina ou então, criar um ambiente virtual e instalar o rich com o seu gerenciador de pacotes (ele é a unica dependencia).
Caso prefira, é possivel rodar com o python global caso tenha o rich instalado

Caso você ja tenha o UV instalado no seu computador, basta entrar pelo terminal
na pasta onde contem o arquivo [pyproject.py](pyproject.toml) e rodar o comando

```bash
uv run src/main.py
```

Caso deseje instalar o uv o basta clickar no seguinte link: [UV Astral](https://docs.astral.sh/uv/getting-started/installation/)

O projeto é desenvolvido em python utilizando ferramentas para tipagem e linting.

Utilizamos o ruff (formater e linter) e pyright (type checker). Eles nos trazem um padrão com o mercado.

## Dependencias

O projeto tem o intuito de ser o mais puro possivel, utilizando apenas o rich, para a criação de prints coloridos, apenas para questão estética.

# Lista de Tokens

> Abaixo estão todos os tokens aceitos pelo analizador lexico.

- **id** : [a-zA-Z][a-zA-Z0-9]\*
- **palavras_reservadas**: (string | boolean | float | int | for |while | if | else | else if | input | console)
- **operador_atribuicao**: "<-"
- **operador_matematico**: ("+" | "-" | "/" | "\*" | "%")
- **operador_logico**: ("&&' | "||" | "!")
- **operador_relacional**: (">" | "<" | ">="| "<=" | "=" | "!=")
- **Operador saida**: "<<"
- **abre_parenteses**: "("
- **fecha_parenteses**: ")"
- **abre_chaves**: "{"
- **fecha_chaves**: "}"
- **fim_instrucao**: ";"
- **numero_inteiro**: [0-9]+
- **numero_decimal**: [0-9]+.[0-9]+
- **textos**: [a-z _ A-Z 0-9 ]\*

# Gramatica

> Exemplos da sintaxe da nossa linguagem
> obs: Linguagem livre de contexto ainda não feita, está em nossos proximos steps

- **Input**

```
int variavel;
variavel << input;
```

- **Console output**

```
console << variavel;
```

- **Controle de fluxo**

```
int variavel;
variavel << input;
if (variavel > 10) ->{
  console << variavel
} else if (variavel < -10) ->{
  console << "Variavel menor que -10";
} else ->{
  console << "Esta dentro do intervalo -10 e 10";
}

```

- **Atribuição**

```
int variavel <- 30;
variavel <- variavel + 3;
console << variavel;
```

- **Operadores logicos**

```
int variavel;
variavel << input;
bool estaNoIntervalo;
if ( variavel > 10 && variavel < 30 ) -> {
  estaNoIntervalo = true;
}
if (!estaNoIntervalor){
  console << "Não está no intervalo";
}
if(variavel = 30){
  console<< "A variavel é exatamente 30";
}
```
