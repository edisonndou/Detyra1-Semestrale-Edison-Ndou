"""Bounded trace rendering; Graphviz preferred, NetworkX/Matplotlib fallback."""
from pathlib import Path
import textwrap
import shutil
import subprocess


def graphviz_executable() -> str | None:
    """Prefer PATH, then the optional project-local portable installation."""
    installed = shutil.which("dot")
    if installed:
        return installed
    portable = Path(__file__).resolve().parents[2] / ".tools/graphviz"
    if portable.is_dir():
        return next((str(path) for path in sorted(portable.glob("**/bin/dot.exe"))), None)
    return None


def path_nodes(result):
    """Match a solution prefix using parent identity, including repeated IDDFS roots."""
    selected = set()
    parents = {None}
    for depth, state in enumerate(result.path):
        matching = {node.id for node in result.trace
                    if node.depth == depth and node.state == str(state)
                    and node.parent in parents and not node.rejected}
        selected.update(matching)
        parents = matching
        if not parents:
            break
    return selected


def node_color(node, result, selected):
    """Rejected duplicates retain their status even when they equal the goal state."""
    if node.rejected:
        return "#fbe6e6"
    if node.id in selected and node.state == str(result.solution):
        return "#a8d7b9"
    if node.depth == 0:
        return "#dce8f5"
    return "#e5f2ed" if node.id in selected else "#f4f5f7"


def to_dot(result):
    from graphviz import Digraph
    graph = Digraph("search", graph_attr={"rankdir": "TB", "bgcolor": "white"})
    selected = path_nodes(result)
    for node in result.trace:
        color = node_color(node, result, selected)
        # Large states are abbreviated; full values remain in the JSON trace.
        label = f"#{node.id} · d={node.depth}\n" + textwrap.fill(node.state[:150], 38)
        graph.node(str(node.id), label, style="filled", fillcolor=color, shape="box", fontname="Arial")
        if node.parent is not None:
            graph.edge(str(node.parent), str(node.id), node.action[:70],
                       color="#26745a" if node.id in selected else "#89939f", fontname="Arial")
    return graph.source


def export_tree(result, destination, format="svg", engine="auto"):
    if format not in ("png", "svg") or engine not in ("auto", "graphviz", "networkx"):
        raise ValueError("Formatet: png/svg. Motorët: auto/graphviz/networkx.")
    destination = Path(destination).with_suffix("." + format)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if engine != "networkx":
        executable = graphviz_executable()
        if executable:
            content = subprocess.run([executable, f"-T{format}"], input=to_dot(result).encode("utf-8"),
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=30).stdout
            destination.write_bytes(content)
            return destination
        if engine == "graphviz":
            raise FileNotFoundError("Graphviz dot mungon në PATH dhe te .tools/graphviz.")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx
    graph = nx.DiGraph()
    for node in result.trace:
        graph.add_node(node.id)
        if node.parent is not None:
            graph.add_edge(node.parent, node.id)
    by_depth = {}
    for node in result.trace:
        by_depth.setdefault(node.depth, []).append(node.id)
    positions = {node: ((i + 1) / (len(level) + 1), -depth)
                 for depth, level in by_depth.items() for i, node in enumerate(level)}
    selected = path_nodes(result)
    colors = [node_color(node, result, selected) for node in result.trace]
    fig, ax = plt.subplots(figsize=(22, max(6, len(by_depth) * 2.2)))
    labels = {node.id: f"#{node.id} d={node.depth}\n{node.state[:48]}" for node in result.trace}
    edge_colors = ["#26745a" if child in selected and parent in selected else "#89939f"
                   for parent, child in graph.edges]
    nx.draw_networkx(graph, positions, ax=ax, labels=labels, node_color=colors, edge_color=edge_colors,
                     node_shape="s", node_size=1800, font_size=5, arrows=True)
    nx.draw_networkx_edge_labels(graph, positions, ax=ax,
                                edge_labels={(n.parent, n.id): n.action[:28] for n in result.trace if n.parent is not None},
                                font_size=4)
    ax.set_title("Pemë e kufizuar: blu = fillimi; gjelbër = rruga; kuqe = refuzim")
    ax.axis("off")
    fig.savefig(destination, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return destination
