import re
import sys
from Compiler.parse import Parser

class PrePro():
    '''
    Pré-processamento usando regex e expressões regulares
    '''
    @staticmethod
    def filter(input):
        filtered = re.sub(r'//.*', "", input)
        return filtered
          
if __name__ == "__main__":

    input_file = sys.argv[1]

    with open(input_file, 'r') as f:
        input = f.read()
        
    filtered = PrePro.filter(input)
    parser = Parser()
    parser.run(filtered)