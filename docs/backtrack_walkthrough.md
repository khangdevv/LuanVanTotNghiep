# Walkthrough chi tiết _backtrack — 7 môn, 7-8 nhóm/môn

## 1. Dữ liệu đầu vào

### 1.1 Cấu hình

```
avoid_days      = {7, 8}          # tránh Thứ 7 và Chủ Nhật
personal_events = [Event(Thứ3, 12:00–14:00)]   # trưa Thứ 3 bận
max_solutions   = 5
```

### 1.2 Ký hiệu khung giờ

| Ký hiệu | Giờ học |
|---------|---------|
| S1 | 07:00 – 09:00 |
| S2 | 09:30 – 11:30 |
| S3 | 13:00 – 15:00 |
| S4 | 15:30 – 17:30 |

### 1.3 Bảng 7 môn — 52 nhóm lớp

| ID | Môn | Thứ | Giờ | Ghi chú |
|----|-----|-----|-----|---------|
| TCC1 | Toán Cao Cấp | 2 | S1 | |
| TCC2 | Toán Cao Cấp | 2 | S3 | |
| TCC3 | Toán Cao Cấp | 3 | S1 | |
| TCC4 | Toán Cao Cấp | 3 | S2 | |
| TCC5 | Toán Cao Cấp | 4 | S1 | |
| TCC6 | Toán Cao Cấp | 4 | S3 | |
| TCC7 | Toán Cao Cấp | 5 | S1 | |
| TCC8 | Toán Cao Cấp | **7** | S1 | ← AVOID |
| VL1 | Vật Lý | 2 | S1 | |
| VL2 | Vật Lý | 2 | S2 | |
| VL3 | Vật Lý | 3 | S1 | |
| VL4 | Vật Lý | 3 | S3 | |
| VL5 | Vật Lý | 4 | S1 | |
| VL6 | Vật Lý | 4 | S3 | |
| VL7 | Vật Lý | 5 | S2 | |
| VL8 | Vật Lý | **7** | S3 | ← AVOID |
| LP1 | Lập Trình Python | 2 | S2 | |
| LP2 | Lập Trình Python | 2 | S4 | |
| LP3 | Lập Trình Python | 3 | S3 | ← PERSONAL EVENT |
| LP4 | Lập Trình Python | 4 | S2 | |
| LP5 | Lập Trình Python | 5 | S1 | |
| LP6 | Lập Trình Python | 5 | S3 | |
| LP7 | Lập Trình Python | **7** | S2 | ← AVOID |
| CS1 | Cơ Sở Dữ Liệu | 2 | S1 | |
| CS2 | Cơ Sở Dữ Liệu | 2 | S3 | |
| CS3 | Cơ Sở Dữ Liệu | 3 | S2 | |
| CS4 | Cơ Sở Dữ Liệu | 4 | S2 | |
| CS5 | Cơ Sở Dữ Liệu | 5 | S1 | |
| CS6 | Cơ Sở Dữ Liệu | 5 | S4 | |
| CS7 | Cơ Sở Dữ Liệu | **7** | S3 | ← AVOID |
| MM1 | Mạng Máy Tính | 2 | S4 | |
| MM2 | Mạng Máy Tính | 3 | S2 | |
| MM3 | Mạng Máy Tính | 3 | S4 | |
| MM4 | Mạng Máy Tính | 4 | S4 | |
| MM5 | Mạng Máy Tính | 5 | S2 | |
| MM6 | Mạng Máy Tính | 6 | S1 | |
| MM7 | Mạng Máy Tính | **7** | S4 | ← AVOID |
| GT1 | Giải Tích | 2 | S1 | |
| GT2 | Giải Tích | 2 | S2 | |
| GT3 | Giải Tích | 3 | S1 | |
| GT4 | Giải Tích | 3 | S3 | ← PERSONAL EVENT |
| GT5 | Giải Tích | 4 | S1 | |
| GT6 | Giải Tích | 5 | S2 | |
| GT7 | Giải Tích | 6 | S1 | |
| GT8 | Giải Tích | **7** | S1 | ← AVOID |
| TA1 | Tiếng Anh | 2 | S1 | |
| TA2 | Tiếng Anh | 3 | S3 | ← PERSONAL EVENT |
| TA3 | Tiếng Anh | 4 | S1 | |
| TA4 | Tiếng Anh | 4 | S3 | |
| TA5 | Tiếng Anh | 5 | S1 | |
| TA6 | Tiếng Anh | 5 | S2 | |
| TA7 | Tiếng Anh | **7** | S1 | ← AVOID |

