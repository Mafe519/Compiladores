"""


<C> ::= <IF>
      | <WHILE>
      | <WRITE>
      | <READ>
      | <ASSIGN>
      | <VAR_DECL>
      | <FOR>
      | <DO>
      | begin <C_LIST> end;

<C_LIST> ::= <C> ";" <C_LIST>
      |î;
<IF> ::= if"("<EXP_LOGIC_HEAD>")" then "{"<C_LIST>"}" <ELSE>;

<ELSE> ::= else "{" <C_LIST> "}" | î;

//<WHILE> ::= while <E> do <C>;
<WRITE> ::= write "(" <E> ")";
<E> ::= id
      | num
      | string;
<READ> ::= read "("id")";
<ASSIGN> ::= id assign <EXP_ARIT_HEAD>;
<VAR_DECL> ::= var id;

<EXP_ARIT_HEAD> ::= <E> <EXP_ARIT_TAIL>;
<EXP_ARIT_TAIL> ::= OpAritmetic <E> <EXP_ARIT_TAIL>
		| î;

<EXP_LOGIC_HEAD> ::= <EXP_ARIT_HEAD> <EXP_LOGIC_TAIL>;// IF(A) SIGNIFICA : A != 0
<EXP_LOGIC_TAIL> ::= OpLogical <EXP_ARIT_HEAD> <EXP_LOGIC_TAIL> 
		| î;

<FOR> ::= for "(" <ASSIGN> ";"  <EXP_LOGIC_HEAD> ";" <ASSIGN> ")" 	"{" <C_LIST> "}";
<WHILE>::= while <EXP_LOGIC_HEAD> do "{" <C_LIST> "}";
              
"""
#from analisadorSemantico import SemanticAnalyzer

