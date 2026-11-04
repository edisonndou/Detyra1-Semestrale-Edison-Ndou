"""Command-line composition root. All academic output is in Albanian."""
import argparse
from dataclasses import asdict
from pathlib import Path
import json
import sys
from src.problems import sudoku, latin_square, eight_puzzle, missionaries_cannibals
from src.problems.social_golfers import Golfers, maximize
from src.problems.workforce_scheduling import Workforce
from src.utils.metrics import Limits
from src.visualization.search_tree import export_tree
from src.utils.golfers_certificate import load_certificate


def emit(payload: dict, output: Path | None) -> None:
    """Serialize the CLI result consistently for stdout and optional files."""
    rendered = json.dumps(payload, ensure_ascii=False, indent=2)
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    print(rendered)


def main():
    parser = argparse.ArgumentParser(description="Teknikat e kërkimit të painformuar — 2026/27")
    parser.add_argument("problem", choices=["golfers", "sudoku", "latin", "puzzle", "missionaries", "workforce", "benchmark"])
    parser.add_argument("--seconds", type=float, default=5)
    parser.add_argument("--nodes", type=int, default=100_000)
    parser.add_argument("--frontier", type=int, default=50_000)
    parser.add_argument("--depth", type=int, default=100)
    parser.add_argument("--algorithm", choices=["bfs", "dfs", "iddfs"], default="bfs")
    parser.add_argument("--n", type=int, default=3)
    parser.add_argument("--groups", type=int, default=8)
    parser.add_argument("--players", type=int, default=4)
    parser.add_argument("--weeks", type=int, default=2)
    golf_mode = parser.add_mutually_exclusive_group()
    golf_mode.add_argument("--maximize", action="store_true")
    golf_mode.add_argument("--certificate", action="store_true", help="Verifiko dëshminë e botuar 8×4×10; nuk nis DFS.")
    parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], default="easy")
    parser.add_argument("--input", type=Path, help="JSON: rrjet Sudoku, tabelë Puzzle ose konfigurim punonjësish")
    parser.add_argument("--tree", choices=["png", "svg"])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        limits = Limits(args.seconds, args.nodes, args.frontier, args.depth)
        if args.certificate and args.problem != "golfers":
            parser.error("--certificate zbatohet vetëm për golfers.")
        custom = json.loads(args.input.read_text(encoding="utf-8")) if args.input else None
        if args.problem == "benchmark":
            from src.experiments import run_experiments
            payload = run_experiments(args.seconds)
        else:
            if args.problem == "golfers":
                if args.certificate:
                    if (args.groups, args.players) != (8, 4):
                        parser.error("Dëshmia e botuar zbatohet vetëm për 8 grupe me 4 lojtarë.")
                    emit(load_certificate(), args.output)
                    return
                config = Golfers(args.groups, args.players, args.weeks)
                if args.maximize:
                    report = maximize(config, limits)
                    payload = {**report, "runs": [(w, asdict(r)) for w, r in report["runs"]]}
                    emit(payload, args.output)
                    return
                result = config.solve(limits)
            elif args.problem == "sudoku":
                file = Path(__file__).parent / f"data/sudoku/{args.difficulty}.json"
                grid = custom if custom is not None else json.loads(file.read_text(encoding="utf-8"))["grid"]
                result = sudoku.solve(grid, limits)
            elif args.problem == "latin":
                result = latin_square.solve(args.n, limits)
            elif args.problem == "puzzle":
                result = eight_puzzle.solve(custom or eight_puzzle.problem().initial, args.algorithm, limits)
            elif args.problem == "missionaries":
                if args.algorithm == "iddfs":
                    parser.error("Misionarët mbështesin bfs ose dfs.")
                result = missionaries_cannibals.solve(args.algorithm, limits)
            else:
                options = custom or {}
                for field in ("unavailable", "unwanted"):
                    if field in options:
                        options[field] = frozenset(tuple(pair) for pair in options[field])
                result = Workforce(**options).solve(limits)
            payload = asdict(result)
            if args.tree:
                export_tree(result, Path("outputs/search_trees") / args.problem, args.tree)
        emit(payload, args.output)
    except (ValueError, TypeError, OSError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    main()
