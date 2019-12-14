import reader
import grammar
import parser

# The purose of this module is to wrap all the other modules together and provide the actual program
# that provides a result.

inFile = 'input.grammar.json'

inGrammar = reader.readAll(inFile)

print('Successfully read input grammar from ' + inFile + '.')
print('This is the parsed grammar: ' + str(inGrammar) + '.')

annotatedGrammar = grammar.addDetails(inGrammar)

print('Generated an enriched grammar from the input grammar: ' + str(annotatedGrammar) + '.')

parsingTable = grammar.createParsingTableLL1(annotatedGrammar)

print('Generated a parsing table from the input grammar: ' + str(parsingTable) + '.')
