"""
    python -m pytest
"""
import io
import sys
from datetime import time
from pathlib import Path

import pytest

# Fix encoding cho Windows terminal
if isinstance(sys.stdout, io.TextIOWrapper):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Đưa thư mục gốc core_schedule vào sys.path để các file test import được
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from csp_generator import generate_schedules          # noqa: E402
from data_loader import DEFAULT_SEMESTER_ID, load_course_groups  # noqa: E402
from detect_conflicts import build_conflict_set       # noqa: E402
from models import ClassSection, PersonalEvent        # noqa: E402

SEMESTER_ID = DEFAULT_SEMESTER_ID

COURSE_IDS = [
    "CS03042", "CS03002", "CS09002", "GS49005",
    "GS19008", "CS03058", "GS79005", "GS33002",
]

AVOID_DAYS: list[int] = [6, 7, 8]

PERSONAL_EVENTS: list[PersonalEvent] = [
    PersonalEvent(
        event_id=1,
        student_id="test_student",
        title="Làm thêm quán cà phê",
        day_of_week=4,
        start_time=time(12, 35),
        end_time=time(15, 5),
        is_recurring=True,
    ),
]

# fixtures (session-scoped để chạy 1 lần cho cả suite) 
@pytest.fixture(scope="session")
def course_groups() -> dict[str, list[ClassSection]]:
    groups = load_course_groups(COURSE_IDS)
    return {cid: secs for cid, secs in groups.items() if secs}


@pytest.fixture(scope="session")
def all_classes(course_groups) -> list[ClassSection]:
    return [cls for secs in course_groups.values() for cls in secs]


@pytest.fixture(scope="session")
def conflict_set(all_classes) -> set[tuple[str, str]]:
    return build_conflict_set(all_classes)


@pytest.fixture(scope="session")
def valid_schedules(course_groups, conflict_set) -> list[dict]:
    return generate_schedules(
        course_groups=course_groups,
        conflict_set=conflict_set,
        avoid_days=AVOID_DAYS,
        personal_events=PERSONAL_EVENTS,
        max_solutions=200,
    )
