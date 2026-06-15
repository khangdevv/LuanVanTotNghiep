"""
pytest tests/test_ortools_generator.py -v
pytest tests/test_ortools_generator.py -v -s      # in TKB ra terminal
"""
from datetime import time

import pytest

from conftest import AVOID_DAYS, PERSONAL_EVENTS, SEMESTER_ID
from or_tools_generator import solve_schedule as generate_schedules
from detect_conflicts import build_conflict_set
from models import ClassSection, PersonalEvent


def _make(cid: str, course: str, day: int, sh: int, eh: int) -> ClassSection:
    return ClassSection(
        class_id=cid, course_id=course, semester_id=SEMESTER_ID,
        day_of_week=day, start_time=time(sh, 0), end_time=time(eh, 0),
    )


# Tích hợp với dữ liệu thật
class TestOrToolsGenerateSchedules:
    def test_returns_list(self, valid_schedules_ortools):
        """Kết quả phải là list."""
        assert isinstance(valid_schedules_ortools, list)

    def test_each_schedule_covers_all_courses(self, valid_schedules_ortools, course_groups):
        """Mỗi TKB phải có đúng 1 nhóm cho mỗi môn."""
        if not valid_schedules_ortools:
            pytest.skip("Không có nghiệm — kiểm tra COURSE_IDS và AVOID_DAYS")
        for sched in valid_schedules_ortools:
            assert set(sched.keys()) == set(course_groups.keys()), (
                "TKB thiếu hoặc thừa môn học"
            )

    def test_no_internal_conflict(self, valid_schedules_ortools, conflict_set):
        """Không có TKB nào chứa hai lớp xung đột với nhau."""
        for sched in valid_schedules_ortools:
            classes = list(sched.values())
            for i in range(len(classes)):
                for j in range(i + 1, len(classes)):
                    a, b = classes[i], classes[j]
                    assert (a.class_id, b.class_id) not in conflict_set, (
                        f"Xung đột lọt qua: {a.class_id} ↔ {b.class_id}"
                    )

    def test_no_avoid_day_classes(self, valid_schedules_ortools):
        """Không có lớp nào rơi vào ngày trong AVOID_DAYS."""
        for sched in valid_schedules_ortools:
            for cls in sched.values():
                assert cls.day_of_week not in AVOID_DAYS, (
                    f"{cls.class_id} rơi vào ngày tránh: {cls.day_of_week}"
                )

    def test_no_personal_event_conflict(self, valid_schedules_ortools):
        """Không có lớp nào trùng với PersonalEvents."""
        for sched in valid_schedules_ortools:
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

    @pytest.mark.parametrize("limit", [1, 3, 5])
    def test_max_solutions_respected(self, course_groups, conflict_set, limit):
        """Số nghiệm trả về không vượt quá max_solutions."""
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

    def test_schedules_are_unique(self, valid_schedules_ortools):
        """Không có hai TKB giống hệt nhau."""
        seen: list[frozenset] = []
        for sched in valid_schedules_ortools:
            key = frozenset((k, v.class_id) for k, v in sched.items())
            assert key not in seen, "Có TKB bị lặp"
            seen.append(key)


# Test đơn giản với dữ liệu tạo thủ công
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
        """Mọi tổ hợp (A×B) đều xung đột → không có nghiệm."""
        # Tất cả nhóm cùng Thứ2 7-9 → mọi cặp (A,B) đều xung đột nhau
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


# Edge cases
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

    def test_max_solutions_zero_returns_empty(self):
        """max_solutions=0 → trả [] ngay lập tức."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9)],
            "B": [_make("B1", "B", 3, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        result = generate_schedules(groups, cs, set(), [], max_solutions=0)
        assert result == []

    def test_partial_conflict_finds_valid_combo(self):
        """
        A1 xung đột B1 (cùng Thứ2 7-9) nhưng A2 (Thứ3) không xung đột B1 →
        chỉ nghiệm (A2, B1) hợp lệ.
        Solver OR-Tools phải loại bỏ đúng cặp (A1, B1).
        """
        a1 = _make("A1", "A", 2, 7, 9)
        a2 = _make("A2", "A", 3, 7, 9)
        b1 = _make("B1", "B", 2, 7, 9)  # xung đột với A1 (cùng ngày+giờ)
        groups = {"A": [a1, a2], "B": [b1]}
        cs = build_conflict_set([a1, a2, b1])  # chỉ A1↔B1 conflict
        results = generate_schedules(groups, cs, set(), [], max_solutions=5)
        # Nghiệm hợp lệ là (A2, B1); (A1, B1) bị loại do xung đột
        valid = [r for r in results if r["A"].class_id == "A2"]
        assert len(valid) >= 1
        assert all(r["B"].class_id == "B1" for r in valid)

    def test_three_courses_all_distinct_days(self):
        """3 môn mỗi môn 2 nhóm, tất cả khác ngày → đúng 2³=8 tổ hợp."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9), _make("A2", "A", 3, 7, 9)],
            "B": [_make("B1", "B", 4, 7, 9), _make("B2", "B", 5, 7, 9)],
            "C": [_make("C1", "C", 6, 7, 9), _make("C2", "C", 7, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=20)
        assert len(results) == 8

    def test_personal_event_partial_block(self):
        """
        PersonalEvent chặn A1 (Thứ3) nhưng không chặn A2 (Thứ2) →
        chỉ còn A2 hợp lệ.
        """
        groups = {
            "A": [_make("A1", "A", 3, 7, 9), _make("A2", "A", 2, 7, 9)],
        }
        event = PersonalEvent(
            event_id=1, student_id="s", title="Họp nhóm",
            day_of_week=3, start_time=time(6, 0), end_time=time(10, 0),
            is_recurring=True,
        )
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [event], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A2"

    def test_avoid_days_filters_multiple_days(self):
        """Tránh Thứ2 và Thứ3 → chỉ còn A3 (Thứ4)."""
        groups = {
            "A": [
                _make("A1", "A", 2, 7, 9),
                _make("A2", "A", 3, 7, 9),
                _make("A3", "A", 4, 7, 9),
            ],
        }
        cs = build_conflict_set(groups["A"])
        results = generate_schedules(groups, cs, {2, 3}, [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A3"

    def test_single_section_per_course_always_selected(self):
        """Mỗi môn chỉ có 1 nhóm không xung đột nhau → kết quả đúng 1 nghiệm."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9)],
            "B": [_make("B1", "B", 3, 7, 9)],
            "C": [_make("C1", "C", 4, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A1"
        assert results[0]["B"].class_id == "B1"
        assert results[0]["C"].class_id == "C1"

    def test_max_solutions_one_returns_exactly_one(self):
        """max_solutions=1 → trả đúng 1 nghiệm dù có nhiều nghiệm tồn tại."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9), _make("A2", "A", 3, 7, 9)],
            "B": [_make("B1", "B", 4, 7, 9), _make("B2", "B", 5, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=1)
        assert len(results) == 1

    def test_adjacent_times_no_conflict(self):
        """
        A kết thúc lúc 9:00, B bắt đầu lúc 9:00 → không xung đột (liền kề).
        Cả hai nhóm đều hợp lệ trong cùng 1 TKB.
        """
        groups = {
            "A": [_make("A1", "A", 2, 7, 9)],
            "B": [_make("B1", "B", 2, 9, 11)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A1"
        assert results[0]["B"].class_id == "B1"
