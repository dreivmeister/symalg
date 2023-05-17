import re

class Lexer:
    def __init__(self, source):
        # source is a string containing the expression read from stdin
        # two character token might not work -> make it work or change to '^'
        
        source_split = source.split()
        if source_split[0] in ['der','simp']:
            self.keyword = source_split[0]
            self.var = None
            self.val = None
            self.source = re.sub(r'\s+', '', "".join(source_split[1:]))
        elif source_split[0] in ['eval']:
            self.keyword = source_split[0]
            self.var = source_split[1]
            self.val = int(source_split[2])
            
            self.source = re.sub(r'\s+', '', "".join(source_split[3:]))

            
            
        self.len_source = len(self.source)
        self.cursor = 0
        self.current_char = None
        
        self.read_next_char()
        
    def is_EOF(self):
        return self.cursor > self.len_source-1
    
    def read_next_char(self):
        # reads next char advances cursor
        if self.is_EOF():
            self.current_char = None
            return
        
        self.current_char = self.source[self.cursor]
        self.cursor += 1
    
    def read_next_token(self):
        if self.current_char.isdigit():
            return self.read_number()
        if self.current_char.isalpha():
            return self.read_symbol()
        else:
            return self.read_operator()
    
    def read_number(self):
        number = []
        while self.current_char.isdigit() and not self.is_EOF():
            number.append(self.current_char)
            self.read_next_char()
        return int("".join(number))
    
    def read_symbol(self):
        symbol = []
        while not self.current_char.isdigit() and not self.current_char in ['+','-','*','^','/','(',')'] and not self.is_EOF():
            symbol.append(self.current_char)
            self.read_next_char()
            break
        return "".join(symbol)

    def read_operator(self):
        operator = []
        while not self.current_char.isalpha() and not self.current_char.isdigit() and not self.is_EOF():
            operator.append(self.current_char)
            self.read_next_char()
            break
        return "".join(operator)

def tokenize(source):
    tokens = []
    lexer = Lexer(source)
    
    while not lexer.is_EOF():
        token = lexer.read_next_token()
        
        if lexer.is_EOF() and lexer.current_char != None:
            # digit in last
            if str(token).isdigit() and lexer.current_char.isdigit():
                tokens.append(int(str(token) + lexer.current_char))
            # other in last
            else:
                tokens.append(token)
                tokens.append(lexer.current_char)
        else:
            tokens.append(token)    
    return tokens, lexer.keyword, [lexer.var, lexer.val]

def build_expr(tokens):
    expr_str = "kw['e']="
    for t in tokens:
        t = str(t)
        if t.isdigit():
            expr_str += 'Const(' + t + ')'
        elif t.isalpha():
            expr_str += 'Var(' + "'" + t + "'" + ')'
        else:
            if t == '^':
                expr_str += '**'
            else:
                expr_str += t
    return expr_str
        
        