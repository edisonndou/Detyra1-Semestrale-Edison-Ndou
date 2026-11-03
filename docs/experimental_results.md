# Rezultatet eksperimentale

Koha e regjistrimit (UTC): 2026-10-24T11:02:35.734305+00:00

Python 3.12.14; Windows-11-10.0.26300-SP0.

Kufijtë për rast: 3 s, 200000 nyje, front 50000, thellësi 100.
Tracemalloc aktiv; një ekzekutim për rast. Matjet nuk përfshijnë renderimin e figurave.

| Rasti | Statusi | Koha (s) | Zgjeruar | Gjeneruar | Fronti max | Thellësia | Kthime | Memoria Python (KiB) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| golfers-2x2-3w | solved | 0.000286 | 4 | 5 | 5 | 4 | 0 | 9.0 |
| golfers-8x4-2w | solved | 0.014505 | 8 | 9 | 9 | 8 | 0 | 38.2 |
| golfers-8x4-10w | limit | 3.000018 | 3960 | 3960 | 33 | 32 | 3929 | 456.2 |
| sudoku-easy | solved | 0.009635 | 51 | 52 | 1 | 51 | 0 | 50.6 |
| sudoku-medium | solved | 0.008789 | 49 | 50 | 1 | 49 | 0 | 48.6 |
| sudoku-hard | solved | 0.423476 | 2231 | 2232 | 93 | 58 | 0 | 1732.2 |
| latin-3 | solved | 0.001267 | 49 | 60 | 10 | 9 | 50 | 21.1 |
| latin-4 | solved | 0.005405 | 261 | 308 | 17 | 16 | 291 | 32.4 |
| latin-5 | solved | 0.131869 | 5848 | 6761 | 26 | 25 | 6735 | 42.7 |
| puzzle-bfs | solved | 0.000425 | 8 | 23 | 8 | 2 | 0 | 7.4 |
| puzzle-dfs | solved | 0.000598 | 30 | 48 | 31 | 30 | 0 | 30.6 |
| puzzle-iddfs | solved | 0.000306 | 4 | 15 | 3 | 2 | 10 | 6.4 |
| missionaries-bfs | solved | 0.000367 | 14 | 31 | 3 | 11 | 0 | 11.6 |
| missionaries-dfs | solved | 0.000371 | 12 | 19 | 12 | 11 | 1 | 12.1 |
| workforce-dfs | optimal | 0.007590 | 14 | 72 | 58 | 14 | 0 | 41.5 |

Numëruesit e refuzimeve, kufijtë e IDDFS dhe objektivi janë në CSV/JSON.

- Social Golfers: DFS gjen orarin 2-javor; prova DFS 10-javore mund të ndërpritet nga kufijtë. Veçmas, dëshmia e botuar e validuar provon maksimumin 10; shiko golfers-optimality.json. Nuk i atribuohen metrika kërkimi certifikatës.
- Sudoku: tri zgjidhje valide; renditja e kohës nuk është certifikim i vështirësisë njerëzore.
- Latin Square: gjurmët regjistrojnë çdo kufi deri n², për n=3,4,5.
- 8-Puzzle: BFS/IDDFS japin 2 hapa për input-in standard; DFS mund të japë rrugë më të gjatë.
- Misionarët: BFS jep 11 kalime, të kontrolluara nga validuesi dhe testet.
- Punonjësit: objektivi bazë 34 është kufiri i shpërndarjes së 14 punëve mes 6 punonjësve (4×2²+2×3²).

[Të dhënat CSV](../outputs/results/benchmarks.csv) · [JSON me mjedisin dhe kufijtë](../outputs/results/benchmarks.json)

![Kohët dhe zgjerimet e matura](../outputs/results/performance.png)
