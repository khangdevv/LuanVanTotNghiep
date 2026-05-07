# Danh sách môn học trong schedule_data_from_web.json

**Nguồn:** Trường Đại học Công nghệ Sài Gòn (STU)
**Tổng số môn:** 19
**Tổng số nhóm lớp:** 141

---

## Bảng chi tiết

| # | Mã môn | Tên môn | Số nhóm | Ghi chú |
|---|--------|---------|---------|---------|
| 1 | CS03001 | Kỹ thuật số | 6 | |
| 2 | CS03002 | Thí nghiệm Kỹ thuật số | 15 | |
| 3 | CS03042 | Triển khai hệ thống thông tin | 23 | Nhiều nhóm nhất |
| 4 | CS03043 | Xây dựng phần mềm Web | 7 | |
| 5 | CS03044 | Xây dựng phần mềm Windows | 3 | |
| 6 | CS03057 | AI cơ bản và ứng dụng | 8 | |
| 7 | CS03058 | Xây dựng phần mềm thiết bị di động | 11 | |
| 8 | CS03153 | Đồ án / Khóa luận tốt nghiệp | 1 | Chỉ 1 nhóm |
| 9 | CS09001 | Nhập môn lập trình | 6 | |
| 10 | CS09002 | Thực hành Nhập môn lập trình | 15 | |
| 11 | CS09151 | Thực tập tốt nghiệp | 1 | Chỉ 1 nhóm |
| 12 | GS19008 | Tiếng Anh 2 | 9 | |
| 13 | GS19010 | Tiếng Anh 4 | 1 | Chỉ 1 nhóm |
| 14 | GS33002 | Toán A2 (Hàm nhiều biến, giải tích vec tơ) | 6 | |
| 15 | GS43002 | Vật lý 2 | 6 | |
| 16 | GS49005 | Thí nghiệm Vật lý Phần 2 | 15 | |
| 17 | GS79005 | Triết học Mác - Lênin | 6 | |
| 18 | GS79006 | Kinh tế chính trị Mác - Lênin | 6 | |
| 19 | GS93005 | Giáo dục thể chất 1 | 6 | |

---

## Phân loại theo nhóm môn

### Chuyên ngành Công nghệ thông tin (CS)

| Mã môn | Tên môn | Số nhóm |
|--------|---------|---------|
| CS03001 | Kỹ thuật số | 6 |
| CS03002 | Thí nghiệm Kỹ thuật số | 15 |
| CS03042 | Triển khai hệ thống thông tin | 23 |
| CS03043 | Xây dựng phần mềm Web | 7 |
| CS03044 | Xây dựng phần mềm Windows | 3 |
| CS03057 | AI cơ bản và ứng dụng | 8 |
| CS03058 | Xây dựng phần mềm thiết bị di động | 11 |
| CS03153 | Đồ án / Khóa luận tốt nghiệp | 1 |
| CS09001 | Nhập môn lập trình | 6 |
| CS09002 | Thực hành Nhập môn lập trình | 15 |
| CS09151 | Thực tập tốt nghiệp | 1 |

### Đại cương (GS)

| Mã môn | Tên môn | Số nhóm |
|--------|---------|---------|
| GS19008 | Tiếng Anh 2 | 9 |
| GS19010 | Tiếng Anh 4 | 1 |
| GS33002 | Toán A2 (Hàm nhiều biến, giải tích vec tơ) | 6 |
| GS43002 | Vật lý 2 | 6 |
| GS49005 | Thí nghiệm Vật lý Phần 2 | 15 |
| GS79005 | Triết học Mác - Lênin | 6 |
| GS79006 | Kinh tế chính trị Mác - Lênin | 6 |
| GS93005 | Giáo dục thể chất 1 | 6 |

---

## Lưu ý khi dùng trong test

### Môn chỉ có 1 nhóm

Các môn dưới đây **không có lựa chọn thay thế**. MRV sẽ ưu tiên chọn
trước (domain = 1). Nếu nhóm duy nhất bị xung đột hoặc rơi vào avoid_days
→ không có nghiệm cho toàn bộ TKB.

| Mã môn | Tên môn |
|--------|---------|
| CS03153 | Đồ án / Khóa luận tốt nghiệp |
| CS09151 | Thực tập tốt nghiệp |
| GS19010 | Tiếng Anh 4 |

### Gợi ý bộ môn cho test

```python
# Bộ test nhẹ — ít nhóm, chạy nhanh
COURSE_IDS = ["CS03001", "GS33002", "GS43002", "GS79005"]

# Bộ test trung bình — đa dạng số nhóm
COURSE_IDS = ["CS03001", "CS03057", "CS03058", "GS19008", "GS33002"]

# Bộ test nặng — nhiều nhóm, kiểm tra hiệu năng
COURSE_IDS = ["CS03042", "CS03002", "CS09002", "GS49005", "GS19008",
              "CS03058", "GS79005"]
```
