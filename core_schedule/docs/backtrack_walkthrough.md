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

Nhóm theo (thứ, slot) để liệt kê đầy đủ:

```
T2 S1 → TCC1, VL1, CS1, GT1, TA1   (C(5,2) = 10 cặp)
T2 S2 → VL2, LP1, GT2               (C(3,2) =  3 cặp)
T2 S3 → TCC2, CS2                   (C(2,2) =  1 cặp)
T2 S4 → LP2, MM1                    (C(2,2) =  1 cặp)  ← nhóm hay bị bỏ sót
T3 S1 → TCC3, VL3, GT3              (C(3,2) =  3 cặp)
T3 S2 → TCC4, CS3, MM2              (C(3,2) =  3 cặp)
T3 S3 → VL4, LP3, GT4, TA2          (C(4,2) =  6 cặp)
T4 S1 → TCC5, VL5, GT5, TA3         (C(4,2) =  6 cặp)
T4 S2 → LP4, CS4                    (C(2,2) =  1 cặp)
T4 S3 → TCC6, VL6, TA4              (C(3,2) =  3 cặp)
T5 S1 → TCC7, LP5, CS5, TA5         (C(4,2) =  6 cặp)
T5 S2 → VL7, MM5, GT6, TA6          (C(4,2) =  6 cặp)
T6 S1 → MM6, GT7                    (C(2,2) =  1 cặp)
──────────────────────────────────────────────────────
Tổng                                              50 cặp → 100 tuples (cả 2 chiều)
```

Toàn bộ 50 cặp xung đột:

```
─── T2 S1 ──────────────────────────────────────────────
TCC1↔VL1   TCC1↔CS1   TCC1↔GT1   TCC1↔TA1
VL1↔CS1    VL1↔GT1    VL1↔TA1
CS1↔GT1    CS1↔TA1
GT1↔TA1

─── T2 S2 ──────────────────────────────────────────────
VL2↔LP1    VL2↔GT2    LP1↔GT2

─── T2 S3 ──────────────────────────────────────────────
TCC2↔CS2

─── T2 S4 ──────────────────────────────────────────────
LP2↔MM1

─── T3 S1 ──────────────────────────────────────────────
TCC3↔VL3   TCC3↔GT3   VL3↔GT3

─── T3 S2 ──────────────────────────────────────────────
TCC4↔CS3   TCC4↔MM2   CS3↔MM2

─── T3 S3 ──────────────────────────────────────────────
VL4↔LP3    VL4↔GT4    VL4↔TA2
LP3↔GT4    LP3↔TA2    GT4↔TA2

─── T4 S1 ──────────────────────────────────────────────
TCC5↔VL5   TCC5↔GT5   TCC5↔TA3
VL5↔GT5    VL5↔TA3    GT5↔TA3

─── T4 S2 ──────────────────────────────────────────────
LP4↔CS4

─── T4 S3 ──────────────────────────────────────────────
TCC6↔VL6   TCC6↔TA4   VL6↔TA4

─── T5 S1 ──────────────────────────────────────────────
TCC7↔LP5   TCC7↔CS5   TCC7↔TA5
LP5↔CS5    LP5↔TA5    CS5↔TA5

─── T5 S2 ──────────────────────────────────────────────
VL7↔MM5    VL7↔GT6    VL7↔TA6
MM5↔GT6    MM5↔TA6    GT6↔TA6

─── T6 S1 ──────────────────────────────────────────────
MM6↔GT7
```

Lưu cả hai chiều → conflict_set có **100 tuples** (50 cặp × 2).

---

## 4. Luồng `_backtrack` — Tổng quan các bước

```
Mỗi lần đệ quy thực hiện theo thứ tự:
  1. Nếu đủ max_solutions → dừng.
  2. Nếu unassigned rỗng → lưu nghiệm.
  3. MRV: chọn môn có domain nhỏ nhất.
  4. LCV: sắp xếp nhóm lớp của môn đó theo số xung đột
          với domain các môn chưa gán (ít xung đột → thử trước).
  5. Với mỗi nhóm lớp theo thứ tự LCV:
       a. Bỏ qua nếu xung đột PersonalEvents.
       b. Bỏ qua nếu xung đột với môn đã gán (conflict_set).
       c. Forward Check: lan truyền ràng buộc sang các domain còn lại.
       d. Nếu OK → đệ quy sâu hơn.
       e. Restore domain → thử nhóm tiếp theo.
```

