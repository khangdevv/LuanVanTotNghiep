"""
So sanh 2 phuong phap sinh thoi khoa bieu:
  1. Backtracking + MRV/LCV + Forward Checking  (csp_generator.py)
  2. OR-Tools CP-SAT                             (or_tools_generator.py)

Do 2 tieu chi:
  - Thoi gian chay (ms)
  - Chat luong: diem fitness tot nhat, so TKB tim duoc, ti le thanh cong

Cach chay (tu thu muc core_schedule/):
  python compare_algorithms.py

Ket qua ghi ra:
  benchmark_results/detail.csv   -- du lieu tho tung luot
  benchmark_results/summary.csv  -- trung binh moi muc do
  
python compare_algorithms.py
"""

from __future__ import annotations

import csv
import random
import time
from datetime import time as dt_time
from pathlib import Path
from typing import Optional

from data_loader import load_course_groups
from detect_conflicts import build_conflict_set
from models import ClassSection, PersonalEvent
from models.preferences import Preference
from enums.preferred_slot import PreferredSlot
import csp_generator
import or_tools_generator
from scoring_function import calculate_total_score

# ──────────────────────────────────────────────────────────────
# Cau hinh
# ──────────────────────────────────────────────────────────────
random.seed(42)

COURSE_IDS = [
    "CS03042", "CS03002", "CS09002", "GS49005", "GS19008",
    "CS03058", "CS03043", "CS03057", "CS03001",
]
RUNS_PER_LEVEL = 20   # luot chay moi muc
MAX_SOLUTIONS  = 200  # gioi han TKB toi da / luot


def _constraint_profile(n: int) -> tuple[int, int]:
    """(so ngay tranh, so lich ban ca nhan) theo so mon."""
    table = {
        1: (0, 0), 2: (0, 0),
        3: (1, 0), 4: (1, 0),
        5: (2, 1), 6: (2, 1),
        7: (3, 2), 8: (3, 2),
    }
    return table.get(n, (0, 0))


# ──────────────────────────────────────────────────────────────
# Tien ich
# ──────────────────────────────────────────────────────────────
def _best_fitness(
    schedules: list[dict[str, ClassSection]],
    pref: Preference,
    avoid_days: list[int],
) -> float:
    if not schedules:
        return 0.0
    return round(
        max(
            calculate_total_score(list(s.values()), pref, avoid_days)["score_total"]
            for s in schedules
        ),
        4,
    )


def _make_pref() -> Preference:
    return Preference(
        student_id="bench",
        preferred_slot=PreferredSlot.MORNING,
        min_break_minutes=15,
        w_break=0.40, w_preference=0.30, w_balance=0.30,
    )


def _gen_events(count: int) -> list[PersonalEvent]:
    events = []
    for i in range(count):
        sh = random.randint(8, 15)
        events.append(PersonalEvent(
            event_id=i + 1, student_id="bench",
            title=f"Busy {i+1}",
            day_of_week=random.choice([2, 3, 4, 5, 6, 7, 8]),
            start_time=dt_time(sh, 0),
            end_time=dt_time(sh + random.randint(2, 4), 0),
            is_recurring=True,
        ))
    return events


# ──────────────────────────────────────────────────────────────
# Chay 1 luot: do ca 2 thuat toan tren cung 1 bo du lieu
# ──────────────────────────────────────────────────────────────
def run_one(
    course_ids: list[str],
    avoid_days: list[int],
    personal_events: list[PersonalEvent],
    pref: Preference,
) -> dict:
    course_groups = load_course_groups(course_ids)
    if not course_groups:
        return {}
    all_classes  = [c for secs in course_groups.values() for c in secs]
    conflict_set = build_conflict_set(all_classes)

    # ── Backtracking + MRV/LCV
    t0 = time.perf_counter()
    bt_list = csp_generator.generate_schedules(
        course_groups=course_groups,
        conflict_set=conflict_set,
        avoid_days=avoid_days,
        personal_events=personal_events,
        max_solutions=MAX_SOLUTIONS,
    )
    bt_ms = (time.perf_counter() - t0) * 1000

    # ── OR-Tools CP-SAT
    t0 = time.perf_counter()
    ort_list = or_tools_generator.solve_schedule(
        course_groups=course_groups,
        conflict_set=conflict_set,
        avoid_days=avoid_days,
        personal_events=personal_events,
        max_solutions=MAX_SOLUTIONS,
    )
    ort_ms = (time.perf_counter() - t0) * 1000

    return {
        "bt_ms":      round(bt_ms, 4),
        "bt_found":   len(bt_list),
        "bt_fitness": _best_fitness(bt_list,  pref, avoid_days),
        "ort_ms":     round(ort_ms, 4),
        "ort_found":  len(ort_list),
        "ort_fitness":_best_fitness(ort_list, pref, avoid_days),
    }


