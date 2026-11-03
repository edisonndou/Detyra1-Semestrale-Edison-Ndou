"""Iterative-stack DFS and depth-limited backtracking, with path cycle checks."""
from src.utils.metrics import Context, Limits, Problem, ResourceLimit, SearchResult, S


def _depth_search(problem, context, depth_limit, graph_search=False):
    path = [problem.initial]
    actions = []
    active = {problem.initial}
    visited = {problem.initial} if graph_search else set()
    root = context.record(problem.initial, None, "Fillimi", 0)
    # Frames retain successor iterators rather than whole sibling frontiers.
    stack = [(problem.initial, root, None)]
    cutoff = False
    while stack:
        context.check()
        state, trace_id, iterator = stack[-1]
        depth = len(path) - 1
        context.stats.max_depth = max(context.stats.max_depth, depth)
        context.stats.max_frontier = max(context.stats.max_frontier, len(stack))
        if iterator is None:
            if problem.is_goal(state):
                return list(path), list(actions), cutoff
            if depth >= depth_limit:
                cutoff = True
                iterator = iter(())
            else:
                context.stats.expanded += 1
                iterator = iter(problem.successors(state, context))
            stack[-1] = (state, trace_id, iterator)
        try:
            action, child = next(iterator)
        except StopIteration:
            stack.pop()
            active.remove(path.pop())
            if actions:
                actions.pop()
            context.stats.backtracks += 1
            continue
        context.stats.generated += 1
        context.check()
        duplicate = child in (visited if graph_search else active)
        child_trace = context.record(child, trace_id, action, depth + 1, duplicate)
        if duplicate:
            context.stats.rejected += 1
            continue
        if len(stack) >= context.limits.max_frontier:
            raise ResourceLimit("U arrit kufiri i stivës DFS.")
        path.append(child)
        actions.append(action)
        active.add(child)
        if graph_search:
            visited.add(child)
        stack.append((child, child_trace, None))
    return [], [], cutoff


def depth_limited_search(problem: Problem[S], depth: int, limits: Limits = Limits(), *, graph_search=False) -> SearchResult[S]:
    if depth < 0:
        raise ValueError("Kufiri i thellësisë duhet të jetë jonegativ.")
    context = Context(limits)
    try:
        path, actions, cutoff = _depth_search(problem, context, min(depth, limits.max_depth), graph_search)
        return context.finish("solved" if path else "cutoff" if cutoff else "exhausted", path, actions)
    except ResourceLimit as error:
        return context.finish("limit", message=str(error))


def dfs(problem: Problem[S], limits: Limits = Limits(), *, graph_search=False) -> SearchResult[S]:
    return depth_limited_search(problem, limits.max_depth, limits, graph_search=graph_search)