---

## 5. Bước 3 — `_backtrack` bắt đầu

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

### LCV cho LP

next_unassigned = ["TCC","VL","CS","MM","GT","TA"]

Đếm conflict_count của từng LP với tất cả nhóm lớp trong domain các môn còn lại:

| Nhóm | Xung đột với | conflict_count |
|------|-------------|---------------|
| LP6 (T5 S3) | không có nhóm nào cùng T5 S3 | **0** |
| LP2 (T2 S4) | MM1(T2 S4) | **1** |
| LP4 (T4 S2) | CS4(T4 S2) | **1** |
| LP1 (T2 S2) | VL2(T2 S2), GT2(T2 S2) | **2** |
| LP3 (T3 S3) | VL4, GT4, TA2 (T3 S3) ← sẽ bị skip PersonalEvent | **3** |
| LP5 (T5 S1) | TCC7, CS5, TA5 (T5 S1) | **3** |

**Thứ tự LCV (ascending, stable sort):** LP6 → LP2 → LP4 → LP1 → LP3 → LP5

---

## 6. Nhánh LP — Thử LP6 trước (LCV = 0)

### 6.1 Thử LP6 (Thứ5 S3 = 13:00-15:00)

```
4a — _conflicts_with_personal_events(LP6):
     LP6: Thứ5, Event: Thứ3 → Thứ5 ≠ Thứ3 → KHÔNG xung đột → OK

4b — chosen={} → bỏ qua

4c — chosen["LP"] = LP6
     _forward_check(LP6, ["TCC","VL","CS","MM","GT","TA"], ...)
```

**FC với LP6 (T5 S3 — không có nhóm nào cùng slot):**

```
Xét TCC, VL, CS, MM, GT, TA:
  Không có nhóm nào ở T5 S3 trong bất kỳ môn nào
  → removed = {tất cả: []}
→ return (True, removed={})
```

FC OK → không thu hẹp domain nào.

---

```
CALL #2
  chosen     = {LP: LP6}
  unassigned = ["TCC","VL","CS","MM","GT","TA"]
  domains    = { TCC:7, VL:7, CS:6, MM:6, GT:7, TA:6 }   ← không thay đổi
```

### MRV lần 2

```
TCC=7, VL=7, CS=6, MM=6, GT=7, TA=6
→ tie: CS=6, MM=6, TA=6 → chọn "CS" (đầu tiên trong list)
```

### LCV cho CS

next_unassigned = ["TCC","VL","MM","GT","TA"]

| Nhóm | Xung đột với | conflict_count |
|------|-------------|---------------|
| CS4 (T4 S2) | không có TCC/VL/MM/GT/TA cùng T4 S2 | **0** |
| CS6 (T5 S4) | không có nhóm cùng T5 S4 | **0** |
| CS2 (T2 S3) | TCC2(T2 S3) | **1** |
| CS3 (T3 S2) | TCC4(T3 S2), MM2(T3 S2) | **2** |
| CS5 (T5 S1) | TCC7(T5 S1), TA5(T5 S1) | **2** |
| CS1 (T2 S1) | TCC1, VL1, GT1, TA1 (T2 S1) | **4** |

**Thứ tự LCV:** CS4 → CS6 → CS2 → CS3 → CS5 → CS1

---

### 6.2 Thử CS4 (Thứ4 S2 = 09:30-11:30)

```
4a: Thứ4 ≠ Thứ3 → OK
4b: ("CS4","LP6")? T4 S2 vs T5 S3 → khác thứ → OK
4c: chosen["CS"] = CS4
    _forward_check(CS4, ["TCC","VL","MM","GT","TA"], ...)
```

