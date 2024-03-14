interface swatResult {
  seqsA: string[];
  seqsB: string[];
  scores: number[];
  identities: number[];
}

const GAP_SYMBOL = "_";

function smithWaterman(
  seqA: string,
  seqB: string,
  match: number,
  mismatch: number,
  gap: number
): swatResult {
  const rows: number = seqB.length + 1;
  const columns: number = seqA.length + 1;
  const matrix: number[][] = Array(rows)
    .fill(0)
    .map(() => Array(columns).fill(0));

  let maxScore = -1;

  for (let i = 1; i < rows; i++) {
    for (let j = 1; j < columns; j++) {
      matrix[i][j] = Math.max(
        matrix[i - 1][j - 1] + (seqB[i - 1] === seqA[j - 1] ? match : mismatch),
        matrix[i - 1][j] + gap,
        matrix[i][j - 1] + gap,
        0
      );

      if (matrix[i][j] > maxScore) {
        maxScore = matrix[i][j];
      }
    }
  }

  let bestScores: number[][] = [];

  for (let i = 1; i < rows; i++) {
    for (let j = 1; j < columns; j++) {
      if (matrix[i][j] === maxScore) {
        bestScores.push([i, j]);
      }
    }
  }

  let seqAarr: string[] = [];
  let seqBarr: string[] = [];

  while (bestScores.length > 0) {
    let [i, j] = bestScores[bestScores.length - 1];

    let strA = "";
    let strB = "";

    while (i > 0 || j > 0) {
      if (matrix[i][j] === 0) {
        break;
      }

      const left = matrix[i][j - 1];
      const diagonal = matrix[i - 1][j - 1];
      const above = matrix[i - 1][j];

      const maxCell = Math.max(diagonal, left, above);

      if (seqA[j - 1] === seqB[i - 1] || maxCell === diagonal) {
        strA = seqA[j - 1] + strA;
        strB = seqB[i - 1] + strB;
        i--;
        j--;
      } else if (maxCell === left) {
        strA = seqA[j - 1] + strA;
        strB = GAP_SYMBOL + strB;
        j--;
      } else {
        strA = GAP_SYMBOL + strA;
        strB = seqB[i - 1] + strB;
        i--;
      }
    }

    seqAarr.push(strA);
    seqBarr.push(strB);
    bestScores.pop();
  }

  let scores: number[] = [];
  let identities: number[] = [];

  seqAarr.forEach((arr, index) => {
    let score = 0;
    let matchCounter = 0;

    for (let i = 0; i < arr.length; i++) {
      if (seqAarr[index][i] === seqBarr[index][i]) {
        score += match;
        matchCounter++;
      } else if (
        seqAarr[index][i] === GAP_SYMBOL ||
        seqBarr[index][i] === GAP_SYMBOL
      ) {
        score += gap;
      } else if (seqAarr[index][i] !== seqBarr[index][i]) {
        score += mismatch;
      }
    }

    scores.push(score);
    identities.push(matchCounter > 0 ? matchCounter / arr.length : 0);
  });

  return {
    seqsA: seqAarr,
    seqsB: seqBarr,
    scores: scores,
    identities: identities,
  };
}

const seqA =
  "MTENSTSTPAAKPKRAKASKKSTDHPKYSDMIVAAIQAEKNRAGSSRQSIQKYIKSHYKVGENADSQIKLSIKRLVTTGVLKQTKGVGASGSFRLAKSDEPKRSVAFKKTKKEVKKVATPKKAAKPKKAASKAPSKKPKATPVKKAKKKPAATPKKTKKPKTVKAKPVKASKPKKTKPVKPKAKSSAKRTGKKK";
const seqB =
  "MSETAPVPQPASVAPEKPAATKKTRKPAKAAVPRKKPAGPSVSELIVQAVSSSKERSGVSLAALKKSLAAAGYDVEKNNSRIKLGLKSLVNKGTLVQTKGTGAAGSFKLNKKAESKASTTKVTVKAKASGAAKKPKKTAGAAAKKTVKTPKKPKKPAVSKKTSSKSPKKPKVVKAKKVAKSPAKAKAVKPKAAKVKVTKPKTPAKPKKAAPKKK";

console.log(smithWaterman(seqA, seqB, 1, -1, -2));
