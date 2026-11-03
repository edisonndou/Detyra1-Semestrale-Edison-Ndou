# Lista e përmbushjes së kërkesave

Statuset: **Implementuar dhe testuar** për prova të ekzekutueshme; **Dokumentuar** për
arsyetimet që u kontrolluan në burim; **Pjesërisht / e hapur** kur ka kufizim të deklaruar.
Fusha e këtij kontrolli është **Detyra e parë semestrale**, jo implementimi i të gjithë
programit të lëndës. Kërkesat funksionale të saj janë mbuluar; kufizimet e lejuara të burimeve
raportohen veçmas dhe nuk përkthehen në pretendime për zgjidhjen e çdo instance të mundshme.

| Kërkesa | Statusi | Prova / vendndodhja |
|---|---|---|
| Python 3.12+, instalimi dhe arkitektura modulare | Implementuar dhe ekzekutuar | `.venv`, `pyproject.toml`, README |
| Algoritme manuale pa solver të jashtëm | Implementuar dhe testuar | `src/algorithms`, `tests/test_algorithms.py` |
| BFS FIFO, DFS, DLS, IDDFS, Backtracking | Implementuar dhe testuar | Rrugët, minimaliteti BFS, kufijtë IDDFS, dega e vdekur |
| Kufijtë e kohës/nyjeve/frontit/thellësisë | Implementuar dhe testuar | Statuset limit/cutoff; kontrolle bashkëpunuese |
| Rindërtimi i rrugës dhe veprimeve | Implementuar dhe testuar | Rezultatet dhe testet e kalimeve |
| Çaktivizimi opsional i rindërtimit të rrugës | Implementuar dhe testuar | `Limits(reconstruct_path=False)` ruan vetëm rezultatin final në output |
| Social Golfers i përgjithësuar, DFS + Backtracking | Implementuar dhe testuar | Rasti 2×2×3 dhe orari 32-lojtarësh 2-javor |
| Krasitja e çifteve dhe thyerja e simetrive | Implementuar dhe testuar | Java e parë kanonike, ankorimi i grupit, validimi i çifteve |
| Maksimumi për 4 lojtarë në çifte | Provuar dhe testuar | 3 javë arrijnë kufirin teorik |
| Maksimumi global për 32 lojtarë në grupe 4 | **Provuar dhe verifikuar: 10 javë** | Dëshmia e atribuuar Aguado-s ka 480 çifte unike; arrihet kufiri i sipërm; DFS matet veçmas |
| Kërkimi progresiv i maksimumit | Implementuar dhe testuar në rast të vogël | CLI `--maximize`; nuk raporton provë pas kufizimit |
| Sudoku vetëm BFS me krasitje | Implementuar dhe testuar | Tri enigmat përfundojnë e validohen; nuk ka DFS të fshehur |
| Input Sudoku i pavlefshëm dhe i pazgjidhshëm | Implementuar dhe testuar | Kufijtë e vlerave, përmasat, përsëritjet dhe domeni bosh |
| Nivelet e vështirësisë Sudoku | Dokumentuar me kufizim | Etiketa pedagogjike; jo standard i certifikuar apo provë unikësie |
| Latin Square me IDDFS të vërtetë për 3,4,5 | Implementuar dhe testuar | Çdo kufi 0..n² regjistrohet; validim i pavarur |
| 8-Puzzle BFS/DFS/IDDFS, veprime dhe paritet | Implementuar dhe testuar | Rrugët valide dhe rast i paarritshëm; vizitim global BFS/DFS |
| Misionarët/Kanibalët BFS/DFS dhe siguria | Implementuar dhe testuar | BFS 11 kalime; 16 gjendje të arritshme |
| Punonjësit: kërkesë, ngarkesë, pushim, disponueshmëri | Implementuar dhe testuar | Validuesi, konfliktet dhe instancat e pamundshme |
| Objektivi i drejtësisë/preferencave, DFS branch-and-bound | Implementuar dhe testuar | Krahasim me numërim të pavarur shterues në rast të vogël |
| Supozimet e orarit rrotullues | Dokumentuar | Ndërrime abstrakte, horizont i fundëm; pa cikël ndërmjet javëve |
| Pemë për tri problemet, ID/gjendje/thellësi/veprime | Implementuar dhe eksportuar | `outputs/search_trees`, PNG dhe SVG |
| Fillimi/qëllimi/rruga dhe refuzimet | Implementuar, mbulim i kufizuar | Ngjyrat DOT/fallback; refuzimet e domeneve kryesisht në numërues |
| Graphviz dhe NetworkX | Implementuar dhe testuar në të dy motorët | Graphviz portable 16.1.0 me SHA256; PNG/SVG native dhe fallback kalojnë testet |
| UI me shtatë seksione, parametra dhe eksporte | Implementuar dhe testuar | Streamlit AppTest për çdo faqe dhe ndërveprimin IDDFS |
| UI desktop/telefon | Kontrolluar vizualisht | Edge; pamjet `.impeccable/review`, 1440 px / 390 px |
| Përgjigjshmëria gjatë kërkimit | Implementuar me kufij | Afat bashkëpunues; spinner, jo anulim interaktiv i procesit |
| Matjet, CSV/JSON, grafikët dhe memoria | Implementuar dhe ekzekutuar | `outputs/results`, tracemalloc dhe metadata reale |
| 17 elemente modelimi për çdo problem | Dokumentuar | `docs/mathematical_models.md` |
| Kompleksiteti dhe dallimi teori/matje | Dokumentuar | `docs/complexity_analysis.md` |
| README, raporti dhe literatura në shqip | Dokumentuar | README dhe `docs/report.md`; referenca të verifikuara bibliografikisht |
| Pema e plotë dhe numërimi i saktë i nyjeve | Dokumentuar, testuar dhe eksportuar | Pemë binare D=3: 15 nyje DFS/BFS dhe 26 vizita IDDFS |
| Literatura sipas dokumentit të kursit | Dokumentuar | AIMA botimi 3; Michalewicz/Fogel botimi 2; dëshmia origjinale Aguado |
| Testet automatike | Ekzekutuar | 60 raste pytest, përfshirë certifikatën, CLI, AppTest dhe dy motorët e eksportimit |

## Kufijtë e deklaruar të përdorimit

Maksimumi 32-lojtarësh është 10, i provuar nga dëshmia e validuar dhe kufiri matematikor.
Kërkimi i pavarur DFS nuk garantohet ta rizbulojë brenda kufijve të parazgjedhur; raportimi
i kësaj ndërprerjeje kërkohet nga specifikimi. Nuk mbetet kërkesë funksionale e papërfunduar
në këtë kontroll, por kjo nuk është garanci për përfundim të shpejtë të kërkimeve shteruese.
Pemët mund të shkurtojnë rrugën përfundimtare
kur ajo tejkalon thellësinë/numrin e lejuar të nyjeve. Për çdo problem rruga e plotë mbetet në JSON.
Kufijtë nuk janë kontroll i izoluar i RAM-it; memoria e matur është vetëm ajo që sheh tracemalloc.
Versionet dhe numrat e rezultateve të ekzekutimit jepen te `outputs/results/benchmarks.json`
dhe `outputs/results/test-summary.txt`. [Shpjegimi i provës së maksimumit](golfers_optimality.md)
dhe [përputhja me dokumentin e lëndës](course_alignment.md) sqarojnë dallimin kërkim/dëshmi.