**FC với CS4 (T4 S2 — không trùng slot với TCC/VL/MM/GT/TA):**

```
TCC không có T4 S2 (TCC5=T4S1, TCC6=T4S3) → OK
VL  không có T4 S2 (VL5=T4S1, VL6=T4S3)   → OK
MM  không có T4 S2 (MM4=T4S4)              → OK
GT  không có T4 S2 (GT5=T4S1)              → OK
TA  không có T4 S2 (TA3=T4S1, TA4=T4S3)   → OK
→ return (True, removed={})
```

---

```
CALL #3
  chosen     = {LP:LP6, CS:CS4}
  unassigned = ["TCC","VL","MM","GT","TA"]
  domains    = { TCC:7, VL:7, MM:6, GT:7, TA:6 }   ← không thay đổi
```

### MRV lần 3

```
TCC=7, VL=7, MM=6, GT=7, TA=6
→ min=6: MM, TA → chọn "MM" (đầu tiên gặp min)
```

### LCV cho MM

next_unassigned = ["TCC","VL","GT","TA"]

| Nhóm | Xung đột với | conflict_count |
|------|-------------|---------------|
| MM1 (T2 S4) | không có TCC/VL/GT/TA cùng T2 S4 | **0** |
| MM3 (T3 S4) | không có nhóm cùng T3 S4 | **0** |
| MM4 (T4 S4) | không có nhóm cùng T4 S4 | **0** |
| MM2 (T3 S2) | TCC4(T3 S2) | **1** |
| MM6 (T6 S1) | GT7(T6 S1) | **1** |
| MM5 (T5 S2) | VL7, GT6, TA6 (T5 S2) | **3** |

**Thứ tự LCV:** MM1 → MM3 → MM4 → MM2 → MM6 → MM5

---

### 6.3 Thử MM1 (Thứ2 S4 = 15:30-17:30)

```
4a: Thứ2 ≠ Thứ3 → OK
4b: ("MM1","LP6")? T2 S4 vs T5 S3 → khác thứ → OK
    ("MM1","CS4")? T2 S4 vs T4 S2 → khác thứ → OK
4c: chosen["MM"] = MM1
    _forward_check(MM1, ["TCC","VL","GT","TA"], ...)
```

**FC với MM1 (T2 S4 — không trùng slot với TCC/VL/GT/TA):**

```
→ return (True, removed={})
```

---

```
CALL #4
  chosen     = {LP:LP6, CS:CS4, MM:MM1}
  unassigned = ["TCC","VL","GT","TA"]
  domains    = { TCC:7, VL:7, GT:7, TA:6 }
```

### MRV lần 4

```
TCC=7, VL=7, GT=7, TA=6
→ min=6: TA → chọn "TA"
```

### LCV cho TA

next_unassigned = ["TCC","VL","GT"]

| Nhóm | Xung đột với | conflict_count |
|------|-------------|---------------|
| TA5 (T5 S1) | TCC7(T5 S1) | **1** |
| TA2 (T3 S3) | VL4, GT4 ← sẽ bị skip PersonalEvent | **2** |
| TA4 (T4 S3) | TCC6, VL6 (T4 S3) | **2** |
| TA6 (T5 S2) | VL7, GT6 (T5 S2) | **2** |
| TA1 (T2 S1) | TCC1, VL1, GT1 (T2 S1) | **3** |
| TA3 (T4 S1) | TCC5, VL5, GT5 (T4 S1) | **3** |

**Thứ tự LCV:** TA5 → TA2 → TA4 → TA6 → TA1 → TA3

---

### 6.4 Thử TA5 (Thứ5 S1 = 07:00-09:00)

```
4a: Thứ5 ≠ Thứ3 → OK
4b: ("TA5","LP6")? T5 S1 07:00-09:00 vs T5 S3 13:00-15:00
      09:00 ≤ 13:00 → không giao giờ → OK
    ("TA5","CS4")? khác thứ → OK
    ("TA5","MM1")? khác thứ → OK
4c: chosen["TA"] = TA5
    _forward_check(TA5, ["TCC","VL","GT"], ...)
```

