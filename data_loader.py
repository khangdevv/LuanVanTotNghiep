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
    raw: list[dict] = json.loads(json_path.read_text(encoding="utf-8"))  # Đọc và parse JSON.
    seen: set[tuple[str, str]] = set()  # Lưu các cặp môn-nhóm đã xử lý.
    groups: dict[str, list[ClassSection]] = {cid: [] for cid in course_ids} 

    for rec in raw:  
        cid = rec["ma_mh"]  
        if cid not in groups:  
            continue

        nhom = rec["nhom_to"]  
        if (cid, nhom) in seen: 
            continue
        seen.add((cid, nhom)) 

        lich = rec["lich_hoc"]  
        if lich["so_tiet"] <= 0: 
            continue

        start, end = tiet_to_time(lich["tiet_bat_dau"], lich["so_tiet"])  # Đổi tiết sang giờ.

        groups[cid].append( 
            ClassSection(
                class_id=f"{cid}_{nhom}", 
                course_id=cid,  
                semester_id=semester_id,  
                day_of_week=int(lich["thu"]),  
                start_time=start, 
                end_time=end, 
                room=lich.get("phong"),  
                instructor=lich.get("giang_vien"),  
                max_students=1, # chỗ này nên lưu ý để nhận realtime giá trị thật 
            )
        )

    return {cid: secs for cid, secs in groups.items() if secs}  
