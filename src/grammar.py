import utils

# The purpose of this module is to provide helpers for dealing with the input grammar.
# E.g. generate a parsing table, enrich the read grammar, etc.

# This constructs a more detailed object from the input grammar,
# e.g. generate a set of all the nonterminals for easier verification in later parts of the program.
# This doesn't perform validation.
def addDetails(inGrammar):
  nonterminals = set(inGrammar['productions'].keys())

  terminals = set(utils.flatten2(inGrammar['productions'].values()))

  for nonterminal in nonterminals:
    terminals.remove(nonterminal)

  terminals.remove(epsilon())

  enrichedGrammar = {
    'startSymbol': inGrammar['startSymbol'],
    'productions': inGrammar['productions'],
    'nonterminals': nonterminals,
    'terminals': terminals
  }

  return enrichedGrammar

# Denotes the empty sequence.
def epsilon():
  return 'ε'

# Creates the parsing table for this LL(1) grammar (if this isn't LL(1), then this throws an exception.)
def createParsingTableLL1(enrichedGrammar):
  firstX = computeFirstXSet(enrichedGrammar)
  followX = computeFollowXSet(enrichedGrammar, firstX)

  return (firstX, followX)

# Computes the First(X) set for the grammar.
def computeFirstXSet(enrichedGrammar):
  nonterminals = enrichedGrammar['nonterminals']
  productions = enrichedGrammar['productions']
  terminals = enrichedGrammar['terminals']

  firstXTable = {}

  for terminal in terminals:
    firstXTable[terminal] = set([terminal])

  for nonterminal in nonterminals:
    computeFirstXForNonTerminal(nonterminal, firstXTable, enrichedGrammar)

  return firstXTable

# Helper for computeFirstXSet
def computeFirstXForNonTerminal(nonterminal, firstXTable, enrichedGrammar):
  if nonterminal in firstXTable:
    return

  productions = enrichedGrammar['productions'][nonterminal]
  firstX = set()

  for production in productions:
    if len(production) == 0:
      raise Exception('Nonterminal "' + str(nonterminal) + '" does not have a right-handside.')

    if len(production) == 1 and production[0] == epsilon():
      firstX.add(epsilon())
    else:
      computeFirstXForNonTerminal(production[0], firstXTable, enrichedGrammar)

      hasEpsilon = False

      for terminal in firstXTable[production[0]]:
        if terminal == epsilon():
          hasEpsilon = True
        else:
          firstX.add(terminal)

      if hasEpsilon:
        for nonterminal in production[1:]:
          computeFirstXForNonTerminal(nonterminal, firstXTable, enrichedGrammar)

          hasEpsilon = False
          for terminal in firstXTable[nonterminal]:
            if terminal == epsilon():
              hasEpsilon = True
            else:
              firstX.add(terminal)

          if not hasEpsilon:
            break

      if hasEpsilon:
        firstX.add(epsilon())

  firstXTable[nonterminal] = firstX

# Given a grammar and the First(X) set, construct the Follow(X) set.
def computeFollowXSet(enrichedGrammar, firstXTable):
  productions = enrichedGrammar['productions']
  startSymbol = enrichedGrammar['startSymbol']
  nonterminals = enrichedGrammar['nonterminals']
  terminals = enrichedGrammar['terminals']

  followXTable = {}

  for nonterminal in nonterminals:
    followXTable[nonterminal] = set()

  followXTable[startSymbol].add("$")

  hasChanged = True

  while hasChanged:
    hasChanged = False

    for nonterminal in productions.keys():
      for production in productions[nonterminal]:
        lastIndex = len(production) - 1

        for symbolIndex in range(lastIndex + 1):
          symbol = production[symbolIndex]

          if symbol in nonterminals:
            if symbolIndex == lastIndex:
              hasChanged = addAllIntoFromExceptEpsilon(followXTable[symbol], followXTable[nonterminal], hasChanged)
              hasChanged = addAllIntoFromExceptEpsilon(followXTable[nonterminal], followXTable[symbol], hasChanged)
            else:
              foundNonEpsilon = False

              for followingIndex in range(symbolIndex + 1, lastIndex + 1):
                followingSymbol = production[followingIndex]

                hasChanged = addAllIntoFromExceptEpsilon(followXTable[symbol], firstXTable[followingSymbol], hasChanged)

                if epsilon() not in followXTable[symbol]:
                  foundNonEpsilon = True
                  break

                followXTable[symbol].remove(epsilon())
              
              if not foundNonEpsilon:
                hasChanged = addAllIntoFromExceptEpsilon(followXTable[symbol], followXTable[nonterminal], hasChanged)

  return followXTable

def addAllIntoFromExceptEpsilon(addInto, addFrom, hasChanged):
  changed = False

  for item in addFrom:
    if item not in addInto:
      changed = changed or item is not epsilon()
      addInto.add(item)

  return hasChanged or changed
