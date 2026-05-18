"""
pytest tests/test_data_loader.py -v
"""
from conftest import COURSE_IDS


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