**FC với TA5 (T5 S1):**

```
Xét TCC:
  TCC7(T5 S1): ("TA5","TCC7") IN conflict_set → ✅ → xóa TCC7
  domains["TCC"] = [TCC1,TCC2,TCC3,TCC4,TCC5,TCC6]  len=6 → OK

Xét VL: không có VL nào ở T5 S1 → removed["VL"]=[]
Xét GT: không có GT nào ở T5 S1 → removed["GT"]=[]

→ return (True, removed={TCC:[TCC7], VL:[], GT:[]})
```

---

```
CALL #5
  chosen     = {LP:LP6, CS:CS4, MM:MM1, TA:TA5}
  unassigned = ["TCC","VL","GT"]
  domains    = { TCC:6, VL:7, GT:7 }
```

### MRV lần 5

```
TCC=6, VL=7, GT=7
→ min=6: TCC → chọn "TCC"
```

### LCV cho TCC

TCC candidates (TCC7 đã bị xóa): [TCC1,TCC2,TCC3,TCC4,TCC5,TCC6]
next_unassigned = ["VL","GT"]

| Nhóm | Xung đột với | conflict_count |
|------|-------------|---------------|
| TCC2 (T2 S3) | không có VL/GT cùng T2 S3 | **0** |
| TCC4 (T3 S2) | không có VL/GT cùng T3 S2 | **0** |
| TCC6 (T4 S3) | VL6(T4 S3) | **1** |
| TCC1 (T2 S1) | VL1, GT1 (T2 S1) | **2** |
| TCC3 (T3 S1) | VL3, GT3 (T3 S1) | **2** |
| TCC5 (T4 S1) | VL5, GT5 (T4 S1) | **2** |

**Thứ tự LCV:** TCC2 → TCC4 → TCC6 → TCC1 → TCC3 → TCC5

---

### 6.5 Thử TCC2 (Thứ2 S3 = 13:00-15:00)

```
4a: Thứ2 ≠ Thứ3 → OK
4b: ("TCC2","LP6")? T2 S3 vs T5 S3 → khác thứ → OK
    ("TCC2","CS4")? T2 S3 vs T4 S2 → khác thứ → OK
    ("TCC2","MM1")? T2 S3 13:00-15:00 vs T2 S4 15:30-17:30
      15:00 ≤ 15:30 → không giao giờ → OK
    ("TCC2","TA5")? T2 S3 vs T5 S1 → khác thứ → OK
4c: chosen["TCC"] = TCC2
    _forward_check(TCC2, ["VL","GT"], ...)
```

**FC với TCC2 (T2 S3):**

```
Xét VL:
  TCC2 T2 S3 — từ conflict_set: TCC2↔CS2. Không có VL cùng T2 S3 → removed["VL"]=[]
Xét GT:
  GT1=T2S1, GT2=T2S2, không có GT cùng T2 S3 → removed["GT"]=[]

→ return (True, removed={VL:[], GT:[]})
```

---

```
CALL #6
  chosen     = {LP:LP6, CS:CS4, MM:MM1, TA:TA5, TCC:TCC2}
  unassigned = ["VL","GT"]
  domains    = { VL:7, GT:7 }
```

### MRV lần 6

```
VL=7, GT=7 → tie → chọn "VL" (đầu tiên trong list)
```

### LCV cho VL

next_unassigned = ["GT"]

| Nhóm | Xung đột với GT | conflict_count |
|------|----------------|---------------|
| VL6 (T4 S3) | không có GT cùng T4 S3 | **0** |
| VL1 (T2 S1) | GT1(T2 S1) | **1** |
| VL2 (T2 S2) | GT2(T2 S2) | **1** |
| VL3 (T3 S1) | GT3(T3 S1) | **1** |
| VL4 (T3 S3) | GT4(T3 S3) | **1** |
| VL5 (T4 S1) | GT5(T4 S1) | **1** |
| VL7 (T5 S2) | GT6(T5 S2) | **1** |

