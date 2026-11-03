"""Sudoku CSP with FIFO BFS; MRV orders variables, never search nodes."""
from src.algorithms import bfs
from src.utils.metrics import Context, Limits, Problem


def units():
    rows = [tuple(range(r * 9, r * 9 + 9)) for r in range(9)]
    columns = [tuple(range(c, 81, 9)) for c in range(9)]
    boxes = [tuple((br + r) * 9 + bc + c for r in range(3) for c in range(3))
             for br in (0, 3, 6) for bc in (0, 3, 6)]
    return rows + columns + boxes


UNITS = units()
PEERS = tuple(set(j for unit in UNITS if i in unit for j in unit) - {i} for i in range(81))


def parse_grid(grid):
    if len(grid) == 9 and all(isinstance(row, (list, tuple)) for row in grid):
        if any(len(row) != 9 for row in grid):
            raise ValueError("Çdo rresht duhet të përmbajë 9 qeliza.")
        grid = [value for row in grid for value in row]
    values = tuple(grid)
    if len(values) != 81 or any(type(value) is not int or not 0 <= value <= 9 for value in values):
        raise ValueError("Sudoku kërkon 81 numra të plotë nga 0 deri në 9.")
    if any(len([values[i] for i in unit if values[i]]) != len({values[i] for i in unit if values[i]}) for unit in UNITS):
        raise ValueError("Të dhënat kanë shifra të përsëritura në rresht, kolonë ose kuti.")
    return values


def valid_solution(state, clues=None):
    try:
        state = parse_grid(state)
    except (TypeError, ValueError):
        return False
    return (all({state[i] for i in unit} == set(range(1, 10)) for unit in UNITS)
            and (clues is None or all(not clue or state[i] == clue for i, clue in enumerate(clues))))


def problem(grid):
    initial = parse_grid(grid)

    def successors(state, context: Context):
        choices = []
        for index, value in enumerate(state):
            context.check()
            if value:
                continue
            candidates = sorted(set(range(1, 10)) - {state[j] for j in PEERS[index]})
            if not candidates:
                context.stats.rejected += 9
                return
            choices.append((len(candidates), index, candidates))
        if not choices:
            return
        _, index, candidates = min(choices)
        context.stats.rejected += 9 - len(candidates)
        for value in candidates:
            child = state[:index] + (value,) + state[index + 1:]
            yield f"R{index // 9 + 1}K{index % 9 + 1} = {value}", child

    return Problem(initial, lambda state: 0 not in state, successors)


def solve(grid, limits: Limits = Limits()):
    model = problem(grid)
    result = bfs(model, limits)
    if result.solution is not None and not valid_solution(result.solution, model.initial):
        raise RuntimeError("Zgjidhja Sudoku nuk kaloi validimin.")
    return result
