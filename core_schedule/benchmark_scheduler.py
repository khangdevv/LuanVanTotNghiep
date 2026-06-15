"""
    python benchmark_scheduler.py
"""

from __future__ import annotations
import random
from pathlib import Path
from datetime import time as dt_time
from data_loader import load_course_groups, DEFAULT_JSON_PATH
from detect_conflicts import build_conflict_set
from models import PersonalEvent
import csp_generator
import or_tools_generator

random.seed(42)

COURSE_IDS = [
    "CS03042", "CS03002", "CS09002", "GS49005", "GS19008",
    "CS03058", "CS03043", "CS03057", "CS03001",
]

RUNS_PER_LEVEL = 20

MAX_SOLUTIONS = 200

def _constraint_profile(courses_count: int) -> tuple[int, int]:
    # (avoid_days_count, events_count)
    table = {
        1:  (0, 0),
        2:  (0, 0),
        3:  (1, 0),
        4:  (1, 0),
        5:  (2, 1),
        6:  (2, 1),
        7:  (3, 2),
        8:  (3, 2),
    }
    return table.get(courses_count, (0, 0))


def generate_random_personal_events(count: int) -> list[PersonalEvent]:
    events = []
    days = [2, 3, 4, 5, 6, 7, 8]
    for i in range(count):
        day = random.choice(days)
        start_hour = random.randint(8, 15)
        duration = random.randint(2, 4)
        events.append(
            PersonalEvent(
                event_id=i + 1,
                student_id="benchmark_student",
                title=f"Lịch bận ngẫu nhiên {i+1}",
                day_of_week=day,
                start_time=dt_time(start_hour, 0),
                end_time=dt_time(start_hour + duration, 0),
                is_recurring=True
            )
        )
    return events


def run_single_test(
    course_ids: list[str],
    avoid_days: list[int],
    personal_events: list[PersonalEvent],
    max_solutions: int = MAX_SOLUTIONS
) -> dict:
    course_groups = load_course_groups(course_ids)
    if not course_groups:
        return {}

    all_classes = [cls for secs in course_groups.values() for cls in secs]
    conflict_set = build_conflict_set(all_classes)

    schedules = csp_generator.generate_schedules(
        course_groups=course_groups,
        conflict_set=conflict_set,
        avoid_days=avoid_days,
        personal_events=personal_events,
        max_solutions=max_solutions
    )

    ort_schedules = or_tools_generator.solve_schedule(
        course_groups=course_groups,
        conflict_set=conflict_set,
        avoid_days=avoid_days,
        personal_events=personal_events,
        max_solutions=max_solutions
    )

    return {
        "num_courses": len(course_groups),
        "num_sections": len(all_classes),
        "course_ids": list(course_groups.keys()),
        "sections_per_course": {cid: len(secs) for cid, secs in course_groups.items()},
        "feasible": len(schedules) > 0,
        "bt_found": len(schedules),
        "ort_feasible": len(ort_schedules) > 0,
        "ort_found": len(ort_schedules),
    }




def run_benchmark():
    results_by_level: dict[int, list[dict]] = {}

    for n in range(1, 9):
        avoid_days_count, events_count = _constraint_profile(n)
        print(f"Dang chay muc {n}/8...", flush=True)

        results: list[dict] = []
        for _ in range(RUNS_PER_LEVEL):
            selected = random.sample(COURSE_IDS, n)
            avoid_days = (
                random.sample([2, 3, 4, 5, 6, 7, 8], avoid_days_count)
                if avoid_days_count > 0 else []
            )
            personal_events = generate_random_personal_events(events_count)
            res = run_single_test(selected, avoid_days, personal_events)
            if res:
                results.append(res)

        results_by_level[n] = results

    generate_markdown_report(results_by_level)


def generate_markdown_report(results_by_level: dict[int, list[dict]]):
    report_path = Path("BACKTRACKING_PERFORMANCE_REPORT.md")

    lines: list[str] = []
    lines.append("# Báo cáo Thực nghiệm: Backtracking vs OR-Tools CP-SAT")
    lines.append("")
    lines.append(f"- **Số lượt chạy mỗi mức**: {RUNS_PER_LEVEL} lượt")
    lines.append(f"- **Giới hạn tối đa TKB mỗi lượt**: {MAX_SOLUTIONS}")
    lines.append("")

    for n in range(1, 9):
        results = results_by_level.get(n, [])
        av, ev = _constraint_profile(n)
        total = len(results)

        lines.append("---")
        lines.append(
            f"## Mức {n}: {n} môn học | {av} ngày tránh | {ev} lịch bận cá nhân"
        )

        if total == 0:
            lines.append("_Không có kết quả._")
            lines.append("")
            continue

        # Bảng môn học
        first = results[0]
        lines.append("")
        lines.append("**Danh sách môn học trong lần chạy mẫu:**")
        lines.append("")
        lines.append("| STT | Mã môn | Số nhóm lớp |")
        lines.append("|-----|--------|-------------|")
        for i, (cid, cnt) in enumerate(first["sections_per_course"].items(), 1):
            lines.append(f"| {i} | {cid} | {cnt} nhóm |")
        lines.append("")

        # So sánh thuật toán
        bt_ok   = sum(1 for r in results if r["feasible"])
        ort_ok  = sum(1 for r in results if r["ort_feasible"])
        bt_avg  = sum(r["bt_found"]  for r in results) / total
        ort_avg = sum(r["ort_found"] for r in results) / total

        lines.append("**Kết quả so sánh hai thuật toán:**")
        lines.append("")
        lines.append("| Thuật toán | Tìm được nghiệm | Tỉ lệ thành công | Số TKB trung bình |")
        lines.append("|------------|----------------|-----------------|------------------|")
        lines.append(f"| Backtracking | {bt_ok}/{total} | {bt_ok/total*100:.1f}% | {bt_avg:.1f} |")
        lines.append(f"| OR-Tools CP-SAT | {ort_ok}/{total} | {ort_ok/total*100:.1f}% | {ort_avg:.1f} |")
        lines.append("")


    # ── Tổng hợp
    lines.append("---")
    lines.append("## Tổng hợp")
    lines.append("")
    total_runs = sum(len(r) for r in results_by_level.values())
    total_bt   = sum(1 for rs in results_by_level.values() for r in rs if r["feasible"])
    total_ort  = sum(1 for rs in results_by_level.values() for r in rs if r["ort_feasible"])

    lines.append(f"- Tổng lượt chạy: **{total_runs}**")
    lines.append(
        f"- Backtracking tìm được nghiệm: **{total_bt}/{total_runs}** "
        f"({total_bt/total_runs*100:.1f}%)"
    )
    lines.append(
        f"- OR-Tools CP-SAT tìm được nghiệm: **{total_ort}/{total_runs}** "
        f"({total_ort/total_runs*100:.1f}%)"
    )

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[+] Bao cao: {report_path}")



if __name__ == "__main__":
    run_benchmark()
