"""Streamlit presentation only; domain search remains in src/."""
from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import streamlit as st
from src.problems import sudoku, latin_square, eight_puzzle, missionaries_cannibals
from src.problems.social_golfers import Golfers, maximize
from src.problems.workforce_scheduling import Workforce
from src.utils.metrics import Limits
from src.visualization.search_tree import export_tree, to_dot
from src.utils.golfers_certificate import load_certificate

ROOT = Path(__file__).resolve().parent
PAGES = ["Paneli", "Social Golfers", "Sudoku", "Latin Square", "Pemët e kërkimit",
         "Analiza e performancës", "Shpjegimet matematikore"]
STATUS = {"solved": "Zgjidhje e gjetur dhe e validuar", "optimal": "Zgjidhje optimale e provuar",
          "limit": "U arrit kufiri i burimeve", "cutoff": "U arrit kufiri i thellësisë",
          "exhausted": "Nuk ekziston zgjidhje në hapësirën e kërkuar"}


def grid_table(values, n):
    st.table([{f"K{c + 1}": values[r * n + c] or "·" for c in range(n)} for r in range(n)])


def show_solution(kind, result, options):
    solution = result.solution
    if solution is None:
        st.info("Nuk u gjet zgjidhje në këtë ekzekutim. Rrit kufijtë ose ndrysho parametrat.")
        return
    if kind == "sudoku":
        st.subheader("Rrjeti i zgjidhur")
        grid_table(solution, 9)
    elif kind == "latin":
        grid_table(solution, options["n"])
    elif kind == "golfers":
        g = options["groups"]
        st.table([{"Java": i // g + 1, "Grupi": i % g + 1,
                   "Lojtarët": ", ".join(str(p + 1) for p in group)} for i, group in enumerate(solution)])
    elif kind == "workforce":
        shifts = options["shifts_per_day"]
        st.table([{"Dita": i // shifts + 1, "Ndërrimi": i % shifts + 1,
                   "Punonjësit (ID nga 0)": ", ".join(map(str, team)) or "Pa kërkesë"}
                  for i, team in enumerate(solution)])
        if result.objective is not None:
            st.write(f"Penaliteti i objektivit: {result.objective:g}")
    elif kind == "puzzle":
        for i, state in enumerate(result.path):
            st.write("Fillimi" if i == 0 else f"Lëvizja {i}: {result.actions[i - 1]}")
            grid_table(state, 3)
    else:
        st.table([{"Hapi": i, "M majtas": state[0], "K majtas": state[1],
                   "Varka": "Majtas" if state[2] == 0 else "Djathtas",
                   "Kalimi": result.actions[i - 1] if i else "Fillimi"}
                  for i, state in enumerate(result.path)])


def show_result(kind, result, options):
    message = STATUS[result.status]
    if result.status in ("solved", "optimal"):
        st.success(message)
    elif result.status in ("limit", "cutoff"):
        st.warning(message + ". Kjo nuk provon pamundësi.")
    else:
        st.info(message)
    if result.message:
        st.write(result.message)
    stats = asdict(result.stats)
    st.subheader("Matjet e ekzekutimit")
    st.table([{"Koha (s)": round(stats["elapsed_seconds"], 5), "Të zgjeruara": stats["expanded"],
                   "Të gjeneruara": stats["generated"], "Fronti maksimal": stats["max_frontier"],
                   "Thellësia": stats["max_depth"], "Kthime": stats["backtracks"], "Refuzime": stats["rejected"]}])
    if stats["depth_limits"]:
        st.write("Kufijtë e ekzekutuar të IDDFS: " + ", ".join(map(str, stats["depth_limits"])))
    left, right = st.columns([1, 1])
    with left:
        st.subheader("Zgjidhja")
        show_solution(kind, result, options)
    with right:
        st.subheader("Pema e kufizuar")
        st.caption("Blu: fillimi · Gjelbër: rruga/qëllimi · Kuqe: refuzim i regjistruar. Degët e tjera mund të jenë lënë jashtë.")
        st.graphviz_chart(to_dot(result), width="stretch")
        st.download_button("Shkarko pemën DOT", to_dot(result), f"{kind}.dot", "text/plain")
        if st.button("Përgatit PNG dhe SVG", key=f"export-{kind}"):
            with TemporaryDirectory() as directory:
                exports = {format: export_tree(result, Path(directory) / kind, format).read_bytes()
                           for format in ("png", "svg")}
            st.session_state[f"exports-{kind}"] = exports
        for format, content in st.session_state.get(f"exports-{kind}", {}).items():
            st.download_button(f"Shkarko {format.upper()}", content, f"{kind}.{format}",
                               "image/png" if format == "png" else "image/svg+xml")
    st.download_button("Shkarko rezultatin dhe metrikat JSON", json.dumps(asdict(result), ensure_ascii=False, indent=2),
                       f"{kind}-result.json", "application/json")


