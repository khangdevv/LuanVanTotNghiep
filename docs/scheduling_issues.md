# Các vấn đề hiện tại của thuật toán xếp thời khóa biểu

Tài liệu này ghi lại các vấn đề đang tồn tại khi dùng dữ liệu từ
`schedule_data_from_web.json` cho thuật toán CSP hiện tại, cùng hướng xử lý đề
xuất cho các bước phát triển tiếp theo.

---

## 1. Demo đang bỏ mất nhiều dòng lịch của cùng một nhóm lớp

### Hiện trạng

Trong loader của `demo/main.py`, mỗi cặp `(ma_mh, nhom_to)` chỉ được tạo thành
một `ClassSection` duy nhất từ dòng JSON đầu tiên. Các dòng sau của cùng nhóm bị
bỏ qua.

### Vấn đề

Dữ liệu JSON thực tế không phải mỗi nhóm chỉ có một dòng lịch. Một nhóm có thể có
nhiều dòng vì:

- học cùng thứ/tiết nhưng chia thành nhiều khoảng ngày khác nhau;
- có thay đổi số tiết hoặc tiết bắt đầu theo từng giai đoạn;
- một số học phần có nhiều buổi học thành phần.

Nếu chỉ lấy dòng đầu tiên, thuật toán sẽ thiếu dữ liệu lịch học thật của nhóm.

### Hướng giải quyết

Loader cần gom dữ liệu theo `(ma_mh, nhom_to)`, nhưng không bỏ các dòng lịch.
Mỗi nhóm lớp nên có danh sách các buổi học/khoảng học tương ứng.

---

## 2. `ClassSection` hiện đang đại diện cho một buổi học

### Hiện trạng

Model `ClassSection` hiện có trực tiếp các trường:

- `day_of_week`
- `start_time`
- `end_time`
- `room`
- `instructor`

Điều này khiến một nhóm lớp bị hiểu như chỉ có một lịch học cố định.

### Vấn đề

Trong dữ liệu thật, một nhóm lớp có thể có nhiều lịch học. Vì vậy nếu nhét trực
tiếp thông tin thời gian vào `ClassSection`, model sẽ không biểu diễn đúng dữ
liệu.

### Hướng giải quyết

Nên tách:

- `ClassSection`: đại diện cho một nhóm lớp, ví dụ `CS03042_01`;
- `ClassMeeting` hoặc `ClassSession`: đại diện cho một dòng lịch học cụ thể của
  nhóm đó.

Một `ClassSection` sẽ có nhiều `ClassMeeting`.

---

## 3. Kiểm tra xung đột chưa xét khoảng ngày học

### Hiện trạng

Logic xung đột hiện chỉ xét:

```text
cùng thứ
+ trùng khoảng giờ
```

### Vấn đề

Hai nhóm có thể trùng thứ và trùng tiết, nhưng nếu khoảng ngày học không giao
nhau thì thực tế không xung đột.

Ví dụ:

- Lớp A học Thứ 2, tiết 1-3, từ 01/01/26 đến 31/01/26.
- Lớp B học Thứ 2, tiết 1-3, từ 01/03/26 đến 31/03/26.

Hai lớp này trùng lịch tuần, nhưng không học cùng giai đoạn nên có thể cùng tồn
tại trong một thời khóa biểu.

### Hướng giải quyết

Xung đột nên được xác định theo đủ 3 điều kiện:

```text
same day
+ time overlap
+ date range overlap
```

Nếu thiếu ngày bắt đầu/kết thúc thì có thể dùng fallback bảo thủ: xem như có
giao ngày để tránh sinh lịch sai.

---

## 4. `avoid_days`, `PersonalEvent` và scoring đang dựa vào lịch đại diện

### Hiện trạng

Các phần sau đang dùng trực tiếp thông tin trên `ClassSection`:

- lọc ngày tránh trong CSP;
- kiểm tra trùng với lịch cá nhân;
- tính điểm khoảng nghỉ;
- tính điểm khớp sở thích sáng/chiều;
- tính điểm cân bằng workload.

### Vấn đề

Nếu `ClassSection` chỉ chứa một dòng lịch đại diện, các phép tính trên có thể
sai khi nhóm lớp có nhiều dòng lịch.

Ví dụ một nhóm có dòng đầu học Thứ 2 nhưng dòng sau học Thứ 6. Nếu sinh viên
muốn tránh Thứ 6, thuật toán có thể vẫn giữ nhóm đó vì chỉ nhìn dòng đầu.

### Hướng giải quyết

Các logic này cần duyệt toàn bộ `ClassMeeting` của mỗi `ClassSection`:

- `avoid_days`: loại nhóm nếu bất kỳ meeting nào rơi vào ngày cần tránh;
- `PersonalEvent`: kiểm tra từng meeting với lịch cá nhân;
- scoring: tính trên các meeting thật, có xét khoảng ngày nếu cần.