---

## 2. Bước 1 — `_init_domains` lọc avoid_days

Loại tất cả nhóm lớp có `day_of_week IN {7, 8}`:

```
TCC: bỏ TCC8        → còn [TCC1, TCC2, TCC3, TCC4, TCC5, TCC6, TCC7]  (7)
VL : bỏ VL8         → còn [VL1, VL2, VL3, VL4, VL5, VL6, VL7]         (7)
LP : bỏ LP7         → còn [LP1, LP2, LP3, LP4, LP5, LP6]               (6)
CS : bỏ CS7         → còn [CS1, CS2, CS3, CS4, CS5, CS6]               (6)
MM : bỏ MM7         → còn [MM1, MM2, MM3, MM4, MM5, MM6]               (6)
GT : bỏ GT8         → còn [GT1, GT2, GT3, GT4, GT5, GT6, GT7]          (7)
TA : bỏ TA7         → còn [TA1, TA2, TA3, TA4, TA5, TA6]               (6)
```

**Domains sau _init_domains:**

```
domains = {
  "TCC": [TCC1,TCC2,TCC3,TCC4,TCC5,TCC6,TCC7],   len=7
  "VL" : [VL1,VL2,VL3,VL4,VL5,VL6,VL7],           len=7
  "LP" : [LP1,LP2,LP3,LP4,LP5,LP6],                len=6
  "CS" : [CS1,CS2,CS3,CS4,CS5,CS6],                len=6
  "MM" : [MM1,MM2,MM3,MM4,MM5,MM6],                len=6
  "GT" : [GT1,GT2,GT3,GT4,GT5,GT6,GT7],            len=7
  "TA" : [TA1,TA2,TA3,TA4,TA5,TA6],                len=6
}
```

Không môn nào rỗng → tiếp tục backtracking.

---

## 3. Bước 2 — `build_conflict_set` (Tầng 1)

Duyệt O(n²) tất cả 52×51/2 = 1.326 cặp nhóm lớp.
Các cặp xung đột (cùng thứ, giao giờ):

```
TCC1↔VL1  (T2 S1 vs T2 S1)      TCC1↔CS1  (T2 S1 vs T2 S1)
TCC1↔GT1  (T2 S1 vs T2 S1)      TCC1↔TA1  (T2 S1 vs T2 S1)
TCC2↔CS2  (T2 S3 vs T2 S3)      TCC3↔VL3  (T3 S1 vs T3 S1)
TCC3↔GT3  (T3 S1 vs T3 S1)      TCC4↔CS3  (T3 S2 vs T3 S2)
TCC4↔MM2  (T3 S2 vs T3 S2)      TCC5↔VL5  (T4 S1 vs T4 S1)
TCC5↔GT5  (T4 S1 vs T4 S1)      TCC5↔TA3  (T4 S1 vs T4 S1)
TCC6↔VL6  (T4 S3 vs T4 S3)      TCC6↔TA4  (T4 S3 vs T4 S3)
TCC7↔LP5  (T5 S1 vs T5 S1)      TCC7↔CS5  (T5 S1 vs T5 S1)
TCC7↔TA5  (T5 S1 vs T5 S1)      VL1↔CS1   (T2 S1 vs T2 S1)
VL1↔GT1   (T2 S1 vs T2 S1)      VL1↔TA1   (T2 S1 vs T2 S1)
VL3↔GT3   (T3 S1 vs T3 S1)      VL5↔GT5   (T4 S1 vs T4 S1)
VL5↔TA3   (T4 S1 vs T4 S1)      VL6↔TA4   (T4 S3 vs T4 S3)
VL7↔TA6   (T5 S2 vs T5 S2)      LP1↔GT2   (T2 S2 vs T2 S2)
LP4↔CS4   (T4 S2 vs T4 S2)      LP5↔CS5   (T5 S1 vs T5 S1)
LP5↔TA5   (T5 S1 vs T5 S1)      CS1↔GT1   (T2 S1 vs T2 S1)
CS1↔TA1   (T2 S1 vs T2 S1)      CS3↔MM2   (T3 S2 vs T3 S2)
CS5↔TA5   (T5 S1 vs T5 S1)      MM5↔GT6   (T5 S2 vs T5 S2)
MM5↔TA6   (T5 S2 vs T5 S2)      MM6↔GT7   (T6 S1 vs T6 S1)
GT1↔TA1   (T2 S1 vs T2 S1)      GT5↔TA3   (T4 S1 vs T4 S1)
GT6↔TA6   (T5 S2 vs T5 S2)
```

