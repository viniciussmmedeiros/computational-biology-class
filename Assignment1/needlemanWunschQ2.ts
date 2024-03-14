interface nwResult {
  seqA: string;
  seqB: string;
  score: number;
  identity: number;
}

const GAP_SYMBOL = "_";

function needlemanWunsh(
  seqA: string,
  seqB: string,
  match: number,
  mismatch: number,
  gap: number
): nwResult {
  const rows: number = seqB.length + 1;
  const columns: number = seqA.length + 1;
  const matrix: number[][] = Array(rows)
    .fill(0)
    .map(() => Array(columns).fill(0));

  matrix[0].forEach((_, i) => (matrix[0][i] = gap * i));
  matrix.forEach((_, i) => (matrix[i][0] = gap * i));

  for (let i = 1; i < rows; i++) {
    for (let j = 1; j < columns; j++) {
      matrix[i][j] = Math.max(
        matrix[i - 1][j - 1] + (seqB[i - 1] === seqA[j - 1] ? match : mismatch),
        matrix[i - 1][j] + gap,
        matrix[i][j - 1] + gap
      );
    }
  }

  let strA = "";
  let strB = "";
  let i = rows - 1;
  let j = columns - 1;

  while (i > 0 || j > 0) {
    const matchMismatch = seqB[i - 1] === seqA[j - 1] ? match : mismatch;

    if (
      i > 0 &&
      j > 0 &&
      matrix[i][j] === matrix[i - 1][j - 1] + matchMismatch
    ) {
      strA = seqA[j - 1] + strA;
      strB = seqB[i - 1] + strB;
      i--;
      j--;
    } else if (i > 0 && matrix[i][j] === matrix[i - 1][j] + gap) {
      strA = GAP_SYMBOL + strA;
      strB = seqB[i - 1] + strB;
      i--;
    } else {
      strA = seqA[j - 1] + strA;
      strB = GAP_SYMBOL + strB;
      j--;
    }
  }

  let score = 0;
  let matchCounter = 0;

  for (let i = 0; i < strA.length; i++) {
    if (strA[i] === strB[i]) {
      score += match;
      matchCounter++;
    } else if (strA[i] === GAP_SYMBOL || strB[i] === GAP_SYMBOL) {
      score += gap;
    } else if (strA[i] !== strB[i]) {
      score += mismatch;
    }
  }

  return {
    seqA: strA,
    seqB: strB,
    score: score,
    identity: matchCounter > 0 ? matchCounter / strA.length : 0,
  };
}

const seqA = "AGGTCTCA";
const seqB = "GGCCA";

console.log(needlemanWunsh(seqA, seqB, 7, -3, -4));
