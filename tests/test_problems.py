import json
from pathlib import Path
import pytest
from src.problems import sudoku, latin_square, eight_puzzle, missionaries_cannibals as mc
from src.problems.social_golfers import Golfers, maximize
from src.problems.workforce_scheduling import Workforce
from src.utils.metrics import Limits, Context


def test_golfers_validation_and_maximum():
    config = Golfers(2, 2, 3)
    result = config.solve()
    assert result.status == "solved" and config.validate(result.solution)
    assert not config.validate(((0, 1), (2, 3)) * 3)
    assert Golfers(2, 2, 4).solve().status == "exhausted"
    assert maximize(Golfers(2, 2, 1))["proven_optimal"]
    assert Golfers().upper_bound == 10


@pytest.mark.parametrize("name", ["easy", "medium", "hard"])
def test_sudoku_fixtures(name):
    fixture = json.loads((Path("data/sudoku") / f"{name}.json").read_text(encoding="utf-8"))
    result = sudoku.solve(fixture["grid"], Limits(max_seconds=10))
    assert result.status == "solved"
    assert sudoku.valid_solution(result.solution, sudoku.parse_grid(fixture["grid"]))


@pytest.mark.parametrize("grid", [[0] * 80, [10] * 81, [True] * 81, [[0] * 8] * 9, [1, 1] + [0] * 79])
def test_sudoku_invalid_input(grid):
    with pytest.raises(ValueError):
        sudoku.solve(grid)


def test_sudoku_unsolvable():
    grid = [0] * 81
    grid[:8] = range(1, 9)
    grid[17] = 9
    assert sudoku.solve(grid).status == "exhausted"
    assert not sudoku.valid_solution([0] * 81)


@pytest.mark.parametrize("n", [3, 4, 5])
def test_latin_square(n):
    result = latin_square.solve(n, Limits(max_seconds=10, max_nodes=2_000_000, max_depth=n*n))
    assert result.status == "solved"
    assert latin_square.valid_square(result.solution, n)
    assert result.stats.depth_limits == list(range(n*n + 1))
    assert not latin_square.valid_square((1,) * (n*n), n)


def test_puzzle_moves_parity_and_algorithms():
    model = eight_puzzle.problem()
    assert len(list(model.successors(model.initial, None))) == 4
    assert not eight_puzzle.reachable((2, 1, 3, 4, 5, 6, 7, 8, 0))
    for algorithm in ("bfs", "dfs", "iddfs"):
        result = eight_puzzle.solve((1, 2, 3, 4, 5, 6, 7, 0, 8), algorithm, Limits(max_depth=3))
        assert result.status == "solved"
        assert result.solution == eight_puzzle.GOAL
    with pytest.raises(ValueError):
        eight_puzzle.problem((0,) * 9)


def test_missionaries_shortest_and_safety():
    result = mc.solve()
    assert result.status == "solved" and len(result.actions) == 11
    assert all(mc.safe(state) for state in result.path)
    assert not mc.safe((1, 2, 0))
    assert mc.solve("dfs").status == "solved"
    # Enumerate reachable legal graph independently of the search algorithm.
    seen, todo = {(3, 3, 0)}, [(3, 3, 0)]
    while todo:
        for _, child in mc.successors(todo.pop(), None):
            if child not in seen:
                seen.add(child)
                todo.append(child)
    assert len(seen) == 16


def test_workforce_constraints_and_optimum():
    config = Workforce(employees=3, days=2, max_shifts=2, unavailable=frozenset({(0, 0)}))
    result = config.solve()
    assert result.status == "optimal" and config.validate(result.solution)
    assert result.objective == 6
    assert not config.validate(((1,), (1,), (2,), (2,)))
    assert Workforce(employees=2, days=3, max_shifts=1).solve().status == "exhausted"


def test_workforce_preferences_and_zero_demand():
    config = Workforce(employees=2, days=1, demand=(1, 0), unwanted=frozenset({(0, 0)}))
    result = config.solve()
    assert result.solution == ((1,), ())
    assert result.objective == 1


def test_workforce_infeasible_rest():
    config = Workforce(employees=1, days=1, max_shifts=2, rest_slots=1)
    assert config.solve().status == "exhausted"


def test_workforce_matches_independent_exhaustive_cost():
    from itertools import product
    config = Workforce(employees=3, days=2, max_shifts=3, unwanted=frozenset({(0, 0), (1, 2)}))
    feasible = []
    for assignments in product(range(3), repeat=4):
        if any(a == b for a, b in zip(assignments, assignments[1:])):
            continue
        loads = [assignments.count(e) for e in range(3)]
        if max(loads) > 3:
            continue
        feasible.append(sum(v*v for v in loads) + 2 * sum((e, i) in config.unwanted for i, e in enumerate(assignments)))
    result = config.solve()
    assert result.status == "optimal"
    assert result.objective == min(feasible)


def test_workforce_depth_limit_does_not_claim_optimal():
    result = Workforce().solve(Limits(max_depth=1))
    assert result.status == "cutoff" and result.solution is None


@pytest.mark.parametrize("factory", [lambda: Golfers(1.5, 2, 3), lambda: Workforce(demand=(1,)),
                                     lambda: Workforce(unavailable=frozenset({(0, 99)})),
                                     lambda: Limits(max_seconds=float("nan"))])
def test_invalid_configuration(factory):
    with pytest.raises(ValueError):
        factory()
