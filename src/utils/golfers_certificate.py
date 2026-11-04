"""Load an attributed existence certificate, never a replacement search result."""
from itertools import combinations
from pathlib import Path
import json
from src.problems.social_golfers import Golfers

DEFAULT_CERTIFICATE = Path(__file__).resolve().parents[2] / "data/golfers/aguado_8_4_10.json"


def verify_certificate(document: dict) -> dict:
    """Check coverage, group sizes and every pair independently of DFS generation."""
    model = Golfers(document["groups"], document["players"], document["weeks"])
    schedule = document["schedule"]
    if len(schedule) != model.weeks or any(len(week) != model.groups for week in schedule):
        raise ValueError("Dëshmia nuk ka numrin e kërkuar të javëve ose grupeve.")
    flat = tuple(tuple(group) for week in schedule for group in week)
    if any(type(player) is not int for group in flat for player in group) or not model.validate(flat):
        raise ValueError("Dëshmia përmban caktime të pavlefshme ose çifte të përsëritura.")
    # A second, player-centric check does not depend on the search/validator pair set.
    opponents = [set() for _ in range(model.n)]
    for group in flat:
        for player in group:
            others = set(group) - {player}
            if opponents[player] & others:
                raise ValueError("Një lojtar ka takuar të njëjtin kundërshtar më shumë se një herë.")
            opponents[player].update(others)
    counts = [len(others) for others in opponents]
    expected = model.weeks * (model.players - 1)
    if any(count != expected for count in counts):
        raise ValueError("Numri i kundërshtarëve unikë nuk përputhet me javët.")
    used = {pair for group in flat for pair in combinations(sorted(group), 2)}
    missing = sorted(set(combinations(range(model.n), 2)) - used)
    upper = model.upper_bound
    return {**document, "valid": True, "origin": "published_certificate",
            "upper_bound": upper, "maximum_weeks": model.weeks if upper == model.weeks else None,
            "proven_optimal": upper is not None and upper == model.weeks,
            "distinct_pairs": len(used), "repeated_pairs": 0,
            "distinct_opponents_per_player": counts, "unused_pairs": missing,
            "proof": f"Orari i validuar realizon {model.weeks} javë; kufiri i sipërm është {upper}. "
                     "Kur kufijtë përputhen, maksimumi është i provuar. Nuk pretendohet se DFS e zbuloi dëshminë."}


def load_certificate(path: Path = DEFAULT_CERTIFICATE) -> dict:
    """Read the bundled research data and reject corruption before presenting proof."""
    return verify_certificate(json.loads(path.read_text(encoding="utf-8")))