class Parser:
    def __init__(self, tokens, lexemes, lines):  #Listas
        self.tokens = tokens
        self.lexemes = lexemes      
        self.lines = lines
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index]      #Mantém o infice so toekens atual que está sendo processado. 
        self.current_lexeme = self.lexemes[self.current_token_index]
        self.current_line = self.lines[self.current_token_index]
        self.operations = []  #lista para armazenar as operações e imprir uma "arvore de derivação"

    def advance(self): 
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):  #verfica se ainda existe tokens na lista
            self.current_token = self.tokens[self.current_token_index]
            self.current_lexeme = self.lexemes[self.current_token_index]
            self.current_line = self.lines[self.current_token_index]
        else:
            self.current_token = None
            self.current_lexeme = None  
            self.current_line = None

    def match(self, expected_token):  #Procedimentos para fazer a comparação entre dois Tokens ou dois lexemas.
        expected_lexeme = None
        
        # Procurar o lexema esperado baseado no token esperado
        for token_type, lexeme in zip(self.tokens, self.lexemes): #Token: [id, assign], Lexema:[x, =], zip = ['id', lexema = 'x']
            if token_type == expected_token:
                expected_lexeme = lexeme    # Se encontrar o token esperado, guarda o lexema correspondente.
                break
        
        if self.current_token == expected_token:
            self.operations.append(f"Desempilhou '{self.current_lexeme}'")  #Se o token atual for o espera, redistra a operação de desempilhar o lexema
            self.advance()
        else:
            error_message = (
                f"Erro sintático na linha {self.current_line}: "
                f"Esperado '{expected_lexeme}', mas encontrado '{self.current_lexeme}'."
            )
            raise SyntaxError(error_message)
        
    def parse(self):  
        self.parse_C()
        if self.current_token is not None: #Começa a analise pelo bloco de comandos <C>
            raise SyntaxError(
                f"Erro sintático na linha {self.current_line}: "
                f"Erro sintático: Tokens restantes após a análise") #Se ainda houver Tokens após a analise , levanta um erro
        self.print_operations()

    def parse_C(self): 
        if self.current_token == 'BEGIN': 
            self.operations.append("Empilhou 'begin'")  #Registra a operação de empilhar
            self.match('BEGIN')  #Verifica se o token atual é begin.
            self.parse_C_LIST() #analisa a lista de comandos
            self.match('END') #verifica se o token final é "END"
            self.operations.append("Empilhou 'end'") #Registra a operação de empilhar
        elif self.current_token == 'IF':
            self.parse_IF()
        elif self.current_token == 'WHILE':
            self.parse_WHILE()
        elif self.current_token == 'WRITE':
            self.parse_WRITE()
        elif self.current_token == 'READ':
            self.parse_READ()
        elif self.current_token == 'ID':
            self.parse_ASSIGN()
        elif self.current_token == 'VAR':
            self.parse_VAR_DECL()
            """semantic_analyzer = SemanticAnalyzer(self.tokens, self.lexemes, self.lines)
            semantic_analyzer.analyze() """
        elif self.current_token == 'FOR':
            self.parse_FOR()
        elif self.current_token == 'DO':
            self.parse_DO()
        else:
            raise SyntaxError(f"Erro sintático: Token inesperado {self.current_token}")

    def parse_C_LIST(self):  
        while self.current_token in {'IF', 'WHILE', 'WRITE', 'READ', 'ID', 'VAR', 'FOR', 'DO', 'BEGIN'}:
            self.parse_C()
            if self.current_token == 'SEMICOLON':
                self.match('SEMICOLON')
            elif self.current_token == 'RBRACE':
                break
            #self.match('SEMICOLON')
            #self.parse_C_LIST()

    def parse_IF(self):
        self.operations.append("Empilhou 'if'")
        self.match('IF')
        self.match('LPAREN')
        self.parse_EXP_LOGIC_HEAD()
        self.match('RPAREN')
        self.match('THEN')
        self.match('LBRACE')
        self.parse_C_LIST()
        self.match("RBRACE")
        self.parse_ELSE()

    def parse_ELSE(self):
        if self.current_token == 'ELSE':
            self.match('ELSE')
            self.match('LBRACE')
            self.parse_C_LIST()
            self.match('RBRACE')

    def parse_WHILE(self):
        self.operations.append("Empilhou 'while'")
        self.match('WHILE')
        self.parse_EXP_LOGIC_HEAD()
        self.match('DO')
        self.match('LBRACE')
        self.parse_C_LIST()
        self.match('RBRACE')
        self.operations.append("Empilhou '}'")

    def parse_WRITE(self):
        self.operations.append("Empilhou 'write'")
        self.match('WRITE')
        self.match('LPAREN')
        self.parse_E()
        self.match('RPAREN')

    def parse_READ(self):
        self.operations.append("Empilhou 'read'")
        self.match('READ')
        self.match('LPAREN')
        self.match('ID')
        self.match('RPAREN')

    def parse_ASSIGN(self):
        self.operations.append(f"Empilhou 'assign' ({self.lexemes[self.current_token_index]})")
        self.match('ID')
        self.match('ASSIGN')
        self.parse_EXP_ARIT_HEAD()

    def parse_VAR_DECL(self):
        self.operations.append(f"Empilhou 'var' ({self.lexemes[self.current_token_index]})")
        self.match('VAR')
        self.match('ID')

    def parse_EXP_ARIT_HEAD(self):
        self.operations.append("Empilhou expressão aritmética")
        self.parse_E()
        self.parse_EXP_ARIT_TAIL()

    def parse_EXP_ARIT_TAIL(self):
        if self.current_token == 'OP_ARITHMETIC':
            self.match('OP_ARITHMETIC')
            self.parse_E()
            self.parse_EXP_ARIT_TAIL()
        # epsilon (í) é tratado automaticamente ao não fazer nada

    def parse_EXP_LOGIC_HEAD(self):
        self.parse_EXP_ARIT_HEAD()
        self.parse_EXP_LOGIC_TAIL()

    def parse_EXP_LOGIC_TAIL(self):
        if self.current_token == 'OP_LOGICAL':
            self.match('OP_LOGICAL')
            self.parse_EXP_ARIT_HEAD()
            self.parse_EXP_LOGIC_TAIL()
        # epsilon (í) é tratado automaticamente ao não fazer nada

    def parse_FOR(self):
        self.operations.append("Empilhou 'for'")
        self.match('FOR')
        self.match('LPAREN')
        self.parse_ASSIGN()
        self.match('SEMICOLON')
        self.parse_EXP_LOGIC_HEAD()
        self.match('SEMICOLON')
        self.parse_ASSIGN()
        self.match('RPAREN')
        self.match('LBRACE')
        self.parse_C_LIST()
        self.match('RBRACE')
        self.operations.append("Empilhou '}'")

    def parse_DO(self):
        raise NotImplementedError("A regra DO não está completamente definida na gramática fornecida.")

    def parse_E(self):
        if self.current_token in {'ID', 'NUM', 'STRING'}:
            self.operations.append(f"Empilhou '{self.lexemes[self.current_token_index]}'")
            self.match(self.current_token)
        else:

            raise SyntaxError(
                f"Erro sintático na linha {self.current_line}: "
                f"Erro sintático: Esperado ID, NUM ou string, mas encontrado {self.current_token}")

    def print_operations(self):
        print("Árvore de Derivação:")
        indent_level = 0                                # Inicializa a variável 'indent_level' com 0 para controlar a indentação das operações.
        for operation in self.operations:               
            print("  " * indent_level + operation)      # Imprime a operação atual com a indentação correspondente ao nível 'indent_level'.
            if "Empilhou" in operation:                 # Se a operação contém a palavra "Empilhou", indica que algo foi empilhado na árvore.
                indent_level += 1                       # Incrementa 'indent_level' em 1, aumentando a indentação para operações subsequentes.
            elif "Desempilhou" in operation:            # Se a operação contém a palavra "Desempilhou", indica que algo foi desempilhado da árvore.
                indent_level -= 1                      

   