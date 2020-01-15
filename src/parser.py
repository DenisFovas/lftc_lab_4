# The purose of this module is to provide the actual parsing algorithm for an input.
# For constructing the parsing table (or other pre-requisites for this task), see 'grammar'.

from grammar import epsilon
from exception.parsing_exception import ParsingException

def parse(grammar, firstX, followX, input_statement):
    # Initiate the input
    input_statement = input_statement + '$' 
    # Create the table based on the First, Follow
    parse_table = create_parsing_table(firstX, followX, grammar)
    
    starting_symbol = grammar['startSymbol']
    stack = [starting_symbol]

    # The returned statement. This will contain what tokens are parsed.
    parsing_statement = ""
    token = input_statement[0]
    input_statement = input_statement[1:]

    while len(stack) > 0 and len(input_statement) > 0:
        symbol = stack.pop()
        key = (symbol, token)
        rule = parse_table.get(key, None)

        # invlid input until now, so error
        if rule is None:
            raise ParsingException()

        # Case like (token, token), where we pop the first of the input_statement
        if rule == get_pop_method():
            token = input_statement[0]
            input_statement = input_statement[1:]

        stack.append(rule)
    
    # The case that the statement is not done, or the stack is not done.
    if len(stack) > 0 or len(input_statement) > 0:
        raise ParsingException()

    return parsing_statement



def create_parsing_table(firstX, followX, grammar):
    parse_table = {}
    
    production_numbers = numerotate_productions(grammar['productions'])

    terminals = grammar['terminals']
    non_terminals = grammar['nonterminals']

    for terminal in terminals:
        index = (terminal, terminal)
        parse_table[index] = get_pop_method()

    for terminal in terminals:
        for non_terminal in non_terminals:
            index = (non_terminal, terminal)
            parse_table[index] = firstX[non_terminal]

    for non_terminal in non_terminals:
        index = (non_terminal, '$')

    for i, production in enumerate(grammar['productions']):
        for first_element in firstX[production]:
            index = (production, first_element)
            parse_table[index] = grammar['productions'][production]

        if epsilon() in grammar['productions'][production]:
            for first_element in followX[production]:
                index = (production, first_element)
                parse_table[index] = production_numbers.index(grammar['productions'][production])

    return parse_table


def get_pop_method():
    return 'pop'

def numerotate_productions(productions):
    production_numbers = {}
    id = 1
    for production in productions:
        production_numbers[id] = productions[production]
        id += 1
    
    return production_numbers

