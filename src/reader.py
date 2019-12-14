import json

# The objective of this module is to deal with serialization and deserialization of the input grammar.

# Reads the specified grammar into an understandable format (this is a json).
# See the example input file to figure out how this works.
def readAll(inputFile):
  with open(inputFile) as file:
    fileContent = file.read()
    return json.loads(fileContent)
  raise Exception('Could not load input from "' + inputFile + '" for some reason.')
