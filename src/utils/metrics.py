"""Shared search contracts, bounded tracing and resource accounting."""
from dataclasses import dataclass, field
from time import perf_counter
from math import isfinite
from typing import Callable, Generic, Hashable, Iterable, TypeVar

S = TypeVar("S", bound=Hashable)


@dataclass(frozen=True)
class Limits:
    max_seconds: float = 5.0
    max_nodes: int = 100_000
    max_frontier: int = 50_000
    max_depth: int = 100
    trace_nodes: int = 150
    trace_depth: int = 8
    reconstruct_path: bool = True

    def __post_init__(self) -> None:
        if type(self.reconstruct_path) is not bool:
            raise ValueError("reconstruct_path duhet të jetë boolean.")
        if not isfinite(self.max_seconds):
            raise ValueError("Koha duhet të jetë numër i fundëm.")
        if any(type(value) is not int for value in (self.max_nodes, self.max_frontier, self.max_depth, self.trace_nodes, self.trace_depth)):
            raise ValueError("Kufijtë e numërimit duhet të jenë numra të plotë.")
        if self.max_seconds <= 0 or min(self.max_nodes, self.max_frontier) < 1:
            raise ValueError("Koha, nyjet dhe kufiri i frontit duhet të jenë pozitivë.")
        if min(self.max_depth, self.trace_nodes, self.trace_depth) < 0:
            raise ValueError("Thellësia dhe kufijtë e pemës nuk mund të jenë negativë.")


@dataclass
class Statistics:
    expanded: int = 0
    generated: int = 1
    rejected: int = 0
    backtracks: int = 0
    max_frontier: int = 1
    max_depth: int = 0
    max_recursion_depth: int = 0
    elapsed_seconds: float = 0.0
    depth_limits: list[int] = field(default_factory=list)


@dataclass
class TraceNode:
    id: int
    parent: int | None
    state: str
    action: str
    depth: int
    rejected: bool = False


@dataclass
class SearchResult(Generic[S]):
    status: str
    path: list[S]
    actions: list[str]
    stats: Statistics
    trace: list[TraceNode]
    message: str = ""
    objective: float | None = None
    final_state: S | None = None

    @property
    def solution(self) -> S | None:
        return self.path[-1] if self.path else self.final_state


class ResourceLimit(Exception):
    """Controlled termination; never interpreted as proof of infeasibility."""


class Context:
    def __init__(self, limits: Limits) -> None:
        self.limits = limits
        self.stats = Statistics()
        self.trace: list[TraceNode] = []
        self.started = perf_counter()

    def check(self) -> None:
        if perf_counter() - self.started >= self.limits.max_seconds:
            raise ResourceLimit("U arrit kufiri kohor.")
        if self.stats.generated > self.limits.max_nodes:
            raise ResourceLimit("U arrit kufiri i nyjeve të gjeneruara.")

    def record(self, state: Hashable, parent: int | None, action: str, depth: int, rejected: bool = False) -> int | None:
        if depth > self.limits.trace_depth or len(self.trace) >= self.limits.trace_nodes:
            return None
        # Omitted ancestors must not produce disconnected trace fragments.
        if parent is None and depth > 0:
            return None
        index = len(self.trace)
        self.trace.append(TraceNode(index, parent, str(state), action, depth, rejected))
        return index

    def finish(self, status: str, path: list[S] | None = None, actions: list[str] | None = None, message: str = "") -> SearchResult[S]:
        self.stats.elapsed_seconds = perf_counter() - self.started
        resolved_path = path if path is not None else []
        final_state = resolved_path[-1] if resolved_path else None
        stored_path = resolved_path if self.limits.reconstruct_path else []
        stored_actions = (actions or []) if self.limits.reconstruct_path else []
        return SearchResult(status, stored_path, stored_actions, self.stats, self.trace, message,
                            final_state=final_state)


@dataclass(frozen=True)
class Problem(Generic[S]):
    initial: S
    is_goal: Callable[[S], bool]
    successors: Callable[[S, Context], Iterable[tuple[str, S]]]
