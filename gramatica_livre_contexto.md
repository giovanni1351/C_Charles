# Gramática livre de contexto

- **programa** -> tipo 'charles()' '{' bloco '}'

---

> Antes

- **bloco** -> cmd bloco | cmd

---

> Ajustado

- **bloco** -> cmd bloco_options
- **bloco_options** -> bloco | e

---

- **cmd** -> leitura | escrita | atribuicao | cmd_if | declarar

---

> Antes

- **declarar** -> tipo id ';' | tipo atribuicao

---

> Ajustado

- **declarar** -> tipo declarar_options
- **declarar_options** -> id ';' |atribuicao

---

---

> Antes

- **cmd_if** -> 'if' '('condicional')' '->' '{' bloco '}' | 'if' '('condicional')' '->' '{' bloco '}' 'else' '{' bloco'}'

---

> Ajustado

- **cmd_if** -> 'if' '('condicional')' '->' '{' bloco '}' option_else
- **option_else** -> 'else' '{' bloco'}' | e

---

---

> Antes

- **condicional** -> expressão operador_relacional expressão | condicional operador_logico condicional | '!' expressão

---

> Ajustado

- **condicional** -> expressão operador_relacional expressão condicional' |'!' expressão condicional'
- **condicional'** -> operador_logico condicional condicional'

---

> Antes

- **expressão** -> expressão '+' exp_prioridade | expressão '-' exp_prioridade | exp_prioridade

---

> Ajustado

- **expressão** -> exp_prioridade expressão'
- **expressão'** -> '+' exp_prioridade expressão' | - '-' exp_prioridade expressão' | e

---

---

> Antes

- **exp_prioridade** -> exp_prioridade '\*' Fator | exp_prioridade '/' Fator | Fator

---

> Ajustado

- **exp_prioridade** -> Fator exp_prioridade'
- **exp_prioridade'** -> '\*' Fator exp_prioridade' | '/' Fator exp_prioridade' | e

---

- **Fator** -> id | num | '(' expressão ')'
- **leitura** -> id '<<' 'input' ';'

---

> Antes

- **escrita** -> 'console' '<<' id ';' | 'console' '<<' texto_string ';'

---

> Ajustado

- **escrita** -> 'console' '<<' escrita_options ';'
- **escrita_options** -> id | texto_string

---

---

> Antes

- **atribuicao** -> id '<-' expressão; | id '<-' texto_string;

---

> Ajustado

- **atribuicao** -> id '<-' atribuicao_options ';'
- **atribuicao_options** -> expressão | texto_string

---

- **texto_string** -> '"'[a-zA-Z 0-9]'"'
- **num** -> num_int | num_decimal
- **operador_relacional** -> '>' | '<' | '>=' | '<=' | '=' | '!='
- **tipo** -> 'int'| 'float' | 'boolean' | 'string'
- **operador_logico** -> '&&' | '||' | '!'
- **id** -> [a-zA-Z][a-zA-Z0-9]\*
- **num_int** -> [0-9]+
- **num_decimal** -> [0-9]+.[0-9]+
- **loop_for** -> 'for' '(' declarar ';' condicional ';' atribuicao ')' '->' '{' bloco '}'
- **loop_while** -> 'while' '('condicional')' '->' '{' bloco '}'

.
