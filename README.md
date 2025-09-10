
# Lista de Tokens
- id: [a-z _ A-Z] +
- palavras_reservadas: (string | float | int | for |while | if | else | else if | input | console)
- operador_atribuicao: "<-"
- operador_matematico: (+ | - | / | *)
- abre_parenteses: "("
- fecha_parenteses: ")"
- abre_chaves: "{"
- fecha_chaves: "}"
- fim_instrucao: ";"
- numero_inteiro: [0-9]+i
- numero_decimal: [0-9]+.[0-9]+f
- textos: "[a-z _ A-Z 0-9 ]*"