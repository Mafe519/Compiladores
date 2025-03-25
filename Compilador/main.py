from analisadorLexico import Lexer, read_file
from analisadorSintatico import Parser
from analisadorSemantico import SemanticAnalyzer

# Caminho do arquivo de entrada
file_path = 'Compilador/trianguloPascal.txt'  # Altere para o caminho do arquivo de código

# Ler e processar o código
code = read_file(file_path)

# Analisador Léxico
lexer = Lexer(code)
lexer.tokenize()

# Imprimir os tokens gerados
lexer.print_tokens()

# Analisador Sintático
parser = Parser(lexer.tokens, lexer.lexemes, lexer.lines)
try:
    parser.parse()
    print("Código sintaticamente correto.")
    
    # Analisador Semântico
    semantic_analyzer = SemanticAnalyzer(lexer.tokens, lexer.lexemes, lexer.lines)
    semantic_analyzer.analyze()
    print("O código está semanticamente correto.")
except SyntaxError as e:
    print(e)

