# Gramática livre de contexto

- **programa** -> tipo 'charles()' '{' bloco '}'
- **bloco** -> cmd bloco | cmd
- **cmd** -> leitura | escrita | atribuicao | cmd_if | declarar
- **declarar** -> tipo id ';' | tipo atribuicao
- **cmd_if** -> 'if' '('condicional')' '->' '{' bloco '}' | 'if' '('condicional')' '->' '{' bloco '}' 'else' '{' bloco'}'
- **condicional** -> expressão operador_relacional expressão | condicional operador_logico condicional
- **expressão** -> expressão operador_matemático fator | fator
- **fator** -> num | id | '(' expressão ')'
- **leitura** -> id '<<' 'input' ';'
- **escrita** -> 'console' '<<' id;
- **atribuicao** -> id '<-' expressão; | id '<-' texto_string;
- **texto_string** -> '"'[a-zA-Z 0-9]'"'
- **num** -> num_int | num_decimal
- **operador_relacional** -> '>' | '<' | '>=' | '<=' | '=' | '!='
- **operador_matemático** -> '+' | '-' | '\*' | '/' | '%'
- **tipo** -> 'int'| 'float' | 'boolean' | 'string'
- **operador_logico** -> '&&' | '||' | '!'
- **id** -> [a-zA-Z][a-zA-Z0-9]\*
- **num_int** -> [0-9]+
- **num_decimal** -> [0-9]+.[0-9]+

int variavel;
variavel << input;
console << variavel;
