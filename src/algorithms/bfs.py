"""FIFO graph search with global duplicate detection."""
from collections import deque
from src.utils.metrics import Context, Limits, Problem, ResourceLimit, SearchResult, S


def bfs(problem: Problem[S], limits: Limits = Limits()) -> SearchResult[S]:
    context = Context(limits)
    root = context.record(problem.initial, None, "Fillimi", 0)
    queue = deque([(problem.initial, 0, root)])
    parents = {problem.initial: (None, "")}
    cutoff = False
    try:
        while queue:
            context.check()
            state, depth, trace_id = queue.popleft()
            context.stats.max_depth = max(context.stats.max_depth, depth)
            if problem.is_goal(state):
                path, actions = [], []
                current = state
                while True:
                    path.append(current)
                    if current == problem.initial:
                        break
                    previous, action = parents[current]
                    actions.append(action)
                    current = previous
                return context.finish("solved", path[::-1], actions[::-1])
            if depth >= limits.max_depth:
                cutoff = True
                continue
            context.stats.expanded += 1
            for action, child in problem.successors(state, context):
                context.check()
                context.stats.generated += 1
                context.check()
                duplicate = child in parents
                child_trace = context.record(child, trace_id, action, depth + 1, duplicate)
                if duplicate:
                    context.stats.rejected += 1
                    continue
                if len(queue) >= limits.max_frontier:
                    raise ResourceLimit("U arrit kufiri i radhës FIFO.")
                parents[child] = (state, action)
                queue.append((child, depth + 1, child_trace))
                context.stats.max_frontier = max(context.stats.max_frontier, len(queue))
        return context.finish("cutoff" if cutoff else "exhausted")
    except ResourceLimit as error:
        return context.finish("limit", message=str(error))
