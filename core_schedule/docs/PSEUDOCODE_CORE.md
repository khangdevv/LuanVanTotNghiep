# Tài liệu: Thuật Toán Lõi – Sinh Thời Khóa Biểu (`csp_generator.py`)

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Mô hình dữ liệu](#2-mô-hình-dữ-liệu)
3. [Chuyển đổi tiết học (`time_utils.py`)](#3-chuyển-đổi-tiết-học-time_utilspy)
4. [Tải dữ liệu (`data_loader.py`)](#4-tải-dữ-liệu-data_loaderpy)
5. [Phát hiện xung đột (`detect_conflicts.py`)](#5-phát-hiện-xung-đột-detect_conflictspy)
   - [5.1 `_overlaps`](#51-_overlaps)
   - [5.2 `detect_conflicts`](#52-detect_conflicts)
   - [5.3 `build_conflict_set`](#53-build_conflict_set)
6. [Thuật toán CSP (`csp_generator.py`)](#6-thuật-toán-csp-csp_generatorpy)
   - [6.1 `_conflicts_with_personal_events`](#61-_conflicts_with_personal_events)
   - [6.2 `_init_domains`](#62-_init_domains)
   - [6.3 `_choose_next_course` — MRV](#63-_choose_next_course--mrv)
   - [6.4 `_choose_next_section_of_course` — LCV](#64-_choose_next_section_of_course--lcv)
   - [6.5 `_forward_check` — Forward Checking](#65-_forward_check--forward-checking)
   - [6.6 `_restore_domains`](#66-_restore_domains)
   - [6.7 `_backtrack` — Thân đệ quy chính](#67-_backtrack--thân-đệ-quy-chính)
   - [6.8 `generate_schedules` — Entry point](#68-generate_schedules--entry-point)
7. [Luồng dữ liệu tổng thể](#7-luồng-dữ-liệu-tổng-thể)
8. [Ví dụ minh họa](#8-ví-dụ-minh-họa)
9. [Sai khác so với pseudocode gốc](#9-sai-khác-so-với-pseudocode-gốc)

---

## 1. Tổng quan

Pipeline thuật toán lõi thực hiện **3 bước nối tiếp** để đưa dữ liệu thô thành danh sách phương án thời khóa biểu hợp lệ:

```
JSON thô  ──▶  load_course_groups()   ──▶  CourseGroups
                                               │
                                               ▼
              build_conflict_set()    ──▶  ConflictSet
                                               │
                                               ▼
              generate_schedules()    ──▶  list[Schedule]
```

| Bước | Module | Đầu vào | Đầu ra |
|---|---|---|---|
| 1 – Tải dữ liệu | `data_loader.py` | File JSON + danh sách mã môn | `CourseGroups` |
| 2 – Xây conflict set | `detect_conflicts.py` | Tất cả `ClassSection` | `ConflictSet` (set hai chiều) |
| 3 – Sinh TKB | `csp_generator.py` | `CourseGroups`, `ConflictSet`, sở thích | `list[Schedule]` |

Bước 3 sử dụng thuật toán **CSP Backtracking với 3 chiến lược tối ưu**:

| Chiến lược | Hàm | Mục đích |
|---|---|---|
| **MRV** – Minimum Remaining Values | `_choose_next_course` | Chọn môn có ít lựa chọn nhất để xử lý trước |
| **LCV** – Least Constraining Value | `_choose_next_section_of_course` | Ưu tiên nhóm lớp gây ít ràng buộc cho các môn còn lại |
| **FC** – Forward Checking | `_forward_check` | Lan truyền ràng buộc, phát hiện dead-end sớm |

---

## 2. Mô hình dữ liệu

### Type aliases — các kiểu dữ liệu chính

```python
CourseGroups = dict[str, list[ClassSection]]
# Ánh xạ: course_id → danh sách tất cả nhóm lớp của môn đó
# Ví dụ: {"CS03042": [cls_LT01_t1, cls_LT01_t7, cls_LT02_t1, ...]}

Domains = dict[str, list[ClassSection]]
# Ánh xạ: course_id → nhóm lớp còn hợp lệ (sau khi lọc avoid_days & Forward Checking)
# Domains thu hẹp dần trong quá trình backtracking

ConflictSet = set[tuple[str, str]]
# Tập các cặp (class_id_A, class_id_B) xung đột nhau
# Lưu HAI CHIỀU: nếu (A,B) ∈ set thì (B,A) cũng ∈ set

Schedule = dict[str, ClassSection]
# Một phương án TKB hoàn chỉnh: course_id → nhóm lớp đã chọn
# Ví dụ: {"CS03042": cls_LT01_t1, "CS03002": cls_LT02_t7, ...}

Removed = dict[str, list[ClassSection]]
# Snapshot những gì bị xóa khỏi Domains bởi Forward Checking
# Dùng để restore khi backtrack
```

### `ClassSection` — nhóm lớp học

| Trường | Kiểu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| `class_id` | `str` | 1–20 ký tự | Định danh duy nhất. Ví dụ: `"CS03042_LT01_t1"` |
| `course_id` | `str` | 1–20 ký tự | Mã môn học |
| `semester_id` | `str` | — | Mã học kỳ. Ví dụ: `"HK2-2025"` |
| `day_of_week` | `int` | 2–8 | Thứ (2=Thứ Hai … 8=Chủ Nhật) |
| `start_time` | `time` | < `end_time` | Giờ bắt đầu |
| `end_time` | `time` | > `start_time` | Giờ kết thúc |
| `room` | `str?` | tùy chọn | Phòng học |
| `instructor` | `str?` | tùy chọn | Giảng viên |

### `PersonalEvent` — lịch bận cá nhân

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| `day_of_week` | `int?` | Thứ (None = sự kiện một lần không có thứ cố định) |
| `start_time` | `time` | Giờ bắt đầu |
| `end_time` | `time` | Giờ kết thúc |
| `is_recurring` | `bool` | `True` = lặp hàng tuần — CSP chỉ xét sự kiện này |

> **Quan trọng:** CSP chỉ lọc `PersonalEvent` khi **đồng thời** `is_recurring = True` và `day_of_week is not None`. Sự kiện một lần không ảnh hưởng đến việc sinh TKB.

---

## 3. Chuyển đổi tiết học (`time_utils.py`)

### `tiet_to_time(tiet_bat_dau, so_tiet) → (start_time, end_time)`

**Mục đích:** Chuyển cặp (tiết bắt đầu, số tiết) từ dữ liệu JSON của trường sang `(start_time, end_time)` dạng `datetime.time`.

**Bảng tiết học STU:**

| Tiết | Giờ bắt đầu | Tiết | Giờ bắt đầu |
|---|---|---|---|
| 1 | 07:00 | 9 | 14:15 |
| 2 | 07:50 | 10 | 15:10 |
| 3 | 08:40 | 11 | 16:00 |
| 4 | 09:35 | 12 | 16:50 |
| 5 | 10:25 | 13 | 17:45 |
| 6 | 11:15 | 14 | 18:35 |
| 7 | 12:35 | 15 | 19:25 |
| 8 | 13:25 | | |

**Công thức:**
```
start_time = _TIET_START[tiet_bat_dau]
end_time   = _TIET_START[tiet_bat_dau + so_tiet - 1] + 50 phút
```

Mỗi tiết dài 50 phút, `end_time` là giờ kết thúc của tiết cuối cùng trong nhóm.

**Ví dụ:**

| Tiết bắt đầu | Số tiết | start_time | end_time | Ca học |
|---|---|---|---|---|
| 1 | 3 | 07:00 | 09:30 | Ca 1 |
| 4 | 3 | 09:35 | 12:05 | Ca 2 |
| 7 | 3 | 12:35 | 15:05 | Ca 3 |
| 10 | 3 | 15:10 | 17:40 | Ca 4 |
| 1 | 6 | 07:00 | 12:05 | Ca 1–2 (6 tiết liên tục) |

> `tiet_to_time(7, 3)`: tiết cuối = tiết 9, bắt đầu 14:15, end = 14:15 + 50' = **15:05**.

---

## 4. Tải dữ liệu (`data_loader.py`)

### `load_course_groups(course_ids, json_path, semester_id) → CourseGroups`

**Mục đích:** Đọc file JSON chứa lịch mở lớp của trường, lọc theo danh sách môn cần xếp, tạo ra `CourseGroups` làm đầu vào cho CSP.

**Chữ ký:**
```python
def load_course_groups(
    course_ids: list[str],
    json_path: Path = DEFAULT_JSON_PATH,   # schedule_data_from_web.json
    semester_id: str = DEFAULT_SEMESTER_ID, # "HK2-2025"
) -> dict[str, list[ClassSection]]
```

**Cấu trúc một bản ghi JSON:**
```json
{
    "ma_mh": "CS03042",
    "nhom_to": "LT01",
    "lich_hoc": {
        "thu": 2,
        "tiet_bat_dau": 1,
        "so_tiet": 3,
        "phong": "A301",
        "giang_vien": "Thầy Minh",
        "thoi_gian": "01/02/2025 - 30/05/2025"
    }
}
```

**Thuật toán từng bước:**

```
Bước 1: Đọc toàn bộ JSON vào bộ nhớ
        raw = json.loads(json_path.read_text(encoding="utf-8"))

Bước 2: Khởi tạo dict kết quả với tất cả course_ids
        groups = {cid: [] for cid in course_ids}
        seen   = set()   ← tập dedup

Bước 3: Duyệt từng bản ghi trong raw
        - Bỏ qua nếu rec["ma_mh"] không trong course_ids
        - Bỏ qua nếu so_tiet <= 0 (không có tiết học)
        - Tạo key dedup = (course_id, nhom_to, tiet_bat_dau)
        - Bỏ qua nếu key đã thấy (trùng lặp)
        - Thêm key vào seen

Bước 4: Xây dựng ClassSection
        class_id = f"{course_id}_{nhom_to}_t{tiet_bat_dau}"
              →  "CS03042_LT01_t1"
        (start_time, end_time) = tiet_to_time(tiet_bat_dau, so_tiet)

Bước 5: Lọc kết quả cuối
        Chỉ giữ lại môn nào có ít nhất 1 nhóm lớp hợp lệ
```

**Logic dedup:** Khóa `(course_id, nhom_to, tiet_bat_dau)` loại bỏ bản ghi trùng lặp nhưng **giữ lại**:
- Cùng nhóm, khác tiết bắt đầu → 2 nhóm lớp độc lập (xếp lịch khác nhau)
- Cùng nhóm, cùng tiết, khác thứ → dedup, chỉ lấy dòng đầu tiên

**Ví dụ kết quả:**
```python
{
    "CS03042": [
        ClassSection(class_id="CS03042_LT01_t1",  day=2, start=07:00, end=09:30),
        ClassSection(class_id="CS03042_LT01_t7",  day=4, start=12:35, end=15:05),
        ClassSection(class_id="CS03042_LT02_t1",  day=3, start=07:00, end=09:30),
    ],
    "CS03002": [...],
}
```

---

## 5. Phát hiện xung đột (`detect_conflicts.py`)

### 5.1 `_overlaps`

**Chữ ký:**
```python
def _overlaps(a: ClassSection, b: ClassSection) -> bool
```

**Định nghĩa xung đột:** Hai nhóm lớp xung đột khi **đồng thời** thỏa:

```
a.day_of_week == b.day_of_week   ← cùng ngày trong tuần
AND  a.start_time < b.end_time   ← A bắt đầu trước khi B kết thúc
AND  b.start_time < a.end_time   ← B bắt đầu trước khi A kết thúc
```

**Điều kiện biên quan trọng:**

| Tình huống | Kết quả | Giải thích |
|---|---|---|
| A: 7:00–9:30 │ B: 9:35–12:05 | `False` | B.start(9:35) > A.end(9:30) → OK |
| A: 7:00–9:30 │ B: 9:30–12:05 | `False` | B.start(9:30) < A.end(9:30) = `False` → OK |
| A: 7:00–9:30 │ B: 9:00–12:05 | `True`  | B.start(9:00) < A.end(9:30) = `True` → xung đột |
| A: 7:00–12:05 │ B: 9:00–10:00 | `True` | B hoàn toàn nằm trong A → xung đột |

> Hai lớp **nối tiếp nhau** (lớp A kết thúc đúng lúc lớp B bắt đầu) **không** bị coi là xung đột.

---

### 5.2 `detect_conflicts`

**Chữ ký:**
```python
def detect_conflicts(classes: list[ClassSection]) -> list[tuple[ClassSection, ClassSection]]
```

**Mục đích:** Tìm tất cả cặp xung đột để **hiển thị cho người dùng** (UC-06). Kết quả là danh sách cặp `(A, B)` để UI có thể thông báo chi tiết.

**Thuật toán:** Duyệt tất cả cặp `(i, j)` với `j > i` — O(n²).

```
conflicts = []
FOR i FROM 0 TO n-2:
    FOR j FROM i+1 TO n-1:
        IF _overlaps(classes[i], classes[j]):
            conflicts.append((classes[i], classes[j]))
RETURN conflicts
```

> Với n ≤ 50 nhóm lớp thực tế → tối đa C(50,2) = 1.225 phép so sánh → < 1ms.

---

### 5.3 `build_conflict_set`

**Chữ ký:**
```python
def build_conflict_set(classes: list[ClassSection]) -> set[tuple[str, str]]
```

**Mục đích:** Tạo `ConflictSet` làm **đầu vào cho CSP**. Khác với `detect_conflicts` ở chỗ:
- Lưu theo `class_id` (chuỗi) thay vì object
- Lưu **hai chiều**: cả `(A_id, B_id)` và `(B_id, A_id)`

**Tại sao cần lưu hai chiều?**

MRV có thể xử lý môn A trước B hoặc B trước A. Khi kiểm tra trong `_backtrack`:

```python
if any((cls.class_id, chosen[c].class_id) in conflict_set for c in chosen):
```

Nếu môn A được gán trước và ta đang xét nhóm lớp của B, tra cứu dạng `(b_id, a_id)`. Nếu chỉ lưu một chiều `(a_id, b_id)` thì sẽ **bỏ sót xung đột** và sinh ra TKB không hợp lệ.

```python
conflict_set.add((a_id, b_id))
conflict_set.add((b_id, a_id))   # bắt buộc
```

**Ví dụ:**

```
Lớp CS01: Thứ 2, 07:00–09:30
Lớp CS02: Thứ 2, 08:00–10:00  ← xung đột với CS01

build_conflict_set([CS01, CS02, CS03]) → {
    ("CS01_id", "CS02_id"),
    ("CS02_id", "CS01_id"),   # hai chiều
}
```

---

## 6. Thuật toán CSP (`csp_generator.py`)

### 6.1 `_conflicts_with_personal_events`

**Chữ ký:**
```python
def _conflicts_with_personal_events(
    cls: ClassSection,
    personal_events: list[PersonalEvent]
) -> bool
```

**Mục đích:** Kiểm tra xem một nhóm lớp có trùng giờ với bất kỳ sự kiện bận cá nhân nào không.

**Điều kiện lọc sự kiện:** Chỉ xét sự kiện khi **cả hai** điều kiện thỏa:
1. `event.day_of_week is not None` — sự kiện có thứ cố định
2. `event.is_recurring == True` — lặp hàng tuần

**Điều kiện xung đột với lớp học:** Giống `_overlaps`:
```
cls.day_of_week == event.day_of_week
AND cls.start_time < event.end_time
AND event.start_time < cls.end_time
```

**Bảng trường hợp:**

| `is_recurring` | `day_of_week` | Kết quả |
|---|---|---|
| `False` | Bất kỳ | Bỏ qua — sự kiện một lần không ảnh hưởng TKB |
| `True` | `None` | Bỏ qua — không có thứ cố định |
| `True` | Có giá trị | **Kiểm tra xung đột thời gian** |

---

### 6.2 `_init_domains`

**Chữ ký:**
```python
def _init_domains(course_groups: CourseGroups, avoid_days: list[int]) -> Domains
```

**Mục đích:** Khởi tạo `Domains` bằng cách loại bỏ ngay các nhóm lớp rơi vào ngày sinh viên muốn tránh. Đây là **bước lọc sơ bộ** trước khi backtracking.

**Thuật toán:**
```
domains = {}
FOR course_id, sections IN course_groups:
    domains[course_id] = [
        cls FOR cls IN sections
        IF cls.day_of_week NOT IN avoid_days
    ]
RETURN domains
```

**Ví dụ:** `avoid_days = [7, 8]` (tránh Thứ 7 và Chủ Nhật):

```
Môn CS03042 có 4 nhóm lớp:
  LT01_t1: Thứ 2 → GIỮ LẠI
  LT01_t7: Thứ 4 → GIỮ LẠI
  LT02_t1: Thứ 3 → GIỮ LẠI
  LT03_t1: Thứ 7 → LOẠI (avoid_day)

Domains["CS03042"] = [LT01_t1, LT01_t7, LT02_t1]   ← 3 lựa chọn thay vì 4
```

> **Early exit trong `generate_schedules`:** Nếu bất kỳ môn nào có domain rỗng sau bước này → không thể có nghiệm → trả `[]` ngay lập tức.

---

### 6.3 `_choose_next_course` — MRV

**Chữ ký:**
```python
def _choose_next_course(unassigned: list[str], domains: Domains) -> str
```

**Mục đích:** Chọn môn tiếp theo để gán — **chiến lược MRV** (Minimum Remaining Values).

**Nguyên lý MRV:**
> Môn có ít nhóm lớp hợp lệ nhất là môn "khó xếp nhất". Xử lý nó **sớm** giúp phát hiện dead-end trước khi đi sâu vào nhánh đệ quy, giảm công tìm kiếm vô ích.

**Thuật toán:**
```
min_course = unassigned[0]
min_size   = len(domains[unassigned[0]])

FOR course IN unassigned[1:]:
    size = len(domains[course])
    IF size < min_size:
        min_size   = size
        min_course = course

RETURN min_course
```

**Ví dụ so sánh MRV vs không dùng MRV:**

```
Trạng thái hiện tại:
  Môn A: 3 lựa chọn còn lại
  Môn B: 1 lựa chọn còn lại  ← MRV chọn B trước
  Môn C: 4 lựa chọn còn lại

Không dùng MRV (chọn theo thứ tự A→B→C):
  Thử 3 lựa chọn của A × 1 lựa chọn của B × 4 của C = nhiều nhánh

Dùng MRV (chọn B trước):
  B chỉ có 1 lựa chọn. Nếu lựa chọn đó dẫn đến domain rỗng ở A hoặc C
  → phát hiện dead-end ngay, không cần thử 3 × 4 = 12 tổ hợp
```

---

### 6.4 `_choose_next_section_of_course` — LCV

**Chữ ký:**
```python
def _choose_next_section_of_course(
    course_id: str,
    domains: Domains,
    unassigned: list[str],
    conflict_set: ConflictSet,
) -> list[ClassSection]
```

**Mục đích:** Sắp xếp các nhóm lớp của môn đang xét theo thứ tự ưu tiên — **chiến lược LCV** (Least Constraining Value).

**Nguyên lý LCV:**
> Nhóm lớp gây ít xung đột nhất với các môn **chưa gán** nên được thử trước, vì nó để lại nhiều lựa chọn nhất cho các môn còn lại. Điều này giảm khả năng đi vào nhánh chết.

**Thuật toán:**
```
FOR cls IN domains[course_id]:
    conflict_count = 0
    FOR other_id IN unassigned (bỏ qua course_id hiện tại):
        FOR other_cls IN domains[other_id]:
            IF (cls.class_id, other_cls.class_id) IN conflict_set:
                conflict_count += 1

Sắp xếp danh sách theo conflict_count tăng dần
RETURN danh sách đã sắp xếp
```

**Ví dụ:**

```
Môn đang xét: CS03042, các nhóm còn lại: LT01_t1, LT01_t7, LT02_t1
Môn chưa gán: MATH101, CS03002

LT01_t1 (Thứ 2 07:00):
  ↔ MATH101: xung đột với LT01_T2 (Thứ 2 07:00) → +1
  ↔ CS03002: không xung đột → +0
  conflict_count = 1

LT01_t7 (Thứ 4 12:35):
  ↔ MATH101: không xung đột → +0
  ↔ CS03002: không xung đột → +0
  conflict_count = 0    ← ÍT RÀNG BUỘC NHẤT

LT02_t1 (Thứ 3 07:00):
  ↔ MATH101: xung đột với MATH_LT01 (Thứ 3) → +1
  ↔ CS03002: xung đột với CS03002_LT01 (Thứ 3) → +1
  conflict_count = 2

Thứ tự LCV: [LT01_t7, LT01_t1, LT02_t1]
```

---

### 6.5 `_forward_check` — Forward Checking

**Chữ ký:**
```python
def _forward_check(
    cls: ClassSection,
    unassigned: list[str],
    domains: Domains,
    conflict_set: ConflictSet,
) -> tuple[bool, Removed]
```

**Mục đích:** Sau khi gán một nhóm lớp `cls` cho môn hiện tại, loại ngay các nhóm lớp **xung đột với `cls`** khỏi domain của các môn chưa gán. Nếu domain nào về 0 → báo dead-end ngay.

**Tại sao dùng `Removed` thay vì `deep_copy`?**

- `deep_copy(domains)` tạo ra bản sao đầy đủ của tất cả domain mỗi lần gán — tốn O(n×m) bộ nhớ và thời gian.
- `Removed` chỉ ghi lại **những gì bị xóa** → restore chính xác với chi phí tối thiểu.

**Thuật toán:**
```
removed = {}

FOR other_id IN unassigned:
    removed[other_id] = []

    FOR g IN list(domains[other_id]):    ← duyệt bản sao để có thể xóa trong loop
        IF (cls.class_id, g.class_id) IN conflict_set:
            domains[other_id].remove(g)
            removed[other_id].append(g)  ← ghi lại để restore sau

    IF len(domains[other_id]) == 0:
        RETURN (False, removed)          ← dead-end: báo ngay, không tiếp tục

RETURN (True, removed)
```

**Minh họa:**

```
Sau khi gán: CS03042 → LT01_t1 (Thứ 2, 07:00–09:30)

Forward Check với môn MATH101:
  MATH_LT01 (Thứ 2, 07:00–11:30) ← XUNG ĐỘT → xóa khỏi domains["MATH101"]
  MATH_LT02 (Thứ 4, 07:00–11:30) ← OK → giữ lại
  MATH_LT03 (Thứ 3, 07:00–11:30) ← OK → giữ lại

  removed["MATH101"] = [MATH_LT01]
  domains["MATH101"] = [MATH_LT02, MATH_LT03]  ← vẫn còn ≥ 1 → tiếp tục

Forward Check với môn CS03002:
  ... (tương tự)

Nếu domains["MATH101"] về rỗng → RETURN (False, removed)  ← cắt nhánh ngay
```

---

### 6.6 `_restore_domains`

**Chữ ký:**
```python
def _restore_domains(removed: Removed, domains: Domains) -> None
```

**Mục đích:** Hoàn tác Forward Checking — đưa các nhóm lớp đã xóa trở lại domain của từng môn. Được gọi **sau mỗi lần backtrack**.

**Thuật toán:**
```
FOR course_id, classes IN removed:
    domains[course_id].extend(classes)
```

> Thứ tự extend không quan trọng vì CSP không phụ thuộc thứ tự trong domain — chỉ cần tất cả nhóm lớp có mặt trở lại.

---

### 6.7 `_backtrack` — Thân đệ quy chính

**Chữ ký:**
```python
def _backtrack(
    chosen: Schedule,
    unassigned: list[str],
    domains: Domains,
    conflict_set: ConflictSet,
    personal_events: list[PersonalEvent],
    valid_schedules: list[Schedule],
    max_solutions: int,
) -> None
```

**Mục đích:** Lõi đệ quy của CSP. Mỗi lần gọi xử lý một môn, thử từng nhóm lớp hợp lệ và đệ quy sâu hơn.

**Luồng xử lý chi tiết:**

```
Bước 1: Điều kiện dừng sớm
        IF len(valid_schedules) >= max_solutions: RETURN

Bước 2: Điều kiện thành công
        IF unassigned rỗng:
            valid_schedules.append(copy(chosen))
            RETURN

Bước 3: MRV — chọn môn tiếp theo
        course_id     = _choose_next_course(unassigned, domains)
        next_unassigned = unassigned − {course_id}

Bước 4: LCV — sắp xếp nhóm lớp theo ít ràng buộc nhất
        lcv_classes = _choose_next_section_of_course(
                          course_id, domains, next_unassigned, conflict_set)

Bước 5: Thử từng nhóm lớp (theo thứ tự LCV)
        FOR cls IN lcv_classes:

          5a. Lọc PersonalEvents
              IF _conflicts_with_personal_events(cls, personal_events): CONTINUE

          5b. Kiểm tra với các môn ĐÃ GÁN (tra conflict_set)
              IF bất kỳ (cls.class_id, chosen[c].class_id) IN conflict_set: CONTINUE

          5c. Gán thử
              chosen[course_id] = cls

          5d. Forward Checking — lan truyền ràng buộc
              (ok, removed) = _forward_check(cls, next_unassigned, domains, conflict_set)

          5e. Đệ quy nếu không dead-end
              IF ok:
                  _backtrack(chosen, next_unassigned, domains, ...)

          5f. Restore domain và thử nhóm lớp tiếp theo (BACKTRACK)
              _restore_domains(removed, domains)
              del chosen[course_id]

          5g. Kiểm tra lại max_solutions
              IF len(valid_schedules) >= max_solutions: RETURN
```

**Sơ đồ quyết định trong một bước đệ quy:**

```
                    [Chọn môn via MRV]
                           │
              [Sắp xếp nhóm lớp via LCV]
                           │
                    FOR cls IN lcv_classes:
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
        Xung đột PersonalEvent?  Xung đột chosen?
               │YES                    │YES
               ▼                       ▼
            SKIP                    SKIP
               │NO                     │NO
               └───────────┬───────────┘
                           ▼
                    chosen[course] = cls
                           │
                    [Forward Check]
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
            ok=True               ok=False (dead-end)
               │                       │
               ▼                       ▼
           [đệ quy sâu hơn]      restore & SKIP
               │
               ▼
      restore_domains + del chosen[course]
```

---

### 6.8 `generate_schedules` — Entry point

**Chữ ký:**
```python
def generate_schedules(
    course_groups: CourseGroups,
    conflict_set: ConflictSet,
    avoid_days: list[int],
    personal_events: list[PersonalEvent],
    max_solutions: int = 200,
) -> list[Schedule]
```

**Mục đích:** Điểm khởi đầu duy nhất của toàn bộ CSP engine. Thực hiện kiểm tra đầu vào, khởi tạo, và gọi `_backtrack`.

**Thuật toán:**
```
Bước 1: Kiểm tra đầu vào
        IF course_groups rỗng: RETURN []

Bước 2: Khởi tạo domains (lọc avoid_days)
        domains = _init_domains(course_groups, avoid_days)

Bước 3: Early exit — phát hiện domain rỗng trước khi bắt đầu
        IF bất kỳ domains[c] rỗng: RETURN []

Bước 4: Khởi chạy backtracking
        valid_schedules = []
        _backtrack(
            chosen          = {},
            unassigned      = list(course_groups.keys()),
            domains         = domains,
            conflict_set    = conflict_set,
            personal_events = personal_events,
            valid_schedules = valid_schedules,
            max_solutions   = max_solutions,
        )

Bước 5: Trả kết quả
        RETURN valid_schedules
```

**Tham số `max_solutions`:**

| Ngữ cảnh | Giá trị | Lý do |
|---|---|---|
| API (production) | `200` (mặc định) | Đủ để chọn top 3, tiết kiệm tài nguyên |
| Demo CLI | `200.000` | Khám phá không gian tìm kiếm đầy đủ |
| Unit test | `50–100` | Kiểm tra nhanh |

> CSP dừng ngay khi `len(valid_schedules) >= max_solutions` — không duyệt hết không gian tìm kiếm nếu không cần thiết.

---

## 7. Luồng dữ liệu tổng thể

```
┌────────────────────────────────────────────────────┐
│  ĐẦU VÀO                                           │
│  course_ids:      list[str]                        │
│  avoid_days:      list[int]                        │
│  personal_events: list[PersonalEvent]              │
│  preferences:     Preference                       │
└──────────────────────┬─────────────────────────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │   load_course_groups() │
          │   (data_loader.py)     │
          │                        │
          │   JSON → dedup →       │
          │   tiet_to_time()   →   │
          │   ClassSection objects │
          └────────────┬───────────┘
                       │
                       ▼  CourseGroups
          ┌────────────────────────┐
          │  build_conflict_set()  │
          │  (detect_conflicts.py) │
          │                        │
          │  O(n²) duyệt tất cả   │
          │  cặp, lưu 2 chiều      │
          └────────────┬───────────┘
                       │
                       ▼  ConflictSet
          ┌────────────────────────┐
          │  generate_schedules()  │
          │  (csp_generator.py)    │
          │                        │
          │  ┌──────────────────┐  │
          │  │ _init_domains    │  │
          │  │ (lọc avoid_days) │  │
          │  └────────┬─────────┘  │
          │           │ Domains    │
          │           ▼            │
          │  ┌──────────────────┐  │
          │  │  _backtrack()    │  │
          │  │                  │  │
          │  │ MRV → chọn môn   │  │
          │  │ LCV → sắp nhóm   │  │
          │  │ FC  → lan truyền │  │
          │  │ restore → undo   │  │
          │  └────────┬─────────┘  │
          │           │            │
          └───────────┼────────────┘
                       │
                       ▼  list[Schedule]
          ┌────────────────────────┐
          │  calculate_total_score │
          │  (scoring_function.py) │
          │                        │
          │  F_break + F_pref +    │
          │  F_balance → tổng hợp │
          └────────────┬───────────┘
                       │
                       ▼  list[ScoredSchedule]
          ┌────────────────────────┐
          │  Sort giảm dần theo    │
          │  score_total           │
          │  → Trả về top K        │
          └────────────────────────┘
```

---

## 8. Ví dụ minh họa

### Dữ liệu đầu vào

```python
# 2 môn, mỗi môn 2 nhóm lớp
course_groups = {
    "MON_A": [
        ClassSection(class_id="A_G1", day_of_week=2, start_time=time(7,0),  end_time=time(9,30)),
        ClassSection(class_id="A_G2", day_of_week=4, start_time=time(7,0),  end_time=time(9,30)),
    ],
    "MON_B": [
        ClassSection(class_id="B_G1", day_of_week=2, start_time=time(7,0),  end_time=time(9,30)),  # trùng A_G1
        ClassSection(class_id="B_G2", day_of_week=3, start_time=time(12,35),end_time=time(15,5)),
    ],
}

conflict_set  = {"A_G1","B_G1"}, {"B_G1","A_G1"}  # A_G1 và B_G1 cùng Thứ 2, 07:00–09:30
avoid_days    = []
personal_events = []
```

### Bước 1 — `_init_domains`

```
avoid_days = [] → không loại bỏ gì
domains = {
    "MON_A": [A_G1, A_G2],
    "MON_B": [B_G1, B_G2],
}
```

### Bước 2 — `_choose_next_course` (MRV)

```
domains["MON_A"] = 2 lựa chọn
domains["MON_B"] = 2 lựa chọn
→ Hòa — chọn phần tử đầu danh sách: "MON_A"
```

### Bước 3 — `_choose_next_section_of_course` (LCV)

```
course_id = "MON_A", next_unassigned = ["MON_B"]

Xét A_G1: (A_G1, B_G1) ∈ conflict_set → conflict_count = 1
Xét A_G2: (A_G2, B_G1) ∉ set; (A_G2, B_G2) ∉ set → conflict_count = 0

Thứ tự LCV: [A_G2, A_G1]   ← A_G2 ít ràng buộc hơn, thử trước
```

### Bước 4 — Thử `A_G2` (LCV ưu tiên)

```
chosen = {"MON_A": A_G2}

Forward Check với "MON_B":
  (A_G2, B_G1) ∉ conflict_set → giữ B_G1
  (A_G2, B_G2) ∉ conflict_set → giữ B_G2
  removed["MON_B"] = []
  domains["MON_B"] = [B_G1, B_G2]   ← ok = True

→ Đệ quy sâu hơn với unassigned = ["MON_B"]
```

### Bước 5 — Gán `MON_B`

```
unassigned = ["MON_B"]
MRV → "MON_B"
LCV → thử B_G1 trước (conflict_count = 0, vì unassigned đã rỗng)

Kiểm tra chosen:
  (B_G1, A_G2) ∉ conflict_set → OK

chosen = {"MON_A": A_G2, "MON_B": B_G1}
→ unassigned rỗng → NGHIỆM 1: {MON_A: A_G2, MON_B: B_G1}
```

### Bước 6 — Tiếp tục tìm nghiệm 2

```
Backtrack về MON_B, thử B_G2:
  (B_G2, A_G2) ∉ conflict_set → OK
  NGHIỆM 2: {MON_A: A_G2, MON_B: B_G2}
```

### Bước 7 — Backtrack về MON_A, thử `A_G1`

```
chosen = {"MON_A": A_G1}

Forward Check với "MON_B":
  (A_G1, B_G1) ∈ conflict_set → xóa B_G1
  (A_G1, B_G2) ∉ conflict_set → giữ B_G2
  removed["MON_B"] = [B_G1]
  domains["MON_B"] = [B_G2]   ← vẫn ≥ 1 → ok = True

→ Đệ quy với domains["MON_B"] = [B_G2]
  Thử B_G2: (B_G2, A_G1) ∉ conflict_set → OK
  NGHIỆM 3: {MON_A: A_G1, MON_B: B_G2}

→ Restore: domains["MON_B"] = [B_G1, B_G2]  (đưa B_G1 về)
```

### Kết quả cuối

```python
valid_schedules = [
    {"MON_A": A_G2, "MON_B": B_G1},  # Nghiệm 1
    {"MON_A": A_G2, "MON_B": B_G2},  # Nghiệm 2
    {"MON_A": A_G1, "MON_B": B_G2},  # Nghiệm 3
    # Tổ hợp {A_G1, B_G1} bị loại vì A_G1 và B_G1 cùng Thứ 2, 07:00–09:30
]
```

---

## 9. Sai khác so với pseudocode gốc

> **Mục đích:** Ghi lại những điểm implementation hiện tại **khác** với pseudocode gốc (`PSEUDOCODE_CORE.md` phiên bản cũ) để tránh nhầm lẫn khi đọc code.

---

### 9.1 Ràng buộc tín chỉ và `student_type`

#### Pseudocode gốc

```text
FUNCTION credit_bounds(student_type):
    IF student_type == "normal": RETURN (14, +INF)
    IF student_type == "weak":   RETURN (10, 18)
    IF student_type == "summer": RETURN (0, 12)

FUNCTION prune_credit(assigned, domains, courses, credit_min, credit_max):
    ...
```

Pseudocode gốc có cả hệ thống ràng buộc tín chỉ theo `student_type` và hàm `prune_credit`.

#### Implementation hiện tại

Không có ràng buộc tín chỉ. CSP chỉ ràng buộc: (1) không xung đột thời gian, (2) không trùng `avoid_days`, (3) không trùng `PersonalEvent`.

#### Lý do

Đề tài xác định lại phạm vi: sinh viên **đã đăng ký môn** (lưu trong bảng Enrollments), CSP chỉ xếp nhóm lớp cho các môn đó. Không cần tối ưu số tín chỉ vì đó là quyết định của sinh viên trước khi dùng hệ thống.

---

### 9.2 Cấu trúc `conflict_map` vs `conflict_set`

#### Pseudocode gốc

```text
conflicts = set()
conflicts.add((i, j, k, l))   ← dùng index (course_idx, section_idx)

IF (var_i, sec_j, v, s) NOT IN conflict_map: ...
```

Pseudocode gốc dùng tuple 4 phần tử `(course_i, sec_j, course_k, sec_l)` — tra cứu theo chỉ số.

#### Implementation hiện tại

```python
conflict_set: set[tuple[str, str]]   # chỉ lưu (class_id_A, class_id_B)

if (cls.class_id, other_cls.class_id) in conflict_set: ...
```

Dùng `class_id` (chuỗi) thay vì chỉ số nguyên — tra cứu trực tiếp, không cần ánh xạ index.

#### Lý do

`class_id` là định danh bền vững (persist qua serialization), dễ debug, và cho phép tra cứu O(1) trong Python `set`. Tuple 4 phần tử tạo ra phụ thuộc vào thứ tự danh sách — dễ lỗi khi có dedup hay sắp xếp lại.

---

### 9.3 Forward Checking: `deep_copy` vs `Removed`

#### Pseudocode gốc

```text
FUNCTION forward_check(var_i, sec_j, domains, unassigned, conflict_map):
    next_domains = deep_copy(domains)   ← tạo bản sao đầy đủ
    ...
    RETURN (TRUE, next_domains)
```

#### Implementation hiện tại

```python
removed: Removed = {}   # chỉ ghi lại những gì bị xóa

for g in list(domains[other_id]):
    if ...: domains[other_id].remove(g); removed[other_id].append(g)

# Restore bằng:
domains[course_id].extend(removed[course_id])
```

#### Bảng so sánh

| Khía cạnh | Pseudocode gốc | Implementation |
|---|---|---|
| Cơ chế | `deep_copy` toàn bộ domains | Ghi `Removed` — chỉ những gì bị xóa |
| Bộ nhớ | O(n×m) mỗi lần gán | O(số phần tử bị xóa) |
| Tốc độ restore | Thay thế toàn bộ pointer | `extend()` thêm lại phần tử |
| Correctness | Đúng | Đúng (không ảnh hưởng phần tử khác) |

#### Lý do

`deep_copy` với 8 môn × 5 nhóm tạo ra ~40 object mỗi lần gán, nhân với chiều sâu đệ quy → tốn bộ nhớ đáng kể. `Removed` chỉ ghi lại vài phần tử bị loại, tiết kiệm hơn nhiều.

---

### 9.4 LCV — thêm mới, không có trong pseudocode gốc

#### Pseudocode gốc

Không có LCV. Các nhóm lớp được thử theo thứ tự domain (không có ưu tiên).

#### Implementation hiện tại

`_choose_next_section_of_course` đếm số xung đột với các môn chưa gán và sắp xếp nhóm lớp theo thứ tự tăng dần của `conflict_count`.

#### Lý do thêm LCV

Khi có nhiều nghiệm, LCV giúp tìm các nghiệm "tốt hơn" (ít bị loại bỏ sau này) sớm hơn, đặc biệt hữu ích khi `max_solutions` nhỏ và ta chỉ cần top 3.

---

### 9.5 Tóm tắt sai khác

| # | Tính năng | Pseudocode gốc | Implementation | Mức độ ảnh hưởng |
|---|---|---|---|---|
| 1 | Ràng buộc tín chỉ | Có (`credit_bounds`, `prune_credit`) | Không có | **Cao** — loại bỏ hoàn toàn |
| 2 | Khóa conflict | `(i, j, k, l)` — index nguyên | `(class_id_A, class_id_B)` — chuỗi | **Cao** — thay đổi cấu trúc |
| 3 | Forward Checking | `deep_copy` | `Removed` + `extend` | **Trung bình** — semantics giống, hiệu quả hơn |
| 4 | LCV | Không có | Có (`_choose_next_section_of_course`) | **Trung bình** — tăng tốc tìm kiếm |
| 5 | Công thức Score | SRS v1.0 (cũ) | Cập nhật (xem `SCORING_FUNCTIONS.md`) | **Cao** — xem tài liệu riêng |