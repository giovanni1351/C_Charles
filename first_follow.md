| Simbolo              | First                                          | Follow |
|----------------------|------------------------------------------------|--------|
|programa              |int, float, boolean, string                     |    $   |
|bloco                 |id, console, if, int, float, boolean, string    |    $ , '}'  |
|bloco_op              |id, console, if, int, float, boolean, string, e |    $, '}'  |
|cmd                   |id, console, if, int, float, boolean, string    | id, console, if, int, float, boolean, string, $, '}' |
|declarar              |int, float, boolean, string                     | id, console, if, int, float, boolean, string, $, '}', ';' |
|declarar_op           |id                                              | id, console, if, int, float, boolean, string, $, '}', ';' |
|declarar_options_linha| '<-'                                          |
|cmd_if                |if                                              | id, console, if, int, float, boolean, string, $, '}' |
|option_else           |else, E                                         | id, console, if, int, float, boolean, string, $, '}' |
|condicional           |id, num, (, !                                   | ')', &&, \|\|, !, ';' |
|condicional_linha     |&&, \|\|, !                                     | ')', &&, \|\|, !, ';' |
|expressão             |id, num, (                                      | ')', &&, \|\|, !, ';' |
|expressão_linha       |+, -, E                                         | ')', &&, \|\|, !, ';' |
|exp_prioridade        |id, num, (                                      | +, -, ')', &&, \|\|, !, ';' |
|exp_prioridade_linha  |*, /, E                                         | +, -, ')', &&, \|\|, !, ';' |
|fator                 |id, num, (                                      | *, /, +, -, ')', &&, \|\|, !, ';' |
|leitura               |id                                              | id, console, if, int, float, boolean, string, $, '}' |
|escrita               |console                                         | id, console, if, int, float, boolean, string, $, '}' |
|escrita_options       |id, "                                           |    ;   |
|atribuição            |id                                              | id, console, if, int, float, boolean, string, $, '}', ';', ')' |
|atribuição_options    |id, num, (, "                                   |    ;   |
|texto_string          |"                                               | id, console, if, int, float, boolean, string, $, '}', ';', ')' |
|num                   |num_int, num_decimal                            | *, /, +, -, ')', &&, \|\|, !, ';' |
|operador_relacional   |>, <, >=, <=, =, !=                             |        |
|tipo                  |int, float, boolean, string                     |        |
|operador_logico       |&&, ||, !                                       |        |
|id                    |[a-zA-Z][a-zA-Z0-9]\*                           |        |
|num_int               |[0-9]+                                          |        |
|num_decimal           |[0-9]+.[0-9]+                                   |        |
|loop_for              |for                                             |        |
|loop_while            |while                                           |        |
