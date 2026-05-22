from __future__ import annotations

import json
from pathlib import Path

from demo.time_utils import tiet_to_time
from models import ClassSection

DEFAULT_JSON_PATH = Path(__file__).parent / "data" / "schedule_data_from_web.json"
DEFAULT_SEMESTER_ID = "HK2-2025"


def load_course_groups(
    course_ids: list[str],  
    json_path: Path = DEFAULT_JSON_PATH, 
    semester_id: str = DEFAULT_SEMESTER_ID,  
) -> dict[str, list[ClassSection]]:
    raw: list[dict] = json.loads(json_path.read_text(encoding="utf-8"))
    # duyệt theo (môn, nhóm, tiết bắt đầu) — giữ mỗi khung giờ duy nhất 1 lần.
    # Cùng nhóm khác tiết (giai đoạn xen kẽ) → 2 lựa chọn độc lập trong CSP.
    # Cùng nhóm khác thứ nhưng cùng tiết (dữ liệu bất thường) → lấy dòng đầu.
    seen: set[tuple[str, str, int]] = set()
    groups: dict[str, list[ClassSection]] = {cid: [] for cid in course_ids}

    for rec in raw:
        cid = rec["ma_mh"]
        if cid not in groups:
            continue

        nhom = rec["nhom_to"]
        lich  = rec["lich_hoc"]
        if lich["so_tiet"] <= 0:
            continue

        thu        = lich["thu"]
        tiet_start = lich["tiet_bat_dau"]
        key = (cid, nhom, tiet_start)
        if key in seen:
            continue
        seen.add(key)

        start, end = tiet_to_time(tiet_start, lich["so_tiet"])

        groups[cid].append(
            ClassSection(
                class_id=f"{cid}_{nhom}_t{tiet_start}",
                course_id=cid,
                semester_id=semester_id,
                day_of_week=int(thu),
                start_time=start,
                end_time=end,
                room=lich.get("phong"),
                instructor=lich.get("giang_vien"),
                max_students=1,  # TODO: nhận từ BE khi tích hợp API
            )
        )

    return {cid: secs for cid, secs in groups.items() if secs}  
