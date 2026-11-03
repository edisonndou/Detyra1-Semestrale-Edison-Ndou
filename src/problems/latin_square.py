"""Row-major Latin Square CSP solved by genuine iterative deepening."""
from src.algorithms import iddfs
from src.utils.metrics import Context, Limits, Problem, SearchResult


def valid_square(state: tuple[int, ...], n: int) -> bool:
    target = set(range(1, n + 1))
    return (len(state) == n * n and all(set(state[r * n:(r + 1) * n]) == target for r in range(n))
            and all(set(state[c::n]) == target for c in range(n)))


def problem(n: int) -> Problem[tuple[int, ...]]:
    if type(n) is not int or not 1 <= n <= 30:
        raise ValueError("Madhësia n duhet të jetë numër i plotë nga 1 deri në 30.")

    def successors(state, context: Context):
        index = len(state)
        row, col = divmod(index, n)
        used = set(state[row * n:]) | set(state[col::n])
        # Any Latin square can be reduced by permuting symbols and rows.
        # Assign the canonical first row/column one cell per transition;
        # all IDDFS limits still execute, and inner cells remain searched.
        domain = (col + 1,) if row == 0 else (row + 1,) if col == 0 else range(1, n + 1)
        for value in domain:
            context.check()
            if value in used:
                context.stats.rejected += 1
            else:
                yield f"R{row + 1}K{col + 1} = {value}", state + (value,)

    return Problem((), lambda state: len(state) == n * n, successors)


def solve(n: int = 3, limits: Limits = Limits()) -> SearchResult[tuple[int, ...]]:
    result = iddfs(problem(n), limits)
    if result.solution is not None and not valid_square(result.solution, n):
        raise RuntimeError("Katrori Latin nuk kaloi validimin.")
    return result
