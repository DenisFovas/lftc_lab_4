# The purose of this module is to provide the actual parsing algorithm for an input.
# For constructing the parsing table (or other pre-requisites for this task), see 'grammar'.


def parse(grammar, firstX, followX, statement):
    parse_table = create_parsing_table(firstX, followX, grammar)
    pass


def create_parsing_table(firstX, followX, grammar):
    parse_table = {}

    terminals = grammar['terminals']
    non_terminals = grammar['nonterminals']

    for terminal in terminals:
        index = (terminal, terminal)
        parse_table[index] = get_pop_method()

    for terminal in terminals:
        for non_terminal in non_terminals:
            index = (terminal, non_terminal)
            parse_table[index] = firstX[non_terminal]

    for non_terminal in non_terminals:
        index = (non_terminal, '$')

    return parse_table


def get_pop_method():
    return 'pop'
