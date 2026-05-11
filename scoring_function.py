from __future__ import annotations

from collections import defaultdict

from enums.preferred_slot import PreferredSlot
from models.classes import ClassSection
from models.preferences import Preference

_DESIGNED_GAPS = {(570, 575), (725, 755), (905, 910)}
_CA_MINUTES = (420, 575, 755, 910)  # Ca1–Ca4 quy ra phút từ 00:00

_SLOT_TO_CAS: dict[PreferredSlot, set[int]] = {
    PreferredSlot.MORNING:   {1, 2},
    PreferredSlot.AFTERNOON: {3, 4},
}


def _to_minutes(t) -> int:
    return t.hour * 60 + t.minute

# lấy vị trí ca
def _get_ca_num(t) -> int | None:
    m = _to_minutes(t)
    ca1, ca2, ca3, ca4 = _CA_MINUTES
    if m == ca1:
        return 1
    if m == ca2:
        return 2
    if m == ca3:
        return 3
    if m >= ca4:
        return 4
    return None

# giới hạn để trong khoảng 0 đến 1.0
def _clamp_01(value: float) -> float:
    return max(0.0, min(1.0, value))


# ánh xạ điểm theo phút
def _gap_score(gap: int) -> float:
    if gap < 0:
        # quá gấp
        return 0.0 
    if gap < 10:
        # hợp lí nhất
        return 0.2
    if gap <= 90:
        # mức ổn chấp nhận dc
        return 1.0
    if gap <= 180:
        # bỏ trống 1 ca
        return 0.7
    if gap <= 300:
        # bỏ trống 2 ca
        return 0.4
    return 0.1

# tính điểm chất lượng khoảng nghỉ
def calculate_break_time_score(schedule: list[ClassSection]) -> float:
    by_day: dict[int, list[ClassSection]] = defaultdict(list) # tự táo list mới với key mới
    for cls in schedule:
        by_day[cls.day_of_week].append(cls)

    gap_scores: list[float] = []
    for sessions in by_day.values():
        sorted_sessions = sorted(sessions, key=lambda s: _to_minutes(s.start_time)) # sắp xếp theo tăng thời lượng dần
        for i in range(len(sorted_sessions) - 1):
            # tính khoảng nghỉ giữa kết thúc của lớp trước đó và bắt đầu lớp kế tiếp
            end_min   = _to_minutes(sorted_sessions[i].end_time)
            start_min = _to_minutes(sorted_sessions[i + 1].start_time)
            gap = start_min - end_min
            if (end_min, start_min) in _DESIGNED_GAPS:
                gap_scores.append(1.0)
            else:
                gap_scores.append(_gap_score(gap))

    return 1.0 if not gap_scores else _clamp_01(sum(gap_scores) / len(gap_scores))

# tính điểm dự trên tkb sở thích
def calculate_preference_match_score(schedule: list[ClassSection], preferences: Preference, avoid_days: list[int] = [],
) -> float:
    preferred_cas = _SLOT_TO_CAS.get(preferences.preferred_slot, set())
    avoid_set = set(avoid_days)

    class_scores: list[float] = []
    for cls in schedule:
        # lấy vị trí rồi kiểm tra dựa trên buổi yêu thích và ngày cần tránh để tính điểm
        ca_num = _get_ca_num(cls.start_time)
        time_score = 1.0 if ca_num in preferred_cas else 0.0
        day_score  = 0.0 if cls.day_of_week in avoid_set else 1.0
        class_scores.append((time_score + day_score) / 2)

    return 1.0 if not class_scores else _clamp_01(sum(class_scores) / len(class_scores))

# tính điểm phân bố đều khối lượng học
def calculate_workload_balance_score(schedule: list[ClassSection]) -> float:
    by_day: dict[int, int] = defaultdict(int)
    for cls in schedule:
        # đếm số lớp theo ngày
        by_day[cls.day_of_week] += 1

    # lấy điểm tính phương sai
    counts = list(by_day.values())
    if len(counts) <= 1:
        return 1.0

    avg      = sum(counts) / len(counts)
    variance = sum((c - avg) ** 2 for c in counts) / len(counts)
    return _clamp_01(max(0.0, 1.0 - variance / 9.0))


def calculate_total_score(schedule: list[ClassSection], preferences: Preference, avoid_days: list[int] = [],
) -> dict[str, float]:
    break_score      = calculate_break_time_score(schedule)
    preference_score = calculate_preference_match_score(schedule, preferences, avoid_days)
    balance_score    = calculate_workload_balance_score(schedule)

    total = round(
        preferences.w_break       * break_score
        + preferences.w_preference * preference_score
        + preferences.w_balance    * balance_score,
        4,
    )

    return {
        "total":            total,
        "break_time":       round(break_score, 4),
        "preference_match": round(preference_score, 4),
        "workload_balance": round(balance_score, 4),
    }


__all__ = [
    "calculate_break_time_score",
    "calculate_preference_match_score",
    "calculate_workload_balance_score",
    "calculate_total_score",
]
