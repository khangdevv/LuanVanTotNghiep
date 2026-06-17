from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from csp_generator import generate_schedules
from detect_conflicts import build_conflict_set
from models.classes import ClassSection
from schemas.schedule_schema import (
    GenerateScheduleRequest,
    GenerateScheduleResponse,
    ScheduleResult,
)
from scoring_function import calculate_total_score

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/schedules", tags=["schedules"])


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

    # solver
    try:
        raw_schedules = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=req.avoid_days,
            personal_events=req.personal_events,
            max_solutions=req.max_solutions,
        )
    except Exception:
        logger.exception("Solver failed for student=%s", req.student_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Solver gặp lỗi không mong đợi. Vui lòng thử lại.",
        )

    # Chấm điểm từng thời khóa biểu
    scored: list[tuple[dict[str, float], list[ClassSection]]] = []
    for schedule_dict in raw_schedules:
        selected_classes = list(schedule_dict.values())
        scores = calculate_total_score(
            schedule=selected_classes,
            preferences=req.preferences,
            avoid_days=req.avoid_days,
        )
        scored.append((scores, selected_classes))

    # Sắp xếp theo score_total giảm dần
    scored.sort(key=lambda x: x[0]["score_total"], reverse=True)

    # response
    results = [
        ScheduleResult(
            rank=i + 1,
            classes=classes,
            score_total=scores["score_total"],
            score_break=scores["score_break"],
            score_pref=scores["score_pref"],
            score_balance=scores["score_balance"],
        )
        for i, (scores, classes) in enumerate(scored[:5])
    ]

    return GenerateScheduleResponse(
        student_id=req.student_id,
        semester_id=req.semester_id,
        total_found=len(results),
        schedules=results,
    )
