"""Feasibility backtracking is DFS over constraint-pruned partial assignments."""
from src.algorithms.dfs import dfs
from src.utils.metrics import Limits, Problem, SearchResult, S


def backtracking(problem: Problem[S], limits: Limits = Limits()) -> SearchResult[S]:
    """Successor generation owns domain pruning; DFS owns undo/path traversal."""
    return dfs(problem, limits)


def minimize(problem, cost, lower_bound, limits=Limits()):
    """DFS branch-and-bound; retain an incumbent when interrupted by limits."""
    from src.utils.metrics import Context, ResourceLimit
    context = Context(limits)
    best_path, best_actions, best_cost = [], [], float("inf")
    root = context.record(problem.initial, None, "Fillimi", 0)
    stack = [(problem.initial, [problem.initial], [], root)]
    cutoff = False
    try:
        while stack:
            context.check()
            state, path, actions, trace_id = stack.pop()
            depth = len(actions)
            context.stats.max_depth = max(context.stats.max_depth, depth)
            if lower_bound(state) >= best_cost:
                context.stats.rejected += 1
                continue
            if problem.is_goal(state):
                value = cost(state)
                if value < best_cost:
                    best_cost, best_path, best_actions = value, path, actions
                continue
            if depth >= limits.max_depth:
                cutoff = True
                continue
            context.stats.expanded += 1
            children = []
            for action, child in problem.successors(state, context):
                context.stats.generated += 1
                context.check()
                child_id = context.record(child, trace_id, action, depth + 1)
                children.append((child, path + [child], actions + [action], child_id))
                if len(stack) + len(children) > limits.max_frontier:
                    raise ResourceLimit("U arrit kufiri i frontit DFS.")
            stack.extend(reversed(children))
            context.stats.max_frontier = max(context.stats.max_frontier, len(stack))
            if not children:
                context.stats.backtracks += 1
        status = "cutoff" if cutoff else "optimal" if best_path else "exhausted"
        result = context.finish(status, best_path, best_actions)
    except ResourceLimit as error:
        result = context.finish("limit", best_path, best_actions, str(error))
    result.objective = best_cost if best_path else None
    return result
