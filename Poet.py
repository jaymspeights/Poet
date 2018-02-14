import sys
import parser
import re

EOF = 'EOF'
NOOP = 'NOOP'
OP = 'OP'
CONTROL = 'CONTROL'
COMPARISON = 'COMPARISON'
SYSCALL = 'SYSCALL'
VARIABLE = 'VARIABLE'
NUMBER = 'NUMBER'

control = {3:'BLOCK', 4:'IF', 5:'WHILE'}
op = {2:'ASSIGN', 3:'ADD', 4:'SUBTRACT', 5:'MULTIPLY', 6:'DIVIDE', 7:"MOD"}
comparison = {2:'NOT', 3:'EQUAL', 4:'LT', 5:'LTE'}
syscall = {2:'GETADDR', 5:'PRINT'}

class Int(object):
    def __init__(self):
        self.value = 0
    def getVal(self):
        return self.value
    def setVal(self, value):
        self.value=value

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

class Interpreter(object):
    def __init__(self, source):
        self.text = self.lex(source)
        self.pos = 0
        self.args = []
        self.current_char = self.text[0]
        self.current_token = None
        self.variables = {}

    def set_pos(self, pos):
        self.pos = pos
        self.current_char = self.text[pos]
        self.current_token = self.get_next_token()

    def lex(self, source):
        i = 0;
        length = 0;
        text = [];
        while i < len(source):
            if source[i] is ' ' or source[i] is '\n' or source[i] is '\t':
                if length > 0:
                    text.append(length)
                    length = 0;
            else:
                length+=1
            i+=1;
        if len(text) is 0:
            self.error('Source is empty')
        return text;


    def arg(self, argv):
        self.args.append(argv)

    def error(self, message):
        raise Exception("Error parsing input at pos " + str(self.pos) + " : " + message)

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def _number(self):
        self.advance()
        result = 0
        length = self.current_char
        self.advance()
        while self.current_char is not None and length-1 > 0:
            result *= 10
            result += self.current_char%10
            self.advance()
            length-=1
        return Token(NUMBER, result)

    def _variable(self):
        self.advance()
        result = self.current_char
        self.advance()
        return Token(VARIABLE, result)

    def _control(self):
        self.advance()
        result = self.current_char
        self.advance()
        return Token(CONTROL, control[result])

    def _comparison(self):
        self.advance()
        result = self.current_char
        self.advance()
        return Token(COMPARISON, comparison[result])

    def _syscall(self):
        self.advance();
        result = self.current_char
        self.advance()
        return Token(SYSCALL, syscall[result])

    def _op(self):
        self.advance()
        result = self.current_char
        self.advance()
        return Token(OP, op[result])

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char is 2:
                return self._control();

            if self.current_char is 3:
                return self._number();

            if self.current_char is  4:
                return self._op()

            if self.current_char is 5:
                return self._variable()

            if self.current_char is 6:
                return self._comparison()

            if self.current_char is 7:
                return self._syscall()

            self.advance()
            return Token(NOOP, None)

        return Token(EOF, EOF)

    def eat(self, token_type, *value):
        if value is not None and self.current_token.value == value:
            self.error("Expected " + str(value) + " but found " + str(self.current_token.value))
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error("Expected " + token_type + " but found " + self.current_token.type)

    def execute(self, end):
        while self.current_token.value is not end:
            if self.current_token.type is VARIABLE:
                self.noop()

            elif self.current_token.type is NUMBER:
                self.noop()

            elif self.current_token.type is OP:
                self.op()

            elif self.current_token.type is CONTROL:
                self.control()

            elif self.current_token.type is COMPARISON:
                self.noop()

            elif self.current_token.type is SYSCALL:
                self.syscall()

            elif self.current_token.type is EOF:
                self.error("Expected " + end + " but found " + EOF)

            else:
                self.noop()

    def syscall(self):
        token = self.current_token
        self.eat(SYSCALL)

        if token.value is "PRINT":
            value = self.expression()
            print (value)
            return value;

        if token.value is "GETADDR":
            value = self.expression()
            return self.variable[value];

    def control(self):
        token = self.current_token
        pos = self.pos-2;
        self.eat(CONTROL)

        if token.value is "BLOCK":
            self.execute("BLOCK")
            return

        if token.value is "IF":
            condition = self.expression()
            if condition > 0:
                self.execute("BLOCK")
                self.eat(CONTROL, "BLOCK")
            else:
                self.skip_block();
        elif token.value is "WHILE":
            condition = self.expression()
            if condition > 0:
                self.execute("BLOCK")
                self.set_pos(pos)
            else:
                self.skip_block()

    def skip_block(self):
        self.eat(CONTROL, "BLOCK")
        while (self.current_token.value is not "BLOCK"):
            if self.current_token.value is "IF" or self.current_token.value is "WHILE":
                self.eat(CONTROL)
                while self.current_token.type is not CONTROL:
                    self.current_token = self.get_next_token()
                self.skip_block()
            else:
                self.current_token = self.get_next_token()
        self.eat(CONTROL, "BLOCK")

    def noop(self):
        self.current_token = self.get_next_token()

    def op(self):
        op = self.current_token
        self.eat(OP)

        if op.value is "ASSIGN":
            if self.current_token.type is VARIABLE:
                addr = self.current_token.value
                self.eat(VARIABLE)
                value = self.expression()
            else:
                addr = self.expression()
                value = self.expression()
            self.variables[addr] = value;
            return value;

        left = self.expression()
        right = self.expression()

        if op.value is "ADD":
            return left + right
        if op.value is "SUBTRACT":
            return left - right
        if op.value is "MULTIPLY":
            return left * right
        if op.value is "DIVIDE":
            return left / right
        if op.value is "MOD":
            return left % right

    def comparison(self):
        comparison = self.current_token
        self.eat(COMPARISON)

        left = self.expression()

        if comparison.value is 'NOT':
            return 0 if left > 0 else 1

        right = self.expression()

        if comparison.value is "EQUAL":
            return 1 if left == right else 0
        if comparison.value is "LT":
            return 1 if left < right else 0
        if comparison.value is "LTE":
            return 1 if left <= right else 0

    def expression(self):
        token = self.current_token
        if token.type is VARIABLE:
            if token.value not in self.variables:
                self.error('A ' + token.type + ' with length ' + str(token.value) + ' has not been assigned')
            self.eat(VARIABLE)
            return self.variables[token.value]

        if token.type is NUMBER:
            self.eat(NUMBER)
            return token.value

        if token.type is OP:
            return self.op()

        if token.type is COMPARISON:
            return self.comparison()

        if token.type is SYSCALL:
            return self.syscall()


    def run(self):
        self.current_token = self.get_next_token()
        self.execute(EOF)

def main():
    i = 1
    fn = re.compile(r'.*\.poe$')

    while i < len(sys.argv):
        text = ""
        interpreter = None
        if fn.match(sys.argv[i]):
            with open(sys.argv[i]) as f:
                text += f.read()
            f.close()
            interpreter = Interpreter(text)
        elif interpreter is not None:
            interpreter.arg(sys.argv[i])
        i+=1
    if interpreter is None:
        print ('No file argument found')
        return;
    interpreter.run()


if __name__ == '__main__':
    main()
