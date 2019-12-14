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

# Rules to compute FIRST set:
#
# If x is a terminal, then FIRST(x) = { ‘x’ }
# If X-> Є, is a production rule, then add Є to FIRST(X).
# If X->Y1 Y2 Y3...Yn is a production,
#     FIRST(X) = FIRST(Y1)
#     If FIRST(Y1) contains Є then FIRST(X) = { FIRST(Y1) – Є } U { FIRST(Y2) }
#     If FIRST (Yi) contains Є for all i = 1 to n, then add Є to FIRST(X).

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

# If a Non-Terminal on the R.H.S. of any production is followed immediately by a Terminal,
#   then it can immediately be included in the Follow set of that Non-Terminal.
# If a Non-Terminal on the R.H.S. of any production is followed immediately by a Non-Terminal,
#   then the First Set of that new Non-Terminal gets included on the follow set of our original Non-Terminal.
#   In case encountered an epsilon, then move on to the next symbol in the production.
# Note : ε is never included in the Follow set of any Non-Terminal.
# If reached the end of a production while calculating follow,
#   then the Follow set of that non-teminal will include the Follow set of the Non-Terminal
#   on the L.H.S. of that production. This can easily be implemented by recursion.

# Given a grammar and the First(X) set, construct the Follow(X) set.
def computeFollowXSet(enrichedGrammar, firstXTable):
  productions = enrichedGrammar['productions']
  startSymbol = enrichedGrammar['startSymbol']
  nonterminals = enrichedGrammar['nonterminals']
  terminals = enrichedGrammar['terminals']

  followXTable = {}
  followXTable[startSymbol] = set(["$"])

  for production in productions:
    lastIndex = len(production) - 1

    for symbolIndex in range(lastIndex + 1):
      pass
