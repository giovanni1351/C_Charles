# Gramática livre de contexto

- **programa** -> tipo 'charles()' '{' bloco '}'
- **bloco** -> cmd bloco | cmd
- **cmd** -> leitura | escrita | atribuicao | cmd_if | declarar
- **declarar** -> tipo id ';' | tipo atribuicao
- **cmd_if** -> 'if' '('condicional')' '->' '{' bloco '}' | 'if' '('condicional')' '->' '{' bloco '}' 'else' '{' bloco'}'
- **condicional** -> expressão operador_relacional expressão | condicional operador_logico condicional
- **expressao** -> expressao + exp_prioridade | expressao - exp_prioridade | exp_prioridade
- **exp_prioridade** -> exp_prioridade \* Fator | exp_prioridade / Fator | Fator
- **Fator** -> id | num | (expressao)
- **leitura** -> id '<<' 'input' ';'
- **escrita** -> 'console' '<<' id; | 'console' '<<' texto_string
- **atribuicao** -> id '<-' expressão; | id '<-' texto_string;
- **texto_string** -> '"'[a-zA-Z 0-9]'"'
- **num** -> num_int | num_decimal
- **operador_relacional** -> '>' | '<' | '>=' | '<=' | '=' | '!='
- **tipo** -> 'int'| 'float' | 'boolean' | 'string'
- **operador_logico** -> '&&' | '||' | '!'
- **id** -> [a-zA-Z][a-zA-Z0-9]\*
- **num_int** -> [0-9]+
- **num_decimal** -> [0-9]+.[0-9]+
- **loop_for** -> 'for' '(' 'int'

- **loop_for** -> 'for' '(' declarar ';' condicional ';' atribuicao ')' '->' '{' bloco '}'

for (int i =0; i<10 and i< 5 ;i++) ->{

}

int variavel;
variavel << input;
console << variavel;
