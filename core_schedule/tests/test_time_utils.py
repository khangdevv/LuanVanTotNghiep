"""
pytest tests/test_time_utils.py -v
"""
from datetime import time

from demo.time_utils import tiet_to_time


class TestTietToTime:
    def test_tiet_1_6(self):
        """Tiết 1-6: 07:00 – 12:05"""
        start, end = tiet_to_time(1, 6)
        assert start == time(7, 0)
        assert end == time(12, 5)

    def test_tiet_7_12(self):
        """Tiết 7-12: 12:35 – 17:40"""
        start, end = tiet_to_time(7, 6)
        assert start == time(12, 35)
        assert end == time(17, 40)

    def test_tiet_7_3(self):
        """Tiết 7-9: 12:35 – 15:05"""
        start, end = tiet_to_time(7, 3)
        assert start == time(12, 35)
        assert end == time(15, 5)

    def test_tiet_10_3(self):
        """Tiết 10-12: 15:10 – 17:40"""
        start, end = tiet_to_time(10, 3)
        assert start == time(15, 10)
        assert end == time(17, 40)

    def test_tiet_single(self):
        """1 tiết: đúng 50 phút"""
        start, end = tiet_to_time(1, 1)
        assert start == time(7, 0)
        assert end == time(7, 50)

    def test_lunch_boundary(self):
        """
        Tiết 6 kết thúc 12:05, Tiết 7 bắt đầu 12:35.
        Hai lớp này không xung đột (strict <).
        """
        _, end_tiet6 = tiet_to_time(6, 1)
        start_tiet7, _ = tiet_to_time(7, 1)
        assert end_tiet6 < start_tiet7
