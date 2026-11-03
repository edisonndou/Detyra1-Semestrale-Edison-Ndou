"""Regression coverage for the final requirement audit and existence proof."""
from copy import deepcopy
from pathlib import Path
import json
import re
import subprocess
import sys
import pytest
from src.algorithms import bfs, dfs, iddfs, backtracking
from src.utils.metrics import Problem, Limits
from src.utils.golfers_certificate import load_certificate, verify_certificate
from src.visualization.search_tree import export_tree, graphviz_executable, to_dot
from src.problems.missionaries_cannibals import solve


def test_published_certificate_proves_ten_week_optimum():
    report = load_certificate()
    assert report["origin"] == "published_certificate"
    assert report["maximum_weeks"] == report["upper_bound"] == 10
    assert report["valid"] and report["proven_optimal"]
    assert report["distinct_pairs"] == 480 and report["repeated_pairs"] == 0
    assert report["distinct_opponents_per_player"] == [30] * 32
    assert len(report["unused_pairs"]) == 16
    # Independent recount without calling the production validator.
    meetings = [[0] * 32 for _ in range(32)]
    for week in report["schedule"]:
        assert sorted(player for group in week for player in group) == list(range(32))
        for group in week:
            assert len(group) == 4
            for a in group:
                for b in group:
                    if a != b:
                        meetings[a][b] += 1
    assert all(meetings[a][b] <= 1 for a in range(32) for b in range(32))


def test_corrupt_certificate_is_rejected():
    document = deepcopy(load_certificate())
    document["schedule"][1] = document["schedule"][0]
    with pytest.raises(ValueError):
        verify_certificate(document)


def test_bfs_none_state_does_not_break_parent_reconstruction():
    model = Problem(0, lambda s: s == 1,
                    lambda s, c: [("pas None", None)] if s == 0 else [("qëllimi", 1)] if s is None else [])
    result = bfs(model)
    assert result.path == [0, None, 1] and len(result.actions) == 2


def test_complete_binary_tree_counts():
    model = Problem((0, 0), lambda s: False,
                    lambda s, c: [(str(i), (s[0] + 1, 2*s[1] + i)) for i in (0, 1)] if s[0] < 3 else [])
    for method in (bfs, dfs):
        result = method(model)
        assert result.status == "exhausted"
        assert result.stats.generated == result.stats.expanded == 15
        assert len(result.trace) == 15
    repeated = iddfs(model, Limits(max_depth=3))
    assert repeated.stats.generated == 26
    assert repeated.stats.depth_limits == [0, 1, 2, 3]


@pytest.mark.parametrize("method", [bfs, dfs, iddfs, backtracking])
def test_optional_path_reconstruction_preserves_solution(method):
    model = Problem(0, lambda s: s == 3, lambda s, c: [("hapi", s + 1)] if s < 3 else [])
    result = method(model, Limits(reconstruct_path=False))
    assert result.status == "solved" and result.solution == 3
    assert result.path == result.actions == []
    assert result.stats.max_recursion_depth == 0


def test_graphviz_native_exports_when_installed(tmp_path):
    if not graphviz_executable():
        pytest.skip("Graphviz native opsional nuk është i instaluar në këtë mjedis.")
    for format in ("png", "svg"):
        path = export_tree(solve(), tmp_path / "native", format, engine="graphviz")
        data = path.read_bytes()
        assert data.startswith(b"\x89PNG") if format == "png" else b"<svg" in data


def test_rejected_goal_duplicate_is_not_highlighted_as_accepted_goal():
    result = solve(limits=Limits(trace_depth=15))
    rejected_goals = [node for node in result.trace if node.rejected and node.state == str(result.solution)]
    assert rejected_goals
    dot = to_dot(result)
    for node in rejected_goals:
        attributes = re.search(rf"(?ms)^\s*{node.id} \[(.*?)\]\s*$", dot).group(1)
        assert '#fbe6e6' in attributes


def test_cli_certificate_export(tmp_path):
    output = tmp_path / "certificate.json"
    result = subprocess.run([sys.executable, "main.py", "golfers", "--certificate", "--output", str(output)],
                            capture_output=True, check=True)
    assert json.loads(result.stdout)["maximum_weeks"] == 10
    assert json.loads(output.read_text(encoding="utf-8"))["proven_optimal"]
