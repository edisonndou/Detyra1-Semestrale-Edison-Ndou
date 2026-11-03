"""8-Puzzle graph, with parity reachability checked against a configurable goal."""
from src.algorithms import bfs, dfs, iddfs
from src.utils.metrics import Context, Limits, Problem, SearchResult

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def validate_board(board: tuple[int, ...]) -> tuple[int, ...]:
    board = tuple(board)
    if len(board) != 9 or any(type(v) is not int for v in board) or set(board) != set(range(9)):
        raise ValueError("Tabela duhet të jetë një permutim i numrave 0–8.")
    return board


def reachable(initial: tuple[int, ...], goal: tuple[int, ...] = GOAL) -> bool:
    def parity(board):
        values = [v for v in validate_board(board) if v]
        return sum(a > b for i, a in enumerate(values) for b in values[i + 1:]) % 2
    return parity(initial) == parity(goal)


def successors(state, context):
    blank = state.index(0)
    row, col = divmod(blank, 3)
    for action, dr, dc in (("Lart", -1, 0), ("Poshtë", 1, 0), ("Majtas", 0, -1), ("Djathtas", 0, 1)):
        if 0 <= row + dr < 3 and 0 <= col + dc < 3:
            target = (row + dr) * 3 + col + dc
            child = list(state)
            child[blank], child[target] = child[target], child[blank]
            yield action, tuple(child)


def problem(initial: tuple[int, ...] = (1, 2, 3, 4, 0, 6, 7, 5, 8), goal: tuple[int, ...] = GOAL) -> Problem[tuple[int, ...]]:
    initial, goal = validate_board(initial), validate_board(goal)
    return Problem(initial, lambda state: state == goal, successors)


def solve(initial=(1, 2, 3, 4, 0, 6, 7, 5, 8), algorithm="bfs", limits=Limits(), goal=GOAL):
    model = problem(initial, goal)
    if not reachable(initial, goal):
        return Context(limits).finish("exhausted", message="Pariteti provon se qëllimi është i paarritshëm.")
    result = dfs(model, limits, graph_search=True) if algorithm == "dfs" else {"bfs": bfs, "iddfs": iddfs}[algorithm](model, limits)
    if result.path and (result.path[-1] != tuple(goal) or any(
            after not in [child for _, child in successors(before, None)]
            for before, after in zip(result.path, result.path[1:]))):
        raise RuntimeError("Rruga e 8-Puzzle nuk është e vlefshme.")
    return result
