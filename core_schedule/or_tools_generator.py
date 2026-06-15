from __future__ import annotations

import logging
from ortools.sat.python import cp_model

from models import ClassSection, PersonalEvent
from csp_generator import _init_domains, _conflicts_with_personal_events

CourseGroups = dict[str, list[ClassSection]]
Domains = dict[str, list[ClassSection]]
ConflictSet = set[tuple[str, str]]
Schedule = dict[str, ClassSection]

logger = logging.getLogger(__name__)


def solve_schedule(
    course_groups: CourseGroups,
    conflict_set: ConflictSet,
    avoid_days: list[int],
    personal_events: list[PersonalEvent],
    max_solutions: int = 200,
) -> list[Schedule]:
    
    if not course_groups:
        return []

    if max_solutions <= 0:
        return []

    try:
        # lọc avoid days
        init = _init_domains(course_groups, avoid_days)

        # lọc personal events
        domains: Domains = {}
        for course_id, sections in init.items():
            domains[course_id] = []
            for cls in sections:
                if not _conflicts_with_personal_events(cls, personal_events):
                    domains[course_id].append(cls)

        if any(len(domains[c]) == 0 for c in domains):
            return []

        model = cp_model.CpModel()

        # Tạo biến quyết định
        course_vars: dict[str, cp_model.IntVar] = {}
        for course_id, options in domains.items():
            course_vars[course_id] = model.NewIntVar(
                0, len(options) - 1, f"choice_{course_id}"
            )

        # Ràng buộc xung đột cấm các cặp (i, j) xung đột nhau
        for course_id, var in course_vars.items():
            for other_course_id, other_var in course_vars.items():
                if other_course_id <= course_id:
                    continue

                for i, cls_a in enumerate(domains[course_id]):
                    for j, cls_b in enumerate(domains[other_course_id]):
                        if (cls_a.class_id, cls_b.class_id) in conflict_set:
                            model.AddForbiddenAssignments([var, other_var], [(i, j)])


        class SolutionCollector(cp_model.CpSolverSolutionCallback):
            def __init__(self, course_vars, domains, max_results):
                super().__init__()
                self._course_vars = course_vars
                self._domains = domains
                self._max_results = max_results
                self._solutions: list[Schedule] = []

            def on_solution_callback(self) -> None:
                schedule: Schedule = {}
                for cid, var in self._course_vars.items():
                    schedule[cid] = self._domains[cid][self.Value(var)]
                self._solutions.append(schedule)

                if len(self._solutions) >= self._max_results:
                    self.StopSearch()

            @property
            def solutions(self) -> list[Schedule]:
                return self._solutions

        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 10
        solver.parameters.num_search_workers = 1  
        solver.parameters.enumerate_all_solutions = True  

        collector = SolutionCollector(course_vars, domains, max_solutions)
        status = solver.Solve(model, collector)

        if status in (cp_model.INFEASIBLE, cp_model.UNKNOWN):
            logger.warning(
                "solver returned %s: no valid combinations found",
                solver.StatusName(status),
            )
            return []

        if status == cp_model.MODEL_INVALID:
            logger.error("solver returned MODEL_INVALID")
            return []

        if not collector.solutions:
            logger.warning("solver completed with no solutions")
            return []

        return collector.solutions

    except Exception as e:
        logger.exception("Google OR-Tools solver failed unexpectedly: %s", e)
        return []