Lưu cả hai chiều → conflict_set có **82 tuple** (41 cặp × 2).

---

## 4. Bước 3 — `_backtrack` bắt đầu

```
CALL #1
  chosen     = {}
  unassigned = ["TCC","VL","LP","CS","MM","GT","TA"]
  domains    = { TCC:7, VL:7, LP:6, CS:6, MM:6, GT:7, TA:6 }
```

### MRV lần 1

```
TCC=7, VL=7, LP=6, CS=6, MM=6, GT=7, TA=6
→ tie giữa LP, CS, MM, TA (đều =6)
→ min() lấy phần tử đầu tiên trong list → chọn "LP"
```

---

## 5. Nhánh LP — Thử từng nhóm lớp

### 5.1 Thử LP1 (Thứ2 S2)

```
4a — _conflicts_with_personal_events(LP1):
     Event: Thứ3 12:00-14:00
     LP1  : Thứ2 09:30-11:30
     Thứ2 ≠ Thứ3 → KHÔNG xung đột → tiếp tục

4b — chosen={} → bỏ qua

4c — chosen["LP"] = LP1
     _forward_check(LP1, ["TCC","VL","CS","MM","GT","TA"], ...)
```

**FC với LP1 (Thứ2 S2 = 09:30-11:30):**

```
Xét TCC: LP1 xung đột với TCC nào?
  TCC1(T2 S1): ("LP1","TCC1") IN conflict_set? → ❌ (giờ khác nhau)
  TCC2(T2 S3): ("LP1","TCC2")? → ❌
  TCC3..TCC7  → khác thứ → ❌
  removed["TCC"] = []  → domains["TCC"] vẫn 7 → OK

Xét VL: LP1 xung đột với VL nào?
  VL1(T2 S1): LP1=09:30, VL1=07-09 → 09:30 < 09:00? FALSE → không giao giờ
  VL2(T2 S2): ("LP1","VL2")? → T2 09:30-11:30 vs T2 09:30-11:30
              LP1.start(09:30) < VL2.end(11:30) ✓
              VL2.start(09:30) < LP1.end(11:30) ✓ → XUNG ĐỘT
              → xóa VL2, removed["VL"]=[VL2]
  VL3..VL7 → khác thứ hoặc không giao → ❌
  domains["VL"] = [VL1,VL3,VL4,VL5,VL6,VL7]  len=6 → OK

Xét CS: LP1 xung đột CS?
  ("LP1","CS1")? T2 09:30-11:30 vs T2 07-09
    LP1.start(09:30) < CS1.end(09:00)? → 09:30 < 09:00? FALSE → không giao
  CS2(T2 S3), CS3(T3), CS4(T4), CS5(T5), CS6(T5) → ❌
  removed["CS"] = []  → OK

Xét MM: không có MM ở T2 S2 → removed["MM"]=[] → OK

Xét GT: ("LP1","GT2")? T2 09:30-11:30 vs T2 09:30-11:30 → XUNG ĐỘT
  → xóa GT2, removed["GT"]=[GT2]
  domains["GT"] = [GT1,GT3,GT4,GT5,GT6,GT7]  len=6 → OK

Xét TA: ("LP1","TA?")? không có TA ở T2 S2 → removed["TA"]=[] → OK

→ return (True, removed={"TCC":[], "VL":[VL2], "CS":[], "MM":[], "GT":[GT2], "TA":[]})
```

