# Raport semestral: Teknikat e kërkimit të painformuar

## 1. Hyrje

Ky projekt për lëndën Inteligjenca Artificiale, 2026/27, modelon gjashtë probleme dhe
demonstron lidhjen mes përfaqësimit të gjendjes, algoritmit të kërkimit dhe kufizimeve praktike.
Rezultati përbëhet nga implementimi Python, ndërfaqja Streamlit, testet, modelet dhe matjet reale.

## 2. Baza teorike

Një problem kërkimi përshkruhet nga gjendja fillestare, veprimet, tranzicioni dhe qëllimi.
BFS përdor FIFO, DFS përdor stivën, ndërsa IDDFS përsërit kërkimin me thellësi të kufizuar.
Në CSP, një gjendje është caktim i pjesshëm dhe kufizimet eliminojnë pasardhës të pavlefshëm.
Renditja MRV për Sudoku nuk e ndryshon FIFO-n e BFS. Kontrolli i cikleve është i domosdoshëm
në Puzzle dhe transport; në caktime monotone, gjatësia e prefiksit rritet dhe ciklet nuk lindin.
Kapitujt 3 dhe 6 të [Russell dhe Norvig, AIMA](https://aima.cs.berkeley.edu/)
trajtojnë kërkimin dhe CSP. Modelimi dhe trajtimi i kufizimeve lidhen gjithashtu me
[Michalewicz dhe Fogel](https://link.springer.com/book/10.1007/978-3-662-07807-5).

## 3. Modelimi matematikor

[Dokumenti i modeleve](mathematical_models.md) jep 17 elementet e kërkuara për secilin problem.
Social Golfers përdor grupe të pjesshme dhe çiftet e takimeve. Sudoku përdor 81 variabla,
Latin Square n² variabla, Puzzle permutime, Misionarët numërime sipas bregut dhe punonjësit
ekipe kronologjike. Formula e hapësirës bruto nuk barazohet me numrin e zgjidhjeve valide.

## 4. Përshkrimi i algoritmeve

BFS ruan prindin dhe veprimin për çdo gjendje të re dhe përfundon te qëllimi i parë i nxjerrë.
DFS/DLS përdor korniza me iteratorë, rrugën aktive dhe kthim eksplicit pas degëve të shteruara.
Ky backtracking nuk kërkon rekursion Python dhe shmang kufirin e interpreterit për thellësinë.
IDDFS i thërret të njëjtit kërkim të kufizuar çdo thellësi, duke mbledhur metrikat e të gjitha iteracioneve.
Planifikimi përdor DFS branch-and-bound: një relaksim i kostos së shpërndarjes jep kufi të poshtëm.
Zgjidhjet e kërkimit nuk janë lista të paracaktuara dhe nuk thirret solver i jashtëm.
Një dëshmi e veçantë nga literatura për Social Golfers etiketohet si e tillë dhe vetëm verifikohet;
nuk përdoret nga zgjidhësi DFS.

## 5. Hollësitë e implementimit

Kontrata `Problem` është kufiri i ripërdorimit mes algoritmit dhe domenit; funksionet
`successors` zotërojnë rregullat për kandidatët. `Limits` dhe `Context` zotërojnë kufizimin
e burimeve dhe matjet. Vizualizimi, CLI dhe UI varen nga rezultatet dhe nuk ndikojnë te zgjidhja.
Gjendjet janë tuple të hashueshme; renditja është deterministe. Validimi i plotë kryhet pas
kërkimit dhe nuk mbështetet vetëm te statusi që kthen algoritmi.

## 6. Rezultatet eksperimentale

Matjet e ekzekutuara janë në [experimental_results.md](experimental_results.md), CSV dhe JSON
nën `outputs/results`. Çdo problem u ekzekutua me kufij të deklaruar dhe me tracemalloc aktiv.
JSON individual ruan rrugën e plotë, veprimet, objektivin kur ekziston dhe pemën e kufizuar.
Rezultatet nuk janë mesatare të shumë provave dhe nuk mund të përgjithësohen për çdo input.

Për Social Golfers 32/8/4, DFS gjen dhe validon shembullin 2-javor. Kërkimi i drejtpërdrejtë
për 10 javë u ndërpre nga kufiri kohor. Veçmas, [dëshmia e botuar e Aguado-s](golfers_optimality.md)
u transkriptua dhe u validua në projekt: ka 480 çifte unike dhe 30 kundërshtarë për çdo lojtar.
**Maksimumi global është 10 javë**, sepse orari valid arrin kufirin e sipërm.
Nuk pretendohet se DFS e zbuloi orarin e botuar, as që kufiri i sipërm vetëm do të provonte ekzistencën.
Shembulli 4-lojtarësh me grupe dyshe realizon 3 javë dhe arrin kufirin, duke provuar optimalitetin.

## 7. Vizualizimet e pemëve

Figurat PNG dhe SVG për 8-Puzzle, Misionarët dhe punonjësit janë në `outputs/search_trees`.
Nyjet tregojnë ID, gjendjen e shkurtuar dhe thellësinë; harqet tregojnë veprimin.
Fillimi është blu, rruga e zgjidhjes e gjelbër dhe refuzimet e regjistruara të kuqe.
Gjendjet e plota janë në JSON. Numri i nyjeve dhe thellësia e figurës janë të kufizuara.
Refuzimet e domeneve zakonisht numërohen pa ndërtuar një gjendje të pavlefshme në gjurmë;
prandaj jo çdo krasitje shfaqet si nyje e kuqe.
Graphviz portable 16.1.0 u verifikua me checksum dhe eksportet native PNG/SVG u testuan.
Kur Graphviz mungon në një kompjuter tjetër, fallback-u NetworkX është funksional por grafet e dendura lexohen më vështirë;
ul kufirin e nyjeve ose përdor DOT me Graphviz për paraqitje më të qartë.

## 8. Kompleksiteti

[Analiza e veçantë](complexity_analysis.md) dallon kufijtë teorikë nga matjet dhe shpjegon
kostot e kopjimit të gjendjeve. BFS paguan memorie për frontin dhe vizitimin; DFS mund të
shpenzojë kohë në degë të gjata; IDDFS përsërit prefikset. Simetritë dhe krasitja ulin hapësirën
praktike por nuk e bëjnë përgjithësisht polinomiale.

## 9. Diskutim

Zgjedhja e përfaqësimit ndikon fort: grupet e paetiketuara heqin simetri, MRV kufizon degëzimin
e Sudoku dhe reduktimi i Latin Square lejon përfundimin e rasteve 3,4,5 pa zëvendësuar IDDFS.
Etiketat e vështirësisë Sudoku janë pedagogjike, jo standard i certifikuar; nuk pretendohet unikësi.
Punonjësit përdorin intervale abstrakte; nuk përfshihen ligje pune, kohëzgjatje reale të turneve
apo lidhja ciklike ndërmjet javëve. Të gjitha këto supozime janë të deklaruara dhe parametrat
e mbuluar janë të konfigurueshëm. Ndërprerja bashkëpunuese nuk është një proces i izoluar me RAM të fiksuar.

## 10. Përfundime

Projekti demonstron gjashtë probleme përmes algoritmeve të kërkuara, validimit, kufijve dhe
vizualizimit të matshëm. Maksimumi 10-javor i Social Golfers mbështetet nga një dëshmi e validuar
dhe kufiri i sipërm, ndërsa performanca e DFS raportohet veçmas. Kufizimet llogaritëse për
instanca të mëdha janë sjellje e deklaruar e programit dhe nuk raportohen si pamundësi matematikore.
Gjendja e çdo kërkese dhe provat e ekzekutimit jepen te [lista e kërkesave](requirements_checklist.md).

## 11. Referencat

1. Stuart Russell, Peter Norvig. *Artificial Intelligence: A Modern Approach*, botimi 3,
   Prentice Hall, 2009, ISBN 0136042597 sipas [faqes së autorëve për botimet](https://aima.eecs.berkeley.edu/translations.html),
   siç kërkohet në dokumentin e lëndës.
   Kapitujt 3 (kërkimi) dhe 6 (CSP). Referencë teorike; nuk është burim kodi të kopjuar.
2. Zbigniew Michalewicz, David B. Fogel. *How to Solve It: Modern Heuristics*, botimi 2,
   Springer, 2004. [DOI 10.1007/978-3-662-07807-5](https://link.springer.com/book/10.1007/978-3-662-07807-5).
   Modelimi dhe trajtimi i kufizimeve; jo autorizim për të zëvendësuar algoritmet e detyrës me heuristika të tjera.
3. Alejandro Aguado. *A 10 Days Solution to the Social Golfer Problem*, Tabela I.
   [Dëshmia origjinale](https://www.mathpuzzle.com/MAA/54-Golf%20Tournaments/socgolf1.pdf).
   Të dhënat numerike të orarit përdoren si dëshmi ekzistence dhe verifikohen në mënyrë të pavarur.
