"""
Test suite cho Tầng 1 (build_conflict_set) và Tầng 2 (generate_schedules).
Dữ liệu thực từ schedule_data_from_web.json — trường STU.

Cách chạy:
    cd core
    pytest -s tests/test_csp_generator.py -v

Để tuỳ chỉnh:
    - COURSE_IDS     : danh sách môn muốn test
    - AVOID_DAYS     : ngày muốn tránh
    - PERSONAL_EVENTS: lịch bận cá nhân
"""

import json
import sys
from datetime import time, timedelta
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from csp_generator import generate_schedules
from detect_conflicts import build_conflict_set
from models import ClassSection, PersonalEvent

# ---------------------------------------------------------------------------
# Bảng tiết → giờ (theo lịch STU từ ảnh chụp màn hình)
#
#   Tiết 1–3  : 07:00 – 09:30  (mỗi tiết 50 phút)
#   Nghỉ giải lao: 09:30 – 09:35
#   Tiết 4–6  : 09:35 – 12:05
#   Nghỉ trưa : 12:05 – 12:35
#   Tiết 7–9  : 12:35 – 15:05
#   Nghỉ giải lao: 15:05 – 15:10
#   Tiết 10–12: 15:10 – 17:40
#   Nghỉ giải lao: 17:40 – 17:45
#   Tiết 13–15: 17:45 – 20:15
# ---------------------------------------------------------------------------
TIET_START: dict[int, time] = {
    1:  time(7,  0),
    2:  time(7,  50),
    3:  time(8,  40),
    4:  time(9,  35),   # sau nghỉ giải lao 09:30-09:35
    5:  time(10, 25),
    6:  time(11, 15),
    7:  time(12, 35),   # sau nghỉ trưa 12:05-12:35
    8:  time(13, 25),
    9:  time(14, 15),
    10: time(15, 10),   # sau nghỉ giải lao 15:05-15:10
    11: time(16, 0),
    12: time(16, 50),
    13: time(17, 45),   # sau nghỉ giải lao 17:40-17:45
    14: time(18, 35),
    15: time(19, 25),
}


