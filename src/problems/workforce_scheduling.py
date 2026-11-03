"""Configurable shift staffing with hard constraints and a fairness objective."""
from dataclasses import dataclass
from itertools import combinations
from src.algorithms.backtracking import minimize
from src.utils.metrics import Limits, Problem, SearchResult

WorkforceState = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class Workforce:
    employees: int = 6
    days: int = 7
    shifts_per_day: int = 2
    demand: tuple[int, ...] = ()
    max_shifts: int = 4
    rest_slots: int = 1
    unavailable: frozenset[tuple[int, int]] = frozenset()
    unwanted: frozenset[tuple[int, int]] = frozenset()
    preference_weight: int = 2

    def __post_init__(self):
        if any(type(value) is not int for value in (self.employees, self.days, self.shifts_per_day,
                                                   self.max_shifts, self.rest_slots, self.preference_weight)):
            raise ValueError("Parametrat e planifikimit duhet të jenë numra të plotë.")
        object.__setattr__(self, "demand", tuple(self.demand))
        for field in ("unavailable", "unwanted"):
            pairs = frozenset(tuple(pair) for pair in getattr(self, field))
            if any(len(pair) != 2 or any(type(v) is not int for v in pair) for pair in pairs):
                raise ValueError("Kufizimet presin çifte numrash të plotë (punonjësi, ndërrimi).")
            object.__setattr__(self, field, pairs)
        if min(self.employees, self.days, self.shifts_per_day) < 1:
            raise ValueError("Punonjësit, ditët dhe ndërrimet duhet të jenë pozitivë.")
        if min(self.max_shifts, self.rest_slots, self.preference_weight) < 0:
            raise ValueError("Kufijtë dhe peshat nuk mund të jenë negative.")
        if not self.demand:
            object.__setattr__(self, "demand", (1,) * self.slots)
        if len(self.demand) != self.slots or any(type(d) is not int or not 0 <= d <= self.employees for d in self.demand):
            raise ValueError("Kërkesa duhet të ketë një numër 0..punonjës për çdo ndërrim.")
        for employee, slot in self.unavailable | self.unwanted:
            if not 0 <= employee < self.employees or not 0 <= slot < self.slots:
                raise ValueError("Punonjësi ose ndërrimi në kufizime është jashtë intervalit.")

    @property
    def slots(self) -> int:
        return self.days * self.shifts_per_day

    def loads(self, state: WorkforceState) -> list[int]:
        return [sum(employee in shift for shift in state) for employee in range(self.employees)]

    def eligible(self, state: WorkforceState, employee: int) -> bool:
        slot = len(state)
        return ((employee, slot) not in self.unavailable
                and self.loads(state)[employee] < self.max_shifts
                and all(employee not in shift for shift in state[max(0, slot - self.rest_slots):]))

    def cost(self, state: WorkforceState) -> int:
        return sum(load * load for load in self.loads(state)) + self.preference_weight * sum(
            (employee, slot) in self.unwanted for slot, shift in enumerate(state) for employee in shift)

    def lower_bound(self, state: WorkforceState) -> int:
        loads = self.loads(state)
        # Relaxed allocation ignoring rest/availability cannot overestimate optimum.
        for _ in range(sum(self.demand[len(state):])):
            index = min(range(self.employees), key=lambda e: (loads[e], e))
            loads[index] += 1
        penalties = self.preference_weight * sum((e, s) in self.unwanted for s, shift in enumerate(state) for e in shift)
        return sum(load * load for load in loads) + penalties

    def conflicts(self) -> list[str]:
        issues = []
        if sum(self.demand) > self.employees * self.max_shifts:
            issues.append("Kërkesa totale tejkalon kapacitetin maksimal të punonjësve.")
        for slot, demand in enumerate(self.demand):
            available = sum((e, slot) not in self.unavailable for e in range(self.employees))
            if demand > available:
                issues.append(f"Ndërrimi {slot}: kërkohen {demand}, por janë të disponueshëm {available}.")
        return issues

    def problem(self) -> Problem[WorkforceState]:
        def successors(state, context):
            slot = len(state)
            eligible = [e for e in range(self.employees) if self.eligible(state, e)]
            context.stats.rejected += self.employees - len(eligible)
            candidates = combinations(eligible, self.demand[slot])
            teams = []
            for team in candidates:
                context.check()
                if len(teams) >= context.limits.max_frontier:
                    from src.utils.metrics import ResourceLimit
                    raise ResourceLimit("Shumë ekipe kandidate për kufirin e frontit.")
                teams.append(team)
            # Ordering changes exploration only, not the hard constraints/objective.
            teams = sorted(teams, key=lambda team: (self.cost(state + (team,)), team))
            for team in teams:
                context.check()
                yield f"Dita {slot // self.shifts_per_day + 1}, ndërrimi {slot % self.shifts_per_day + 1}: {team}", state + (team,)
        return Problem((), lambda state: len(state) == self.slots, successors)

    def validate(self, state: WorkforceState) -> bool:
        if len(state) != self.slots:
            return False
        for slot, team in enumerate(state):
            if len(team) != self.demand[slot] or len(set(team)) != len(team):
                return False
            for employee in team:
                if type(employee) is not int or not 0 <= employee < self.employees:
                    return False
                if (employee, slot) in self.unavailable:
                    return False
                if any(employee in earlier for earlier in state[max(0, slot - self.rest_slots):slot]):
                    return False
        return max(self.loads(state), default=0) <= self.max_shifts

    def solve(self, limits: Limits = Limits()) -> SearchResult[WorkforceState]:
        if self.conflicts():
            from src.utils.metrics import Context
            return Context(limits).finish("exhausted", message=" ".join(self.conflicts()))
        result = minimize(self.problem(), self.cost, self.lower_bound, limits)
        if result.solution is not None and not self.validate(result.solution):
            raise RuntimeError("Orari nuk kaloi validimin e kufizimeve.")
        return result