---

## 5. Quan hệ dữ liệu giữa semester, class và schedule chưa đủ rõ

### Hiện trạng

Các model hiện đã có `Semester`, `ClassSection`, `Schedule`, `ScheduleClass`,
nhưng quan hệ nghiệp vụ chưa được thể hiện rõ trong thuật toán và loader demo.

### Vấn đề

Nếu không tách rõ các tầng dữ liệu, backend và thuật toán dễ bị lẫn giữa:

- môn học;
- nhóm lớp;
- từng buổi học của nhóm;
- thời khóa biểu được sinh ra;
- các nhóm lớp được chọn trong một thời khóa biểu.

Điều này làm cho việc lưu DB, kiểm tra xung đột và hiển thị lịch đều dễ sai.

### Hướng giải quyết

Mô hình đề xuất:

```text
Semester 1 - N ClassSection
Course   1 - N ClassSection
ClassSection 1 - N ClassMeeting
Student  1 - N Schedule
Schedule N - N ClassSection thông qua ScheduleClass
```

Ý nghĩa:

- `Semester`: học kỳ, có ngày bắt đầu/kết thúc tổng quát.
- `Course`: môn học.
- `ClassSection`: nhóm lớp của một môn trong một học kỳ.
- `ClassMeeting`: từng dòng lịch học thật của nhóm lớp.
- `Schedule`: một phương án thời khóa biểu cho sinh viên.
- `ScheduleClass`: bảng trung gian lưu các nhóm lớp được chọn trong schedule.

---

## Hướng triển khai đề xuất

### Bước 1: Chuẩn hóa model

Thêm model `ClassMeeting` hoặc `ClassSession` với các trường:

- `day_of_week`
- `start_time`
- `end_time`
- `room`
- `instructor`
- `start_date`
- `end_date`
- `date_text` nếu muốn giữ chuỗi gốc từ JSON để debug/hiển thị

`ClassSection` giữ thông tin nhóm lớp và chứa danh sách meetings.

### Bước 2: Sửa loader JSON

Loader cần:

- đọc toàn bộ `schedule_data_from_web.json`;
- gom theo `(ma_mh, nhom_to)`;
- mỗi dòng hợp lệ tạo một `ClassMeeting`;
- mỗi nhóm tạo một `ClassSection` chứa danh sách meetings.

Các dòng thiếu `thu`, `tiet_bat_dau`, `so_tiet` hoặc có `so_tiet = 0` cần được
xử lý riêng vì đó có thể là học phần thực tập/đồ án không có lịch tuần cố định.

### Bước 3: Sửa logic conflict

Hai `ClassSection` xung đột nếu tồn tại ít nhất một cặp meeting thỏa:

```text
meeting_a.day_of_week == meeting_b.day_of_week
meeting_a.start_time < meeting_b.end_time
meeting_b.start_time < meeting_a.end_time
meeting_a.start_date <= meeting_b.end_date
meeting_b.start_date <= meeting_a.end_date
```

### Bước 4: Sửa CSP và scoring

CSP vẫn nên chọn một `ClassSection` cho mỗi môn. Tuy nhiên mọi ràng buộc liên
quan đến thời gian phải xét trên danh sách meetings của section đó.

Các phần cần cập nhật:

- lọc `avoid_days`;
- kiểm tra `PersonalEvent`;
- tạo `conflict_set`;
- tính điểm khoảng nghỉ;
- tính điểm sở thích ca học;
- tính điểm cân bằng workload.

### Bước 5: Bổ sung test

Cần có test cho các trường hợp:

- cùng thứ/giờ nhưng khác khoảng ngày thì không xung đột;
- cùng thứ/giờ và giao khoảng ngày thì xung đột;
- một nhóm có nhiều meeting và một meeting rơi vào `avoid_days` thì nhóm bị loại;
- `PersonalEvent` chặn đúng khi trùng với bất kỳ meeting nào;
- loader không làm mất các dòng lịch cùng `(ma_mh, nhom_to)`.

---

## Kết luận

Vấn đề chính hiện tại không nằm ở backtracking/MRV/forward checking, mà nằm ở mô
hình dữ liệu đầu vào cho thuật toán. Thuật toán đang chọn nhóm lớp đúng về mặt
ý tưởng, nhưng mỗi nhóm lớp chưa chứa đầy đủ các buổi học thật từ JSON.

Do đó, hướng sửa nên ưu tiên chuẩn hóa dữ liệu `ClassSection -> ClassMeeting`
trước. Sau khi dữ liệu đầu vào đúng, các bước conflict, lọc constraint và scoring
sẽ có cơ sở để cho kết quả thời khóa biểu chính xác hơn.
