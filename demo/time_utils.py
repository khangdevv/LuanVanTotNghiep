from __future__ import annotations

from datetime import time, timedelta

_TIET_START: dict[int, time] = {
    1:  time(7,  0),
    2:  time(7,  50),
    3:  time(8,  40),
    4:  time(9,  35),
    5:  time(10, 25),
    6:  time(11, 15),
    7:  time(12, 35),
    8:  time(13, 25),
    9:  time(14, 15),
    10: time(15, 10),
    11: time(16,  0),
    12: time(16, 50),
}


def tiet_to_time(tiet_bat_dau: int, so_tiet: int) -> tuple[time, time]:
    """Chuyển (tiết bắt đầu, số tiết) → (start_time, end_time).

    end_time = giờ bắt đầu tiết cuối + 50 phút, bao gồm khoảng nghỉ giải lao.

    Ví dụ:
        tiet_to_time(1, 3)  → 07:00 – 09:30  (Ca 1)
        tiet_to_time(4, 3)  → 09:35 – 12:05  (Ca 2)
        tiet_to_time(7, 3)  → 12:35 – 15:05  (Ca 3)
        tiet_to_time(10, 3) → 15:10 – 17:40  (Ca 4)
    """
    start = _TIET_START[tiet_bat_dau]
    last_start = _TIET_START[tiet_bat_dau + so_tiet - 1]
    end_delta = (
        timedelta(hours=last_start.hour, minutes=last_start.minute)
        + timedelta(minutes=50)
    )
    end = time(end_delta.seconds // 3600, (end_delta.seconds % 3600) // 60)
    return start, end
