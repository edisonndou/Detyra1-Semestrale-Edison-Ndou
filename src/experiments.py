"""Reproducible real experiments and exports, invoked explicitly from the CLI."""
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import csv
import json
import platform
import tracemalloc
from src.problems import sudoku, latin_square, eight_puzzle, missionaries_cannibals
from src.problems.social_golfers import Golfers
from src.problems.workforce_scheduling import Workforce
from src.utils.metrics import Limits
from src.visualization.search_tree import export_tree, to_dot
from src.visualization.performance_charts import performance_chart
from src.utils.golfers_certificate import load_certificate
from src.utils.metrics import Problem
from src.algorithms import bfs

ROOT = Path(__file__).resolve().parents[1]


def run_experiments(seconds=5.0):
    limits = Limits(max_seconds=seconds, max_nodes=200_000, max_depth=100, trace_nodes=80, trace_depth=15)
    cases = [("golfers-2x2-3w", lambda: Golfers(2, 2, 3).solve(limits)),
             ("golfers-8x4-2w", lambda: Golfers(8, 4, 2).solve(limits)),
             ("golfers-8x4-10w", lambda: Golfers(8, 4, 10).solve(limits))]
    for name in ("easy", "medium", "hard"):
        grid = json.loads((ROOT / f"data/sudoku/{name}.json").read_text(encoding="utf-8"))["grid"]
        cases.append((f"sudoku-{name}", lambda grid=grid: sudoku.solve(grid, limits)))
    for n in (3, 4, 5):
        cases.append((f"latin-{n}", lambda n=n: latin_square.solve(n, limits)))
    for algorithm in ("bfs", "dfs", "iddfs"):
        cases.append((f"puzzle-{algorithm}", lambda a=algorithm: eight_puzzle.solve(algorithm=a, limits=limits)))
    for algorithm in ("bfs", "dfs"):
        cases.append((f"missionaries-{algorithm}", lambda a=algorithm: missionaries_cannibals.solve(a, limits)))
    cases.append(("workforce-dfs", lambda: Workforce().solve(limits)))
    rows = []
    output = ROOT / "outputs/results"
    output.mkdir(parents=True, exist_ok=True)
    certificate = load_certificate()
    (output / "golfers-optimality.json").write_text(json.dumps(certificate, ensure_ascii=False, indent=2), encoding="utf-8")
    for name, run in cases:
        tracemalloc.start()
        try:
            result = run()
            _, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        row = {"name": name, "status": result.status, **asdict(result.stats),
               "peak_traced_bytes": peak, "objective": result.objective,
               "solution_available": result.solution is not None}
        rows.append(row)
        (output / f"{name}.json").write_text(json.dumps(asdict(result), ensure_ascii=False, indent=2), encoding="utf-8")
        if name in ("puzzle-bfs", "missionaries-bfs", "workforce-dfs"):
            for format in ("png", "svg"):
                export_tree(result, ROOT / "outputs/search_trees" / name, format)
    metadata = {"timestamp_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
                "platform": platform.platform(), "limits": asdict(limits),
                "note": "Një ekzekutim për rast, me tracemalloc aktiv; jo mesatare statistikore.", "results": rows}
    (output / "benchmarks.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    with (output / "benchmarks.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    performance_chart(rows, output / "performance.png")
    complete_model = Problem((0, 0), lambda state: False,
                             lambda state, context: [(str(i), (state[0] + 1, 2*state[1] + i)) for i in (0, 1)]
                             if state[0] < 3 else [])
    complete_tree = bfs(complete_model, limits)
    for format in ("png", "svg"):
        export_tree(complete_tree, ROOT / "outputs/search_trees/complete-binary-depth3", format)
    (ROOT / "outputs/search_trees/complete-binary-depth3.dot").write_text(
        to_dot(complete_tree), encoding="utf-8")
    report = ["# Rezultatet eksperimentale", "", f"Koha e regjistrimit (UTC): {metadata['timestamp_utc']}", "",
              f"Python {metadata['python']}; {metadata['platform']}.", "",
              f"Kufijtë për rast: {seconds:g} s, {limits.max_nodes} nyje, front {limits.max_frontier}, thellësi {limits.max_depth}.",
              "Tracemalloc aktiv; një ekzekutim për rast. Matjet nuk përfshijnë renderimin e figurave.", "",
              "| Rasti | Statusi | Koha (s) | Zgjeruar | Gjeneruar | Fronti max | Thellësia | Kthime | Memoria Python (KiB) |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for row in rows:
        report.append(f"| {row['name']} | {row['status']} | {row['elapsed_seconds']:.6f} | {row['expanded']} | "
                      f"{row['generated']} | {row['max_frontier']} | {row['max_depth']} | {row['backtracks']} | {row['peak_traced_bytes']/1024:.1f} |")
    report.extend(["", "Numëruesit e refuzimeve, kufijtë e IDDFS dhe objektivi janë në CSV/JSON.", "",
                   "- Social Golfers: DFS gjen orarin 2-javor; prova DFS 10-javore mund të ndërpritet nga kufijtë. Veçmas, dëshmia e botuar e validuar provon maksimumin 10; shiko golfers-optimality.json. Nuk i atribuohen metrika kërkimi certifikatës.",
                   "- Sudoku: tri zgjidhje valide; renditja e kohës nuk është certifikim i vështirësisë njerëzore.",
                   "- Latin Square: gjurmët regjistrojnë çdo kufi deri n², për n=3,4,5.",
                   "- 8-Puzzle: BFS/IDDFS japin 2 hapa për input-in standard; DFS mund të japë rrugë më të gjatë.",
                   "- Misionarët: BFS jep 11 kalime, të kontrolluara nga validuesi dhe testet.",
                   "- Punonjësit: objektivi bazë 34 është kufiri i shpërndarjes së 14 punëve mes 6 punonjësve (4×2²+2×3²).", "",
                   "[Të dhënat CSV](../outputs/results/benchmarks.csv) · [JSON me mjedisin dhe kufijtë](../outputs/results/benchmarks.json)", "",
                   "![Kohët dhe zgjerimet e matura](../outputs/results/performance.png)", ""])
    (ROOT / "docs/experimental_results.md").write_text("\n".join(report), encoding="utf-8")
    return metadata
