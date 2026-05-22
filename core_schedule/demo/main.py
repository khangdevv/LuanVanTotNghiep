"""
    python demo/main.py
"""

from __future__ import annotations

import sys
from datetime import time
from pathlib import Path
from time import perf_counter

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

# Thêm core/ vào sys.path để import các module gốc
sys.path.insert(0, str(Path(__file__).parent.parent))

from scoring_function import calculate_total_score  # noqa: E402
from enums import PreferredSlot  # noqa: E402
from csp_generator import generate_schedules  # noqa: E402
from detect_conflicts import build_conflict_set  # noqa: E402
from data_loader import DEFAULT_JSON_PATH, load_course_groups  # noqa: E402
from models import ClassSection, PersonalEvent, Preference  # noqa: E402

_DAY_LABEL = {2: "Thứ 2", 3: "Thứ 3", 4: "Thứ 4",
              5: "Thứ 5", 6: "Thứ 6", 7: "Thứ 7", 8: "CN"}
_CA_START_MINUTES = (420, 575, 755, 910)


def _get_ca(t) -> int | None:
    m = t.hour * 60 + t.minute
    ca1, ca2, ca3, ca4 = _CA_START_MINUTES
    if m < ca2:
        return 1
    if m < ca3:
        return 2
    if m < ca4:
        return 3
    return 4

ROOT = Path(__file__).parent.parent   # trỏ về core/

# chỉnh sửa theo nhu cầu
COURSE_IDS: list[str] = [
    "CS03042", "CS03002", "CS09002", "GS49005",
    "GS19008", "CS03058", "CS03043", "CS03057",
]

# Ngày muốn tránh (2=Thứ 2 … 8=CN)
AVOID_DAYS: list[int] = [5, 6, 7, 8]

# Lịch bận cá nhân
PERSONAL_EVENTS: list[PersonalEvent] = [
    PersonalEvent(
        event_id    = 1,
        student_id  = "demo_student",
        title       = "Làm thêm quán cà phê",
        day_of_week = 5,
        start_time  = time(12, 35),
        end_time    = time(18, 00),
        is_recurring= True,
    ),
]

PREFERENCE =  Preference(
        student_id = "demo_student",
        preferred_slot = PreferredSlot.MORNING,
        min_break_minutes = 15,
        w_break = 0.4,
        w_preference = 0.3,
        w_balance = 0.3
    )

MAX_SOLUTIONS = 200000   # giới hạn số TKB sinh ra
PRINT_MAX     = 200000   # số TKB in ra

# Loader
JSON_PATH = DEFAULT_JSON_PATH

# Hiển thị
def print_schedule(idx: int, sched: dict) -> None:
    print(f"\n{'=' * 70}")
    print(f"  TKB #{idx}")
    print(f"{'=' * 70}")
    print(f"{'Môn':<12} {'Nhóm':<20} {'Thứ':<8} {'Giờ':<14} {'Phòng':<10} GV")
    print(f"{'-' * 70}")
    for cid, cls in sorted(sched.items(), key=lambda x: (x[1].day_of_week, x[1].start_time)):
        nhom = cls.class_id.replace(f"{cid}_", "").rsplit("_t", 1)[0]
        gio  = f"{cls.start_time.strftime('%H:%M')}–{cls.end_time.strftime('%H:%M')}"
        thu  = _DAY_LABEL.get(cls.day_of_week, str(cls.day_of_week))
        ca   = _get_ca(cls.start_time)
        print(f"{cid:<12} {nhom:<20} {thu:<8} {gio:<14} {cls.room or '-':<10} "
              f"{cls.instructor or '-'}  [Ca {ca}]")


# main
def main() -> None:
    print("=" * 70)
    print("  DEMO THUẬT TOÁN XẾP THỜI KHÓA BIỂU — STU")
    print("=" * 70)

    t0 = perf_counter()

    print(f"\n[1] Đang tải dữ liệu từ {JSON_PATH.name} ...")
    t1 = perf_counter()
    course_groups = load_course_groups(COURSE_IDS)
    all_classes   = [cls for secs in course_groups.values() for cls in secs]
    print(f"    → {len(course_groups)} môn, {len(all_classes)} nhóm lớp  ({perf_counter()-t1:.3f}s)")

    print("\n[2] Xây dựng tập xung đột ...")
    t2 = perf_counter()
    conflict_set = build_conflict_set(all_classes)
    print(f"    → {len(conflict_set) // 2} cặp xung đột  ({perf_counter()-t2:.3f}s)")

    print(f"\n[3] Sinh TKB (max {MAX_SOLUTIONS} nghiệm) ...")
    print(f"    Tránh ngày : {sorted(AVOID_DAYS)}")
    t3 = perf_counter()
    schedules = generate_schedules(
        course_groups   = course_groups,
        conflict_set    = conflict_set,
        avoid_days      = AVOID_DAYS,
        personal_events = PERSONAL_EVENTS,
        max_solutions   = MAX_SOLUTIONS,
    )
    print(f"    → Backtracking: {perf_counter()-t3:.3f}s")

    if not schedules:
        print("\n[!] Không tìm được TKB hợp lệ. Kiểm tra lại COURSE_IDS / AVOID_DAYS.")
        return

    schedule_scores: list[tuple[dict[str, ClassSection], dict[str, float]]] = []
    t4 = perf_counter()
    for schedule in schedules:
        score = calculate_total_score(list(schedule.values()), PREFERENCE, AVOID_DAYS)
        schedule_scores.append((schedule, score))
    print(f"    → Tính điểm {len(schedules)} TKB: {perf_counter()-t4:.3f}s")

    t5 = perf_counter()
    schedule_scores.sort(key=lambda x: x[1]["score_total"], reverse=True)
    print(f"    → Sắp xếp: {perf_counter()-t5:.3f}s")

    print(f"\n    Tổng thời gian: {perf_counter()-t0:.3f}s")
    print(f"    → Tìm được {len(schedules)} TKB hợp lệ")

    to_print = schedule_scores[:PRINT_MAX]
    print(f"\n[4] In {len(to_print)} TKB đầu tiên:\n")
    
    count = 0
    
    for i, schedule_score in enumerate(to_print, start=1):
        schedule = schedule_score[0]
        score = schedule_score[1]
        
        if count >= 3:
            break

        print(f"\nDiem: {score['score_total']}")
        print(f"  - Break time      : {score['score_break']}")
        print(f"  - Preference match: {score['score_pref']}")
        print(f"  - Workload balance: {score['score_balance']}")
        print_schedule(i, schedule)
        count+=1

    print(f"\n{'=' * 70}")
    print(f"  Tổng thời gian: {perf_counter() - t0:.3f}s")
    print(f"{'=' * 70}\n")


if __name__ == "__main__":
    main()