def tiet_to_time(tiet_bat_dau: int, so_tiet: int) -> tuple[time, time]:
    """
    Chuyển (tiet_bat_dau, so_tiet) → (start_time, end_time).

    end_time = start của tiết cuối + 50 phút.
    Công thức này tự động bao gồm các khoảng nghỉ giải lao nằm
    trong khoảng [tiet_bat_dau, tiet_bat_dau + so_tiet - 1].

    Ví dụ:
        tiet_bat_dau=1, so_tiet=6  → 07:00 – 12:05  (Tiết 1-6)
        tiet_bat_dau=7, so_tiet=6  → 12:35 – 17:40  (Tiết 7-12)
        tiet_bat_dau=7, so_tiet=3  → 12:35 – 15:05  (Tiết 7-9)
    """
    start = TIET_START[tiet_bat_dau]
    last_tiet_start = TIET_START[tiet_bat_dau + so_tiet - 1]
    end_dt = (
        timedelta(hours=last_tiet_start.hour, minutes=last_tiet_start.minute)
        + timedelta(minutes=50)
    )
    end = time(int(end_dt.seconds // 3600), int((end_dt.seconds % 3600) // 60))
    return start, end


# ---------------------------------------------------------------------------
# Loader: JSON → CourseGroups
# ---------------------------------------------------------------------------
JSON_PATH = ROOT / "data" / "schedule_data_from_web.json"
SEMESTER_ID = "HK2-2025"   # dùng cho class_id và semester_id


def load_course_groups(course_ids: list[str]) -> dict[str, list[ClassSection]]:
    """
    Đọc JSON và trả về {course_id: [ClassSection]} cho các môn trong course_ids.

    Mỗi cặp (ma_mh, nhom_to) trong JSON tạo ra 1 ClassSection duy nhất.
    Nhiều record cùng nhom_to (khác thoi_gian) chỉ dùng record đầu tiên
    vì giờ học/ngày học không đổi trong suốt học kỳ.
    """
    raw: list[dict] = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    seen: set[tuple[str, str]] = set()
    groups: dict[str, list[ClassSection]] = {cid: [] for cid in course_ids}

    for rec in raw:
        course_id = rec["ma_mh"]
        if course_id not in groups:
            continue

        nhom = rec["nhom_to"]
        key = (course_id, nhom)
        if key in seen:
            continue            # bỏ qua record lặp cùng nhóm
        seen.add(key)

        lich = rec["lich_hoc"]
        if lich["so_tiet"] <= 0:
            continue

        start, end = tiet_to_time(lich["tiet_bat_dau"], lich["so_tiet"])

        groups[course_id].append(
            ClassSection(
                class_id    = f"{course_id}_{nhom}",
                course_id   = course_id,
                semester_id = SEMESTER_ID,
                day_of_week = int(lich["thu"]),
                start_time  = start,
                end_time    = end,
                room        = lich.get("phong"),
                instructor  = lich.get("giang_vien"),
                max_students= 1,
            )
        )

    return groups


# ===========================================================================
# ── CẤU HÌNH TEST ──────────────────────────────────────────────────────────
# Chỉnh sửa ba biến dưới đây để test theo nhu cầu thực tế.
# ===========================================================================

# Danh sách mã môn muốn xếp lịch (phải có trong schedule_data_from_web.json)
COURSE_IDS = [
   "CS03042", "CS03002", "CS09002", "GS49005", "GS19008", "CS03058", "GS79005", "GS33002",
]

# Ngày muốn tránh (2=Thứ2 … 8=CN). Sửa tuỳ ý.
# Ví dụ: {6, 7} = tránh Thứ 6 và Thứ 7
AVOID_DAYS: set[int] = {6, 7, 8}

# Lịch bận cá nhân. Sao chép và sửa từng mẫu theo nhu cầu.
PERSONAL_EVENTS: list[PersonalEvent] = [
    # Mẫu 1: sự kiện lặp hàng tuần — Thứ 4 buổi trưa
    PersonalEvent(
        event_id    = 1,
        student_id  = "test_student",
        title       = "Làm thêm quán cà phê",
        day_of_week = 4,                # Thứ 4
        start_time  = time(12, 35),     # 12:35
        end_time    = time(15, 5),      # 15:05  (Tiết 7-9)
        is_recurring= True,
    ),
    # Mẫu 2: sự kiện lặp hàng tuần — Thứ 6 sáng
    # PersonalEvent(
    #     event_id    = 2,
    #     student_id  = "test_student",
    #     title       = "Câu lạc bộ",
    #     day_of_week = 6,
    #     start_time  = time(7, 0),
    #     end_time    = time(9, 0),
    #     is_recurring= True,
    # ),
]

# ===========================================================================
# ── FIXTURES ───────────────────────────────────────────────────────────────
# ===========================================================================

@pytest.fixture(scope="session")
def course_groups() -> dict[str, list[ClassSection]]:
    groups = load_course_groups(COURSE_IDS)
    # Bỏ môn không có nhóm nào trong JSON
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
        course_groups   = course_groups,
        conflict_set    = conflict_set,
        avoid_days      = AVOID_DAYS,
        personal_events = PERSONAL_EVENTS,
        max_solutions   = 200,
    )


# ===========================================================================
# ── TEST: tiet_to_time ─────────────────────────────────────────────────────
# ===========================================================================

class TestTietToTime:
    def test_tiet_1_6(self):
        """Tiết 1-6: 07:00 – 12:05 (khớp ảnh chụp màn hình)"""
        start, end = tiet_to_time(1, 6)
        assert start == time(7, 0)
        assert end   == time(12, 5)

    def test_tiet_7_12(self):
        """Tiết 7-12: 12:35 – 17:40 (khớp ảnh chụp màn hình)"""
        start, end = tiet_to_time(7, 6)
        assert start == time(12, 35)
        assert end   == time(17, 40)

    def test_tiet_7_3(self):
        """Tiết 7-9: 12:35 – 15:05"""
        start, end = tiet_to_time(7, 3)
        assert start == time(12, 35)
        assert end   == time(15, 5)

    def test_tiet_10_3(self):
        """Tiết 10-12: 15:10 – 17:40"""
        start, end = tiet_to_time(10, 3)
        assert start == time(15, 10)
        assert end   == time(17, 40)

    def test_tiet_single(self):
        """1 tiết: đúng 50 phút"""
        start, end = tiet_to_time(1, 1)
        assert start == time(7, 0)
        assert end   == time(7, 50)

    def test_lunch_boundary(self):
        """
        Tiết 6 kết thúc lúc 12:05, Tiết 7 bắt đầu 12:35.
        Hai lớp này không xung đột (12:05 == 12:35 là false, SRS 6.1.1).
        """
        _, end_tiet6   = tiet_to_time(6, 1)   # 12:05
        start_tiet7, _ = tiet_to_time(7, 1)   # 12:35
        assert end_tiet6 < start_tiet7         # không giao nhau


# ===========================================================================
# ── TEST: load_course_groups ───────────────────────────────────────────────
# ===========================================================================

class TestLoader:
    def test_all_courses_loaded(self, course_groups):
        """Tất cả môn trong COURSE_IDS phải có nhóm lớp."""
        for cid in COURSE_IDS:
            if cid in course_groups:
                assert len(course_groups[cid]) > 0, f"{cid} không có nhóm lớp nào"

    def test_no_duplicate_class_id(self, all_classes):
        """Mỗi class_id phải là duy nhất."""
        ids = [cls.class_id for cls in all_classes]
        assert len(ids) == len(set(ids)), "Có class_id bị trùng"

    def test_time_valid(self, all_classes):
        """start_time < end_time cho tất cả nhóm lớp."""
        for cls in all_classes:
            assert cls.start_time < cls.end_time, (
                f"{cls.class_id}: start={cls.start_time} >= end={cls.end_time}"
            )

    def test_day_of_week_range(self, all_classes):
        """day_of_week phải trong [2, 8]."""
        for cls in all_classes:
            assert 2 <= cls.day_of_week <= 8, (
                f"{cls.class_id}: day_of_week={cls.day_of_week} ngoài phạm vi"
            )


# ===========================================================================
# ── TEST: build_conflict_set ───────────────────────────────────────────────
# ===========================================================================

class TestConflictSet:
    def test_symmetric(self, conflict_set):
        """Mọi (a,b) phải có (b,a) tương ứng."""
        for a, b in conflict_set:
            assert (b, a) in conflict_set, f"Thiếu chiều ngược: ({b},{a})"

    def test_no_self_conflict(self, conflict_set):
        """Không có lớp xung đột với chính nó."""
        for a, b in conflict_set:
            assert a != b, f"Self-conflict: {a}"

    def test_conflict_means_same_day_overlap(self, all_classes, conflict_set):
        """
        Với mỗi cặp trong conflict_set, hai lớp phải cùng thứ
        và thực sự giao giờ.
        """
        cls_map = {cls.class_id: cls for cls in all_classes}
        checked = set()

        for aid, bid in conflict_set:
            if (bid, aid) in checked:
                continue
            checked.add((aid, bid))

            a = cls_map[aid]
            b = cls_map[bid]
            assert a.day_of_week == b.day_of_week, (
                f"{aid} và {bid} khác thứ nhưng nằm trong conflict_set"
            )
            assert a.start_time < b.end_time, (
                f"{aid}.start >= {bid}.end nhưng nằm trong conflict_set"
            )
            assert b.start_time < a.end_time, (
                f"{bid}.start >= {aid}.end nhưng nằm trong conflict_set"
            )

    def test_non_conflict_not_in_set(self, all_classes, conflict_set):
        """
        Hai lớp khác thứ KHÔNG được có trong conflict_set.
        """
        cls_map = {cls.class_id: cls for cls in all_classes}
        for aid, bid in list(conflict_set)[:50]:   # sample 50 cặp
            a = cls_map[aid]
            b = cls_map[bid]
            assert a.day_of_week == b.day_of_week

    def test_boundary_no_conflict(self, all_classes):
        """
        Lớp A kết thúc đúng lúc lớp B bắt đầu → KHÔNG xung đột (SRS 6.1.1).
        Ví dụ: Tiết 6 kết thúc 12:05, Tiết 7 bắt đầu 12:35.
        """
        # Tạo 2 lớp giả đúng boundary
        a = ClassSection(
            class_id="BOUND_A", course_id="X", semester_id=SEMESTER_ID,
            day_of_week=2, start_time=time(7, 0), end_time=time(9, 0),
        )
        b = ClassSection(
            class_id="BOUND_B", course_id="Y", semester_id=SEMESTER_ID,
            day_of_week=2, start_time=time(9, 0), end_time=time(11, 0),
        )
        cs = build_conflict_set([a, b])
        assert ("BOUND_A", "BOUND_B") not in cs, (
            "Boundary case sai: end==start không được tính là xung đột"
        )


# ===========================================================================
# ── TEST: generate_schedules ───────────────────────────────────────────────
# ===========================================================================

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
                    a = classes[i]
                    b = classes[j]
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
                    if event.day_of_week is None:
                        continue
                    if cls.day_of_week != event.day_of_week:
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
                course_groups   = course_groups,
                conflict_set    = conflict_set,
                avoid_days      = AVOID_DAYS,
                personal_events = PERSONAL_EVENTS,
                max_solutions   = limit,
            )
            assert len(results) <= limit, (
                f"max_solutions={limit} nhưng trả {len(results)} nghiệm"
            )

    def test_empty_when_all_days_avoided(self, course_groups, conflict_set):
        """Nếu tránh tất cả các ngày → không có nghiệm."""
        result = generate_schedules(
            course_groups   = course_groups,
            conflict_set    = conflict_set,
            avoid_days      = {2, 3, 4, 5, 6, 7, 8},   # tránh hết
            personal_events = [],
            max_solutions   = 10,
        )
        assert result == [], "Phải trả [] khi tránh tất cả các ngày"

    def test_empty_course_groups(self, conflict_set):
        """course_groups rỗng → trả []."""
        result = generate_schedules(
            course_groups   = {},
            conflict_set    = conflict_set,
            avoid_days      = set(),
            personal_events = [],
        )
        assert result == []

    def test_schedules_are_unique(self, valid_schedules):
        """Không có hai TKB giống hệt nhau."""
        seen = []
        for sched in valid_schedules:
            key = frozenset((k, v.class_id) for k, v in sched.items())
            assert key not in seen, "Có TKB bị lặp"
            seen.append(key)


