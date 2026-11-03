import pytest
from src.algorithms import bfs, dfs, iddfs, depth_limited_search, backtracking
from src.utils.metrics import Limits, Problem


def graph():
    edges = {0: (1, 2), 1: (0, 3), 2: (4,), 3: (4,), 4: ()}
    return Problem(0, lambda s: s == 4, lambda s, c: ((str(v), v) for v in edges[s]))


@pytest.mark.parametrize("algorithm", [bfs, dfs, iddfs, backtracking])
def test_search_returns_legal_path(algorithm):
    result = algorithm(graph(), Limits(max_depth=8))
    assert result.status == "solved"
    assert result.path[0] == 0 and result.path[-1] == 4
    assert len(result.actions) == len(result.path) - 1
    for a, b in zip(result.path, result.path[1:]):
        assert b in [v for _, v in graph().successors(a, None)]


def test_bfs_shortest_and_dfs_not_promised_shortest():
    assert bfs(graph()).path == [0, 2, 4]
    assert dfs(graph()).path == [0, 1, 3, 4]


def test_iddfs_repeats_all_limits():
    result = iddfs(graph())
    assert result.stats.depth_limits == [0, 1, 2]
    assert len(result.actions) == 2


def test_backtracking_recovers_from_dead_end():
    edges = {0: (1, 2), 1: (), 2: (3,), 3: ()}
    model = Problem(0, lambda s: s == 3, lambda s, c: ((str(v), v) for v in edges[s]))
    result = backtracking(model)
    assert result.path == [0, 2, 3]
    assert result.stats.backtracks > 0


@pytest.mark.parametrize("algorithm", [bfs, dfs, iddfs])
def test_exhausted_and_cycles(algorithm):
    model = Problem(0, lambda s: False, lambda s, c: [("cycle", 0)])
    assert algorithm(model).status == "exhausted"


@pytest.mark.parametrize("algorithm", [bfs, dfs, iddfs])
def test_limits_do_not_claim_unsolvable(algorithm):
    assert algorithm(graph(), Limits(max_nodes=1)).status == "limit"
    assert algorithm(graph(), Limits(max_depth=0)).status == "cutoff"


def test_depth_limited_and_trace_bound():
    assert depth_limited_search(graph(), 1).status == "cutoff"
    assert depth_limited_search(graph(), 2).status == "solved"
    assert len(bfs(graph(), Limits(trace_nodes=2)).trace) == 2
    assert bfs(graph(), Limits(max_frontier=1)).status == "limit"
    assert bfs(graph(), Limits(max_seconds=1e-12)).status == "limit"


def test_input_limits():
    with pytest.raises(ValueError):
        Limits(max_seconds=0)
