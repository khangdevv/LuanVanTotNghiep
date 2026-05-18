"""
pytest tests/test_detect_conflicts.py -v
"""
from datetime import time

from conftest import SEMESTER_ID
from detect_conflicts import build_conflict_set, detect_conflicts
from models import ClassSection


def _make(cid: str, course: str, day: int, sh: int, eh: int) -> ClassSection:
    return ClassSection(
        class_id=cid, course_id=course, semester_id=SEMESTER_ID,
        day_of_week=day, start_time=time(sh, 0), end_time=time(eh, 0),
    )


# ── build_conflict_set ────────────────────────────────────────────────────
class TestBuildConflictSet:
    def test_symmetric(self, conflict_set):
        """Mọi (a,b) phải có (b,a) tương ứng."""
        for a, b in conflict_set:
            assert (b, a) in conflict_set, f"Thiếu chiều ngược: ({b},{a})"

    def test_no_self_conflict(self, conflict_set):
        """Không có lớp xung đột với chính nó."""
        for a, b in conflict_set:
            assert a != b, f"Self-conflict: {a}"

    def test_conflict_means_same_day_overlap(self, all_classes, conflict_set):
        """Mọi cặp trong conflict_set phải cùng thứ và thực sự giao giờ."""
        cls_map = {cls.class_id: cls for cls in all_classes}
        checked: set[tuple[str, str]] = set()
        for aid, bid in conflict_set:
            if (bid, aid) in checked:
                continue
            checked.add((aid, bid))
            a, b = cls_map[aid], cls_map[bid]
            assert a.day_of_week == b.day_of_week, (
                f"{aid} và {bid} khác thứ nhưng nằm trong conflict_set"
            )
            assert a.start_time < b.end_time
            assert b.start_time < a.end_time

    def test_non_conflict_same_day_only(self, all_classes, conflict_set):
        """Mọi cặp trong conflict_set (sample 50) phải cùng thứ."""
        cls_map = {cls.class_id: cls for cls in all_classes}
        for aid, bid in list(conflict_set)[:50]:
            assert cls_map[aid].day_of_week == cls_map[bid].day_of_week

    def test_boundary_no_conflict(self):
        """end_time == start_time → KHÔNG xung đột (strict <)."""
        a = _make("BOUND_A", "X", 2, 7, 9)
        b = _make("BOUND_B", "Y", 2, 9, 11)
        cs = build_conflict_set([a, b])
        assert ("BOUND_A", "BOUND_B") not in cs


# ── detect_conflicts ──────────────────────────────────────────────────────
class TestDetectConflicts:
    def test_empty_input(self):
        """Danh sách rỗng → trả []."""
        assert detect_conflicts([]) == []

    def test_single_class(self):
        """1 lớp → không có cặp xung đột."""
        assert detect_conflicts([_make("A1", "A", 2, 7, 9)]) == []

    def test_overlap_detected(self):
        """2 lớp cùng thứ, giao giờ → phát hiện đúng 1 cặp."""
        a = _make("A1", "A", 2, 7,  9)
        b = _make("B1", "B", 2, 8, 10)
        result = detect_conflicts([a, b])
        assert len(result) == 1
        assert {result[0][0].class_id, result[0][1].class_id} == {"A1", "B1"}

    def test_different_day_no_conflict(self):
        """2 lớp khác thứ, cùng giờ → không xung đột."""
        assert detect_conflicts([_make("A1", "A", 2, 7, 9),
                                 _make("B1", "B", 3, 7, 9)]) == []

    def test_boundary_no_conflict(self):
        """end_time == start_time → không xung đột (strict <)."""
        assert detect_conflicts([_make("A1", "A", 2, 7, 9),
                                 _make("B1", "B", 2, 9, 11)]) == []

    def test_returns_classsection_objects(self):
        """Kết quả là list[tuple[ClassSection, ClassSection]]."""
        a = _make("A1", "A", 2, 7, 9)
        b = _make("B1", "B", 2, 7, 9)
        result = detect_conflicts([a, b])
        assert len(result) == 1
        assert isinstance(result[0], tuple)
        assert isinstance(result[0][0], ClassSection)
        assert isinstance(result[0][1], ClassSection)

    def test_three_classes_same_slot(self):
        """3 lớp cùng thứ cùng giờ → C(3,2) = 3 cặp."""
        classes = [_make(f"X{i}", "X", 2, 7, 9) for i in range(3)]
        assert len(detect_conflicts(classes)) == 3