FC OK → đệ quy sâu hơn.

---

```
CALL #2
  chosen     = {LP: LP1}
  unassigned = ["TCC","VL","CS","MM","GT","TA"]
  domains    = { TCC:7, VL:6, CS:6, MM:6, GT:6, TA:6 }
```

### MRV lần 2

```
TCC=7, VL=6, CS=6, MM=6, GT=6, TA=6
→ tie: VL, CS, MM, GT, TA (=6) → chọn "VL"
```

---

### 5.2 Thử VL1 (Thứ2 S1)

```
4a: Thứ2 ≠ Thứ3 → OK
4b: ("VL1","LP1")? T2 S1 vs T2 S2 → không giao giờ → OK
4c: chosen["VL"] = VL1
    _forward_check(VL1, ["TCC","CS","MM","GT","TA"], ...)
```

**FC với VL1 (Thứ2 S1 = 07:00-09:00):**

```
Xét TCC:
  TCC1(T2 S1): ("VL1","TCC1") IN conflict_set → ✅ → xóa TCC1
  TCC2..TCC7 → ❌
  domains["TCC"] = [TCC2,TCC3,TCC4,TCC5,TCC6,TCC7]  len=6 → OK

Xét CS:
  CS1(T2 S1): ("VL1","CS1") IN conflict_set → ✅ → xóa CS1
  CS2..CS6 → ❌
  domains["CS"] = [CS2,CS3,CS4,CS5,CS6]  len=5 → OK

Xét MM: VL1 T2 S1, MM không có T2 S1 → removed["MM"]=[] → OK

Xét GT:
  GT1(T2 S1): ("VL1","GT1") IN conflict_set → ✅ → xóa GT1
  GT3..GT7 → ❌
  domains["GT"] = [GT3,GT4,GT5,GT6,GT7]  len=5 → OK

Xét TA:
  TA1(T2 S1): ("VL1","TA1") IN conflict_set → ✅ → xóa TA1
  TA2..TA6 → ❌
  domains["TA"] = [TA2,TA3,TA4,TA5,TA6]  len=5 → OK

→ (True, removed={TCC:[TCC1], CS:[CS1], MM:[], GT:[GT1], TA:[TA1]})
```

---

```
CALL #3
  chosen     = {LP:LP1, VL:VL1}
  unassigned = ["TCC","CS","MM","GT","TA"]
  domains    = { TCC:6, CS:5, MM:6, GT:5, TA:5 }
```

### MRV lần 3

```
TCC=6, CS=5, MM=6, GT=5, TA=5
→ tie: CS, GT, TA (=5) → chọn "CS"
```

---

### 5.3 Thử CS2 (Thứ2 S3)

```
4a: Thứ2 ≠ Thứ3 → OK
4b: ("CS2","LP1")? T2 S3 vs T2 S2 → không giao → OK
    ("CS2","VL1")? T2 S3 vs T2 S1 → không giao → OK
4c: chosen["CS"] = CS2
    _forward_check(CS2, ["TCC","MM","GT","TA"], ...)
```

**FC với CS2 (Thứ2 S3):**

```
Xét TCC:
  TCC2(T2 S3): ("CS2","TCC2") IN conflict_set → ✅ → xóa TCC2
  domains["TCC"] = [TCC3,TCC4,TCC5,TCC6,TCC7]  len=5 → OK

Xét MM: không T2 S3 trong MM → removed["MM"]=[] → OK

Xét GT: không T2 S3 trong GT (GT1 đã bị xóa, GT2 đã bị xóa trước) → OK

Xét TA: không T2 S3 trong TA → OK

→ (True, removed={TCC:[TCC2], MM:[], GT:[], TA:[]})
```

---

```
CALL #4
  chosen     = {LP:LP1, VL:VL1, CS:CS2}
  unassigned = ["TCC","MM","GT","TA"]
  domains    = { TCC:5, MM:6, GT:5, TA:5 }
```

### MRV lần 4

```
TCC=5, MM=6, GT=5, TA=5
→ tie: TCC, GT, TA → chọn "TCC"
```

---

### 5.4 Thử TCC3 (Thứ3 S1)

