from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from csp_generator import generate_schedules
from or_tools_generator import solve_schedule as or_tools_solve
from detect_conflicts import build_conflict_set, detect_conflicts
from models.classes import ClassSection
from schemas.schedule_schema import (
    GenerateScheduleRequest,
    GenerateScheduleResponse,
    ScheduleResult,
    DetectConflictRequest,
    DetectConflictResponse,
)
from scoring_function import calculate_total_score

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/schedules", tags=["schedules"])

# conflicts
@router.post(
    "/conflicts",
    response_model=DetectConflictResponse,
    summary="Kiểm tra xung đột",
    description=(
        "Nhận danh sách nhóm lớp, sở thích và sự kiện cá nhân của sinh viên. "
        "Trả về danh sách thời khóa biểu hợp lệ đã được chấm điểm và xếp hạng."
    ),
)
async def check_conflicts(req: DetectConflictRequest) -> DetectConflictResponse:
    conflicts_list: list[tuple[ClassSection, ClassSection]] = []

    conflicts_list = detect_conflicts(req.classes)

    return DetectConflictResponse(
        semester_id=req.semester_id,
        conflicts=conflicts_list,
        total_conflicts=len(conflicts_list),
        is_valid=len(conflicts_list) == 0,
    )

# generate
@router.post(
    "/generate",
    response_model=GenerateScheduleResponse,
    summary="Sinh thời khóa biểu",
    description=(
        "Nhận danh sách nhóm lớp, sở thích và sự kiện cá nhân của sinh viên. "
        "Trả về danh sách thời khóa biểu hợp lệ đã được chấm điểm và xếp hạng."
    ),
)
async def generate_schedule(req: GenerateScheduleRequest) -> GenerateScheduleResponse:

    # Validate avoid_days
    invalid_days = [d for d in req.avoid_days if not (2 <= d <= 8)]
    if invalid_days:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"avoid_days chứa giá trị không hợp lệ: {invalid_days}. Hợp lệ: 2–8.",
        )

    # Gom nhóm lớp theo course_id
    course_groups: dict[str, list[ClassSection]] = {}
    for cls in req.classes:
        course_groups.setdefault(cls.course_id, []).append(cls)

    # conflict_set
    conflict_set = build_conflict_set(req.classes)

    # helper chấm điểm
    def score_schedules(raw_list):
        scored_list = []
        for schedule_dict in raw_list:
            selected_classes = list(schedule_dict.values())
            scores = calculate_total_score(
                schedule=selected_classes,
                preferences=req.preferences,
                avoid_days=req.avoid_days,
            )
            scored_list.append((scores, selected_classes))
        scored_list.sort(key=lambda x: x[0]["score_total"], reverse=True)
        return scored_list

    # csp
    try:
        raw_csp = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=req.avoid_days,
            personal_events=req.personal_events,
            max_solutions=req.max_solutions,
        )
    except Exception:
        logger.exception("CSP Solver failed for student=%s", req.student_id)
        raw_csp = []

    # or-tools
    try:
        raw_ortools = or_tools_solve(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=req.avoid_days,
            personal_events=req.personal_events,
            max_solutions=req.max_solutions,
        )
    except Exception:
        logger.exception("OR-Tools Solver failed for student=%s", req.student_id)
        raw_ortools = []

    # Chấm điểm và lấy Top 3
    scored_csp = score_schedules(raw_csp)[:3]
    scored_ortools = score_schedules(raw_ortools)[:3]

    # Gộp và lọc trùng lặp
    final_candidates = []
    seen_hashes = set()

    # Hàm hash cho 1 TKB
    def get_hash(classes: list[ClassSection]) -> str:
        return ",".join(sorted([c.class_id for c in classes]))

    for scores, classes in scored_csp:
        h = get_hash(classes)
        if h not in seen_hashes:
            seen_hashes.add(h)
            final_candidates.append((scores, classes, "CSP"))

    for scores, classes in scored_ortools:
        h = get_hash(classes)
        if h not in seen_hashes:
            seen_hashes.add(h)
            final_candidates.append((scores, classes, "OR-Tools"))

    # Sắp xếp lại
    final_candidates.sort(key=lambda x: x[0]["score_total"], reverse=True)

    results = [
        ScheduleResult(
            rank=i + 1,
            is_recommended=(i == 0),
            algorithm=algo,
            classes=classes,
            score_total=scores["score_total"],
            score_break=scores["score_break"],
            score_pref=scores["score_pref"],
            score_balance=scores["score_balance"],
        )
        for i, (scores, classes, algo) in enumerate(final_candidates)
    ]

    return GenerateScheduleResponse(
        student_id=req.student_id,
        semester_id=req.semester_id,
        total_found=len(results),
        schedules=results,
    )
