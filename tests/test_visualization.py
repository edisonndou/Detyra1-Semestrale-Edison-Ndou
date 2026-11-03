from src.problems.missionaries_cannibals import solve
from src.visualization.search_tree import export_tree, to_dot, path_nodes
from src.visualization.performance_charts import performance_chart


def test_tree_fallback_exports_and_path(tmp_path):
    result = solve()
    assert "digraph" in to_dot(result)
    assert path_nodes(result)
    for format in ("svg", "png"):
        path = export_tree(result, tmp_path / "tree", format, engine="networkx")
        assert path.stat().st_size > 100
        assert b"<svg" in path.read_bytes() if format == "svg" else path.read_bytes().startswith(b"\x89PNG")


def test_measurement_chart(tmp_path):
    path = performance_chart([{"name": "provë", "elapsed_seconds": 0.1, "expanded": 5}], tmp_path / "chart.png")
    assert path.read_bytes().startswith(b"\x89PNG")
