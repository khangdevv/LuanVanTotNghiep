"""
    python demo/main.py
"""

from __future__ import annotations

import json
import sys
from datetime import time
from pathlib import Path

# Thêm core/ vào sys.path để import các module gốc
sys.path.insert(0, str(Path(__file__).parent.parent))

from scoring_function import calculate_total_score
from enums import PreferredSlot
from csp_generator import generate_schedules  
from detect_conflicts import build_conflict_set  
from models import ClassSection, PersonalEvent, Preference  
from demo.time_utils import tiet_to_time 

_DAY_LABEL = {2: "Thứ 2", 3: "Thứ 3", 4: "Thứ 4",
              5: "Thứ 5", 6: "Thứ 6", 7: "Thứ 7", 8: "CN"}
_CA_START_MINUTES = (420, 575, 755, 910)


def _get_ca(t) -> int | None:
    m = t.hour * 60 + t.minute
    ca1, ca2, ca3, ca4 = _CA_START_MINUTES
    if m == ca1: return 1
    if m == ca2: return 2
    if m == ca3: return 3
    if m >= ca4: return 4
    return None

ROOT = Path(__file__).parent.parent   # trỏ về core/

# ===========================================================================
# CẤU HÌNH DEMO — chỉnh sửa theo nhu cầu
# ===========================================================================

COURSE_IDS: list[str] = [
    "CS03042", "CS03002", "CS09002", "GS49005",
    "GS19008", "CS03058", "GS79005", "GS33002",
]

# Ngày muốn tránh (2=Thứ 2 … 8=CN)
AVOID_DAYS: set[int] = {6, 7, 8}

# Lịch bận cá nhân
PERSONAL_EVENTS: list[PersonalEvent] = [
    PersonalEvent(
        event_id    = 1,
        student_id  = "demo_student",
        title       = "Làm thêm quán cà phê",
        day_of_week = 4,
        start_time  = time(12, 35),
        end_time    = time(15, 5),
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

MAX_SOLUTIONS = 20   # giới hạn số TKB sinh ra
PRINT_MAX     = 20   # số TKB in ra

# ===========================================================================
# Loader
# ===========================================================================

JSON_PATH   = ROOT / "data" / "schedule_data_from_web.json"
SEMESTER_ID = "HK2-2025"


def load_course_groups(course_ids: list[str]) -> dict[str, list[ClassSection]]:
    raw: list[dict] = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    seen: set[tuple[str, str]] = set()
    groups: dict[str, list[ClassSection]] = {cid: [] for cid in course_ids}

    for rec in raw:
        cid = rec["ma_mh"]
        if cid not in groups:
            continue

        nhom = rec["nhom_to"]
        if (cid, nhom) in seen:
            continue
        seen.add((cid, nhom))

        lich = rec["lich_hoc"]
        if lich["so_tiet"] <= 0:
            continue

        start, end = tiet_to_time(lich["tiet_bat_dau"], lich["so_tiet"])

        groups[cid].append(
            ClassSection(
                class_id    = f"{cid}_{nhom}",
                course_id   = cid,
                semester_id = SEMESTER_ID,
                day_of_week = int(lich["thu"]),
                start_time  = start,
                end_time    = end,
                room        = lich.get("phong"),
                instructor  = lich.get("giang_vien"),
                max_students= 1,
            )
        )

    return {cid: secs for cid, secs in groups.items() if secs}


# ===========================================================================
# Hiển thị
# ===========================================================================

def print_schedule(idx: int, sched: dict) -> None:
    print(f"\n{'=' * 70}")
    print(f"  TKB #{idx}")
    print(f"{'=' * 70}")
    print(f"{'Môn':<12} {'Nhóm':<20} {'Thứ':<8} {'Giờ':<14} {'Phòng':<10} GV")
    print(f"{'-' * 70}")
    for cid, cls in sorted(sched.items(), key=lambda x: (x[1].day_of_week, x[1].start_time)):
        nhom = cls.class_id.replace(f"{cid}_", "")
        gio  = f"{cls.start_time.strftime('%H:%M')}–{cls.end_time.strftime('%H:%M')}"
        thu  = _DAY_LABEL.get(cls.day_of_week, str(cls.day_of_week))
        ca   = _get_ca(cls.start_time)
        print(f"{cid:<12} {nhom:<20} {thu:<8} {gio:<14} {cls.room or '-':<10} "
              f"{cls.instructor or '-'}  [Ca {ca}]")


# ===========================================================================
# Main
# ===========================================================================

def main() -> None:
    print("=" * 70)
    print("  DEMO THUẬT TOÁN XẾP THỜI KHÓA BIỂU — STU")
    print("=" * 70)

    print(f"\n[1] Đang tải dữ liệu từ {JSON_PATH.name} ...")
    course_groups = load_course_groups(COURSE_IDS)
    all_classes   = [cls for secs in course_groups.values() for cls in secs]
    print(f"    → {len(course_groups)} môn, {len(all_classes)} nhóm lớp")

    print("\n[2] Xây dựng tập xung đột ...")
    conflict_set = build_conflict_set(all_classes)
    print(f"    → {len(conflict_set) // 2} cặp xung đột")

    print(f"\n[3] Sinh TKB (max {MAX_SOLUTIONS} nghiệm) ...")
    print(f"    Tránh ngày : {sorted(AVOID_DAYS)}")
    schedules = generate_schedules(
        course_groups   = course_groups,
        conflict_set    = conflict_set,
        avoid_days      = AVOID_DAYS,
        personal_events = PERSONAL_EVENTS,
        max_solutions   = MAX_SOLUTIONS,
    )
    
    schedule_scores : list[tuple[dict[str, ClassSection], dict[str, float]]] = []
    
    for schedule in schedules:
        sections = list(schedule.values())
        
        score = calculate_total_score(sections, PREFERENCE, list(AVOID_DAYS))
        
        schedule_scores.append((schedule, score))

    for i in range(len(schedule_scores)):
        max_index = i
        
        for j in range(i + 1, len(schedule_scores)):
            current_score = schedule_scores[j][1]["total"]
            max_score = schedule_scores[max_index][1]["total"]
            
            if current_score > max_score:
                max_index = j
                
        temp = schedule_scores[i]
        schedule_scores[i] = schedule_scores[max_index]
        schedule_scores[max_index] = temp

    if not schedules:
        print("\n[!] Không tìm được TKB hợp lệ. Kiểm tra lại COURSE_IDS / AVOID_DAYS.")
        return

    print(f"    → Tìm được {len(schedules)} TKB hợp lệ")

    to_print = schedule_scores[:PRINT_MAX]
    print(f"\n[4] In {len(to_print)} TKB đầu tiên:\n")
    for i, schedule_score in enumerate(to_print, start=1):
        schedule = schedule_score[0]
        score = schedule_score[1]

        print(f"\nDiem: {score['total']}")
        print(f"  - Break time      : {score['break_time']}")
        print(f"  - Preference match: {score['preference_match']}")
        print(f"  - Workload balance: {score['workload_balance']}")
        print_schedule(i, schedule)

    print(f"\n{'=' * 70}\n")


if __name__ == "__main__":
    main()
