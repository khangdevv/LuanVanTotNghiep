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
9. [Sai khác so với SRS v1.0](#9-sai-khác-so-với-srs-v10)

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
| `min_break_minutes` | `int` | `15` | Số phút nghỉ tối thiểu mong muốn giữa 2 tiết |
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

### `_get_ca_num(t) -> int`

Xác định tiết học bắt đầu ở **ca số mấy** dựa trên khoảng giờ. Không yêu cầu đúng giờ bắt đầu ca chuẩn — lớp bắt đầu ở bất kỳ tiết nào trong ca đều được nhận diện đúng.

| Khoảng giờ bắt đầu | Ca trả về |
|---|---|
| trước 09:35 | 1 |
| 09:35 – 12:34 | 2 |
| 12:35 – 15:09 | 3 |
| 15:10 trở đi | 4 |

> Không bao giờ trả `None` — mọi giờ bắt đầu hợp lệ đều được ánh xạ về Ca 1–4.

### `_clamp_01(value) -> float`

Giới hạn giá trị trong đoạn [0.0, 1.0].

```
-0.5  →  0.0
 0.7  →  0.7
 1.3  →  1.0
```

### `_gap_score(gap: int, min_break: int) -> float`

Ánh xạ **số phút nghỉ** giữa 2 tiết liền kề → điểm chất lượng.

Phần dưới ngưỡng dùng `min_break` cá nhân làm chuẩn (tuyến tính). Phần trên ngưỡng dùng hằng số trường (cấu trúc ca học cố định).

| Khoảng nghỉ | Điểm | Lý do |
|---|---|---|
| < 0 phút | 0.0 | Chồng lịch (lỗi dữ liệu) |
| 0 – `min_break-1` phút | `gap / min_break` | Chưa đủ ngưỡng nghỉ — tuyến tính |
| `min_break` – 90 phút | **1.0** | Đủ nghỉ, vùng lý tưởng |
| 91 – 180 phút | 0.7 | Bỏ trống ~1 ca |
| 181 – 300 phút | 0.4 | Bỏ trống ~2 ca |
| > 300 phút | 0.1 | Quá dài, lãng phí thời gian |

> Ngưỡng 90 / 180 / 300 phút gắn với cấu trúc ca STU (1 ca ≈ 150 phút), không phụ thuộc `min_break`.

```
Với min_break = 15 (mặc định):

  0      15         90   91        180  181       300  301+
  |──────|───────────|    |──────────|    |─────────|    |───
  0→1.0      1.0          0.7              0.4            0.1
  (tuyến tính)
```

---

## 5. Hàm điểm thành phần

### 5.1 `calculate_break_time_score`

**Chữ ký:**
```python
def calculate_break_time_score(schedule: list[ClassSection], min_break: int = 15) -> float
```

**Mục đích:** Đánh giá chất lượng khoảng nghỉ giữa các tiết trong từng ngày học. Dùng `min_break` của sinh viên làm ngưỡng chuẩn để chấm điểm khoảng nghỉ ngắn.

**Thuật toán từng bước:**

```
Bước 1: Nhóm các tiết theo ngày trong tuần
        {2: [cls_A, cls_B], 4: [cls_C], 6: [cls_D, cls_E, cls_F]}

Bước 2: Với mỗi ngày, sắp xếp tiết theo giờ bắt đầu tăng dần

Bước 3: Tính gap giữa mỗi cặp tiết liền kề
        gap = start_time(tiết sau) − end_time(tiết trước)  [đơn vị: phút]

Bước 4: Chấm điểm từng gap
        - Nếu (end, start) ∈ _DESIGNED_GAPS → điểm 1.0 (giờ ra chơi STU thiết kế sẵn)
        - Ngược lại → _gap_score(gap, min_break)

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

Bước 2: Xử lý trường hợp chỉ có 1 ngày học
        - Đúng 1 lớp → không có gì để cân bằng → trả 1.0
        - Nhiều lớp cùng 1 ngày → phân bổ tệ nhất → trả 0.0

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
| 1 lớp duy nhất | — | **1.0** |
| 8 lớp cùng 1 ngày | — | **0.0** |
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

---

## 9. Sai khác so với SRS v1.0

> **Mục đích:** Ghi lại những điểm implementation hiện tại **khác** với đặc tả SRS v1.0 (Chương 6.2) để báo cáo điều chỉnh lên giảng viên hướng dẫn.

---

### 9.1 F_break — Chất lượng khoảng nghỉ

#### SRS v1.0 (mục 6.2.2)

```
f_break_d = mean( min(gap_i / (2 × min_break), 1.0)  for all gap_i in ngày d )
F_break(S) = mean( f_break_d  for all d có ≥ 2 buổi )
Nếu không ngày nào có ≥ 2 buổi → F_break = 1.0
```

- **Ngưỡng đạt 1.0:** `gap ≥ 2 × min_break` (với min_break=15 → cần ≥ 30 phút).
- **Không có phạt** cho khoảng nghỉ quá dài.
- **Không có** khái niệm "designed gaps" (giờ ra chơi STU).

#### Implementation hiện tại

```python
def _gap_score(gap, min_break):
    if gap < 0:         return 0.0
    if gap < min_break: return gap / min_break   # chia min_break, không phải 2×min_break
    if gap <= 90:       return 1.0               # vùng lý tưởng (cứng)
    if gap <= 180:      return 0.7               # bỏ trống ~1 ca — phạt
    if gap <= 300:      return 0.4               # bỏ trống ~2 ca — phạt
    return 0.1                                   # quá dài — phạt nặng

# Nếu (end_min, start_min) ∈ _DESIGNED_GAPS → điểm 1.0 (bỏ qua công thức trên)
```

#### Bảng so sánh

| Khía cạnh | SRS v1.0 | Implementation |
|---|---|---|
| Công thức gap score | `min(gap / (2×min_break), 1.0)` | Step function theo 4 vùng |
| Ngưỡng đạt điểm 1.0 | `gap ≥ 2 × min_break` | `min_break ≤ gap ≤ 90` |
| Phạt nghỉ quá dài | Không có | Có (0.7 / 0.4 / 0.1) |
| Giờ ra chơi STU | Không đề cập | `_DESIGNED_GAPS` → luôn 1.0 |

#### Lý do điều chỉnh

1. **Chia `min_break` thay vì `2×min_break`:** Công thức SRS yêu cầu gap gấp đôi ngưỡng mới đạt 1.0, dẫn đến tình huống lịch chuẩn STU (nghỉ 5 phút giữa Ca1→Ca2) bị phạt nặng dù đây là thiết kế của trường. Điều chỉnh về `min_break` để ngưỡng đạt điểm 1.0 bằng đúng mức sinh viên đặt ra.
2. **Phạt khoảng nghỉ quá dài:** SRS không phạt gap lớn, nhưng thực tế khoảng trống >3 tiết lãng phí thời gian di chuyển/chờ đợi. Step function bổ sung hành vi này.
3. **`_DESIGNED_GAPS`:** STU có 3 khoảng nghỉ cố định (5–30 phút) được nhà trường thiết kế sẵn. Đây không phải "nghỉ quá ngắn" mà là lịch chuẩn, cần cho điểm 1.0 trực tiếp thay vì áp công thức phạt.

---

### 9.2 F_pref — Độ khớp sở thích

#### SRS v1.0 (mục 6.2.3)

```
match_i = 1  nếu buổi học i thuộc khung giờ ưa thích VÀ không học vào ngày avoid
match_i = 0  ngược lại (thiếu một trong hai điều kiện là 0 hết)
F_pref(S) = (số buổi match) / (tổng số buổi)
```

SRS dùng logic **AND cứng (binary)**: chỉ cần một điều kiện sai là điểm tiết = 0.

#### Implementation hiện tại

```python
time_score = 1.0 if ca_num in preferred_cas else 0.0
day_score  = 0.0 if day_of_week in avoid_set else 1.0
score_per_class = (time_score + day_score) / 2   # trung bình cộng
```

Implementation dùng **trung bình cộng (partial credit)**: mỗi tiết được điểm riêng.

#### Bảng so sánh điểm từng tiết

| Khớp ca? | Bị tránh ngày? | SRS v1.0 | Implementation |
|---|---|---|---|
| ✅ | ❌ | **1.0** | **1.0** |
| ✅ | ✅ | **0.0** | **0.5** |
| ❌ | ❌ | **0.0** | **0.5** |
| ❌ | ✅ | **0.0** | **0.0** |

#### Lý do điều chỉnh

SRS xử lý AND cứng khiến một lớp sai ca nhưng đúng ngày vẫn bị 0 điểm — không phân biệt được "hoàn toàn sai" với "đúng một nửa". Partial credit phản ánh đúng hơn mức độ phù hợp: lớp học vào Ca 1 dù không phải ca ưa thích nhưng không rơi vào ngày tránh vẫn tốt hơn lớp học vào ngày tránh. Cách này cũng tránh ép Score(S) về 0 chỉ vì một tiết lệch ca.

---

### 9.3 F_balance — Cân bằng khối lượng

#### SRS v1.0 (mục 6.2.4)

```
σ   = độ lệch chuẩn của {n_d}  (std dev)
n_max = max(n_d)
F_balance(S) = 1 − (σ / n_max)   [nếu chỉ 1 ngày học → 0.5]
```

- Chuẩn hóa **thích nghi** theo `n_max`.
- Chỉ 1 ngày học → cố định **0.5**.

#### Implementation hiện tại

```python
avg      = mean(counts)
variance = mean((c − avg)² for c in counts)     # phương sai, không phải σ
score    = clamp(1.0 − variance / 9.0, 0, 1)    # hằng số 9.0 cố định

# Trường hợp đặc biệt:
# - 1 lớp học duy nhất   → 1.0
# - Nhiều lớp cùng 1 ngày → 0.0
```

#### Bảng so sánh

| Khía cạnh | SRS v1.0 | Implementation |
|---|---|---|
| Đo lường phân tán | Độ lệch chuẩn σ | Phương sai (variance) |
| Chuẩn hóa | Thích nghi theo `n_max` | Hằng số cố định `9.0` |
| Chỉ 1 ngày học | 0.5 | 1 lớp → 1.0; nhiều lớp cùng ngày → 0.0 |

#### Lý do điều chỉnh

1. **Phương sai thay vì σ:** Cả hai đều đo độ phân tán. Dùng phương sai trực tiếp đơn giản hơn (không cần sqrt), phù hợp hơn với mục đích chuẩn hóa về khoảng [0,1].
2. **Hằng số 9.0 thay vì `n_max`:** Chuẩn hóa theo `n_max` có vấn đề khi `n_max = 1` (mẫu số nhỏ) hoặc khi σ > n_max (điểm âm). Hằng số 9.0 đặt mức "lịch rất mất cân bằng" (ví dụ 0 vs 3 tiết/ngày cho 3 ngày) tương đương variance≈9, đảm bảo score không âm và nhất quán hơn.
3. **Trường hợp 1 ngày học:** SRS trả 0.5 cố định — không phân biệt 1 lớp và nhiều lớp dồn cùng ngày. Implementation phân biệt: 1 lớp duy nhất thì không cần cân bằng (1.0), còn nhiều lớp cùng 1 ngày là mất cân bằng tệ nhất (0.0).

---

### 9.4 Tổng kết sai khác

| # | Thành phần | Điểm khác biệt chính | Mức độ ảnh hưởng |
|---|---|---|---|
| 1 | F_break | Ngưỡng đạt 1.0 (`min_break` vs `2×min_break`); step-function phạt gap lớn; `_DESIGNED_GAPS` | **Cao** — thay đổi giá trị số rõ rệt |
| 2 | F_pref | Partial credit (0.5) vs AND cứng (0/1) khi chỉ khớp một trong hai điều kiện | **Trung bình** — chỉ ảnh hưởng khi có tiết "khớp một nửa" |
| 3 | F_balance | Phương sai/9.0 vs σ/n_max; xử lý 1 ngày học khác | **Trung bình** — giá trị lệch nhau nhưng thứ tự xếp hạng tương tự |

> **Ghi chú cho buổi báo cáo:** Cả ba điều chỉnh đều có lý do cụ thể gắn với thực tế lịch STU (ca học cố định, giờ ra chơi) và tính ổn định số học của công thức. Có thể trình bày như "refinement có căn cứ" chứ không phải "sai SRS".