**Thứ tự LCV:** VL6 → VL1 → VL2 → VL3 → VL4 → VL5 → VL7

---

### 6.6 Thử VL6 (Thứ4 S3 = 13:00-15:00)

```
4a: Thứ4 ≠ Thứ3 → OK
4b: ("VL6","LP6")? T4 S3 vs T5 S3 → khác thứ → OK
    ("VL6","CS4")? T4 S3 13:00-15:00 vs T4 S2 09:30-11:30
      13:00 ≥ 11:30 → không giao giờ → OK
    ("VL6","MM1")? khác thứ → OK
    ("VL6","TA5")? khác thứ → OK
    ("VL6","TCC2")? T4 S3 vs T2 S3 → khác thứ → OK
4c: chosen["VL"] = VL6
    _forward_check(VL6, ["GT"], ...)
```

**FC với VL6 (T4 S3):**

```
Xét GT:
  GT1..GT7: không có GT nào cùng T4 S3 → removed["GT"]=[]

→ return (True, removed={GT:[]})
```

---

```
CALL #7
  chosen     = {LP:LP6, CS:CS4, MM:MM1, TA:TA5, TCC:TCC2, VL:VL6}
  unassigned = ["GT"]
  domains    = { GT:7 }
```

### MRV lần 7 — Môn cuối cùng

```
→ chọn "GT" (duy nhất)
```

**LCV cho GT (next_unassigned = []):**
Không còn môn nào để đếm xung đột → tất cả conflict_count = 0.
Giữ nguyên thứ tự domain: [GT1, GT2, GT3, GT4, GT5, GT6, GT7]

---

**Thử GT1 (Thứ2 S1 = 07:00-09:00):**

```
4a: Thứ2 ≠ Thứ3 → OK
4b: Kiểm tra GT1 với toàn bộ chosen:
    ("GT1","LP6")? T2 S1 vs T5 S3 → khác thứ → OK
    ("GT1","CS4")? T2 S1 vs T4 S2 → khác thứ → OK
    ("GT1","MM1")? T2 S1 07:00-09:00 vs T2 S4 15:30-17:30
      09:00 ≤ 15:30 → không giao giờ → OK
    ("GT1","TA5")? T2 S1 vs T5 S1 → khác thứ → OK
    ("GT1","TCC2")? T2 S1 07:00-09:00 vs T2 S3 13:00-15:00
      09:00 ≤ 13:00 → không giao giờ → OK
    ("GT1","VL6")? T2 S1 vs T4 S3 → khác thứ → OK
    → tất cả OK
4c: chosen["GT"] = GT1, FC(GT1, [], ...) → (True, {})
```

---

```
CALL #8 — BASE CASE
  unassigned = []
  chosen = {LP:LP6, CS:CS4, MM:MM1, TA:TA5, TCC:TCC2, VL:VL6, GT:GT1}
```

```
✅ NGHIỆM 1 tìm được:
{
  TCC: TCC2  (Thứ2 S3),
  VL : VL6   (Thứ4 S3),
  LP : LP6   (Thứ5 S3),
  CS : CS4   (Thứ4 S2),
  MM : MM1   (Thứ2 S4),
  GT : GT1   (Thứ2 S1),
  TA : TA5   (Thứ5 S1),
}
```

---

## 7. Restore theo chiều ngược — quay lại tìm thêm nghiệm

Sau khi lưu Nghiệm 1, backtracking **restore** và tiếp tục thử GT còn lại trong CALL #7:

