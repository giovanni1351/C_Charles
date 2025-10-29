| Simbolo              | First                                          | Follow                                                                                               |
|----------------------|------------------------------------------------|------------------------------------------------------------------------------------------------------|
|programa              |int, float, boolean, string                     | $                                                                                                    |
|bloco                 |id, console, if, int, float, boolean, string    | '}'                                                                                                  |
|bloco_op              |id, console, if, int, float, boolean, string, e | '}'                                                                                                  |
|cmd                   |id, console, if, int, float, boolean, string    | id, console, if, int, float, boolean, string, '}'                                                    |
|declarar              |int, float, boolean, string                     | id, console, if, int, float, boolean, string, '}', ';'                                               |
|declarar_op           |id                                              | id, console, if, int, float, boolean, string, '}', ';'                                               |
|declarar_options_linha| '<-'                                           | ';'                                                                                                  |
|cmd_if                |if                                              | id, console, if, int, float, boolean, string, '}'                                                    |
|option_else           |else, e                                         | id, console, if, int, float, boolean, string, '}'                                                    |
|condicional           |id, num, (, !                                   | ')', '&&', '\|\|', '!', ';'                                                                          |
|condicional_linha     |&&, \|\|, !                                     | ')', '&&', '\|\|', '!', ';'                                                                          |
|expressão             |id, num, (                                      | '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                                         |
|expressão_linha       |+, -, e                                         | '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                                         |
|exp_prioridade        |id, num, (                                      | '+', '-', '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                               |
|exp_prioridade_linha  |*, /, e                                         | '+', '-', '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                               |
|fator                 |id, num, (                                      | '*', '/', '+', '-', '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                     |
|leitura               |id                                              | id, console, if, int, float, boolean, string, '}'                                                    |
|escrita               |console                                         | id, console, if, int, float, boolean, string, '}'                                                    |
|escrita_options       |id, "                                           | ';'                                                                                                  |
|atribuição            |id                                              | id, console, if, int, float, boolean, string, '}', ';', ')'                                          |
|atribuição_options    |id, num, (, "                                   | ';'                                                                                                  |
|texto_string          |"                                               | ';'                                                                                                  |
|num                   |num_int, num_decimal                            | '*', '/', '+', '-', '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                     |
|operador_relacional   |>, <, >=, <=, =, !=                             | id, num, (                                                                                           |
|tipo                  |int, float, boolean, string                     | 'charles', id                                                                                        |
|operador_logico       |&&, \|\|, !                                     | id, num, (, !                                                                                        |
|id                    |[a-zA-Z][a-zA-Z0-9]\*                           | '*', '/','+', '-', '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';', '<<', '<-',id, "    |
|num_int               |[0-9]+                                          | '*', '/', '+', '-', '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                     |
|num_decimal           |[0-9]+.[0-9]+                                   | '*', '/', '+', '-', '>', '<', '>=', '<=', '=', '!=', ')', '&&', '\|\|', '!', ';'                     |
|loop_for              |for                                             | id, console, if, int, float, boolean, string, '}'                                                    |
|loop_while            |while                                           | id, console, if, int, float, boolean, string, '}'                                                    |
