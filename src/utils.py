# The purpose of this module is to export whatever re-usable components one may use in whatever ways.

# Flatten a list twice -> [[[]]] turns into [].
def flatten2(flattenableList):
  return sum(sum(flattenableList, []), [])