```
CALL #7: GT domain = [GT1,GT2,GT3,GT4,GT5,GT6,GT7]  (next_unassigned=[] → giữ nguyên)

Thử GT2 (T2 S2):
  4a: Thứ2 ≠ Thứ3 → OK
  4b: kiểm tra tất cả chosen → không có xung đột → OK
  → ✅ NGHIỆM 2: GT=GT2

Thử GT3 (T3 S1):
  4a: Thứ3 S1 07:00-09:00, Event T3 12:00-14:00
      07:00 < 14:00 ✓ nhưng 12:00 < 09:00? FALSE → KHÔNG xung đột → OK
  → ✅ NGHIỆM 3: GT=GT3

Thử GT4 (T3 S3):
  4a: T3 S3 = 13:00-15:00, Event T3 12:00-14:00
      13:00 < 14:00 ✓ và 12:00 < 15:00 ✓ → XUNG ĐỘT PersonalEvent → SKIP

Thử GT5 (T4 S1):
  4b: ("GT5","CS4")? T4 S1 07:00-09:00 vs T4 S2 09:30-11:30
      09:00 ≤ 09:30 → không giao giờ → OK (strict <)
      ("GT5","VL6")? T4 S1 vs T4 S3 → S1 07:00-09:00, S3 13:00-15:00 → OK
  → ✅ NGHIỆM 4: GT=GT5

Thử GT6 (T5 S2):
  4b: ("GT6","LP6")? T5 S2 09:30-11:30 vs T5 S3 13:00-15:00
      11:30 ≤ 13:00 → không giao giờ → OK
      ("GT6","TA5")? T5 S2 09:30-11:30 vs T5 S1 07:00-09:00
      09:30 ≥ 09:00 → không giao giờ → OK
  → ✅ NGHIỆM 5: GT=GT6
```

**Đủ max_solutions=5 → dừng toàn bộ cây đệ quy.**

---

## 8. Tổng kết các trường hợp đã bao phủ

### TH1 — avoid_days lọc sơ bộ

```
TCC8, VL8, LP7, CS7, MM7, GT8, TA7 bị loại trước khi backtracking bắt đầu.
→ 7 nhóm lớp không bao giờ được thử.
```

### TH2 — personal_events lọc trong vòng lặp

```
LP3 (Thứ3 S3 = 13:00-15:00) — SKIP khi thử cho LP (CALL #1)
GT4 (Thứ3 S3 = 13:00-15:00) — SKIP khi thử cho GT (CALL #7, Step 7)
TA2 (Thứ3 S3 = 13:00-15:00) — nếu được thử cho TA, sẽ SKIP ở 4a
→ Kiểm tra xảy ra ở 4a, trước khi gán và chạy FC → không tốn chi phí FC
```

### TH3 — LCV giảm nhánh thử đầu tiên

```
CALL #1 thử LP:
  Không dùng LCV → thử LP1 đầu tiên, LP1 xung đột VL2 và GT2 → FC thu hẹp domain
  Dùng LCV → thử LP6 đầu tiên (conflict_count=0) → FC không thu hẹp domain nào
  → LP6 giữ nguyên tất cả domain → không cắt mất lựa chọn của các môn khác

CALL #6 thử VL:
  VL6 có conflict_count=0 với GT → thử VL6 trước
  → FC không thu hẹp GT → GT vẫn 7 lựa chọn → tìm được 5 nghiệm liên tiếp nhanh hơn
```

### TH4 — FC phát hiện dead-end sớm

```
CALL #4 (TA=TA5): FC xóa TCC7 khỏi domain TCC
  domains["TCC"] = 7 → 6 → OK (không dead-end)

Ví dụ dead-end: nếu TCC chỉ còn TCC7 trước bước này:
  domains["TCC"] = [] → DEAD-END
  → return (False, removed) ngay lập tức
  → không đi sâu vào VL, GT
  → tiết kiệm toàn bộ nhánh con
```

### TH5 — MRV chọn đúng môn bị ràng buộc nhất

```
Sau CALL #4 (FC của TA5 xóa TCC7):
  domains = { TCC:6, VL:7, GT:7 }
  → TCC=6 nhỏ nhất → chọn TCC trước
  → Nếu chọn VL hay GT (=7) trước, sẽ đi sâu 7 nhánh trước khi biết
    TCC bị mất một lựa chọn
```

### TH6 — Restore domain chính xác

```
Sau CALL #7 (GT1→GT6, tìm đủ 5 nghiệm), khi backtrack lên CALL #6 để thử VL1:
  _restore_domains({"GT":[]}, domains)    ← FC của VL6 không xóa gì
  → Đúng — domain GT không bị thay đổi sai
  → Tiếp tục thử VL1 với GT đầy đủ 7 lựa chọn (nếu chưa đủ max_solutions)
```

