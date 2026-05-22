"""
pytest tests/test_generate_schedules.py -v
pytest tests/test_generate_schedules.py -v -s      # in TKB ra terminal
"""
from datetime import time

import pytest

from conftest import AVOID_DAYS, PERSONAL_EVENTS, SEMESTER_ID
from csp_generator import generate_schedules
from detect_conflicts import build_conflict_set
from models import ClassSection, PersonalEvent


def _make(cid: str, course: str, day: int, sh: int, eh: int) -> ClassSection:
    return ClassSection(
        class_id=cid, course_id=course, semester_id=SEMESTER_ID,
        day_of_week=day, start_time=time(sh, 0), end_time=time(eh, 0),
    )


# ── Tích hợp với dữ liệu thật ────────────────────────────────────────────
class TestGenerateSchedules:
    def test_returns_list(self, valid_schedules):
        """Kết quả phải là list."""
        assert isinstance(valid_schedules, list)

    def test_each_schedule_covers_all_courses(self, valid_schedules, course_groups):
        """Mỗi TKB phải có đúng 1 nhóm cho mỗi môn."""
        if not valid_schedules:
            pytest.skip("Không có nghiệm — kiểm tra COURSE_IDS và AVOID_DAYS")
        for sched in valid_schedules:
            assert set(sched.keys()) == set(course_groups.keys()), (
                "TKB thiếu hoặc thừa môn học"
            )

    def test_no_internal_conflict(self, valid_schedules, conflict_set):
        """Không có TKB nào chứa hai lớp xung đột với nhau."""
        for sched in valid_schedules:
            classes = list(sched.values())
            for i in range(len(classes)):
                for j in range(i + 1, len(classes)):
                    a, b = classes[i], classes[j]
                    assert (a.class_id, b.class_id) not in conflict_set, (
                        f"Xung đột lọt qua: {a.class_id} ↔ {b.class_id}"
                    )

    def test_no_avoid_day_classes(self, valid_schedules):
        """Không có lớp nào rơi vào ngày trong AVOID_DAYS."""
        for sched in valid_schedules:
            for cls in sched.values():
                assert cls.day_of_week not in AVOID_DAYS, (
                    f"{cls.class_id} rơi vào ngày tránh: {cls.day_of_week}"
                )

    def test_no_personal_event_conflict(self, valid_schedules):
        """Không có lớp nào trùng với PersonalEvents."""
        for sched in valid_schedules:
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

    def test_schedules_are_unique(self, valid_schedules):
        """Không có hai TKB giống hệt nhau."""
        seen: list[frozenset] = []
        for sched in valid_schedules:
            key = frozenset((k, v.class_id) for k, v in sched.items())
            assert key not in seen, "Có TKB bị lặp"
            seen.append(key)


# ── Test đơn giản với dữ liệu tạo thủ công ───────────────────────────────
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

    def test_mrv_finds_correct_solution(self):
        """MRV chọn môn ít lựa chọn nhất → kết quả đúng."""
        groups = {
            "A": [_make("A1", "A", 2, 7, 9)],
            "B": [_make("B1", "B", 2, 7, 9), _make("B2", "B", 3, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A1"
        assert results[0]["B"].class_id == "B2"


# ── Edge cases ────────────────────────────────────────────────────────────
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

    def test_fc_dead_end_pruned(self):
        """
        Gán A1 → FC xóa B1 (domain B rỗng) → dead-end → backtrack sang A2.
        B chỉ có 1 nhóm → chỉ A2 tạo được nghiệm.
        """
        groups = {
            "A": [_make("A1", "A", 2, 7, 9), _make("A2", "A", 3, 7, 9)],
            "B": [_make("B1", "B", 2, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A2"
        assert results[0]["B"].class_id == "B1"

    def test_lcv_effect_on_solution_order(self):
        """
        LCV ưu tiên nhóm ít xung đột → nghiệm đầu tiên dùng nhóm ít ràng buộc,
        dù domain gốc sắp nó sau.
        """
        a_free = _make("A_free", "A", 5, 7, 9)   # không xung đột với B
        a_busy = _make("A_busy", "A", 2, 7, 9)   # xung đột B1
        b1     = _make("B1",     "B", 2, 7, 9)
        b2     = _make("B2",     "B", 4, 7, 9)
        cs = build_conflict_set([a_free, a_busy, b1, b2])
        groups = {"A": [a_busy, a_free], "B": [b1, b2]}  # a_busy đứng trước trong domain
        results = generate_schedules(groups, cs, set(), [], max_solutions=1)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A_free"


# ── In kết quả TKB (chạy với pytest -s) ──────────────────────────────────
_DAY_LABEL = {2: "Thu 2", 3: "Thu 3", 4: "Thu 4",
              5: "Thu 5", 6: "Thu 6", 7: "Thu 7", 8: "CN"}
_PRINT_MAX = 200


def _print_schedule(idx: int, sched: dict) -> None:
    print(f"\n{'='*70}")
    print(f"  TKB #{idx}")
    print(f"{'='*70}")
    print(f"{'Mon':<12} {'Nhom':<25} {'Thu':<8} {'Gio':<14} {'Phong':<12} GV")
    print(f"{'-'*70}")
    for cid, cls in sorted(sched.items(), key=lambda x: x[1].day_of_week):
        nhom = cls.class_id.replace(cid + "_", "").rsplit("_t", 1)[0]
        day  = _DAY_LABEL.get(cls.day_of_week, str(cls.day_of_week))
        gio  = f"{cls.start_time.strftime('%H:%M')}-{cls.end_time.strftime('%H:%M')}"
        print(f"{cid:<12} {nhom:<25} {day:<8} {gio:<14} {cls.room or '-':<12} {cls.instructor or '-'}")


class TestPrintSchedules:
    def test_print_valid_schedules(self, valid_schedules):
        """In tối đa _PRINT_MAX TKB ra terminal — không assert, chỉ để xem."""
        if not valid_schedules:
            print("\n[!] Khong tim duoc TKB hop le. Kiem tra COURSE_IDS / AVOID_DAYS.")
            return
        to_print = valid_schedules[:_PRINT_MAX]
        print(f"\n\nTim duoc {len(valid_schedules)} TKB. In ra {len(to_print)} TKB:\n")
        for i, sched in enumerate(to_print, start=1):
            _print_schedule(i, sched)
        print()
