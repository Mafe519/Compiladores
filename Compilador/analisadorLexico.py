"""
****Tokens *****

//pontuação
"("
")"
";"
"{"
"}"

//Programa para testar todas as funcionalidades:
// begin 
//var a;
//var b;
//var i;
//var sum;
//a = 2;
//b = 3;
//sum = a+b;

//for(i=0; i<10;i=i+1)
//{
//	write(i);
//};

//while i != 9 do
//{
//	write(i);
//	i = i + 1;
//};
//end 


//palavras chave

id : {L} ( {L} | {D} | _ )*
begin = id : "begin"
end   = id : "end"
if    = id : "if"
then  = id : "then"
else  = id : "else"
while = id : "while"
do    = id : "do"
write = id : "write"
read  = id : "read"
assign     : "="
var   = id : "var"
for   = id : "for"

string : \"({L}| {D} | {E}| {S})*\" 
num : {D} ({D})*//um ou mais dígitos, seguido de qqr char menos letra

// Expressoes aritmética



//exp_arit: ^[\s\d()+\-*\/]+$


OpLogical: "==" | "!=" | "<" | ">" | "<=" | ">=" | "||"| "&&" | "!"
OpAritmetic: "+" | "-" | "*" | "/"

//ignorar espaços em branco e comentários
 : {WS}*
 :! {COMMENT}
"""
import re

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.lexemes = []
        self.positions = []
        self.lines = []

        self.keywords = {  
            "begin", "end", "if", "then", "else", "while", "do", "write", "read", "var", "for"
        }
        self.token_patterns = [  
            ("COMMENT", r"\(\*.*?\*\)"),
            ("WS", r"[ \t\n\r]+"),
            ("BEGIN", r"\bbegin\b"),
            ("END", r"\bend\b"),
            ("STRING", r"\"([A-Za-z0-9\s!@#$%^&*()_+={}\[\]:;,.<>?|\\\/-]*)\""),
            ("IF", r"\bif\b"),
            ("THEN", r"\bthen\b"),
            ("ELSE", r"\belse\b"),
            ("WHILE", r"\bwhile\b"),
            ("DO", r"\bdo\b"),
            ("WRITE", r"\bwrite\b"),
            ("READ", r"\bread\b"),
            ("VAR", r"\bvar\b"),
            ("FOR", r"\bfor\b"),
            ("OP_LOGICAL", r"==|!=|<=|>=|<|>|&&|\|\||!"),
            ("ASSIGN", r"="),
            ("OP_ARITHMETIC", r"\+|-|\*|/"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("LBRACE", r"\{"),
            ("RBRACE", r"\}"),
            ("SEMICOLON", r";"),
            ("ID", r"\b[A-Za-z_][A-Za-z0-9_]*\b"),
            ("NUM", r"\b[0-9]+\b"),
        ]

        self.token_regex = self.compile_regex() 

    def compile_regex(self): 
        token_regex = []
        for token_type, pattern in self.token_patterns:  
            token_regex.append(f"(?P<{token_type}>{pattern})") #(?P<nome_do_grupo>expressão) ("IF", r"\bif\b")
        return re.compile("|".join(token_regex))   # Cria um objeto regex que pode ser usado para fazer correspondencias, join combina todos os padrões na lista separado por "|"

    #percorre o código fonte casando cada trecho com os padrões de tokens definidos
    def tokenize(self):   
        position = 0
        line_number = 1
        while position < len(self.code):  # Continua até que toda a string do código-fonte seja processada.
            match = self.token_regex.match(self.code, position)
            if match: #se token foi encontrado
                token_type = match.lastgroup #retorna o nome do grupo que foi casado
                lexeme = match.group(token_type) #obtem o lexema que corresponde ao token
                if token_type != "WS" and token_type != "COMMENT":  
                    self.tokens.append(token_type)
                    self.lexemes.append(lexeme)
                    self.positions.append(position)
                    self.lines.append(line_number)
                position = match.end() #atualiza a posição para o fim do lexema casado.

                line_number += lexeme.count('\n')
            else:
                print(f"Caractere illegal na posicao: {position}")
                break

    def print_tokens(self):
        print(f"{'Token':<15} {'Lexema':<15} {'Posição':<10} {'Linha':<5}")
        print("-" * 50)
        for token, lexeme, position, line in zip(self.tokens, self.lexemes, self.positions, self.lines):
            print(f"{token:<15} {lexeme:<15} {position:<10} {line:<5}")

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

"""# Testandooooo
file_path = 'arquivo.txt'  
code = read_file(file_path)

lexer = Lexer(code)
lexer.tokenize()
lexer.print_tokens()
"""