```
4a: Thứ3 ≠ Thứ3? đúng là Thứ3, kiểm tra giờ:
    Event 12:00-14:00, TCC3 07:00-09:00
    TCC3.start(07:00) < Event.end(14:00) ✓
    Event.start(12:00) < TCC3.end(09:00)? 12:00 < 09:00? FALSE
    → KHÔNG xung đột → tiếp tục

4b: chosen = {LP:LP1, VL:VL1, CS:CS2}
    ("TCC3","LP1")? T3 S1 vs T2 S2 → khác thứ → OK
    ("TCC3","VL1")? T3 S1 vs T2 S1 → khác thứ → OK
    ("TCC3","CS2")? T3 S1 vs T2 S3 → khác thứ → OK

4c: chosen["TCC"] = TCC3
    _forward_check(TCC3, ["MM","GT","TA"], ...)
```

**FC với TCC3 (Thứ3 S1):**

```
Xét MM: TCC3 T3 S1, MM có MM2(T3 S2) → không giao giờ → OK

Xét GT:
  GT3(T3 S1): ("TCC3","GT3") IN conflict_set → ✅ → xóa GT3
  domains["GT"] = [GT4,GT5,GT6,GT7]  len=4 → OK

Xét TA: không T3 S1 trong TA → OK

→ (True, removed={MM:[], GT:[GT3], TA:[]})
```

---

```
CALL #5
  chosen     = {LP:LP1, VL:VL1, CS:CS2, TCC:TCC3}
  unassigned = ["MM","GT","TA"]
  domains    = { MM:6, GT:4, TA:5 }
```

### MRV lần 5

```
MM=6, GT=4, TA=5
→ GT nhỏ nhất → chọn "GT"
```

---

### 5.5 Thử GT4 (Thứ3 S3)

```
4a — _conflicts_with_personal_events(GT4):
     GT4: Thứ3 13:00-15:00
     Event: Thứ3 12:00-14:00
     GT4.start(13:00) < Event.end(14:00) ✓
     Event.start(12:00) < GT4.end(15:00) ✓
     → XUNG ĐỘT VỚI PERSONAL EVENT → SKIP GT4
```

### 5.6 Thử GT5 (Thứ4 S1)

```
4a: Thứ4 ≠ Thứ3 → OK
4b: chosen = {LP:LP1, VL:VL1, CS:CS2, TCC:TCC3}
    ("GT5","LP1")? T4 S1 vs T2 S2 → OK
    ("GT5","VL1")? T4 S1 vs T2 S1 → OK
    ("GT5","CS2")? T4 S1 vs T2 S3 → OK
    ("GT5","TCC3")? T4 S1 vs T3 S1 → khác thứ → OK

4c: chosen["GT"] = GT5
    _forward_check(GT5, ["MM","TA"], ...)
```

**FC với GT5 (Thứ4 S1):**

```
Xét MM: không T4 S1 trong MM → OK

Xét TA:
  TA3(T4 S1): ("GT5","TA3") IN conflict_set → ✅ → xóa TA3
  TA4(T4 S3): ("GT5","TA4")? → ❌
  TA5,TA6: khác thứ → ❌
  domains["TA"] = [TA2,TA4,TA5,TA6]  len=4 → OK

→ (True, removed={MM:[], TA:[TA3]})
```

---

```
CALL #6
  chosen     = {LP:LP1, VL:VL1, CS:CS2, TCC:TCC3, GT:GT5}
  unassigned = ["MM","TA"]
  domains    = { MM:6, TA:4 }
```

### MRV lần 6

```
MM=6, TA=4 → chọn "TA"
```

---

### 5.7 Thử TA2 (Thứ3 S3)

```
4a — _conflicts_with_personal_events(TA2):
     TA2: Thứ3 13:00-15:00
     Event: Thứ3 12:00-14:00
     13:00 < 14:00 ✓ và 12:00 < 15:00 ✓
     → XUNG ĐỘT VỚI PERSONAL EVENT → SKIP TA2
```

### 5.8 Thử TA4 (Thứ4 S3)