### TH7 — Điều kiện biên end_time == start_time

```
GT1 : 07:00–09:00   (T2 S1)
TCC2: 13:00–15:00   (T2 S3)
MM1 : 15:30–17:30   (T2 S4)

Giữa TCC2 và MM1:
  TCC2.end(15:00) < MM1.start(15:30) → không giao → đúng (strict <)
  Nếu là 15:00–15:00 (touch): TCC2.end == MM1.start → không giao → đúng SRS 6.1.1
```

### TH8 — Conflict_set đối xứng phát huy tác dụng

```
CALL #4 (TA=TA5): bước 4b kiểm tra TCC7↔TA5 từ conflict_set
  Trong conflict_set có cả (TCC7,TA5) lẫn (TA5,TCC7)
  → Dù môn nào được gán trước, lookup luôn thành công
```

---

## 9. Kết quả cuối cùng

```python
valid_schedules = [
  {TCC:TCC2, VL:VL6, LP:LP6, CS:CS4, MM:MM1, GT:GT1, TA:TA5},  # nghiệm 1
  {TCC:TCC2, VL:VL6, LP:LP6, CS:CS4, MM:MM1, GT:GT2, TA:TA5},  # nghiệm 2
  {TCC:TCC2, VL:VL6, LP:LP6, CS:CS4, MM:MM1, GT:GT3, TA:TA5},  # nghiệm 3
  {TCC:TCC2, VL:VL6, LP:LP6, CS:CS4, MM:MM1, GT:GT5, TA:TA5},  # nghiệm 4 (GT4 bị skip)
  {TCC:TCC2, VL:VL6, LP:LP6, CS:CS4, MM:MM1, GT:GT6, TA:TA5},  # nghiệm 5
]
→ dừng vì đủ max_solutions=5
→ Tầng 3 nhận 5 nghiệm này, tính Score(S), trả top 3
```

**Lịch nghiệm 1 kiểm chứng:**

| Thứ | Ca học |
|-----|--------|
| Thứ2 | GT1(S1 07:00) · TCC2(S3 13:00) · MM1(S4 15:30) |
| Thứ4 | CS4(S2 09:30) · VL6(S3 13:00) |
| Thứ5 | TA5(S1 07:00) · LP6(S3 13:00) |

Không trùng slot, không trùng avoid_days, không trùng PersonalEvent ✓

---

## 10. Sơ đồ cây đệ quy (rút gọn)

```
root
└── LP=LP6  [LCV=0, FC: không thay đổi domain]
    └── CS=CS4  [LCV=0, FC: không thay đổi domain]
        └── MM=MM1  [LCV=0, FC: không thay đổi domain]
            └── TA=TA5  [LCV=1, FC: xóa TCC7]
                └── TCC=TCC2  [LCV=0, FC: không thay đổi domain]
                    └── VL=VL6  [LCV=0, FC: không thay đổi domain]
                        ├── GT=GT1 ✅ NGHIỆM 1
                        ├── GT=GT2 ✅ NGHIỆM 2
                        ├── GT=GT3 ✅ NGHIỆM 3
                        ├── GT=GT4 ✗ (PersonalEvent T3 S3)
                        ├── GT=GT5 ✅ NGHIỆM 4
                        └── GT=GT6 ✅ NGHIỆM 5 → DỪNG
                    ├── VL=VL1 → ... (nếu còn chỗ)
                    └── ...
                ├── TCC=TCC4 → ...
                └── ...
            ├── TA=TA2 ✗ (PersonalEvent T3 S3)  [sẽ bị skip ở 4a]
            ├── TA=TA4 → ...
            └── ...
        ├── MM=MM3 → ...
        └── ...
    ├── CS=CS6 → ...
    └── ...
├── LP=LP2 → ...
└── ...

✗ = bị lọc bởi PersonalEvent (bước 4a)
LCV=n = conflict_count khi được chọn thử
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