# ──────────────────────────────────────────────────────────────
# Chay toan bo benchmark
# ──────────────────────────────────────────────────────────────
def run_benchmark() -> list[dict]:
    pref = _make_pref()
    rows: list[dict] = []

    for n in range(1, 9):
        av, ev = _constraint_profile(n)
        print(
            f"  Muc {n}/8: {n} mon | {av} ngay tranh | {ev} lich ban ...",
            flush=True,
        )

        for run_i in range(RUNS_PER_LEVEL):
            selected   = random.sample(COURSE_IDS, n)
            avoid_days = random.sample([2, 3, 4, 5, 6, 7, 8], av) if av else []
            events     = _gen_events(ev)

            r = run_one(selected, avoid_days, events, pref)
            if r:
                r["level"] = n
                r["run"]   = run_i + 1
                rows.append(r)

    return rows


# ──────────────────────────────────────────────────────────────
# Luu CSV
# ──────────────────────────────────────────────────────────────
DETAIL_FIELDS = [
    "level", "run",
    "bt_ms",  "bt_found",  "bt_fitness",
    "ort_ms", "ort_found", "ort_fitness",
]


def save_csv(rows: list[dict], out_dir: Path) -> list[dict]:
    # Detail
    detail_path = out_dir / "detail.csv"
    with open(detail_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=DETAIL_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in DETAIL_FIELDS})

    # Summary
    by_level: dict[int, list[dict]] = {}
    for r in rows:
        by_level.setdefault(r["level"], []).append(r)

    summary: list[dict] = []
    sum_fields = [
        "level", "runs",
        "bt_ms_avg",  "ort_ms_avg",
        "bt_found_avg", "ort_found_avg",
        "bt_fitness_avg", "ort_fitness_avg",
        "bt_success_%", "ort_success_%",
    ]
    sum_path = out_dir / "summary.csv"
    with open(sum_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=sum_fields)
        w.writeheader()
        for lv in sorted(by_level):
            rs = by_level[lv]
            n  = len(rs)
            def avg(k): return round(sum(r[k] for r in rs) / n, 4)
            row = {
                "level":           lv,
                "runs":            n,
                "bt_ms_avg":       avg("bt_ms"),
                "ort_ms_avg":      avg("ort_ms"),
                "bt_found_avg":    round(avg("bt_found"),  1),
                "ort_found_avg":   round(avg("ort_found"), 1),
                "bt_fitness_avg":  avg("bt_fitness"),
                "ort_fitness_avg": avg("ort_fitness"),
                "bt_success_%":    round(sum(1 for r in rs if r["bt_found"]  > 0) / n * 100, 1),
                "ort_success_%":   round(sum(1 for r in rs if r["ort_found"] > 0) / n * 100, 1),
            }
            w.writerow(row)
            summary.append(row)

    print(f"  CSV chi tiet : {detail_path}")
    print(f"  CSV tong hop : {sum_path}")
    return summary


# ──────────────────────────────────────────────────────────────
# In bang ket qua ra terminal
# ──────────────────────────────────────────────────────────────
def print_table(summary: list[dict]) -> None:
    SEP = (
        "+------+-------------+-------------+"
        "---------+---------+"
        "-----------+-----------+"
        "--------+--------+"
    )
    HEADER = (
        "| Mon | BT-Time(ms) |ORT-Time(ms) |"
        " BT-Found|ORT-Found|"
        " BT-Fitness|ORT-Fitness|"
        "  BT-OK%| ORT-OK%|"
    )
    print()
    print(SEP)
    print(HEADER)
    print(SEP)
    for r in summary:
        print(
            f"| {r['level']:>3} "
            f"| {r['bt_ms_avg']:>11.4f} "
            f"| {r['ort_ms_avg']:>11.4f} |"
            f" {r['bt_found_avg']:>7.1f} "
            f"| {r['ort_found_avg']:>7.1f} |"
            f" {r['bt_fitness_avg']:>10.4f} "
            f"| {r['ort_fitness_avg']:>10.4f} |"
            f" {r['bt_success_%']:>5.1f}% "
            f"| {r['ort_success_%']:>5.1f}% |"
        )
    print(SEP)
    print()
    print("  Giai thich cot:")
    print("    BT-Time  / ORT-Time  : thoi gian chay trung binh (ms)")
    print("    BT-Found / ORT-Found : so TKB hop le tim duoc (toi da 200)")
    print("    BT-Fitness/ ORT-Fitness : diem chat luong TKB tot nhat (0..1)")
    print("    BT-OK%   / ORT-OK%   : ti le luot chay tim duoc nghiem")
    print()


# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    out_dir = Path(__file__).parent / "benchmark_results"
    out_dir.mkdir(exist_ok=True)

    print("=" * 62)
    print("  SO SANH 2 PHUONG PHAP SINH THOI KHOA BIEU")
    print("  1. Backtracking + MRV/LCV + Forward Checking")
    print("  2. OR-Tools CP-SAT")
    print(f"  So luot chay moi muc : {RUNS_PER_LEVEL}")
    print(f"  Gioi han TKB / luot  : {MAX_SOLUTIONS}")
    print("=" * 62)

    rows    = run_benchmark()
    summary = save_csv(rows, out_dir)
    print_table(summary)

    print("=" * 62)
    print("  HOAN THANH -- ket qua luu tai: benchmark_results/")
    print("=" * 62)
