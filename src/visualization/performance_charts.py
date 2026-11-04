"""Charts consume measured rows only; no synthetic benchmark values."""
from pathlib import Path


def performance_chart(rows, destination):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))
    labels = [row["name"] for row in rows]
    for ax, field, title in zip(axes, ("elapsed_seconds", "expanded"), ("Koha (s)", "Gjendje të zgjeruara")):
        ax.barh(labels, [row[field] for row in rows], color="#286454")
        ax.set_xlabel(title)
        ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(destination, dpi=150)
    plt.close(fig)
    return destination
