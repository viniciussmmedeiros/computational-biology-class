import os
from typing import NamedTuple

GAP_SYMBOL = "_"

class NWResult(NamedTuple):
  seqA: str
  seqB: str
  score: int
  identity: float

def needleman_wunsch(seqA, seqB, match, mismatch, gap):
  rows = len(seqB) + 1
  columns = len(seqA) + 1
  matrix = [[0 for _ in range(columns)] for _ in range(rows)]

  for i in range(columns):
      matrix[0][i] = gap * i
  for i in range(rows):
      matrix[i][0] = gap * i

  for i in range(1, rows):
      for j in range(1, columns):
          match_mismatch = match if seqB[i - 1] == seqA[j - 1] else mismatch
          matrix[i][j] = max(
              matrix[i - 1][j - 1] + match_mismatch,
              matrix[i - 1][j] + gap,
              matrix[i][j - 1] + gap
          )

  strA = ""
  strB = ""
  i = rows - 1
  j = columns - 1

  while i > 0 or j > 0:
      match_mismatch = match if seqB[i - 1] == seqA[j - 1] else mismatch

      if i > 0 and j > 0 and matrix[i][j] == matrix[i - 1][j - 1] + match_mismatch:
          strA = seqA[j - 1] + strA
          strB = seqB[i - 1] + strB
          i -= 1
          j -= 1
      elif i > 0 and matrix[i][j] == matrix[i - 1][j] + gap:
          strA = GAP_SYMBOL + strA
          strB = seqB[i - 1] + strB
          i -= 1
      else:
          strA = seqA[j - 1] + strA
          strB = GAP_SYMBOL + strB
          j -= 1

  score = 0
  match_counter = 0

  for i in range(len(strA)):
      if strA[i] == strB[i]:
          score += mismatch
          # score += match --> invertido
          match_counter += 1
      elif strA[i] == GAP_SYMBOL or strB[i] == GAP_SYMBOL:
          score += gap
      elif strA[i] != strB[i]:
          score += match
          # score += mismatch --> invertido

  identity = match_counter / len(strA) if match_counter > 0 else 0

  return NWResult(seqA=strA, seqB=strB, score=score, identity=identity)

def iterator_needleman_wunsch():
  path = './q2/dataset2/fasta'
  folder = os.listdir(path)
  folder.sort()
  print(folder)

  for i in range(len(folder)):
    for j in range(len(folder)):
      if folder[i] != folder[j]:
        seq1 = open(f"{path}/{folder[i]}", "r").read()
        seq2 = open(f"{path}/{folder[j]}", "r").read()
        result = needleman_wunsch(seq1, seq2, 1, -1, -2)
        print(f"{folder[i]} vs {folder[j]}: {result.score}")
    print("\n")

iterator_needleman_wunsch()