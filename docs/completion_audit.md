# Kontrolli përfundimtar i detyrës së parë semestrale

Data e kontrollit: 24 tetor 2026 (Europe/Berlin).
Fusha: katër pjesët e **Detyrës së parë semestrale — Teknikat e painformuara të kërkimit**,
së bashku me specifikimin teknik të bashkëngjitur. Programi i plotë i lëndës nuk trajtohet
si kërkesë për implementimin e A*, metaheuristikave, SAT dhe lojërave në këtë dorëzim.

## Përfundimi i kontrollit

Kërkesat funksionale të detyrës së parë janë implementuar dhe kontrolluar. Nuk mbetet
një veçori e detyrueshme e shënuar si e papërfunduar në listën e kërkesave.
Kjo nuk do të thotë se një algoritëm shterues përfundon për çdo madhësi input-i:
kufijtë dhe raportimi i ndershëm i ndërprerjes janë kërkesa të vetë specifikimit.

## Mangësitë e mbyllura në kontrollin e fundit

| Mangësia e versionit të mëparshëm | Plotësimi dhe prova |
|---|---|
| Maksimumi i 32 golfistëve nuk kishte dëshmi në projekt | Tabela origjinale e Aguado-s u transkriptua me atribim, u validua lokalisht dhe u rikontrollua me matricë takimesh në test. 10 javë arrijnë kufirin e sipërm; 480 çifte unike, 30 kundërshtarë për lojtar. |
| Graphviz native nuk ishte ekzekutuar | U vendos Graphviz portable 16.1.0, u verifikua SHA256 nga botimi zyrtar dhe kaluan eksportet native PNG/SVG, veçmas nga fallback-u NetworkX. |
| DFS ruante gjendje globale edhe në modalitetin e rrugës aktive | Seti global mbushet vetëm kur kërkohet kërkim grafik; DFS/IDDFS bazë nuk mbajnë më të gjitha gjendjet e degëve të përfunduara. |
| Rindërtimi i BFS përdorte None si kufi të prindërve | Rruga rindërtohet deri te gjendja fillestare; një None i ndërmjetëm nuk e ndërpret rrugën. |
| Rruga nuk mund të çaktivizohej në output | `Limits(reconstruct_path=False)` ruan gjendjen finale, pa listën e rrugës dhe veprimeve; testuar për katër metodat. |
| Nuk jepej shprehimisht thellësia e rekursionit Python | Metrika `max_recursion_depth=0` dokumenton implementimin me stivë eksplicite; thellësia logjike matet veçmas. |
| Mungonte shembulli i pemës së plotë dhe numërimi i saktë | Pemë binare D=3: 15 nyje për DFS/BFS dhe 26 vizita IDDFS; testuar dhe eksportuar DOT/PNG/SVG. |
| Raporti citonte botimin e katërt të AIMA-s | Bibliografia u përshtat me botimin e tretë të kërkuar nga dokumenti i lëndës. |
| Një dublikatë e refuzuar e qëllimit ngjyrosej si qëllim i pranuar | Statusi i refuzimit ka përparësi në të dy motorët e vizualizimit; mbulohet me regresion. |

## Rezultatet e verifikimit

- **60 teste kaluan**, pa dështime ose raste të kapërcyera në këtë mjedis.
  Prova e ruajtur: `outputs/results/test-summary.txt`.
- Përpilimi i sintaksës me `compileall` kaloi.
- `pip check` raportoi `No broken requirements found`.
- Eksperimentet u rigjeneruan nga ekzekutime reale, me kufij dhe metadata në
  `outputs/results/benchmarks.json`, CSV dhe `docs/experimental_results.md`.
- Certifikimi i maksimumit ruhet veçmas në `outputs/results/golfers-optimality.json`,
  me `origin=published_certificate`; nuk ka metrika të sajuara zbulimi nga DFS.
- UI u kontrollua në Edge, desktop 1440 px dhe telefon 390 px. Pamjet janë te
  `.impeccable/review`. Rishikuesi i pavarur i pamjes së certifikatës dha `ship`,
  pa gjetje materiale. Tabela e gjerë lëviz brenda zonës së saj në ekran të ngushtë.

Checksum SHA256 i arkivit portable Graphviz të përdorur:
`733e49626c492242eb8dca30ea627b6ead20710e207998c7933b4909d92d6abc`.
Burimi zyrtar dhe procedura e verifikimit janë në `tools/setup_graphviz.ps1`.

## Kufijtë e deklaruar, pa pretendime të rreme

DFS i përgjithshëm ruhet dhe mund të arrijë kufirin për 8×4×10. Përgjigjja matematikore
10-javore provohet me dëshminë e atribuuar dhe të validuar, siç lejon shprehimisht specifikimi.
Kufijtë e burimeve janë bashkëpunues; pemët janë të kufizuara; memoria është ajo që mat
tracemalloc; vështirësitë Sudoku janë etiketa pedagogjike. Supozimet e punonjësve janë
të konfigurueshme dhe nuk paraqiten si rregulla ligjore pune apo cikël i detyrueshëm ndërmjet javëve.

[Lista e plotë e kërkesave](requirements_checklist.md) ·
[Prova e maksimumit](golfers_optimality.md) ·
[Përputhja me dokumentin e lëndës](course_alignment.md)
