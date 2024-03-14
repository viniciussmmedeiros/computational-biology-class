from newick import loads

def printMatriz(matriz):
  for i in range(len(matriz)):
    for j in range(len(matriz[i])):
      if matriz[i][j] is not None:
        print(matriz[i][j], end=' ')
    print()

def upgma(matriz):
  newickTree = ""
  while len(matriz) > 3:
    menor = float('inf')
    smallerValuesList = []

    for i in range(1, len(matriz)):
      for j in range(1, len(matriz[i])):
        if matriz[i][j] < menor and matriz[i][j] != 0:
          menor = matriz[i][j]
    
    for i in range(1, len(matriz)):
      for j in range(1, len(matriz[i])):
        if matriz[i][j] == menor:
          smallerValuesList.append([i, j])

    smallestValues = []
    for sublist in smallerValuesList:
        sublist.sort() 
        if all(sublist != outra_lista or sorted(sublist) != sorted(outra_lista) for outra_lista in smallestValues):
            smallestValues.append(sublist)

    for smallestValue in smallestValues:
      for i in range(1, len(matriz)):
        if matriz[i][0] != matriz[smallestValue[0]][0] and matriz[i][0] != matriz[smallestValue[1]][0]:
          dist_A = matriz[i][smallestValue[0]]
          dist_B = matriz[i][smallestValue[1]]

          new_distance = (dist_A + dist_B) / 2
          
          matriz[i][smallestValue[0]] = new_distance
          matriz[i][smallestValue[1]] = new_distance
          matriz[smallestValue[0]][i] = new_distance
          matriz[smallestValue[1]][i] = new_distance

    parX = matriz[smallestValues[0][0]][0]
    parY = matriz[smallestValues[0][1]][0]

    matriz[0][smallestValues[0][0]] = f"{parX}/{parY}"
    matriz[smallestValues[0][0]][0] = f"{parX}/{parY}"

    if len(newickTree) == 0:
      newickTree = f"('{parX}', '{parY}')"
    elif "/" not in parX:
      newickTree = f"({newickTree}, ('{parX}', '{parY}'))"
    elif "/" in parX and parX.count('/') > 1 and "/" not in parY:
      newickTree = f"({newickTree}, {parY})"
    elif "/" in parX and "/" not in parY:
      newickTree = newickTree.replace(f"('{parX[0]}', '{parX[2]}')", f"(({parX[0]}, {parX[2]}), {parY})")

    for i in range(0, len(matriz)):
      del matriz[i][smallestValues[0][1]]
    del matriz[smallestValues[0][1]]
    print('Matriz')
    printMatriz(matriz)

  print(newickTree)
  print(loads(newickTree)[0].ascii_art())

# matriz1 = [
#   ['#', 'L. braziliensis', 'T. rangeli', 'T. cruzi', 'T. gambiae'],
#   ['L. braziliensis', 0.000, 0.010, 0.300, 0.280],
#   ['T. rangeli', 0.010, 0.000, 0.280, 0.270],
#   ['T. cruzi', 0.300, 0.280, 0.000, 0.015],
#   ['T. gambiae', 0.280, 0.270, 0.015, 0.000]
# ]

# upgma(matriz1)

# matriz dataset 1
# ----- seq_1 seq_2 seq_3 seq_4 seq_5 seq_6 seq_7 seq_8 seq_9 seq_10
# seq_1   0    -36   -13    -8   -15   -23   -11   -54   -14    -9
# seq_2  -36     0   -28     8   -15    -7   -10   -36    12   -27
# seq_3  -13   -28     0   -14   -16   -11   -12   -14   -28   -34
# seq_4  -8     8    -14     0   -11   -37   -10   -20   -24   -27
# seq_5  -15   -15   -16   -11     0   -34   -32   -23   -20   -13
# seq_6  -23   -7    -11   -37   -34     0   -36    -7   -27   -17
# seq_7  -11   -10   -12   -10   -32   -36     0   -29   -32   -26
# seq_8  -54   -36   -14   -20   -23    -7   -29     0    -7   -16
# seq_9  -14    12   -28   -24   -20   -27   -32    -7     0   -17
# seq_10 -9    -27   -34   -27   -13   -17   -26   -16   -17     0


