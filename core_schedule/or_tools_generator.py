from __future__ import annotations

import logging
from ortools.sat.python import cp_model

from models import ClassSection, PersonalEvent
from csp_generator import _init_domains, _conflicts_with_personal_events

CourseGroups = dict[str, list[ClassSection]]    # {course_id: [ClassSection]}
Domains = dict[str, list[ClassSection]]         # {course_id: [ClassSection còn hợp lệ]}
ConflictSet = set[tuple[str, str]]              # {(class_id_A, class_id_B)}
Schedule = dict[str, ClassSection]              # {course_id: ClassSection đã chọn}

logger = logging.getLogger(__name__)


def sovle_schedule(
    course_groups: CourseGroups,
    avoid_days: list[int],
    conflict_set: ConflictSet,
    personal_events: list[PersonalEvent],
    max_solutions: int = 200,
)-> list[Schedule]:
    
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

        # Tạo các biến quyết định 
        course_vars = {}
        for course_id, options in domains.items():
            var_name = f"choice_{course_id}"
            if len(options) == 1:
                course_vars[course_id] = options[0]
            else:
                var = model.NewIntVar(0, len(options) - 1, var_name)
                course_vars[course_id] = var

        # Ràng buộc loại bỏ 
        for course_id, var in course_vars.items():
            if isinstance(var, ClassSection):
                for other_course_id, other_var in course_vars.items():
                    if course_id != other_course_id and isinstance(other_var, ClassSection):
                        if (var.class_id, other_var.class_id) in conflict_set:
                            return []

        for course_id in domains.keys():
            var = course_vars[course_id]
            if isinstance(var, ClassSection):
                continue  

            for other_course_id in domains.keys():
                if other_course_id == course_id:
                    continue

                other_var = course_vars[other_course_id]
                


    except Exception as e:
        logger.exception("Google OR-Tools solver failed unexpectedly: %s", e)
        return []
