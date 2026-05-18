"""
pytest tests/test_lcv.py -v
"""
from datetime import time

from csp_generator import _choose_next_section_of_course
from detect_conflicts import build_conflict_set
from models import ClassSection


def _make(cid: str, course: str, day: int, sh: int, eh: int) -> ClassSection:
    return ClassSection(
        class_id=cid, course_id=course, semester_id="TEST",
        day_of_week=day, start_time=time(sh, 0), end_time=time(eh, 0),
    )


class TestLCV:
    def test_less_constraining_first(self):
        """Nhóm ít xung đột với domain còn lại phải đứng trước."""
        a1 = _make("A1", "A", 2, 7, 9)   # xung đột B1
        a2 = _make("A2", "A", 3, 7, 9)   # không xung đột
        b1 = _make("B1", "B", 2, 7, 9)
        b2 = _make("B2", "B", 4, 7, 9)
        cs = build_conflict_set([a1, a2, b1, b2])
        domains = {"A": [a1, a2], "B": [b1, b2]}
        result = _choose_next_section_of_course("A", domains, ["B"], cs)
        assert result[0].class_id == "A2"
        assert result[1].class_id == "A1"

    def test_empty_unassigned_preserves_order(self):
        """Không còn môn nào chưa gán → conflict_count đều 0 → giữ thứ tự gốc."""
        a1 = _make("A1", "A", 2, 7, 9)
        a2 = _make("A2", "A", 3, 7, 9)
        domains = {"A": [a1, a2]}
        result = _choose_next_section_of_course("A", domains, [], set())
        assert result[0].class_id == "A1"
        assert result[1].class_id == "A2"

    def test_stable_sort_on_tie(self):
        """Khi conflict_count bằng nhau → thứ tự gốc được giữ (stable sort)."""
        a1 = _make("A1", "A", 2, 7,  9)
        a2 = _make("A2", "A", 2, 9, 11)
        b1 = _make("B1", "B", 3, 7,  9)   # không xung đột với cả hai
        cs = build_conflict_set([a1, a2, b1])
        domains = {"A": [a1, a2], "B": [b1]}
        result = _choose_next_section_of_course("A", domains, ["B"], cs)
        assert result[0].class_id == "A1"
        assert result[1].class_id == "A2"

    def test_sums_conflicts_across_multiple_courses(self):
        """conflict_count là tổng xung đột qua tất cả môn chưa gán."""
        # A1 xung đột B1 + C1 → count=2;  A2 chỉ xung đột C2 → count=1
        a1 = _make("A1", "A", 2, 7, 9)
        a2 = _make("A2", "A", 2, 9, 11)
        b1 = _make("B1", "B", 2, 7, 9)
        c1 = _make("C1", "C", 2, 7, 9)
        c2 = _make("C2", "C", 2, 9, 11)
        cs = build_conflict_set([a1, a2, b1, c1, c2])
        domains = {"A": [a1, a2], "B": [b1], "C": [c1, c2]}
        result = _choose_next_section_of_course("A", domains, ["B", "C"], cs)
        assert result[0].class_id == "A2"
        assert result[1].class_id == "A1"

    def test_returns_all_candidates(self):
        """Số phần tử trả về bằng đúng số nhóm trong domain."""
        classes = [_make(f"A{i}", "A", 2 + i, 7, 9) for i in range(4)]
        domains = {"A": classes}
        result = _choose_next_section_of_course("A", domains, [], set())
        assert len(result) == 4