# matrizDataSet1 = [
#   ['#', 'seq_1', 'seq_2', 'seq_3', 'seq_4', 'seq_5', 'seq_6', 'seq_7', 'seq_8', 'seq_9', 'seq_10'],
#   ['seq_1', 0, -36, -13, -8, -15, -23, -11, -54, -14, -9],
#   ['seq_2', -36, 0, -28, 8, -15, -7, -10, -36, 12, -27],
#   ['seq_3', -13, -28, 0, -14, -16, -11, -12, -14, -28, -34],
#   ['seq_4', -8, 8, -14, 0, -11, -37, -10, -20, -24, -27],
#   ['seq_5', -15, -15, -16, -11, 0, -34, -32, -23, -20, -13],
#   ['seq_6', -23, -7, -11, -37, -34, 0, -36, -7, -27, -17],
#   ['seq_7', -11, -10, -12, -10, -32, -36, 0, -29, -32, -26],
#   ['seq_8', -54, -36, -14, -20, -23, -7, -29, 0, -7, -16],
#   ['seq_9', -14, 12, -28, -24, -20, -27, -32, -7, 0, -17],
#   ['seq_10', -9, -27, -34, -27, -13, -17, -26, -16, -17, 0]
# ]

# upgma(matrizDataSet1)

# matriz dataset 2
# ----- seq_1 seq_2 seq_3 seq_4 seq_5 seq_6 seq_7 seq_8 seq_9 seq_10
# seq_1   0     -6    -25   -7    -7    -11   1     4     5     -45
# seq_2  -6      0    -21    3    -49   -24  -41    4    -22    -17
# seq_3  -25    -21    0    -10   -29   -16  -18    0    -26    -5
# seq_4  -7      3    -10    0    -17   -22  -23   -17   -16    -11
# seq_5  -7     -49   -29   -17    0    -39  -26   -14   -28    -16
# seq_6  -11    -24   -16   -22   -39    0   -14   -6    -8     -17
# seq_7   1     -41   -18   -23   -26   -14    0   -6    -25    -25
# seq_8   4      4     0    -17   -14   -22   -6     0    18    -18
# seq_9   5     -22   -26   -16   -28   -8   -25    18    0     -19
# seq_10  -45   -17    -5   -11   -16   -1   -25   -18   -19     0

# matrizDataSet2 = [
#   ['#', 'seq_1', 'seq_2', 'seq_3', 'seq_4', 'seq_5', 'seq_6', 'seq_7', 'seq_8', 'seq_9', 'seq_10'],
#   ['seq_1', 0, -6, -25, -7, -7, -11, 1, 4, 5, -45],
#   ['seq_2', -6, 0, -21, 3, -49, -24, -41, 4, -22, -17],
#   ['seq_3', -25, -21, 0, -10, -29, -16, -18, 0, -26, -5],
#   ['seq_4', -7, 3, -10, 0, -17, -22, -23, -17, -16, -11],
#   ['seq_5', -7, -49, -29, -17, 0, -39, -26, -14, -28, -16],
#   ['seq_6', -11, -24, -16, -22, -39, 0, -14, -6, -8, -17],
#   ['seq_7', 1, -41, -18, -23, -26, -14, 0, -6, -25, -25],
#   ['seq_8', 4, 4, 0, -17, -14, -22, -6, 0, 18, -18],
#   ['seq_9', 5, -22, -26, -16, -28, -8, -25, 18, 0, -19],
#   ['seq_10', -45, -17, -5, -11, -16, -1, -25, -18, -19, 0]
# ]

# upgma(matrizDataSet2)