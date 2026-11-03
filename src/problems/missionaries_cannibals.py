"""Classic safe-bank graph. Boat side 0 = left, 1 = right."""
from src.algorithms import bfs, dfs
from src.utils.metrics import Limits, Problem


def safe(state):
    m, c, side = state
    return (0 <= m <= 3 and 0 <= c <= 3 and side in (0, 1)
            and (m == 0 or m >= c) and (m == 3 or 3 - m >= 3 - c))


def successors(state, context):
    m, c, side = state
    direction = -1 if side == 0 else 1
    for missionaries, cannibals in ((0, 1), (0, 2), (1, 0), (1, 1), (2, 0)):
        child = m + direction * missionaries, c + direction * cannibals, 1 - side
        if safe(child):
            arrow = "majtas → djathtas" if side == 0 else "djathtas → majtas"
            yield f"{missionaries} M, {cannibals} K: {arrow}", child
        elif context is not None:
            context.stats.rejected += 1


def problem():
    return Problem((3, 3, 0), lambda state: state == (0, 0, 1), successors)


def solve(algorithm="bfs", limits: Limits = Limits()):
    if algorithm not in ("bfs", "dfs"):
        raise ValueError("Algoritmi duhet të jetë bfs ose dfs.")
    result = dfs(problem(), limits, graph_search=True) if algorithm == "dfs" else bfs(problem(), limits)
    if result.path and (not all(safe(state) for state in result.path) or any(
            after not in [child for _, child in successors(before, None)]
            for before, after in zip(result.path, result.path[1:]))):
        raise RuntimeError("Kalimet nuk plotësojnë kufizimet.")
    return result
