class SemanticAnalyzer:
    def __init__(self, tokens, lexemes, lines):
        self.tokens = tokens
        self.lexemes = lexemes
        self.lines = lines
        self.current_token_index = 0
        self.declared_variables = set()  # Conjunto para armazenar variáveis já declaradas.
        self.reserved_keywords = {"var", "begin", "end", "if", "then", "else", "endif", 
                                  "for", "while", "do", "write", "read", "assign"}
    
    def analyze(self):
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            lexeme = self.lexemes[self.current_token_index]
            line = self.lines[self.current_token_index]
            
            if token == "VAR":
                self.current_token_index += 1
                self.declare_variable()
            elif token == "ID":
                if lexeme not in self.declared_variables:
                    raise SyntaxError(f"Erro Semântico: Variável '{lexeme}' utilizada antes de ser declarada na linha {line}.")
                self.current_token_index += 1
            elif token == "OP_ARITHMETIC" and lexeme == "/":
                self.check_division_by_zero()
            else:
                self.current_token_index += 1

    def declare_variable(self):
        if self.current_token_index < len(self.tokens):
            var_name = self.lexemes[self.current_token_index]
            line = self.lines[self.current_token_index]
            
            if var_name in self.reserved_keywords:
                print(f"Erro Semântico: Nome de variável '{var_name}' não pode ser uma palavra reservada na linha {line}.")
                self.current_token_index += 1
            elif var_name in self.declared_variables:
                raise SystemError(f"Erro Semântico: Variável '{var_name}' já declarada anteriormente na linha {line}.")
            else:
                self.declared_variables.add(var_name)
            
            self.current_token_index += 1
    
    def check_division_by_zero(self):
        if (self.current_token_index + 1 < len(self.tokens) and 
            self.tokens[self.current_token_index + 1] == "NUM" and 
            self.lexemes[self.current_token_index + 1] == "0"):
            line = self.lines[self.current_token_index + 1]
            raise SyntaxError(f"Erro Semântico: Divisão por zero detectada na linha {line}.")
        
        self.current_token_index += 2  # Avançar o operador e o próximo token
