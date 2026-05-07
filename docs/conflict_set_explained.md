# Giải thích cơ chế conflict_set trong thuật toán backtracking

## 1. Conflict_set là gì?

`conflict_set` là một **tập tra cứu tĩnh** được tính một lần trước khi backtracking chạy.
Nó lưu tất cả các cặp `(class_id_A, class_id_B)` mà hai nhóm lớp đó **không thể xuất hiện
cùng nhau** trong một thời khóa biểu hợp lệ.

```
conflict_set: set[tuple[str, str]]

Ví dụ: { ("T1", "L1"), ("L1", "T1"), ("T1", "H2"), ("H2", "T1") }
```

Trong backtracking, mỗi khi thử gán một nhóm lớp mới, chỉ cần một phép tra cứu O(1):

```python
if (cls_mới.class_id, cls_đã_chọn.class_id) in conflict_set:
    bỏ qua, thử nhóm khác
```

---

## 2. Dữ liệu ví dụ

| Tên | class_id | Thứ | Giờ bắt đầu | Giờ kết thúc |
|-----|----------|-----|-------------|--------------|
| Toán Nhóm 1 | T1 | Thứ 2 | 07:00 | 09:00 |
| Toán Nhóm 2 | T2 | Thứ 3 | 07:00 | 09:00 |
| Lý Nhóm 1 | L1 | Thứ 2 | 08:00 | 10:00 |
| Lý Nhóm 2 | L2 | Thứ 4 | 07:00 | 09:00 |

**Điều kiện xung đột (SRS 6.1.1):**

```
conflict(A, B) ⟺
    A.day_of_week == B.day_of_week
    AND A.start_time < B.end_time
    AND B.start_time < A.end_time
```

> Điều kiện biên: `A.end_time == B.start_time` → **KHÔNG xung đột** (dùng strict `<`).

---

## 3. Bước 1 — build_conflict_set duyệt tất cả cặp

```
i=0 (T1) vs j=1 (T2): Thứ 2 ≠ Thứ 3           → không xung đột
i=0 (T1) vs j=2 (L1): Thứ 2 = Thứ 2
                        07:00 < 10:00 ✓
                        08:00 < 09:00 ✓          → XUNG ĐỘT
i=0 (T1) vs j=3 (L2): Thứ 2 ≠ Thứ 4           → không xung đột
i=1 (T2) vs j=2 (L1): Thứ 3 ≠ Thứ 2           → không xung đột
i=1 (T2) vs j=3 (L2): Thứ 3 ≠ Thứ 4           → không xung đột
i=2 (L1) vs j=3 (L2): Thứ 2 ≠ Thứ 4           → không xung đột
```

Kết quả: chỉ có cặp **(T1, L1)** xung đột. Lưu vào set **cả hai chiều**:

```python
conflict_set = {
    ("T1", "L1"),  # chiều xuôi
    ("L1", "T1"),  # chiều ngược
}
```

---

## 4. Bước 2 — Backtracking chạy

MRV (Minimum Remaining Values) chọn môn có ít lựa chọn hợp lệ nhất để gán trước.
Thứ tự này **thay đổi động** theo từng trạng thái của bài toán — đây là lý do
phải lưu đối xứng.

### Kịch bản A: MRV chọn Lý trước

```
Bước 1 — gán Lý → L1
    chosen = { "Lý": L1 }

Bước 2 — thử Toán → T1
    kiểm tra: ("T1", "L1") IN conflict_set → ✅ có → bỏ T1

Bước 2 — thử Toán → T2
    kiểm tra: ("T2", "L1") IN conflict_set → ❌ không có → chấp nhận

    chosen = { "Lý": L1, "Toán": T2 }  ✅ Hợp lệ
```

### Kịch bản B: MRV chọn Toán trước

```
Bước 1 — gán Toán → T1
    chosen = { "Toán": T1 }

Bước 2 — thử Lý → L1
    kiểm tra: ("L1", "T1") IN conflict_set → ✅ có → bỏ L1

Bước 2 — thử Lý → L2
    kiểm tra: ("L2", "T1") IN conflict_set → ❌ không có → chấp nhận

    chosen = { "Toán": T1, "Lý": L2 }  ✅ Hợp lệ
```

---

## 5. Điều gì xảy ra nếu chỉ lưu một chiều?

Giả sử chỉ lưu `("T1", "L1")`, bỏ `("L1", "T1")`:

### Kịch bản A: MRV chọn Lý trước (vẫn đúng — may mắn)

```
Bước 2 — thử Toán → T1
    kiểm tra: ("T1", "L1") IN conflict_set → ✅ có → bỏ T1  ← bắt được
```

### Kịch bản B: MRV chọn Toán trước (sai — bỏ sót)

```
Bước 2 — thử Lý → L1
    kiểm tra: ("L1", "T1") IN conflict_set → ❌ KHÔNG CÓ → chấp nhận

    chosen = { "Toán": T1, "Lý": L1 }  ❌ XUNG ĐỘT lọt qua!
```

**Kết quả:** thuật toán trả về TKB sai mà không có lỗi nào được báo.

---

## 6. Tổng kết

```
Lưu 1 chiều  →  phụ thuộc thứ tự MRV  →  kết quả không nhất quán
Lưu 2 chiều  →  độc lập thứ tự MRV    →  luôn đúng, O(1) mỗi lookup
```

| | Lưu 1 chiều | Lưu 2 chiều |
|---|---|---|
| Kịch bản A (Lý trước) | ✅ Đúng | ✅ Đúng |
| Kịch bản B (Toán trước) | ❌ Bỏ sót | ✅ Đúng |
| Chi phí bộ nhớ | n cặp | 2n cặp |
| Lookup | O(1) | O(1) |

Chi phí bộ nhớ tăng gấp đôi nhưng hoàn toàn chấp nhận được — với n ≤ 40 nhóm,
số cặp tối đa là `C(40,2) × 2 = 1.560` phần tử trong set.