def execute(kind, function, options):
    with st.spinner("Kërkimi po ekzekutohet brenda kufijve të zgjedhur…"):
        result = function()
    st.session_state[f"result-{kind}"] = (result, options)
    st.session_state.pop(f"exports-{kind}", None)
    st.session_state.setdefault("history", []).append({"name": kind, "status": result.status, **asdict(result.stats)})


def main():
    st.set_page_config(page_title="Laboratori AI · 2026/27", layout="wide")
    st.markdown("""<style>
        [data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {
            color: #41566a; opacity: 1;
        }
        [data-testid="stMain"] th { color: #41566a; font-weight: 600; }
    </style>""", unsafe_allow_html=True)
    st.sidebar.title("Laboratori AI")
    st.sidebar.caption("Teknikat e kërkimit të painformuar · 2026/27")
    page = st.sidebar.radio("Seksioni", PAGES)
    with st.sidebar.expander("Kufijtë e kërkimit", expanded=True):
        seconds = st.number_input("Koha maksimale (s)", 0.1, 30.0, 5.0)
        nodes = st.number_input("Nyje të gjeneruara", 100, 1_000_000, 100_000, step=100)
        frontier = st.number_input("Fronti maksimal", 10, 200_000, 50_000, step=10)
        depth = st.number_input("Thellësia maksimale", 0, 1000, 100)
        trace_nodes = st.slider("Nyje në figurë", 10, 150, 45)
        trace_depth = st.slider("Thellësia e figurës", 1, 15, 5)
    limits = Limits(seconds, nodes, frontier, depth, trace_nodes, trace_depth)
    st.title(page)
    try:
        if page == "Paneli":
            st.write("Eksploro si DFS, BFS dhe IDDFS përshkojnë hapësirën e gjendjeve për gjashtë probleme.")
            st.table([{"Problemi": "Social Golfers", "Metoda": "DFS + Backtracking", "Qëllimi": "Pa çifte të përsëritura"},
                      {"Problemi": "Sudoku", "Metoda": "BFS FIFO + krasitje", "Qëllimi": "Plotësim i rrjetit"},
                      {"Problemi": "Latin Square", "Metoda": "IDDFS + Backtracking", "Qëllimi": "Unikësi rresht/kolonë"},
                      {"Problemi": "8-Puzzle", "Metoda": "BFS / DFS / IDDFS", "Qëllimi": "Rrugë drejt tabelës finale"},
                      {"Problemi": "Misionarët dhe Kanibalët", "Metoda": "BFS / DFS", "Qëllimi": "Kalime të sigurta"},
                      {"Problemi": "Punonjësit", "Metoda": "DFS + kufizim me kufi të poshtëm", "Qëllimi": "Ngarkesë dhe preferenca"}])
            st.info("Zgjidh një seksion nga navigimi. Çdo kërkim ka kufij kohe, nyjesh, fronti dhe thellësie.")
            st.write("Një rezultat i ndërprerë nuk është provë pamundësie. DFS nuk garanton rrugën më të shkurtër.")
        elif page == "Social Golfers":
            g = st.number_input("Grupe për javë", 1, 16, 8)
            p = st.number_input("Lojtarë për grup", 1, 8, 4)
            w = st.number_input("Javë të kërkuara", 1, 30, 2)
            config = Golfers(g, p, w)
            st.write(f"Lojtarë: {config.n}. Kufiri teorik i javëve: {config.upper_bound or 'pa kufi për p=1'}.")
            st.caption("Vetëm kufiri teorik nuk provon ekzistencën. Dëshmia më poshtë e provon për 32 lojtarë.")
            if (g, p) == (8, 4):
                with st.expander("Përgjigjja e provuar: 10 javë — dëshmia nga literatura"):
                    certificate = load_certificate()
                    st.success("Maksimumi është 10 javë: dëshmia e validuar arrin kufirin e sipërm.")
                    st.write(certificate["provenance"])
                    st.markdown(f"[Tabela origjinale e Alejandro Aguado-s]({certificate['source']})")
                    st.write(f"Çifte të ndryshme: {certificate['distinct_pairs']}; përsëritje: 0. "
                             "Çdo lojtar takon 30 kundërshtarë të ndryshëm.")
                    st.table([{"Java": i + 1, **{f"Grupi {j + 1}": ", ".join(map(str, team))
                               for j, team in enumerate(week)}} for i, week in enumerate(certificate["schedule"])])
                    st.caption("ID 0–31, si në burim. Kontrollet më poshtë ekzekutojnë DFS të pavarur nga dëshmia.")
                    st.download_button("Shkarko dëshminë dhe verifikimin JSON",
                                       json.dumps(certificate, ensure_ascii=False, indent=2),
                                       "golfers-optimality-certificate.json", "application/json")
            if st.button("Kërko orarin", type="primary"):
                execute("golfers", lambda: config.solve(limits), {"groups": g})
            if p > 1 and st.button("Kërko maksimumin e javëve"):
                with st.spinner("Kërkim progresiv; kufijtë zbatohen për secilin numër javësh…"):
                    report = maximize(config, limits)
                st.session_state["maximum"] = report
            if "maximum" in st.session_state:
                report = st.session_state["maximum"]
                st.write({"Javë të gjetura": report["best_weeks"], "Optimalitet i provuar": report["proven_optimal"]})
                st.table([{"Javë": w, "Status": STATUS[r.status]} for w, r in report["runs"]])
            if "result-golfers" in st.session_state:
                show_result("golfers", *st.session_state["result-golfers"])
        elif page == "Sudoku":
            difficulty = st.selectbox("Shembulli", ["easy", "medium", "hard"],
                                      format_func={"easy": "E lehtë", "medium": "Mesatare", "hard": "E vështirë"}.get)
            fixture = json.loads((ROOT / f"data/sudoku/{difficulty}.json").read_text(encoding="utf-8"))
            st.caption(fixture["difficulty_basis"])
            raw = st.text_area("Rrjeti JSON; 0 shënon qelizë bosh", json.dumps(fixture["grid"]), height=150, key=f"grid-{difficulty}")
            grid = sudoku.parse_grid(json.loads(raw))
            grid_table(grid, 9)
            st.caption("Përzgjedhja MRV zgjedh qelizën; zgjerimi i gjendjeve mbetet BFS FIFO.")
            if st.button("Zgjidh me BFS", type="primary"):
                execute("sudoku", lambda: sudoku.solve(grid, limits), {})
            if "result-sudoku" in st.session_state:
                result, options = st.session_state["result-sudoku"]
                if result.path:
                    with st.expander("Rrjeti origjinal i këtij ekzekutimi"):
                        grid_table(result.path[0], 9)
                show_result("sudoku", result, options)
        elif page == "Latin Square":
            n = st.number_input("Madhësia n", 1, 12, 5)
            st.caption("IDDFS ekzekuton çdo kufi. Rreshti dhe kolona e parë normalizohen për të hequr simetritë.")
            if st.button("Gjenero me IDDFS", type="primary"):
                execute("latin", lambda: latin_square.solve(n, limits), {"n": n})
            if "result-latin" in st.session_state:
                show_result("latin", *st.session_state["result-latin"])
        elif page == "Pemët e kërkimit":
            choice = st.selectbox("Problemi", ["8-Puzzle", "Misionarët dhe Kanibalët", "Planifikimi i punonjësve"])
            if choice == "8-Puzzle":
                algorithm = st.selectbox("Algoritmi", ["bfs", "dfs", "iddfs"])
                raw = st.text_input("Tabela fillestare (JSON)", "[1,2,3,4,0,6,7,5,8]")
                board = eight_puzzle.validate_board(json.loads(raw))
                grid_table(board, 3)
                st.caption("0 shënon boshllëkun. Qëllimi: 1,2,3 / 4,5,6 / 7,8,0.")
                kind, options = "puzzle", {}
                run = lambda: eight_puzzle.solve(board, algorithm, limits)
            elif choice == "Misionarët dhe Kanibalët":
                algorithm = st.selectbox("Algoritmi", ["bfs", "dfs"])
                st.write("3 misionarë, 3 kanibalë; varka merr 1 ose 2 njerëz. BFS gjen minimumin e kalimeve.")
                kind, options = "missionaries", {}
                run = lambda: missionaries_cannibals.solve(algorithm, limits)
            else:
                employees = st.number_input("Punonjës", 1, 20, 6)
                days = st.number_input("Ditë", 1, 14, 7)
                shifts = st.number_input("Ndërrime në ditë", 1, 4, 2)
                maximum = st.number_input("Maksimumi i ndërrimeve për punonjës", 0, 56, 4)
                rest = st.number_input("Ndërrime të lira ndërmjet dy punëve", 0, 20, 1)
                demand = json.loads(st.text_input("Kërkesa për çdo ndërrim (JSON; [] = një punonjës)", "[]"))
                unavailable = json.loads(st.text_input("Padisponueshmëria [[ID punonjësi, indeks ndërrimi], …]", "[]"))
                unwanted = json.loads(st.text_input("Ndërrime të papëlqyera [[ID, indeks], …]", "[]"))
                weight = st.number_input("Pesha e preferencave", 0, 100, 2)
                config = Workforce(employees, days, shifts, tuple(demand), maximum, rest,
                                   frozenset(tuple(v) for v in unavailable), frozenset(tuple(v) for v in unwanted), weight)
                st.caption("Indekset nisin nga 0. Një ndërrim ka gjatësi abstrakte; pushimi matet në ndërrime, jo në orë.")
                for conflict in config.conflicts():
                    st.warning(conflict)
                kind, options, run = "workforce", {"shifts_per_day": shifts}, lambda: config.solve(limits)
            if st.button("Nis kërkimin", type="primary"):
                execute(kind, run, options)
            if f"result-{kind}" in st.session_state:
                show_result(kind, *st.session_state[f"result-{kind}"])
        elif page == "Analiza e performancës":
            rows = st.session_state.get("history", [])
            benchmark = ROOT / "outputs/results/benchmarks.json"
            if benchmark.exists():
                measured = json.loads(benchmark.read_text(encoding="utf-8"))
                st.caption("Eksperimente të ruajtura: " + measured["timestamp_utc"] + ". Me tracemalloc aktiv.")
                rows = measured["results"] + rows
            if rows:
                st.dataframe(rows, hide_index=True, width="stretch")
                st.bar_chart([{ "Rasti": f"{i + 1}. {r['name']}", "Koha (s)": r["elapsed_seconds"]} for i, r in enumerate(rows)], x="Rasti", y="Koha (s)")
                st.download_button("Shkarko matjet JSON", json.dumps(rows, ensure_ascii=False, indent=2), "measurements.json")
            else:
                st.info("Ekzekuto një problem që të shfaqen matjet. Për eksperimentet: python main.py benchmark.")
        else:
            document = st.selectbox("Dokumenti", ["mathematical_models", "complexity_analysis", "report", "course_alignment", "golfers_optimality"])
            st.markdown((ROOT / f"docs/{document}.md").read_text(encoding="utf-8"))
    except (ValueError, TypeError, KeyError, OSError) as error:
        st.error(f"Kontrollo parametrat ose skedarin: {error}")


if __name__ == "__main__":
    main()
