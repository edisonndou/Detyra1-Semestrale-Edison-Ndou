# Analiza e kompleksitetit dhe matjeve

Le të jetë b një kufi i degëzimit, d thellësia e zgjidhjes më të cekët,
m kufiri i thellësisë, V numri i gjendjeve dhe E numri i lidhjeve të grafit të arritshëm.
Kufijtë më poshtë numërojnë nyje; kontrolli i kufizimeve, gjenerimi dhe kopjimi i një gjendjeje
kanë kosto shtesë sipas problemit. Në kod nuk ka një formulë universale të saktë për kohën.

| Metoda | Koha teorike në pemë | Memoria e kërkimit | Garancia |
|---|---|---|---|
| BFS | O(b^(d+1)) me testin e qëllimit në dalje | O(b^(d+1)) | Rrugë minimale për kosto njësi |
| DFS/DLS | O(b^m) | O(m) korniza me gjeneratorë dembelë | Pa garanci për rrugë minimale |
| IDDFS | O(b^d), për b>1 konstant | O(d) korniza aktive | Thellësi minimale për kosto njësi |
| DFS branch-and-bound | Eksponenciale në rastin më të keq | Deri O(bm) gjendje në stivën konkrete | Optimalitet vetëm pas shterimit/krasitjes së sigurt |

BFS mund të gjenerojë fëmijë të nivelit d+1 përpara nxjerrjes së qëllimit në nivelin d,
prandaj këtu shënohet forma konservative b^(d+1). Për problemet me thellësi të plotë fikse
k, si Sudoku, nuk ka fëmijë përtej k dhe përdoret O(9^k).
Për graf të fundëm me vizitim global, BFS dhe DFS kanë O(V+E) kohë dhe O(V) memorie vizitimi,
duke supozuar gjenerim dhe hashing me kosto konstante. Gjendjet dhe tuple-t e gjata e shtojnë koston reale.

## Pse IDDFS përsërit punë

Në kufirin L, kërkimi nis sërish nga rrënja dhe përshkon prefikset deri L.
Numri i vizitave deri d është afërsisht shuma për i=0..d e (d−i+1)b^i në një pemë të plotë.
Kur b>1, nivelet e fundit dominojnë dhe rendi mbetet O(b^d); kur b=1, përsëritja bëhet O(d²).
Normalizimi i katrorëve Latinë krijon prefikse të gjata me degëzim 1, ndaj përmirësimi praktik
nuk përmblidhet nga një b mesatar i zgjedhur arbitrarisht. Kodi regjistron çdo kufi që ekzekuton.

## Kërkim në graf kundrejt kërkimit në pemë

Një nyje peme përfaqëson një rrugë; dy nyje mund të përmbajnë të njëjtën gjendje.
Grafi bashkon gjendjet e barabarta. BFS ruan `parents` si tabelë vizitimi dhe rindërton rrugën.
DFS bazë përdor një set të rrugës aktive: shmang ciklet, por mund të eksplorojë të njëjtën gjendje
nga rrugë të ndryshme. DFS grafik i 8-Puzzle dhe Misionarëve ruan gjithashtu një set global.
Me thellësi të kufizuar, një DFS me vizitim global mund të takojë fillimisht një gjendje përmes
një rruge më të gjatë; prandaj një rezultat `cutoff` mbetet jokonkluziv, jo provë e pamundësisë.
IDDFS nuk bart një tabelë globale ndërmjet limiteve: kjo do të eliminonte kërkimet e kërkuara.

## Kuptimi i metrikave konkrete

- `generated`: rrënja plus pasardhësit që algoritmi merr nga gjeneratori, përfshirë dublikatat;
  në IDDFS përfshihen rrënjët e përsëritura. Në ndërprerje mund të jetë një mbi kufirin.
- `expanded`: gjendje për të cilat hapet gjeneratori i pasardhësve; qëllimi nuk zgjerohet.
- `rejected`: kandidatë të refuzuar nga domeni, cikle/dublikata dhe krasitje nga kufiri i kostos.
  Nuk është metrikë identike mes problemeve: te Sudoku numërohen vlerat e palejueshme të qelizës
  së zgjedhur; domeni bosh shton 9. Te golfistët numërohen grupet e refuzuara për çifte.
- `backtracks`: korniza të DFS që hiqen pas një dege të përfunduar; përfshin kthime nga thellësia
  e kufizuar. Te branch-and-bound numërohen fundet e degëve pa fëmijë; BFS ka 0 kthime stive.
- `max_frontier`: madhësia e radhës për BFS, kornizat aktive për DFS/DLS/IDDFS,
  ose madhësia e stivës së kandidatëve për optimizimin. Nuk krahasohet si bajt mes algoritmeve.
- `max_depth`: thellësia më e madhe e një gjendjeje të përpunuar, me rrënjën në 0.
- `max_recursion_depth`: 0 për këto algoritme, sepse përdorin stiva eksplicite dhe nuk bëjnë
  thirrje rekursive Python. Thellësia logjike e kërkimit jepet veçmas nga `max_depth`.
- `elapsed_seconds`: `perf_counter` rreth kërkimit, pa eksportim figurash, por me gjenerim dhe gjurmim.
  Validimi final kryhet pas kësaj matjeje.
- `peak_traced_bytes`: maksimumi i alokimeve Python që sheh tracemalloc gjatë gjithë thirrjes
  së problemit, përfshirë modelimin dhe validimin; nuk përfshin të gjithë memorien native ose RSS.

## Kufijtë dhe kostoja e implementimit

Kufijtë janë bashkëpunues: kontrollohen në ciklet e algoritmit dhe gjeneratorët e kandidatëve.
Nuk janë ndërprerje të sistemit operativ apo kufi i rreptë RAM në bajt. Një operacion elementar,
si renditja e një liste kandidate, mund të mbarojë pak pas afatit. Fronti dhe nyjet kufizojnë
rritjen e strukturave; `tracemalloc` jep matje reale, jo garanci të RAM-it.

DFS me gjeneratorë ruan pak korniza, por prefikset immutable të gjata mund të marrin O(m²)
vlera totale. Optimizimi i punonjësve ruan rrugët e kandidatëve për rindërtim, me faktorë shtesë.
Gjurmimi i pemës ka kufij të veçantë për numrin e nyjeve dhe thellësinë. Vizualizimi nuk është
pema e plotë dhe mungesa e qëllimit në figurë nuk nënkupton mungesë zgjidhjeje në rezultat.

## Interpretimi eksperimental

`Limits(reconstruct_path=False)` çaktivizon ruajtjen e rrugës/veprimeve në rezultat,
duke ruajtur gjendjen përfundimtare te `SearchResult.final_state` dhe `solution`.
Strukturat e brendshme të kërkimit mbeten të nevojshme për vizitimin dhe kthimin pas;
ky opsion nuk premton eliminim të të gjithë tabelës së prindërve të BFS.

Matjet e ruajtura nuk janë kompleksiteti teorik. Ato varen nga renditja deterministe, kufijtë,
input-i, sistemi, gjurmimi dhe tracemalloc. Krahasimet mes algoritmeve kanë kuptim te i njëjti
problem dhe input; krahasimi Sudoku kundrejt golfistëve nuk është renditje e përgjithshme e algoritmeve.
Shiko CSV/JSON dhe tabelën e gjeneruar në `experimental_results.md` për numrat e këtij ekzekutimi.
