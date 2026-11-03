# Teknikat e kërkimit të painformuar

Projekt semestral për **Inteligjencën Artificiale, viti akademik 2026/27**.
Autor i projektit të punës: Edison Ndou. Lënda: AI — Adrian Ymeri.

Algoritmet DFS, BFS, IDDFS, kërkimi me thellësi të kufizuar dhe Backtracking
janë implementuar me bibliotekën standarde të Python-it. Nuk përdoret solver i jashtëm.
Ndërfaqja Streamlit është e ndarë nga modelet dhe algoritmet.

## Instalimi në Windows

Kërkohet Python 3.12 ose më i ri. Hap PowerShell në këtë dosje:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Aktivizimi nuk është i detyrueshëm: përdor `.\.venv\Scripts\python.exe` në vend të `python`.
Në mjedisin ku u krijua projekti, Python 3.12.14 u gjet te
`C:\Users\Lenovo\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`;
mjedisi `.venv` tashmë është krijuar dhe varësitë janë instaluar.
Ky shteg është specifik për kompjuterin, jo kusht portabiliteti.

Paketa Python `graphviz` nuk instalon ekzekutuesin `dot`.
Për renderim Graphviz instalo aplikacionin nga [graphviz.org](https://graphviz.org/download/)
dhe shtoje dosjen `bin` në PATH. Kur `dot` mungon, eksportet PNG/SVG përdorin automatikisht
NetworkX dhe Matplotlib. DOT mbetet i disponueshëm, ndërsa pema në Streamlit renderohet në shfletues.
Në këtë workspace është vendosur dhe verifikuar Graphviz portable 16.1.0 te `.tools/graphviz`;
eksportuesi e gjen automatikisht, pa ndryshuar PATH të sistemit.
Për të përsëritur vendosjen portable përdor `powershell -ExecutionPolicy Bypass -File tools/setup_graphviz.ps1`.
Skripti shkarkon ZIP-in zyrtar dhe checksum-in SHA256 nga lidhja e botuar te graphviz.org.

## Ekzekutimi

```powershell
python -m streamlit run app.py
python main.py golfers --groups 2 --players 2 --weeks 3
python main.py golfers --groups 8 --players 4 --weeks 2
python main.py golfers --groups 8 --players 4 --maximize --seconds 5
python main.py golfers --certificate --output outputs/results/golfers-optimality.json
python main.py sudoku --difficulty easy
python main.py sudoku --difficulty medium
python main.py sudoku --difficulty hard --seconds 10
python main.py latin --n 5
python main.py puzzle --algorithm bfs --tree svg
python main.py puzzle --algorithm dfs --depth 100
python main.py puzzle --algorithm iddfs
python main.py missionaries --algorithm bfs --tree png
python main.py workforce --input data/workforce.json
python main.py benchmark --seconds 3 --output outputs/results/experiment-run.json
```

Shto `--seconds`, `--nodes`, `--frontier`, `--depth` për kufizimet.
`--output skedar.json` ruan rezultatin. Për Sudoku `--input` pret rrjet JSON 9×9 ose listë me 81 numra;
për Puzzle pret listë me nëntë numra. `0` shënon qelizën bosh.
Identifikuesit e punonjësve dhe ndërrimeve nisin nga 0; ndërfaqja i shfaq golfistët nga 1.

Shembull i vogël Social Golfers, 2 grupe × 2 lojtarë × 3 javë (ID nga 0):

| Java | Grupi 1 | Grupi 2 |
|---|---|---|
| 1 | 0, 1 | 2, 3 |
| 2 | 0, 2 | 1, 3 |
| 3 | 0, 3 | 1, 2 |

Për Misionarët dhe Kanibalët, BFS gjen **11 kalime**. Për gjendjen fillestare
`[1,2,3,4,0,6,7,5,8]`, BFS i 8-Puzzle gjen **2 lëvizje**: Poshtë, Djathtas.
Rrugët e plota dhe oraret ruhen në skedarët e rezultateve.

## Testet dhe eksperimentet

Kërkesa e projektit autorizoi shkrimin dhe ekzekutimin e testeve:

```powershell
python -m pytest -q -p no:cacheprovider
```

Testet përfshijnë algoritmet, ciklet, kthimin pas, kufijtë, validuesit, problemet e pazgjidhshme,
tre Sudoku, Latin Square 3/4/5, kalimet, planifikimin, eksportet dhe faqet Streamlit.
Eksperimentet janë veçmas në `python main.py benchmark`. Ato prodhojnë JSON, CSV dhe grafikë
me matje reale, versionin e Python-it dhe kufijtë. Një ekzekutim me `tracemalloc` nuk është
mesatare statistikore dhe ngadalëson programin; memoria e matur nuk është RSS totale e procesit.

Kontrolli vizual opsional `python tools/capture_ui.py` kërkon një server Streamlit aktiv,
Microsoft Edge të instaluar dhe `pip install playwright`; pamjet ruhen te `.impeccable/review`.
`requirements-lock.txt` regjistron versionet reale të mjedisit, përfshirë këtë mjet opsional.

## Arkitektura

```text
main.py                         CLI dhe përzgjedhja e problemeve
app.py                          Ndërfaqja Streamlit në shqip
src/algorithms/                 BFS, DFS, DLS, IDDFS, Backtracking, branch-and-bound
src/problems/                   Gjashtë modele dhe validuesit përkatës
src/utils/metrics.py            Kontrata Problem, Limits, SearchResult dhe matjet
src/visualization/              Pemët DOT/PNG/SVG dhe grafikët e performancës
src/experiments.py              Eksperimentet e riprodhueshme
data/sudoku/                    Tre enigma me etiketë pedagogjike vështirësie
data/workforce.json             Shembull konfigurimi të punonjësve
tests/                          Testet pytest dhe Streamlit AppTest
docs/                           Modelet, kompleksiteti, raporti dhe lista e kërkesave
outputs/search_trees/           Eksporte të kufizuara
outputs/results/                Matje dhe rrugë reale
```

`Problem` përmban vetëm gjendjen fillestare, testin e qëllimit dhe gjeneratorin e pasardhësve.
Algoritmet nuk njohin Streamlit, Matplotlib apo formatin e skedarëve. Kufizimet zotërohen nga
moduli përkatës i problemit. Përfundimi validohet përpara raportimit si zgjidhje.

## Interpretimi i rezultateve

| Statusi | Kuptimi |
|---|---|
| `solved` | U gjet zgjidhje e vlefshme; nuk premton optimalitet të DFS |
| `optimal` | Branch-and-bound shteroi/krasiti hapësirën duke provuar optimalitetin |
| `exhausted` | Hapësira e përfaqësuar u shterua, ose një kufi matematikor provon pamundësi |
| `cutoff` | U arrit kufiri i thellësisë; nuk është provë pamundësie |
| `limit` | U arrit kufiri i kohës, nyjeve ose frontit; mund të ruhet një orar kandidat |

Për 32 golfistë, maksimumi i provuar është **10 javë**: dëshmia e botuar e Aguado-s
validohet lokalisht dhe arrin kufirin teorik. Shiko [provën dhe prejardhjen](docs/golfers_optimality.md).
Ky certifikim është i ndarë nga DFS dhe nuk paraqitet si zbulim i algoritmit të projektit.
Eksperimenti DFS i kufizuar për 10 javë mund të kthejë `limit`; kjo nuk kundërshton dëshminë.
Komanda `--maximize` provon në rend rritës numrin e javëve dhe ndalet te kufizimi i parë.
Kufiri kohor zbatohet për çdo provë, prandaj i gjithë kërkimi i maksimumit mund të zgjasë më shumë.

Lexo [modelet matematikore](docs/mathematical_models.md),
[analizën e kompleksitetit](docs/complexity_analysis.md), [raportin](docs/report.md)
dhe [listën e kërkesave](docs/requirements_checklist.md).
Përmbledhja e verifikimit përfundimtar është në [completion_audit.md](docs/completion_audit.md).
Për përputhjen me programin e lëndës, numërimin e saktë të nyjeve dhe pyetjet e mbrojtjes,
lexo [course_alignment.md](docs/course_alignment.md). Pjesët A*, metaheuristikat dhe lojërat
janë tema të programit të përgjithshëm, jo implementime të kërkuara të detyrës së parë.
