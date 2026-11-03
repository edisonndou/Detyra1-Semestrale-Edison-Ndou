"""Genuine iterative deepening: every depth starts again from the root."""
from src.algorithms.dfs import _depth_search
from src.utils.metrics import Context, Limits, Problem, ResourceLimit, SearchResult, S


def iddfs(problem: Problem[S], limits: Limits = Limits()) -> SearchResult[S]:
    context = Context(limits)
    try:
        for depth in range(limits.max_depth + 1):
            context.stats.depth_limits.append(depth)
            if depth:
                context.stats.generated += 1
            context.check()
            path, actions, cutoff = _depth_search(problem, context, depth)
            if path:
                return context.finish("solved", path, actions)
            if not cutoff:
                return context.finish("exhausted")
        return context.finish("cutoff", message="U arrit thellësia maksimale e IDDFS.")
    except ResourceLimit as error:
        return context.finish("limit", message=str(error))
