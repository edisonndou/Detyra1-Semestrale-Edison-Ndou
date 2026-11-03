"""Canonical group construction with pair pruning and week-one symmetry breaking."""
from dataclasses import dataclass
from itertools import combinations
from math import factorial
from src.algorithms import backtracking
from src.utils.metrics import Context, Limits, Problem, SearchResult

Schedule = tuple[tuple[tuple[int, ...], ...], ...]
GolfState = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class Golfers:
    groups: int = 8
    players: int = 4
    weeks: int = 2

    def __post_init__(self):
        if any(type(value) is not int for value in (self.groups, self.players, self.weeks)):
            raise ValueError("Parametrat e golfistëve duhet të jenë numra të plotë.")
        if min(self.groups, self.players, self.weeks) < 1:
            raise ValueError("Grupet, lojtarët dhe javët duhet të jenë pozitivë.")

    @property
    def n(self) -> int:
        return self.groups * self.players

    @property
    def upper_bound(self) -> int | None:
        return (self.n - 1) // (self.players - 1) if self.players > 1 else None

    @property
    def partitions(self) -> int:
        return factorial(self.n) // (factorial(self.players) ** self.groups * factorial(self.groups))

    def problem(self) -> Problem[GolfState]:
        # State is a flat tuple of complete groups. Each transition fills one group.
        first = tuple(tuple(range(i, i + self.players)) for i in range(0, self.n, self.players))

        def successors(state, context: Context):
            complete = len(state) // self.groups
            in_week = len(state) % self.groups
            used_pairs = {pair for group in state[:complete * self.groups] for pair in combinations(group, 2)}
            current = state[complete * self.groups:]
            remaining = sorted(set(range(self.n)) - {p for group in current for p in group})
            if not remaining:
                return
            anchor = remaining[0]
            # Smallest remaining player anchors the next unlabeled group.
            for rest in combinations(remaining[1:], self.players - 1):
                context.check()
                group = (anchor,) + rest
                if any(pair in used_pairs for pair in combinations(group, 2)):
                    context.stats.rejected += 1
                    continue
                yield f"Java {complete + 1}, grupi {in_week + 1}: {group}", state + (group,)

        return Problem(first, lambda state: len(state) == self.weeks * self.groups, successors)

    def solve(self, limits: Limits = Limits()) -> SearchResult[GolfState]:
        if self.upper_bound is not None and self.weeks > self.upper_bound:
            from src.utils.metrics import Context
            return Context(limits).finish("exhausted", message="Javët tejkalojnë kufirin teorik.")
        result = backtracking(self.problem(), limits)
        if result.solution is not None and not self.validate(result.solution):
            raise RuntimeError("Orari i golfistëve dështoi në validimin përfundimtar.")
        return result

    def validate(self, flat: GolfState) -> bool:
        if len(flat) != self.weeks * self.groups:
            return False
        seen = set()
        for week in range(self.weeks):
            groups = flat[week * self.groups:(week + 1) * self.groups]
            if any(len(group) != self.players for group in groups):
                return False
            if sorted(player for group in groups for player in group) != list(range(self.n)):
                return False
            for group in groups:
                for pair in combinations(sorted(group), 2):
                    if pair in seen:
                        return False
                    seen.add(pair)
        return True


def maximize(config: Golfers, limits: Limits = Limits()):
    """Find consecutive feasible week counts; a limited run leaves optimality open."""
    if config.players == 1:
        raise ValueError("Me një lojtar për grup nuk ka maksimum të fundëm javësh.")
    runs = []
    best = None
    for weeks in range(1, config.upper_bound + 1):
        result = Golfers(config.groups, config.players, weeks).solve(limits)
        runs.append((weeks, result))
        if result.status != "solved":
            return {"best_weeks": best, "proven_optimal": result.status == "exhausted", "runs": runs}
        best = weeks
    return {"best_weeks": best, "proven_optimal": True, "runs": runs}