```
4a: Thứ4 ≠ Thứ3 → OK
4b: ("TA4","GT5")? T4 S3 vs T4 S1 → không giao giờ → OK
    ("TA4","TCC3")? khác thứ → OK
    ("TA4","VL1")? khác thứ → OK
    ... → OK tất cả

4c: chosen["TA"] = TA4
    _forward_check(TA4, ["MM"], ...)
```

**FC với TA4 (Thứ4 S3):**

```
Xét MM: không T4 S3 trong MM → OK
→ (True, removed={MM:[]})
```

---

```
CALL #7
  chosen     = {LP:LP1, VL:VL1, CS:CS2, TCC:TCC3, GT:GT5, TA:TA4}
  unassigned = ["MM"]
  domains    = { MM:6 }
```

### MRV lần 7 — Môn cuối cùng

```
→ chọn "MM" (duy nhất)
```

**Thử MM1 (Thứ2 S4):**

```
4a: Thứ2 ≠ Thứ3 → OK
4b: kiểm tra MM1 với toàn bộ chosen:
    ("MM1","LP1")? T2 S4 vs T2 S2 → không giao giờ → OK
    ("MM1","VL1")? T2 S4 vs T2 S1 → không giao giờ → OK
    ... tất cả OK
4c: chosen["MM"] = MM1
    _forward_check(MM1, [], ...) → unassigned rỗng → (True, {})
```

---

```
CALL #8 — BASE CASE
  unassigned = []
  chosen = {LP:LP1, VL:VL1, CS:CS2, TCC:TCC3, GT:GT5, TA:TA4, MM:MM1}
```

```
✅ NGHIỆM 1 tìm được:
{
  TCC: TCC3  (Thứ3 S1),
  VL : VL1   (Thứ2 S1),
  LP : LP1   (Thứ2 S2),
  CS : CS2   (Thứ2 S3),
  MM : MM1   (Thứ2 S4),
  GT : GT5   (Thứ4 S1),
  TA : TA4   (Thứ4 S3),
}
```

---

## 6. Restore theo chiều ngược — quay lại tìm thêm nghiệm

Sau khi lưu Nghiệm 1, backtracking **restore** từng tầng và tiếp tục:

```
CALL #7: thử MM2 → MM3 → ... → MM6
  → Mỗi MM hợp lệ cho ra 1 nghiệm mới với cùng 6 môn còn lại
  → NGHIỆM 2: MM=MM2  (Thứ3 S2)
    4b: ("MM2","TCC3")? T3 S2 vs T3 S1 → không giao giờ → OK
    → ✅ NGHIỆM 2

  → NGHIỆM 3: MM=MM3  (Thứ3 S4) → ✅
  → NGHIỆM 4: MM=MM4  (Thứ4 S4)
    4b: ("MM4","GT5")? T4 S4 vs T4 S1 → không giao → OK
    → ✅ NGHIỆM 4
  → NGHIỆM 5: MM=MM5  (Thứ5 S2) → ✅
```

**Đủ max_solutions=5 → dừng toàn bộ cây đệ quy.**

---

## 7. Tổng kết các trường hợp đã bao phủ

### TH1 — avoid_days lọc sơ bộ

```
TCC8, VL8, LP7, CS7, MM7, GT8, TA7 bị loại trước khi backtracking bắt đầu.
→ 7 nhóm lớp không bao giờ được thử.
```

### TH2 — personal_events lọc trong vòng lặp

```
LP3  (Thứ3 S3 = 13:00-15:00) — SKIP khi thử cho LP
GT4  (Thứ3 S3 = 13:00-15:00) — SKIP khi thử cho GT  (Step 5.5)
TA2  (Thứ3 S3 = 13:00-15:00) — SKIP khi thử cho TA  (Step 5.7)
→ Kiểm tra xảy ra ở 4a, trước khi gán và chạy FC → không tốn chi phí
```

### TH3 — FC phát hiện dead-end sớm

Ví dụ: Nếu ở CALL #2 thử VL1 và CS chỉ còn lại nhóm lớp Thứ2 S1:

```
_forward_check(VL1, ["TCC","CS",...]):
  Xét CS: xóa CS1(T2 S1)
           domains["CS"] còn [CS2,CS3,CS4,CS5,CS6] = 5 → OK

Trường hợp cực đoan — nếu CS CHỈ có CS1:
  domains["CS"] = [] → DEAD-END
  → return (False, removed) ngay lập tức
  → không đi sâu vào TCC, MM, GT, TA
  → tiết kiệm toàn bộ nhánh con
```

### TH4 — MRV chọn đúng môn bị ràng buộc nhất

```
CALL #5:
  domains = { MM:6, GT:4, TA:5 }
  → GT=4 nhỏ nhất → chọn GT trước
  → Phát hiện sớm GT4 và GT3 bị loại
  → Nếu chọn MM (=6) trước, sẽ đi sâu 6 nhánh trước khi biết GT bị hỏng
```

### TH5 — Restore domain chính xác

```
Sau CALL #7 (MM1→MM6), khi backtrack lên CALL #6 để thử TA5, TA6:
  _restore_domains({"TA":[TA3]}, domains)
  → domains["TA"] trở về [TA2,TA3,TA4,TA5,TA6]  ← TA3 được trả lại
  → Tiếp tục thử TA5 (dù TA5 có thể bị chặn bởi conflict_set)
```

### TH6 — Điều kiện biên end_time == start_time

```
VL1: 07:00–09:00
LP1: 09:30–11:30

Nếu LP2 = 09:00–11:00 thì:
  LP2.start(09:00) < VL1.end(09:00)? → 09:00 < 09:00 → FALSE
  → KHÔNG xung đột (strict <, đúng SRS 6.1.1)
```

### TH7 — Conflict_set đối xứng phát huy tác dụng

```
CALL #3: gán VL=VL1 trước, sau đó thử TCC
  → kiểm tra ("TCC1","VL1") IN conflict_set → ✅ có (chiều ngược)
  → bắt được dù thứ tự gán là VL trước TCC
```

---

## 8. Kết quả cuối cùng

```python
valid_schedules = [
  {TCC:TCC3, VL:VL1, LP:LP1, CS:CS2, MM:MM1, GT:GT5, TA:TA4},  # nghiệm 1
  {TCC:TCC3, VL:VL1, LP:LP1, CS:CS2, MM:MM2, GT:GT5, TA:TA4},  # nghiệm 2
  {TCC:TCC3, VL:VL1, LP:LP1, CS:CS2, MM:MM3, GT:GT5, TA:TA4},  # nghiệm 3
  {TCC:TCC3, VL:VL1, LP:LP1, CS:CS2, MM:MM4, GT:GT5, TA:TA4},  # nghiệm 4
  {TCC:TCC3, VL:VL1, LP:LP1, CS:CS2, MM:MM5, GT:GT5, TA:TA4},  # nghiệm 5
]
→ dừng vì đủ max_solutions=5
→ Tầng 3 nhận 5 nghiệm này, tính Score(S), trả top 3
```

---

## 9. Sơ đồ cây đệ quy (rút gọn)

```
root
└── LP=LP1
    └── VL=VL1  [FC: xóa TCC1,CS1,GT1,TA1]
        └── CS=CS2  [FC: xóa TCC2]
            └── TCC=TCC3  [FC: xóa GT3]
                └── GT=GT5  [FC: xóa TA3]
                    ├── TA=TA2 ✗ (PersonalEvent)
                    ├── TA=TA4
                    │   ├── MM=MM1 ✅ NGHIỆM 1
                    │   ├── MM=MM2 ✅ NGHIỆM 2
                    │   ├── MM=MM3 ✅ NGHIỆM 3
                    │   ├── MM=MM4 ✅ NGHIỆM 4
                    │   └── MM=MM5 ✅ NGHIỆM 5 → DỪNG
                    ├── TA=TA5 (nếu còn chỗ)
                    └── TA=TA6 (nếu còn chỗ)
                ├── GT=GT6 → ...
                └── GT=GT7 → ...
            ├── TCC=TCC4 → ...
            └── ...
        ├── CS=CS3 → ...
        └── ...
    ├── VL=VL2 → ...
    └── ...
├── LP=LP2 → ...
└── ...

✗ = bị lọc bởi PersonalEvent
FC xóa = những nhóm bị loại khỏi domain của môn khác
```
