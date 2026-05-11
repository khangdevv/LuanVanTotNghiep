# Tài liệu: Hàm Chấm Điểm Thời Khóa Biểu (`scoring_function.py`)

## Mục lục

1. [Tổng quan](#1-tổng-quan)
2. [Mô hình dữ liệu đầu vào](#2-mô-hình-dữ-liệu-đầu-vào)
3. [Hằng số & Mapping](#3-hằng-số--mapping)
4. [Hàm tiện ích nội bộ](#4-hàm-tiện-ích-nội-bộ)
5. [Hàm điểm thành phần](#5-hàm-điểm-thành-phần)
   - [5.1 calculate_break_time_score](#51-calculate_break_time_score)
   - [5.2 calculate_preference_match_score](#52-calculate_preference_match_score)
   - [5.3 calculate_workload_balance_score](#53-calculate_workload_balance_score)
6. [Hàm tổng hợp](#6-hàm-tổng-hợp-calculate_total_score)
7. [Luồng dữ liệu tổng thể](#7-luồng-dữ-liệu-tổng-thể)
8. [Ví dụ minh họa](#8-ví-dụ-minh-họa)

---

## 1. Tổng quan

Module `scoring_function.py` cung cấp bộ hàm chấm điểm cho một thời khóa biểu (TKB) đã xếp. Mỗi TKB được đánh giá trên **3 tiêu chí độc lập**, sau đó kết hợp thành **điểm tổng có trọng số**.

| Tiêu chí | Hàm | Ý nghĩa |
|---|---|---|
| Khoảng nghỉ | `calculate_break_time_score` | Nghỉ giữa các tiết có hợp lý không? |
| Sở thích | `calculate_preference_match_score` | TKB có khớp với ca học / ngày muốn tránh? |
| Cân bằng | `calculate_workload_balance_score` | Số tiết phân bổ đều các ngày không? |

Tất cả điểm thành phần đều nằm trong **[0.0, 1.0]**, điểm tổng cũng trong **[0.0, 1.0]**.

---

## 2. Mô hình dữ liệu đầu vào

### `ClassSection` — một tiết học

| Trường | Kiểu | Ràng buộc | Ý nghĩa |
|---|---|---|---|
| `class_id` | `str` | 1–20 ký tự | Mã lớp học phần |
| `course_id` | `str` | 1–20 ký tự | Mã môn học |
| `day_of_week` | `int` | 2–8 | Thứ trong tuần (2=T2 … 8=CN) |
| `start_time` | `time` | < `end_time` | Giờ bắt đầu |
| `end_time` | `time` | > `start_time` | Giờ kết thúc |
| `room` | `str?` | tuỳ chọn | Phòng học |
| `instructor` | `str?` | tuỳ chọn | Giảng viên |

### `Preference` — sở thích sinh viên

| Trường | Kiểu | Mặc định | Ý nghĩa |
|---|---|---|---|
| `student_id` | `str` | bắt buộc | Mã sinh viên |
| `preferred_slot` | `PreferredSlot` | `MORNING` | Ca học ưa thích |
| `w_break` | `float` | `0.40` | Trọng số tiêu chí khoảng nghỉ |
| `w_preference` | `float` | `0.30` | Trọng số tiêu chí sở thích |
| `w_balance` | `float` | `0.30` | Trọng số tiêu chí cân bằng |

> **Ràng buộc:** `w_break + w_preference + w_balance = 1.0` (được validate tự động).

### `PreferredSlot` — enum ca học

| Giá trị | Nghĩa | Ca tương ứng |
|---|---|---|
| `MORNING` | Buổi sáng | Ca 1 (7:00) + Ca 2 (9:35) |
| `AFTERNOON` | Buổi chiều | Ca 3 (12:35) + Ca 4 (15:10) |
| `EVENING` | Buổi tối | Không ánh xạ ca nào |

---

## 3. Hằng số & Mapping

### Lịch ca học STU

```
Ca 1: 07:00 – 09:30  (420 phút từ 00:00)
Ca 2: 09:35 – 12:05  (575 phút từ 00:00)
Ca 3: 12:35 – 15:05  (755 phút từ 00:00)
Ca 4: 15:10 – ...    (910 phút từ 00:00)
```

```python
_CA_MINUTES = (420, 575, 755, 910)
```

### Khoảng nghỉ chuẩn STU

Đây là các khoảng nghỉ **được thiết kế sẵn** trong lịch của trường — khi gặp các khoảng này, hệ thống **luôn cho điểm 1.0** thay vì tính theo công thức phạt.

```python
_DESIGNED_GAPS = {(570, 575), (725, 755), (905, 910)}
```

| Cặp (end_phút, start_phút) | Giải thích | Thời gian nghỉ |
|---|---|---|
| `(570, 575)` | Ca1 kết thúc 9:30, Ca2 bắt đầu 9:35 | 5 phút |
| `(725, 755)` | Ca2 kết thúc 12:05, Ca3 bắt đầu 12:35 | 30 phút (nghỉ trưa) |
| `(905, 910)` | Ca3 kết thúc 15:05, Ca4 bắt đầu 15:10 | 5 phút |

---

## 4. Hàm tiện ích nội bộ

> Các hàm này có tiền tố `_` — chỉ dùng nội bộ trong module, không export ra ngoài.

### `_to_minutes(t) -> int`

Chuyển đối tượng `datetime.time` sang số nguyên phút tính từ 00:00.

```
time(7, 30)  →  7 × 60 + 30  =  450
time(12, 5)  →  12 × 60 + 5  =  725
```

### `_get_ca_num(t) -> int | None`

Xác định tiết học bắt đầu ở **ca số mấy** dựa trên giờ bắt đầu.

| Giờ bắt đầu | Ca trả về |
|---|---|
| đúng 07:00 (420 phút) | 1 |
| đúng 09:35 (575 phút) | 2 |
| đúng 12:35 (755 phút) | 3 |
| ≥ 15:10 (910 phút) | 4 |
| Khác | `None` |

> Ca 4 dùng `>=` vì giờ vào ca 4 có thể bắt đầu muộn hơn mốc chuẩn.

### `_clamp_01(value) -> float`

Giới hạn giá trị trong đoạn [0.0, 1.0].

```
-0.5  →  0.0
 0.7  →  0.7
 1.3  →  1.0
```

### `_gap_score(gap: int) -> float`

Ánh xạ **số phút nghỉ** giữa 2 tiết liền kề → điểm chất lượng (hàm bậc thang).

| Khoảng nghỉ | Điểm | Lý do |
|---|---|---|
| < 0 phút | 0.0 | Chồng lịch (lỗi dữ liệu) |
| 0–9 phút | 0.2 | Quá gấp, không kịp di chuyển |
| 10–90 phút | **1.0** | Lý tưởng |
| 91–180 phút | 0.7 | Chấp nhận được |
| 181–300 phút | 0.4 | Bỏ trống gần 1 ca |
| > 300 phút | 0.1 | Bỏ trống 2 ca trở lên |

```
Trực quan:
  0   10         90   91        180  181       300  301+
  |──|───────────|    |──────────|    |─────────|    |───
 0.2     1.0          0.7              0.4            0.1
```

---

## 5. Hàm điểm thành phần

### 5.1 `calculate_break_time_score`

**Chữ ký:**
```python
def calculate_break_time_score(schedule: list[ClassSection]) -> float
```

**Mục đích:** Đánh giá chất lượng khoảng nghỉ giữa các tiết trong từng ngày học.

**Thuật toán từng bước:**

```
Bước 1: Nhóm các tiết theo ngày trong tuần
        {2: [cls_A, cls_B], 4: [cls_C], 6: [cls_D, cls_E, cls_F]}

Bước 2: Với mỗi ngày, sắp xếp tiết theo giờ bắt đầu tăng dần

Bước 3: Tính gap giữa mỗi cặp tiết liền kề
        gap = start_time(tiết sau) − end_time(tiết trước)  [đơn vị: phút]

Bước 4: Chấm điểm từng gap
        - Nếu (end, start) ∈ _DESIGNED_GAPS → điểm 1.0 (khoảng nghỉ chuẩn STU)
        - Ngược lại → _gap_score(gap)

Bước 5: Trả về trung bình cộng tất cả điểm gap
        - Nếu không có gap nào (mỗi ngày ≤ 1 tiết) → trả 1.0
```

**Ví dụ:**

```
Thứ 2: Tiết A (7:00–9:30), Tiết B (9:35–12:05)
  end=570, start=575 → (570,575) ∈ _DESIGNED_GAPS → điểm 1.0

Thứ 4: Tiết C (7:00–9:30), Tiết D (14:00–16:30)
  gap = 840 − 570 = 270 phút → _gap_score(270) = 0.4

Điểm cuối = (1.0 + 0.4) / 2 = 0.7
```

---

### 5.2 `calculate_preference_match_score`

**Chữ ký:**
```python
def calculate_preference_match_score(
    schedule: list[ClassSection],
    preferences: Preference,
    avoid_days: list[int] = [],
) -> float
```

**Mục đích:** Đo mức độ khớp giữa TKB và sở thích của sinh viên về ca học và ngày tránh.

**Thuật toán từng bước:**

```
Bước 1: Xác định tập ca ưa thích
        MORNING   → {1, 2}
        AFTERNOON → {3, 4}
        EVENING   → {} (rỗng, không ca nào khớp)

Bước 2: Với mỗi tiết học:
        time_score = 1.0  nếu ca học của tiết ∈ tập ca ưa thích
                   = 0.0  nếu không

        day_score  = 0.0  nếu ngày học ∈ avoid_days
                   = 1.0  nếu không

        điểm tiết  = (time_score + day_score) / 2

Bước 3: Trả về trung bình điểm tất cả tiết
```

**Bảng điểm tiết:**

| Ca học khớp? | Ngày tránh? | Điểm tiết |
|---|---|---|
| ✅ | ❌ | **1.0** |
| ✅ | ✅ | 0.5 |
| ❌ | ❌ | 0.5 |
| ❌ | ✅ | **0.0** |

---

### 5.3 `calculate_workload_balance_score`

**Chữ ký:**
```python
def calculate_workload_balance_score(schedule: list[ClassSection]) -> float
```

**Mục đích:** Đánh giá mức độ phân bổ đều số tiết học theo các ngày trong tuần. Tránh tình trạng dồn quá nhiều tiết vào 1–2 ngày.

**Thuật toán từng bước:**

```
Bước 1: Đếm số tiết mỗi ngày
        {2: 3, 4: 1, 6: 2}  →  counts = [3, 1, 2]

Bước 2: Nếu chỉ học 1 ngày → trả 1.0 (không thể so sánh)

Bước 3: Tính phương sai
        avg      = mean(counts)
        variance = mean((c − avg)² for c in counts)

Bước 4: Chuẩn hóa
        score = 1.0 − variance / 9.0
        score = clamp(score, 0.0, 1.0)
```

**Ý nghĩa hằng số 9.0:**

Phương sai tối đa tham chiếu = 9.0 (tương đương lịch rất mất cân bằng, ví dụ 0 tiết vs 3 tiết/ngày). Dùng để chuẩn hóa về thang [0, 1].

| Trường hợp | Phương sai | Điểm |
|---|---|---|
| Đều hoàn toàn (3, 3, 3) | 0.0 | **1.0** |
| Lệch nhẹ (2, 3, 4) | 0.67 | 0.93 |
| Lệch vừa (1, 2, 4) | 1.56 | 0.83 |
| Lệch nhiều (0, 0, 6) | 8.0 | 0.11 |
| Lệch tối đa (≥ 9.0) | ≥ 9.0 | **0.0** |

---

## 6. Hàm tổng hợp: `calculate_total_score`

**Chữ ký:**
```python
def calculate_total_score(
    schedule: list[ClassSection],
    preferences: Preference,
    avoid_days: list[int] = [],
) -> dict[str, float]
```

**Công thức:**

```
total = w_break       × break_score
      + w_preference  × preference_score
      + w_balance     × balance_score
```

Với trọng số mặc định:

```
total = 0.40 × break_score
      + 0.30 × preference_score
      + 0.30 × balance_score
```

**Bảng trọng số:**

| Thành phần | Trọng số mặc định | Lý do |
|---|---|---|
| Khoảng nghỉ (`w_break`) | **40%** | Ảnh hưởng trực tiếp đến sự thoải mái khi học |
| Sở thích (`w_preference`) | **30%** | Phản ánh mong muốn cá nhân sinh viên |
| Cân bằng (`w_balance`) | **30%** | Tránh quá tải một ngày trong tuần |

> Trọng số có thể tuỳ chỉnh qua `Preference`, miễn tổng bằng 1.0.

**Đầu ra:**

```python
{
    "total":            float,   # điểm tổng [0.0, 1.0]
    "break_time":       float,   # điểm khoảng nghỉ
    "preference_match": float,   # điểm sở thích
    "workload_balance": float,   # điểm cân bằng
}
```

Tất cả giá trị làm tròn **4 chữ số thập phân**.

---

## 7. Luồng dữ liệu tổng thể

```
┌─────────────────────────────────────┐
│  Đầu vào                            │
│  schedule:    list[ClassSection]    │
│  preferences: Preference            │
│  avoid_days:  list[int]             │
└──────────────────┬──────────────────┘
                   │
        ┌──────────┼───────────┐
        ▼          ▼           ▼
   ┌─────────┐ ┌──────────┐ ┌──────────┐
   │ Nhóm    │ │ Ca học   │ │ Đếm      │
   │ theo    │ │ ưa thích │ │ tiết     │
   │ ngày    │ │ avoid_set│ │ theo     │
   │ Sort    │ │          │ │ ngày     │
   │ theo    │ │          │ │          │
   │ giờ     │ │          │ │          │
   └────┬────┘ └────┬─────┘ └────┬─────┘
        │           │            │
        ▼           ▼            ▼
   ┌─────────┐ ┌──────────┐ ┌──────────┐
   │ Tính    │ │time_score│ │ Phương   │
   │ gap     │ │+day_score│ │ sai      │
   │ từng    │ │   / 2    │ │ / 9.0    │
   │ cặp     │ │          │ │          │
   └────┬────┘ └────┬─────┘ └────┬─────┘
        │           │            │
        ▼           ▼            ▼
   break_score  pref_score  balance_score
        │           │            │
        └─────────┬─┘────────────┘
                  │
                  ▼
      w_break × B + w_pref × P + w_bal × L
                  │
                  ▼
         ┌────────────────────┐
         │ {                  │
         │   "total":  ...,   │
         │   "break_time": ...,│
         │   "preference": ...,│
         │   "workload": ...  │
         │ }                  │
         └────────────────────┘
```

---

## 8. Ví dụ minh họa

### Dữ liệu mẫu

```python
from datetime import time
from models.classes import ClassSection
from models.preferences import Preference
from enums.preferred_slot import PreferredSlot
from scoring_function import calculate_total_score

schedule = [
    ClassSection(
        class_id="CS101-01", course_id="CS101", semester_id="20241",
        day_of_week=2,                 # Thứ Hai
        start_time=time(7, 0),         # Ca 1 → 420 phút
        end_time=time(9, 30),          #       → 570 phút
    ),
    ClassSection(
        class_id="CS101-01", course_id="CS101", semester_id="20241",
        day_of_week=2,                 # Thứ Hai
        start_time=time(9, 35),        # Ca 2 → 575 phút (khoảng nghỉ chuẩn STU)
        end_time=time(12, 5),
    ),
    ClassSection(
        class_id="MATH201-02", course_id="MATH201", semester_id="20241",
        day_of_week=4,                 # Thứ Tư
        start_time=time(12, 35),       # Ca 3 → 755 phút
        end_time=time(15, 5),
    ),
]

preferences = Preference(
    student_id="SV001",
    preferred_slot=PreferredSlot.MORNING,  # thích Ca 1 + Ca 2
    w_break=0.40,
    w_preference=0.30,
    w_balance=0.30,
)

result = calculate_total_score(schedule, preferences, avoid_days=[6])
```

### Tính tay từng bước

#### Break time score

| Ngày | Cặp tiết | end → start | Loại | Điểm |
|---|---|---|---|---|
| Thứ 2 | Ca1 → Ca2 | 570 → 575 | _DESIGNED_GAPS | **1.0** |
| Thứ 4 | (chỉ 1 tiết) | — | không có gap | — |

```
break_score = 1.0 / 1 = 1.0
```

#### Preference match score

| Tiết | Ca số | time_score | Ngày | day_score | Điểm tiết |
|---|---|---|---|---|---|
| CS101 Ca1 (7:00, T2) | 1 ∈ {1,2} | 1.0 | 2 ∉ {6} | 1.0 | **1.0** |
| CS101 Ca2 (9:35, T2) | 2 ∈ {1,2} | 1.0 | 2 ∉ {6} | 1.0 | **1.0** |
| MATH201 Ca3 (12:35, T4) | 3 ∉ {1,2} | 0.0 | 4 ∉ {6} | 1.0 | **0.5** |

```
preference_score = (1.0 + 1.0 + 0.5) / 3 = 0.8333
```

#### Workload balance score

```
counts = [2, 1]  (T2: 2 tiết, T4: 1 tiết)
avg      = (2 + 1) / 2 = 1.5
variance = ((2 - 1.5)² + (1 - 1.5)²) / 2 = (0.25 + 0.25) / 2 = 0.25
score    = 1.0 - 0.25 / 9.0 = 0.9722
```

#### Tổng hợp

```
total = 0.40 × 1.0000
      + 0.30 × 0.8333
      + 0.30 × 0.9722
      = 0.4000 + 0.2500 + 0.2917
      = 0.9417
```

**Kết quả trả về:**
```python
{
    "total":            0.9417,
    "break_time":       1.0,
    "preference_match": 0.8333,
    "workload_balance": 0.9722,
}
```
