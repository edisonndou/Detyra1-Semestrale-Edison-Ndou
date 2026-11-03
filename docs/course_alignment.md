# Përputhja me dokumentin e lëndës dhe përgatitja për mbrojtje

Dokumenti i dërguar përmban programin e përgjithshëm të ushtrimeve, pastaj
**Detyrën e parë semestrale: Teknikat e painformuara të kërkimit** dhe specifikimin teknik.
Ky projekt realizon katër pjesët e detyrës: Social Golfers, Sudoku, Latin Square dhe
pemët për 8-Puzzle, Misionarët/Kanibalët dhe planifikimin e punonjësve.
Temat e tjera të kursit (A*, algoritmet gjenetike, GSAT, lojërat etj.) janë rezultate mësimore
të mëvonshme të lëndës; nuk kërkohen si implementime të detyrës së parë.

## Literatura dhe botimet

Dokumenti i lëndës përmend AIMA, **botimi i tretë**, sidomos kapitujt 1, 3, 4, 5 dhe 6.
Në raport përdoret kapitulli 3 për kërkimin dhe kapitulli 6 për CSP në këtë botim.
Burimet bibliografike të botimit të tretë jepen në
[faqen e autorëve për botimet](https://aima.eecs.berkeley.edu/translations.html).
Michalewicz dhe Fogel, *How to Solve It: Modern Heuristics*, botimi 2, Springer, 2004,
mbulon konceptet bazë dhe metodat tradicionale; shiko
[botimin te Springer](https://link.springer.com/book/10.1007/978-3-662-07807-5).
Nuk pretendohet lexim i materialeve të mbyllura të edX ose i slajdeve që nuk janë dhënë.

## Hapësira e kërkimit varet nga përfaqësimi

| Problemi / përfaqësimi | Caktimet bruto | Çfarë përjashtohet më vonë |
|---|---|---|
| SAT me v variabla binare | 2^v | Caktimet që nuk kënaqin formulën |
| TSP simetrik me n qytete, qytet fillestar fiks dhe drejtim i paetiketuar | (n−1)!/2 për n≥3 | Kufizime shtesë të itinerarit; në graf jo të plotë, lidhjet që mungojnë |
| Ngjyrosje grafi me k ngjyra dhe v kulme | k^v | Fqinjët me ngjyrë të njëjtë |
| Sudoku me 81 qeliza, pa të dhëna | 9^81 | Përsëritjet në rreshta, kolona dhe kuti |
| N-Queens, një mbretëreshë për rresht | n^n | Konfliktet e kolonave dhe diagonaleve |
| N-Queens me kolonat gjithashtu si permutim | n! | Konfliktet e diagonaleve |
| Latin Square | n^(n²) | Kufizimet e rreshtave dhe kolonave |

Këto janë hapësira caktimesh bruto, jo numra zgjidhjesh valide. Në TSP asimetrik nuk
pjesëtohet me 2. Për Social Golfers përdoret n!/((p!)^g g!) për një javë pa etiketa grupesh.

## Pemë e plotë dhe numri i saktë i nyjeve

Në një pemë të plotë me b fëmijë për nyje dhe thellësi D (rrënja në 0), numri i nyjeve është

**N(b,D)=Σ(i=0..D)b^i=(b^(D+1)−1)/(b−1)**, për b≠1; për b=1 është D+1.

Nëse qëllimi mungon dhe nuk ka cikle/krasitje, DFS dhe BFS vizitojnë të gjitha N nyjet.
“Vizituar” këtu numëron edhe gjethet e nxjerra nga fronti; në kod `expanded` përfshin gjethet
kur hapet gjeneratori i tyre bosh, por nuk përfshin nyje të ndalura nga kufiri i thellësisë.

Për IDDFS deri D, numri i vizitave, duke numëruar përsëritjet, është

**I(b,D)=Σ(L=0..D)Σ(i=0..L)b^i=Σ(i=0..D)(D−i+1)b^i**.

Për b=2 dhe D=3, DFS/BFS vizitojnë 1+2+4+8=15 nyje.
IDDFS viziton 1+3+7+15=26 nyje gjithsej. Për b=1, kjo shumë është (D+1)(D+2)/2.
Këto janë numra të saktë për pemën e deklaruar, jo për çdo Sudoku ose orar të krasitur.
Për degëzim jo uniform përdoret numri real N_i i nyjeve në nivelin i:
N=ΣN_i dhe I=Σ(D−i+1)N_i, kur çdo iteracion i përshkon plotësisht nivelet përkatëse.

Shembulli i plotë me 15 nyje eksportohet në `outputs/search_trees/complete-binary-depth3`
si DOT, PNG dhe SVG. Ka vetëm 4 nivele, prandaj mund të shfaqet i plotë brenda kufijve.
Pemët e instancave të mëdha janë të kufizuara dhe etiketohen si të tilla.

## Përparësitë dhe dobësitë

| Metoda | Përparësia | Dobësia |
|---|---|---|
| DFS | Pak korniza aktive; mund të gjejë shpejt një zgjidhje të thellë | Varet nga renditja; nuk garanton rrugë minimale; pa kufij mund të ngecë në degë të pafundme |
| BFS | Plotësi në degëzim të fundëm dhe rrugë minimale për kosto njësi | Fronti dhe gjendjet e vizituara mund të konsumojnë shumë memorie |
| IDDFS | Thellësi minimale me memorie të rrugës aktive | Përsërit prefikset; degëzimi 1 e bën koston kumulative kuadratike |

Hard constraints përcaktojnë vlefshmërinë. Soft constraints matin cilësinë mes zgjidhjeve
valide. Objective function përcakton çfarë minimizohet/maksimizohet; evaluation function
vlerëson një gjendje/kandidat gjatë punës. Në kërkimin e painformuar këtu nuk përdoret
një heuristikë A*. MRV zgjedh variablin në CSP, ndërsa FIFO/stiva përcakton përshkimin.

## Vërejtje për shembujt e transkriptuar në dokument

Rreshti i shembullit Social Golfers në tekstin e dhënë përmban vetëm 7 grupe; origjinali i
Aguado-s ka edhe grupin (16,17,18,19). Tabela lokale e plotë ruan të 8 grupet dhe validohet.
Shembulli i shtypur Latin Square për n=5 ka vetëm 4 rreshta në tekst; programi prodhon dhe
validon të pesë rreshtat. Këto mungesa në shembuj nuk janë kufizime të reja të problemit.