# ===========================================================================
# ── TEST: tích hợp end-to-end với 2 môn đơn giản ──────────────────────────
# ===========================================================================

class TestEndToEndSimple:
    """
    Test với dữ liệu tạo thủ công — dễ kiểm soát kết quả.
    Không phụ thuộc JSON.
    """

    def _make_class(self, cid, course, day, start_h, end_h) -> ClassSection:
        return ClassSection(
            class_id=cid, course_id=course, semester_id="TEST",
            day_of_week=day,
            start_time=time(start_h, 0), end_time=time(end_h, 0),
        )

    def test_two_courses_no_conflict(self):
        """2 môn, không xung đột → có nghiệm."""
        groups = {
            "A": [self._make_class("A1", "A", 2, 7, 9),
                  self._make_class("A2", "A", 3, 7, 9)],
            "B": [self._make_class("B1", "B", 4, 7, 9),
                  self._make_class("B2", "B", 5, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=10)
        assert len(results) == 4   # 2×2 tổ hợp

    def test_two_courses_full_conflict(self):
        """
        2 môn, mọi nhóm đều xung đột nhau → không có nghiệm.
        (A1,A2 đều Thứ2 07-09; B1,B2 đều Thứ2 07-09)
        """
        groups = {
            "A": [self._make_class("A1", "A", 2, 7, 9),
                  self._make_class("A2", "A", 2, 7, 9)],
            "B": [self._make_class("B1", "B", 2, 7, 9),
                  self._make_class("B2", "B", 2, 7, 9)],
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=10)
        assert results == []

    def test_personal_event_blocks_all(self):
        """
        PersonalEvent chặn tất cả nhóm của một môn → không có nghiệm.
        """
        groups = {
            "A": [self._make_class("A1", "A", 2, 7, 9)],
            "B": [self._make_class("B1", "B", 3, 7, 9)],
        }
        event = PersonalEvent(
            event_id=1, student_id="s",
            title="Bận", day_of_week=3,
            start_time=time(6, 0), end_time=time(10, 0),
            is_recurring=True,
        )
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [event], max_solutions=5)
        assert results == []

    def test_avoid_day_filters_correctly(self):
        """
        Tránh Thứ 2 → chỉ còn A2 (Thứ3) hợp lệ cho môn A.
        """
        groups = {
            "A": [self._make_class("A1", "A", 2, 7, 9),   # Thứ2 — bị lọc
                  self._make_class("A2", "A", 3, 7, 9)],  # Thứ3 — OK
        }
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, {2}, [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A2"

    def test_mrv_finds_correct_solution(self):
        """
        MRV phải chọn môn có ít lựa chọn nhất — kiểm tra kết quả đúng.
        """
        groups = {
            "A": [self._make_class("A1", "A", 2, 7, 9)],        # 1 lựa chọn
            "B": [self._make_class("B1", "B", 2, 7, 9),          # 2 lựa chọn
                  self._make_class("B2", "B", 3, 7, 9)],
        }
        # A1 và B1 cùng Thứ2 07-09 → xung đột
        cs = build_conflict_set([c for s in groups.values() for c in s])
        results = generate_schedules(groups, cs, set(), [], max_solutions=5)
        assert len(results) == 1
        assert results[0]["A"].class_id == "A1"
        assert results[0]["B"].class_id == "B2"   # B1 bị FC loại


# ===========================================================================
# ── IN KẾT QUẢ NGHIỆM ──────────────────────────────────────────────────────
# ===========================================================================

DAY_LABEL = {2: "Thu 2", 3: "Thu 3", 4: "Thu 4",
             5: "Thu 5", 6: "Thu 6", 7: "Thu 7", 8: "CN"}
PRINT_MAX = 200   # số TKB muốn in


def _print_schedule(idx: int, sched: dict) -> None:
    print(f"\n{'='*70}")
    print(f"  TKB #{idx}")
    print(f"{'='*70}")
    print(f"{'Mon':<12} {'Nhom':<25} {'Thu':<8} {'Gio':<14} {'Phong':<12} GV")
    print(f"{'-'*70}")
    for cid, cls in sorted(sched.items(), key=lambda x: x[1].day_of_week):
        nhom = cls.class_id.replace(cid + "_", "")
        day  = DAY_LABEL.get(cls.day_of_week, str(cls.day_of_week))
        gio  = f"{cls.start_time.strftime('%H:%M')}-{cls.end_time.strftime('%H:%M')}"
        print(f"{cid:<12} {nhom:<25} {day:<8} {gio:<14} {cls.room or '-':<12} {cls.instructor or '-'}")


class TestPrintSchedules:
    """In ra tối đa PRINT_MAX TKB để kiểm tra trực quan. Chạy với pytest -s."""

    def test_print_valid_schedules(self, valid_schedules):
        """In PRINT_MAX TKB đầu tiên — không assert, chỉ in để xem."""
        if not valid_schedules:
            print("\n[!] Khong tim duoc TKB hop le. Kiem tra COURSE_IDS / AVOID_DAYS.")
            return

        to_print = valid_schedules[:PRINT_MAX]
        print(f"\n\nTim duoc {len(valid_schedules)} TKB. In ra {len(to_print)} TKB:\n")
        for i, sched in enumerate(to_print, start=1):
            _print_schedule(i, sched)
        print()
