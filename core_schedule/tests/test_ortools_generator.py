"""
pytest tests/test_ortools_generator.py -v
"""
from datetime import time

import pytest

from conftest import AVOID_DAYS, PERSONAL_EVENTS, SEMESTER_ID
from or_tools_generator import sovle_schedule as generate_schedules
from detect_conflicts import build_conflict_set
from models import ClassSection, PersonalEvent


def _make(cid: str, course: str, day: int, sh: int, eh: int) -> ClassSection:
    return ClassSection(
        class_id=cid, course_id=course, semester_id=SEMESTER_ID,
        day_of_week=day, start_time=time(sh, 0), end_time=time(eh, 0),
    )


class TestOrToolsGenerateSchedules:
    def test_returns_list(self, valid_schedules):
        """Kết quả phải là list."""
        assert isinstance(valid_schedules, list)

    def test_each_schedule_covers_all_courses(self, valid_schedules, course_groups, conflict_set):
        """Mỗi TKB phải có đúng 1 nhóm cho mỗi môn."""
        results = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=AVOID_DAYS,
            personal_events=PERSONAL_EVENTS,
            max_solutions=10,
        )
        if not results:
            pytest.skip("Không có nghiệm — kiểm tra COURSE_IDS và AVOID_DAYS")
        for sched in results:
            assert set(sched.keys()) == set(course_groups.keys()), (
                "TKB thiếu hoặc thừa môn học"
            )

    def test_no_internal_conflict(self, course_groups, conflict_set):
        """Không có TKB nào chứa hai lớp xung đột với nhau."""
        results = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=AVOID_DAYS,
            personal_events=PERSONAL_EVENTS,
            max_solutions=10,
        )
        for sched in results:
            classes = list(sched.values())
            for i in range(len(classes)):
                for j in range(i + 1, len(classes)):
                    a, b = classes[i], classes[j]
                    assert (a.class_id, b.class_id) not in conflict_set, (
                        f"Xung đột lọt qua: {a.class_id} ↔ {b.class_id}"
                    )

    def test_no_avoid_day_classes(self, course_groups, conflict_set):
        """Không có lớp nào rơi vào ngày trong AVOID_DAYS."""
        results = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=AVOID_DAYS,
            personal_events=PERSONAL_EVENTS,
            max_solutions=10,
        )
        for sched in results:
            for cls in sched.values():
                assert cls.day_of_week not in AVOID_DAYS, (
                    f"{cls.class_id} rơi vào ngày tránh: {cls.day_of_week}"
                )

    def test_no_personal_event_conflict(self, course_groups, conflict_set):
        """Không có lớp nào trùng với PersonalEvents."""
        results = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=AVOID_DAYS,
            personal_events=PERSONAL_EVENTS,
            max_solutions=10,
        )
        for sched in results:
            for cls in sched.values():
                for event in PERSONAL_EVENTS:
                    if event.day_of_week is None or cls.day_of_week != event.day_of_week:
                        continue
                    overlaps = (
                        cls.start_time < event.end_time
                        and event.start_time < cls.end_time
                    )
                    assert not overlaps, (
                        f"{cls.class_id} trùng với PersonalEvent '{event.title}'"
                    )

    def test_max_solutions_respected(self, course_groups, conflict_set):
        """Số nghiệm trả về không vượt quá max_solutions."""
        for limit in [1, 3, 5]:
            results = generate_schedules(
                course_groups=course_groups,
                conflict_set=conflict_set,
                avoid_days=AVOID_DAYS,
                personal_events=PERSONAL_EVENTS,
                max_solutions=limit,
            )
            assert len(results) <= limit

    def test_empty_when_all_days_avoided(self, course_groups, conflict_set):
        """Tránh tất cả các ngày → không có nghiệm."""
        result = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=[2, 3, 4, 5, 6, 7, 8],
            personal_events=[],
            max_solutions=10,
        )
        assert result == []

    def test_empty_course_groups(self, conflict_set):
        """course_groups rỗng → trả []."""
        result = generate_schedules(
            course_groups={},
            conflict_set=conflict_set,
            avoid_days=[],
            personal_events=[],
        )
        assert result == []

    def test_schedules_are_unique(self, course_groups, conflict_set):
        """Không có hai TKB giống hệt nhau."""
        results = generate_schedules(
            course_groups=course_groups,
            conflict_set=conflict_set,
            avoid_days=AVOID_DAYS,
            personal_events=PERSONAL_EVENTS,
            max_solutions=50,
        )
        seen: list[frozenset] = []
        for sched in results:
            key = frozenset((k, v.class_id) for k, v in sched.items())
            assert key not in seen, "Có TKB bị lặp"
            seen.append(key)


class TestEndToEndSimple:
    def test_two_courses_no_conflict(self):
        """2 môn không xung đột → đủ 2×2 = 4 tổ hợp."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9), _make("A2", "A", 3, 7, 9)],
            "B": [_make("B1", "B", 4, 7, 9), _make("B2", "B", 5, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=10)
        assert len(results) == 4

    def test_two_courses_full_conflict(self):
        """Mọi nhóm đều xung đột nhau → không có nghiệm."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9), _make("A2", "A", 2, 7, 9)],
            "B": [_make("B1", "B", 2, 7, 9), _make("B2", "B", 2, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        assert generate_schedules(groups, cs, set(), [], max_solutions=10) == []

    def test_personal_event_blocks_all(self):
        """PersonalEvent chặn tất cả nhóm của một môn → không có nghiệm."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9)],
            "B": [_make("B1", "B", 3, 7, 9)],
        }
        event = PersonalEvent(
            event_id=1, student_id="s", title="Bận",
            day_of_week=3, start_time=time(6, 0), end_time=time(10, 0),
            is_recurring=True,
        )
        cs = build_conflict_set([c for s in groups.values() for c in s])
        assert generate_schedules(groups, cs, set(), [event], max_solutions=5) == []

    def test_avoid_day_filters_correctly(self):
        """Tránh Thứ2 → chỉ còn A2 (Thứ3) hợp lệ."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9), _make("A2", "A", 3, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, {2}, [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A2"


class TestEdgeCases:
    def test_single_course_single_section(self):
        """1 môn, 1 nhóm → đúng 1 nghiệm."""
        groups = {"A": [_make("A1", "A", 2, 7, 9)]}
        cs = build_conflict_set(groups["A"])
        results = generate_schedules(groups, cs, set(), [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A1"

    def test_non_recurring_event_not_filtered(self):
        """is_recurring=False → KHÔNG chặn nhóm lớp."""
        groups = {"A": [_make("A1", "A", 3, 7, 9)]}
        event = PersonalEvent(
            event_id=1, student_id="s", title="1 lần",
            day_of_week=3, start_time=time(7, 0), end_time=time(9, 0),
            is_recurring=False,
        )
        cs = build_conflict_set(groups["A"])
        results = generate_schedules(groups, cs, set(), [event], max_solutions=5)
        assert len(results) == 1, "is_recurring=False không được lọc nhóm lớp"

    def test_event_without_day_not_filtered(self):
        """day_of_week=None → KHÔNG chặn nhóm lớp."""
        groups = {"A": [_make("A1", "A", 3, 7, 9)]}
        event = PersonalEvent(
            event_id=2, student_id="s", title="Không ngày",
            day_of_week=None, start_time=time(7, 0), end_time=time(9, 0),
            is_recurring=True,
        )
        cs = build_conflict_set(groups["A"])
        results = generate_schedules(groups, cs, set(), [event], max_solutions=5)
        assert len(results) == 1, "day_of_week=None không được lọc nhóm lớp"
