Smart Schedule – SRS v1.0	*Theo chuẩn IEEE 830-1998*

**TRƯỜNG ĐẠI HỌC CÔNG NGHỆ SÀI GÒN**

KHOA CÔNG NGHỆ THÔNG TIN

**ĐẶC TẢ YÊU CẦU PHẦN MỀM**

*(Software Requirements Specification)*

*Theo chuẩn IEEE 830-1998*

**SMART SCHEDULE**

Hệ Thống Tối Ưu Thời Khóa Biểu Cá Nhân

| **Phiên bản** | 1.0 |
| --- | --- |
| **Ngày tạo** | 01/06/2025 |
| **Trạng thái** | Bản thảo hoàn chỉnh |
| **Môn học** | Đồ án tốt nghiệp |

# LỊCH SỬ THAY ĐỔI TÀI LIỆU

| **Phiên bản** | **Ngày** | **Tác giả** | **Mô tả thay đổi** |
| --- | --- | --- | --- |
| 1.0 | 01/06/2025 | Nhóm sinh viên | Tạo tài liệu ban đầu – phiên bản hoàn chỉnh |

	LỊCH SỬ THAY ĐỔI TÀI LIỆU	2

	CHƯƠNG 1: GIỚI THIỆU	6

	1.1 Mục đích tài liệu	6

	1.2 Phạm vi hệ thống	6

	1.3 Định nghĩa, từ viết tắt và thuật ngữ	6

	1.4 Tài liệu tham khảo	7

	1.5 Tổng quan tài liệu	7

	CHƯƠNG 2: MÔ TẢ TỔNG QUAN HỆ THỐNG	8

	2.1 Bối cảnh và hiện trạng vấn đề	8

	2.2 Chức năng tổng quát của hệ thống	8

	2.3 Đặc điểm người dùng	8

	2.4 Ràng buộc triển khai	8

	2.5 Giả định và phụ thuộc	8

	CHƯƠNG 3: YÊU CẦU CHỨC NĂNG	10

	3.1 Danh sách Use Case tổng hợp	10

	3.2 Đặc tả chi tiết Use Case	10

	UC-01: Đăng ký tài khoản	10

	UC-02: Đăng nhập / Đăng xuất	10

	UC-03: Nhập dữ liệu môn học và nhóm lớp	11

	UC-04: Thiết lập sở thích lịch học	11

	UC-05: Quản lý lịch bận cá nhân	12

	UC-06: Phát hiện xung đột lịch	12

	UC-07: Sinh và xếp hạng phương án TKB	12

	UC-08: Xem, so sánh và lưu phương án TKB	13

	UC-09: Hiển thị TKB dạng calendar tuần	13

	UC-10: Tạo lịch tự học tự động	14

	CHƯƠNG 4: YÊU CẦU PHI CHỨC NĂNG	15

	4.1 Yêu cầu hiệu năng (NFR-01)	15

	4.2 Yêu cầu bảo mật (NFR-02)	15

	4.3 Yêu cầu giao diện người dùng (NFR-03)	15

	4.4 Yêu cầu độ tin cậy (NFR-04)	15

	4.5 Yêu cầu bảo trì (NFR-05)	16

	CHƯƠNG 5: THIẾT KẾ CƠ SỞ DỮ LIỆU	17

	5.1 Tổng quan lược đồ	17

	5.2 Mô tả chi tiết các bảng	17

	5.2.1 Bảng Semesters (Học kỳ) – Bảng mới so với SRS gốc	17

	5.2.2 Bảng Students (Sinh viên)	17

	5.2.3 Bảng Courses (Môn học)	17

	5.2.4 Bảng Classes (Nhóm lớp mở theo học kỳ)	18

	5.2.5 Bảng Preferences (Sở thích lịch học)	18

	5.2.6 Bảng PreferenceAvoidDays (Ngày muốn tránh)	19

	5.2.7 Bảng PersonalEvents (Lịch bận cá nhân)	19

	5.2.8 Bảng Schedules (Phương án thời khóa biểu)	19

	5.2.9 Bảng ScheduleClasses (Lớp trong phương án)	20

	5.3 Ràng buộc toàn vẹn dữ liệu bổ sung	20

	CHƯƠNG 6: THIẾT KẾ THUẬT TOÁN	21

	6.1 Thuật toán phát hiện xung đột	21

	6.1.1 Định nghĩa chính thức	21

	6.1.2 Giải thích tại sao dùng thuật toán O(n²) đơn giản	21

	6.1.3 Mã giả (Pseudocode)	21

	6.2 Hàm đánh giá Score(S)	21

	6.2.1 Công thức tổng hợp	21

	6.2.2 Thành phần F_break – Chất lượng khoảng nghỉ	21

	6.2.3 Thành phần F_pref – Độ khớp sở thích	21

	6.2.4 Thành phần F_balance – Cân bằng khối lượng	22

	6.2.5 Ví dụ tính Score minh họa	22

	6.3 Thuật toán sinh tổ hợp TKB	22

	6.3.1 Tại sao chọn thuật toán backtracking đơn giản	22

	6.3.2 Mã giả	22

	6.4 Thiết kế API (REST)	22

	CHƯƠNG 7: KẾ HOẠCH THỰC HIỆN 3 THÁNG (12 TUẦN)	24

	7.1 Phân chia giai đoạn	24

	7.2 Kế hoạch chi tiết theo tuần	24

	7.3 Phân công vai trò nhóm (gợi ý cho nhóm 3–4 người)	25

	7.4 Ngưỡng rủi ro và phương án dự phòng	25

	CHƯƠNG 8: KẾ HOẠCH KIỂM THỬ	26

	8.1 Kiểm thử đơn vị (Unit Test) – Thuật toán xung đột	26

	8.2 Kiểm thử đơn vị – Hàm điểm Score(S)	26

	8.3 Kiểm thử tích hợp (Integration Test)	26

	KẾT LUẬN TÀI LIỆU	28

	PHỤ LỤC A: ROADMAP CHI TIẾT 12 TUẦN	29

	A.1 Các milestone chính (M1–M4)	29

	PHỤ LỤC A: ROADMAP CHI TIẾT 12 TUẦN	30

	A.1 Các milestone chính (M1–M4)	30

	A.2 Bản đồ phụ thuộc giữa các tuần	30

	A.3 Lịch làm việc theo ngày và Definition of Done	31

	A.3.1 Phase 1 – Nền tảng (Tuần 1–3)	31

	Tuần 1 – Khởi tạo môi trường và quy ước nhóm	31

	Tuần 2 – Lược đồ CSDL và migration	31

	Tuần 3 – Xác thực (UC-01, UC-02) — kết thúc Phase 1	32

	A.3.2 Phase 2 – Lõi hệ thống (Tuần 4–8)	33

	Tuần 4 – Nhập dữ liệu, sở thích, lịch bận (UC-03, UC-04, UC-05)	33

	Tuần 5 – Thuật toán phát hiện xung đột (UC-06)	33

	Tuần 6 – Sinh tổ hợp TKB bằng backtracking (UC-07 phần 1)	34

	Tuần 7 – Hàm Score(S) và xếp hạng (UC-07 phần 2)	35

	Tuần 8 – Calendar UI và lưu phương án (UC-08, UC-09) — kết thúc Phase 2	35

	A.3.3 Phase 3 – Hoàn thiện (Tuần 9–11)	36

	Tuần 9 – Lịch tự học (UC-10)	36

	Tuần 10 – Kiểm thử tích hợp end-to-end	36

	Tuần 11 – Sửa lỗi, load test, tài liệu — kết thúc Phase 3	37

	A.3.4 Phase 4 – Nghiệm thu (Tuần 12)	37

	Tuần 12 – Deploy, báo cáo, bảo vệ	37

	A.4 Quỹ thời gian dự phòng (Buffer)	38

	A.5 Chỉ số theo dõi tiến độ (KPI)	38

# CHƯƠNG 1: GIỚI THIỆU

## 1.1 Mục đích tài liệu

Tài liệu này là Đặc tả Yêu cầu Phần mềm (Software Requirements Specification – SRS) cho hệ thống Smart Schedule, được soạn thảo theo chuẩn IEEE 830-1998. Tài liệu mô tả đầy đủ các yêu cầu chức năng, phi chức năng, ràng buộc thiết kế và phạm vi triển khai của hệ thống, phục vụ làm căn cứ cho quá trình thiết kế, cài đặt, kiểm thử và nghiệm thu.

Tài liệu hướng đến các đối tượng đọc sau: (1) nhóm sinh viên phát triển hệ thống, (2) giảng viên hướng dẫn và hội đồng phản biện, (3) người dùng cuối (sinh viên đại học).

## 1.2 Phạm vi hệ thống

Smart Schedule là ứng dụng web hỗ trợ sinh viên đại học tự động tạo thời khóa biểu học tập cá nhân theo học kỳ. Hệ thống thực hiện ba chức năng cốt lõi:

- Phát hiện xung đột lịch học giữa các lớp học phần đã chọn.

- Tự động sinh và xếp hạng các phương án thời khóa biểu theo hàm điểm đa tiêu chí.

- Gợi ý khung giờ tự học xen kẽ vào thời khóa biểu chính thức.

Hệ thống không bao gồm: tích hợp API với cổng học vụ nhà trường, tính năng nhắc nhở qua email/push notification, ứng dụng mobile native, và hỗ trợ đa trường đại học.

## 1.3 Định nghĩa, từ viết tắt và thuật ngữ

| **Thuật ngữ / Viết tắt** | **Định nghĩa** |
| --- | --- |
| SRS | Software Requirements Specification – Đặc tả yêu cầu phần mềm |
| FR | Functional Requirement – Yêu cầu chức năng |
| NFR | Non-Functional Requirement – Yêu cầu phi chức năng |
| UC | Use Case – Trường hợp sử dụng |
| TKB | Thời khóa biểu |
| MSSV | Mã số sinh viên |
| JWT | JSON Web Token – Token xác thực người dùng |
| REST | Representational State Transfer – Kiến trúc API web |
| ORM | Object-Relational Mapping – Ánh xạ đối tượng-quan hệ |
| 3NF | Third Normal Form – Dạng chuẩn ba trong thiết kế CSDL |
| Score(S) | Hàm điểm tổng hợp đánh giá chất lượng phương án TKB |
| CSP | Constraint Satisfaction Problem – Bài toán thỏa mãn ràng buộc |
| Conflict | Xung đột lịch: hai lớp học cùng ngày, giao nhau về thời gian |
| Slot | Khung giờ học: (day_of_week, start_time, end_time) |

## 1.4 Tài liệu tham khảo

- IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications.

- Rossi, F. et al. (2006). Handbook of Constraint Programming. Elsevier.

- Chen, T. & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. KDD 2016.

- Sommerville, I. (2016). Software Engineering, 10th Edition. Pearson.

- PostgreSQL 14 Documentation. https://www.postgresql.org/docs/14/

## 1.5 Tổng quan tài liệu

Phần còn lại của tài liệu được tổ chức như sau: Chương 2 mô tả tổng quan hệ thống. Chương 3 đặc tả chi tiết tất cả yêu cầu chức năng. Chương 4 đặc tả yêu cầu phi chức năng. Chương 5 mô tả thiết kế cơ sở dữ liệu. Chương 6 mô tả thiết kế thuật toán. Chương 7 trình bày kế hoạch thực hiện 3 tháng.

# CHƯƠNG 2: MÔ TẢ TỔNG QUAN HỆ THỐNG

## 2.1 Bối cảnh và hiện trạng vấn đề

Trong môi trường đại học, mỗi học kỳ sinh viên phải tự lựa chọn và ghép lịch từ nhiều nhóm lớp của các môn học khác nhau. Khi đăng ký từ 4–7 môn, mỗi môn có 2–5 nhóm lớp mở, số tổ hợp cần xét có thể lên đến hàng trăm, thậm chí hàng nghìn. Sinh viên hiện thực hiện thủ công, tốn 1–3 giờ mỗi học kỳ và vẫn dễ bỏ sót xung đột.

Các công cụ phổ biến như Google Calendar và Microsoft Excel không có khả năng phát hiện xung đột tự động hay đề xuất phương án tối ưu. Khoảng trống này là động lực để phát triển Smart Schedule.

## 2.2 Chức năng tổng quát của hệ thống

Smart Schedule cung cấp bốn nhóm chức năng chính:

- Quản lý tài khoản: đăng ký, đăng nhập, xác thực bằng JWT.

- Quản lý dữ liệu học tập: nhập môn học, nhóm lớp, thiết lập sở thích cá nhân và lịch bận.

- Tối ưu thời khóa biểu: phát hiện xung đột, sinh tổ hợp, xếp hạng và hiển thị top 3 phương án.

- Lịch tự học: gợi ý khung giờ tự học xen kẽ vào thời khóa biểu đã chọn.

## 2.3 Đặc điểm người dùng

| **Thuộc tính** | **Mô tả** |
| --- | --- |
| Đối tượng | Sinh viên đại học hệ chính quy |
| Trình độ kỹ thuật | Người dùng phổ thông – không cần kiến thức lập trình |
| Thiết bị sử dụng | Máy tính bàn, laptop; hỗ trợ thêm tablet và điện thoại |
| Tần suất sử dụng | Tập trung vào đầu mỗi học kỳ (khoảng 2 lần/năm) |
| Kỳ vọng | Nhận kết quả thời khóa biểu tối ưu trong dưới 5 giây |

## 2.4 Ràng buộc triển khai

- Hệ thống triển khai dưới dạng ứng dụng web, không cần cài đặt phần mềm phía client.

- Thời gian phát triển: 3 tháng (12 tuần), thực hiện bởi nhóm 3–4 sinh viên.

- Công nghệ frontend: React.js. Backend: Python FastAPI. CSDL: PostgreSQL.

- Môi trường triển khai phát triển: localhost; môi trường demo: máy chủ VPS hoặc cloud free-tier.

- Dữ liệu lịch mở lớp được nhập thủ công qua giao diện quản trị hoặc import file CSV – không có tích hợp API trường trong phạm vi đề tài này.

## 2.5 Giả định và phụ thuộc

- Giả định: Mỗi lớp học phần chỉ có một khung giờ cố định trong tuần (không phân chia ca). Lịch học không thay đổi trong suốt học kỳ.

- Phụ thuộc: Trình duyệt hiện đại (Chrome ≥ 90, Firefox ≥ 88, Edge ≥ 90) hỗ trợ ES6+ và CSS Grid. Kết nối Internet ổn định ≥ 1 Mbps.

# CHƯƠNG 3: YÊU CẦU CHỨC NĂNG

## 3.1 Danh sách Use Case tổng hợp

| **Mã UC** | **Tên Use Case** | **Actor** | **Ưu tiên** |
| --- | --- | --- | --- |
| UC-01 | Đăng ký tài khoản | Sinh viên | Cao |
| UC-02 | Đăng nhập / Đăng xuất | Sinh viên | Cao |
| UC-03 | Nhập dữ liệu môn học và nhóm lớp | Sinh viên / Admin | Cao |
| UC-04 | Thiết lập sở thích lịch học | Sinh viên | Cao |
| UC-05 | Quản lý lịch bận cá nhân | Sinh viên | Trung bình |
| UC-06 | Phát hiện xung đột lịch | Hệ thống | Cao |
| UC-07 | Sinh và xếp hạng phương án TKB | Hệ thống | Cao |
| UC-08 | Xem, so sánh và lưu phương án TKB | Sinh viên | Cao |
| UC-09 | Hiển thị TKB dạng calendar tuần | Sinh viên | Cao |
| UC-10 | Tạo lịch tự học tự động | Hệ thống | Thấp |

## 3.2 Đặc tả chi tiết Use Case

### UC-01: Đăng ký tài khoản

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-01 |
| Tên | Đăng ký tài khoản |
| Actor | Sinh viên (chưa có tài khoản) |
| Điều kiện tiên quyết | Người dùng chưa đăng nhập; có kết nối Internet |
| Kịch bản chính | 1. Người dùng truy cập trang đăng ký. 2. Nhập: MSSV, Họ tên, Email đại học, Mật khẩu (≥8 ký tự, có chữ hoa và số). 3. Hệ thống kiểm tra: MSSV đúng định dạng, Email chưa tồn tại, mật khẩu đủ mạnh. 4. Hệ thống mã hóa mật khẩu bằng bcrypt (salt=10), lưu vào DB. 5. Hiển thị thông báo "Đăng ký thành công", chuyển hướng đến trang đăng nhập. |
| Kịch bản thay thế | A1 – Email đã tồn tại: hiển thị lỗi "Email này đã được đăng ký". A2 – Mật khẩu quá yếu: hiển thị gợi ý về độ mạnh mật khẩu. A3 – MSSV sai định dạng: hiển thị lỗi định dạng. |
| Kết quả | Tài khoản mới được tạo; người dùng có thể đăng nhập. |
| Yêu cầu liên quan | NFR-02 (Bảo mật) |

### UC-02: Đăng nhập / Đăng xuất

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-02 |
| Actor | Sinh viên |
| Điều kiện tiên quyết | Tài khoản đã tồn tại trong hệ thống |
| Kịch bản chính (Đăng nhập) | 1. Người dùng nhập Email và Mật khẩu. 2. Hệ thống xác thực: so sánh mật khẩu với hash bcrypt. 3. Nếu hợp lệ: phát hành JWT token (TTL = 24h), lưu vào localStorage. 4. Chuyển hướng về trang Dashboard. |
| Kịch bản thay thế | A1 – Sai mật khẩu ≥ 5 lần: khóa tài khoản 15 phút. A2 – Đăng xuất: xóa JWT khỏi localStorage, chuyển về trang đăng nhập. |
| Kết quả | Người dùng được xác thực; JWT token hợp lệ lưu phía client. |

### UC-03: Nhập dữ liệu môn học và nhóm lớp

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-03 |
| Actor | Sinh viên (chọn môn); Admin (nhập lịch mở lớp) |
| Mô tả | Phân thành 2 luồng: (A) Admin nhập danh mục môn học và lịch mở lớp vào hệ thống; (B) Sinh viên chọn các môn cần xếp lịch trong học kỳ hiện tại. |
| Kịch bản A – Admin | 1. Admin đăng nhập trang quản trị (route /admin). 2. Tạo môn học: nhập Mã môn, Tên môn, Số tín chỉ. 3. Tạo nhóm lớp: gán môn, nhập Thứ, Giờ bắt đầu, Giờ kết thúc, Phòng, Sĩ số tối đa. 4. Hệ thống lưu và hiển thị danh sách lớp đã nhập. |
| Kịch bản B – Sinh viên | 1. Sinh viên vào trang "Chọn môn học". 2. Chọn học kỳ hiện tại. 3. Tích chọn các môn cần đăng ký (tối đa 8 môn). 4. Hệ thống hiển thị tất cả nhóm lớp mở của các môn đã chọn. 5. Sinh viên xác nhận → lưu danh sách vào bảng Enrollments. |
| Kết quả | Dữ liệu đầu vào sẵn sàng cho UC-06 và UC-07. |

### UC-04: Thiết lập sở thích lịch học

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-04 |
| Actor | Sinh viên |
| Điều kiện tiên quyết | Đã đăng nhập |
| Kịch bản chính | 1. Sinh viên vào trang "Cài đặt sở thích". 2. Chọn khung giờ ưa thích: Sáng (06:00–11:30) / Chiều (12:00–17:30) / Tối (17:30–21:00). 3. Đánh dấu các ngày muốn tránh học (checkbox T2–CN). 4. Nhập thời gian nghỉ tối thiểu giữa 2 buổi liên tiếp (mặc định: 15 phút). 5. Nhấn "Lưu" → hệ thống cập nhật bảng Preferences. |
| Kết quả | Sở thích được lưu; được dùng trong hàm tính điểm Score(S). |

### UC-05: Quản lý lịch bận cá nhân

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-05 |
| Mô tả | Sinh viên thêm, sửa, xóa các sự kiện bận cá nhân (làm thêm, câu lạc bộ, v.v.) để hệ thống tránh xếp lịch tự học vào các khung giờ này. |
| Kịch bản chính | 1. Sinh viên nhấn "Thêm sự kiện". 2. Nhập: Tên sự kiện, Thứ (hoặc ngày cụ thể), Giờ bắt đầu, Giờ kết thúc, Lặp lại hàng tuần (toggle). 3. Nhấn "Lưu" → ghi vào bảng PersonalEvents. 4. Sự kiện hiển thị trên calendar dưới dạng ô màu xám. |
| Kết quả | Lịch bận được lưu; thuật toán UC-10 tránh các khung giờ này. |

### UC-06: Phát hiện xung đột lịch

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-06 |
| Actor | Hệ thống (kích hoạt tự động sau UC-03) |
| Điều kiện tiên quyết | Sinh viên đã chọn ít nhất 2 môn học |
| Kịch bản chính | 1. Hệ thống lấy tất cả nhóm lớp của các môn đã chọn. 2. Với mỗi cặp (A, B): kiểm tra điều kiện xung đột. 3. Nếu phát hiện xung đột: ghi nhận cặp (classA_id, classB_id) vào danh sách conflicts. 4. Hiển thị danh sách xung đột kèm tên môn, thứ, giờ bị trùng. 5. Các nhóm lớp xung đột bị loại khỏi quá trình sinh tổ hợp (UC-07). |
| Điều kiện xung đột | Hai lớp A và B xung đột khi và chỉ khi:   (A.day_of_week = B.day_of_week)   AND (A.start_time < B.end_time)   AND (B.start_time < A.end_time) |
| Lưu ý về điều kiện biên | Trường hợp A.end_time = B.start_time KHÔNG được tính là xung đột (lớp A kết thúc đúng lúc lớp B bắt đầu là hợp lệ). |
| Độ phức tạp | O(n²) với n là tổng số nhóm lớp. Với n ≤ 50 (thực tế), thời gian < 1ms. |
| Kết quả | Danh sách conflict hiển thị; input cho UC-07 chỉ gồm các nhóm không xung đột. |

### UC-07: Sinh và xếp hạng phương án TKB

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-07 |
| Actor | Hệ thống |
| Điều kiện tiên quyết | UC-06 đã chạy; sinh viên đã thiết lập sở thích (UC-04) |
| Kịch bản chính | 1. Hệ thống liệt kê các nhóm lớp hợp lệ cho từng môn. 2. Sinh tất cả tổ hợp (chọn 1 nhóm/môn) không có xung đột nội bộ. 3. Với mỗi tổ hợp hợp lệ: tính Score(S) theo công thức ở mục 6.2. 4. Sắp xếp giảm dần theo Score(S). 5. Lưu top 3 phương án vào bảng Schedules. 6. Trả về 3 phương án kèm điểm chi tiết từng thành phần. |
| Ràng buộc hiệu năng | Hoàn thành trong ≤ 3 giây với ≤ 7 môn, mỗi môn ≤ 5 nhóm (tổng hợp lệ ≤ 5^7 = 78.125 – thực tế sau lọc xung đột còn dưới 1.000). |
| Kết quả | Top 3 phương án TKB được lưu và sẵn sàng hiển thị ở UC-08. |

### UC-08: Xem, so sánh và lưu phương án TKB

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-08 |
| Actor | Sinh viên |
| Kịch bản chính | 1. Hiển thị 3 tab (Phương án 1, 2, 3), mỗi tab có điểm tổng và điểm thành phần. 2. Sinh viên chuyển tab để so sánh trực quan trên calendar. 3. Sinh viên chọn "Áp dụng phương án này" → cập nhật is_selected = TRUE trong DB. 4. Hệ thống xác nhận và chuyển sang màn hình calendar chính. |
| Kết quả | Một phương án được đánh dấu is_selected; dùng làm input cho UC-10. |

### UC-09: Hiển thị TKB dạng calendar tuần

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-09 |
| Actor | Sinh viên |
| Mô tả | Hiển thị thời khóa biểu đã chọn dạng lưới 7 cột (T2–CN) × các khung giờ theo trục dọc. Mỗi môn học được tô một màu riêng biệt. Sự kiện bận cá nhân hiển thị màu xám. Lịch tự học (nếu có) hiển thị màu khác với đường viền nét đứt. |
| Tương tác | Hover vào ô lịch: hiển thị tooltip (tên môn, phòng, giảng viên nếu có). Click vào ô lịch tự học: mở modal cho phép xác nhận hoặc xóa buổi tự học đó. |
| Kết quả | Sinh viên có cái nhìn trực quan toàn bộ lịch tuần. |

### UC-10: Tạo lịch tự học tự động

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-10 |
| Ưu tiên | Thấp – triển khai nếu còn thời gian (Phase 3) |
| Actor | Hệ thống |
| Điều kiện tiên quyết | Sinh viên đã chọn phương án TKB (UC-08) |
| Kịch bản chính | 1. Với mỗi môn trong TKB đã chọn, đọc thời lượng tự học mong muốn (mặc định: 60 phút/môn). 2. Tìm khung giờ trống: không trùng với lịch học chính và không trùng PersonalEvents. 3. Ưu tiên xếp buổi tự học trong vòng 24 giờ sau buổi học chính của môn đó. 4. Ghi các buổi tự học vào bảng StudySessions. 5. Hiển thị tích hợp vào calendar (UC-09). |
| Kết quả | Danh sách buổi tự học được gợi ý và hiển thị trên lịch. |

# CHƯƠNG 4: YÊU CẦU PHI CHỨC NĂNG

## 4.1 Yêu cầu hiệu năng (NFR-01)

| **Mã** | **Chỉ tiêu** | **Giá trị mục tiêu** | **Phương pháp kiểm thử** |
| --- | --- | --- | --- |
| NFR-01.1 | Thời gian phản hồi API thông thường | ≤ 500ms (P95) | Dùng Locust hoặc k6 với 50 user đồng thời |
| NFR-01.2 | Thời gian sinh TKB (UC-07) | ≤ 3 giây với 7 môn × 5 nhóm | Unit test với input chuẩn |
| NFR-01.3 | Số người dùng đồng thời | ≥ 50 (mục tiêu tối thiểu) | Load test với Locust |
| NFR-01.4 | Thời gian tải trang chính | ≤ 3 giây trên kết nối 4G | Chrome DevTools Lighthouse |

*Lưu ý: Giá trị 50 người dùng đồng thời là mục tiêu thực tế khả thi trong 3 tháng. Nâng lên 100+ là hướng phát triển tương lai.*

## 4.2 Yêu cầu bảo mật (NFR-02)

| **Mã** | **Yêu cầu** | **Chi tiết kỹ thuật** |
| --- | --- | --- |
| NFR-02.1 | Mã hóa mật khẩu | bcrypt với cost factor = 10. Không bao giờ lưu plain-text. |
| NFR-02.2 | Truyền thông an toàn | HTTPS bắt buộc (TLS 1.2+). Redirect HTTP → HTTPS. |
| NFR-02.3 | Xác thực JWT | Token TTL = 24h. Payload chứa student_id và role. Ký bằng HS256. |
| NFR-02.4 | Chống SQL Injection | Dùng ORM (SQLAlchemy) với parameterized queries. Không dùng raw SQL string nối trực tiếp. |
| NFR-02.5 | Chống XSS | Escape toàn bộ output HTML. Dùng thư viện DOMPurify phía client. |
| NFR-02.6 | CORS | Chỉ cho phép origin của frontend đã cấu hình. |

## 4.3 Yêu cầu giao diện người dùng (NFR-03)

- Responsive design: hoạt động đúng trên màn hình ≥ 768px (tablet) và ≥ 1024px (desktop). Mobile là optional.

- Calendar grid: 7 cột (T2–CN), trục dọc hiển thị từng khung 30 phút từ 06:00 đến 21:00.

- Phân biệt màu sắc: mỗi môn học được gán 1 màu từ bảng màu cố định (tối thiểu 8 màu dễ phân biệt).

- Accessibility: văn bản có độ tương phản ≥ 4.5:1 theo WCAG 2.1 AA.

## 4.4 Yêu cầu độ tin cậy (NFR-04)

- Hệ thống xử lý đúng các trường hợp biên: sinh viên chọn 1 môn duy nhất, tất cả lớp bị xung đột, không có khung giờ trống cho tự học.

- Dữ liệu không bị mất khi trình duyệt reload (lưu phương án đã chọn vào DB, không chỉ lưu state phía client).

## 4.5 Yêu cầu bảo trì (NFR-05)

- Mã nguồn backend tổ chức theo cấu trúc: /routers, /services, /models, /schemas.

- Mã nguồn frontend tổ chức theo: /components, /pages, /hooks, /api.

- Mỗi hàm logic phức tạp (thuật toán phát hiện xung đột, tính điểm) phải có unit test riêng.

- README.md mô tả đầy đủ cách cài đặt và chạy dự án trong môi trường local.

# CHƯƠNG 5: THIẾT KẾ CƠ SỞ DỮ LIỆU

## 5.1 Tổng quan lược đồ

Cơ sở dữ liệu gồm 9 bảng quan hệ, thiết kế theo dạng chuẩn hóa 3NF. Sơ đồ ERD (Entity-Relationship Diagram) mô tả các bảng và quan hệ khóa ngoại.

*Ghi chú ERD: Đường liền = quan hệ bắt buộc (NOT NULL FK); Đường đứt = tùy chọn (NULL FK).*

## 5.2 Mô tả chi tiết các bảng

### 5.2.1 Bảng Semesters (Học kỳ) – Bảng mới so với SRS gốc

Bảng này giải quyết vấn đề thiếu thực thể "học kỳ" trong thiết kế gốc.

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| semester_id | VARCHAR(10) | PRIMARY KEY | Mã học kỳ, ví dụ: "20241" = HK1 năm 2024-2025 |
| name | VARCHAR(50) | NOT NULL | Tên học kỳ, ví dụ: "Học kỳ 1 – 2024/2025" |
| start_date | DATE | NOT NULL | Ngày bắt đầu học kỳ |
| end_date | DATE | NOT NULL, > start_date | Ngày kết thúc học kỳ |
| is_active | BOOLEAN | DEFAULT FALSE | TRUE = học kỳ hiện tại đang diễn ra |

### 5.2.2 Bảng Students (Sinh viên)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| student_id | VARCHAR(20) | PRIMARY KEY | Mã số sinh viên (MSSV) |
| name | VARCHAR(100) | NOT NULL | Họ và tên đầy đủ |
| email | VARCHAR(150) | UNIQUE, NOT NULL | Email đại học |
| password_hash | VARCHAR(255) | NOT NULL | Mật khẩu sau băm bcrypt |
| role | ENUM | ('student','admin'), DEFAULT 'student' | Phân quyền người dùng |
| created_at | TIMESTAMP | DEFAULT NOW() | Thời điểm tạo tài khoản |

### 5.2.3 Bảng Courses (Môn học)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| course_id | VARCHAR(20) | PRIMARY KEY | Mã môn học |
| course_name | VARCHAR(200) | NOT NULL | Tên môn học |
| credits | SMALLINT | NOT NULL, CHECK (credits > 0) | Số tín chỉ |
| department | VARCHAR(100) | NULL | Khoa/Bộ môn phụ trách (tùy chọn) |

### 5.2.4 Bảng Classes (Nhóm lớp mở theo học kỳ)

Bảng này thêm khóa ngoại semester_id để liên kết với học kỳ – khắc phục thiếu sót của SRS gốc.

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| class_id | VARCHAR(20) | PRIMARY KEY | Mã nhóm lớp |
| course_id | VARCHAR(20) | FK → Courses, NOT NULL | Môn học tương ứng |
| semester_id | VARCHAR(10) | FK → Semesters, NOT NULL | Học kỳ mở lớp |
| day_of_week | SMALLINT | NOT NULL, CHECK (2..8) | Thứ (2=T2, 8=CN) |
| start_time | TIME | NOT NULL | Giờ bắt đầu |
| end_time | TIME | NOT NULL, > start_time | Giờ kết thúc |
| room | VARCHAR(50) | NULL | Phòng học |
| instructor | VARCHAR(100) | NULL | Giảng viên (tùy chọn) |
| max_students | SMALLINT | NOT NULL, > 0 | Sĩ số tối đa |

### 5.2.5 Bảng Preferences (Sở thích lịch học)

Lưu ý: avoid_days được tách thành bảng riêng PreferenceAvoidDays để tuân thủ 1NF.

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| pref_id | SERIAL | PRIMARY KEY | Mã bản ghi |
| student_id | VARCHAR(20) | FK → Students, UNIQUE | Mỗi sinh viên có 1 bản ghi sở thích |
| preferred_slot | ENUM | ('morning','afternoon','evening') | Khung giờ ưa thích |
| min_break_minutes | SMALLINT | DEFAULT 15, CHECK (≥ 0) | Nghỉ tối thiểu giữa 2 buổi (phút) |
| w_break | DECIMAL(3,2) | DEFAULT 0.40 | Trọng số thành phần khoảng nghỉ |
| w_preference | DECIMAL(3,2) | DEFAULT 0.30 | Trọng số thành phần sở thích |
| w_balance | DECIMAL(3,2) | DEFAULT 0.30 | Trọng số thành phần cân bằng |

### 5.2.6 Bảng PreferenceAvoidDays (Ngày muốn tránh)

Tách từ Preferences để đảm bảo 1NF – khắc phục lỗi thiết kế của SRS gốc (avoid_days VARCHAR).

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| pref_id | INT | FK → Preferences | Khóa ngoại |
| day_of_week | SMALLINT | CHECK (2..8) | Thứ muốn tránh |
|  |  | PRIMARY KEY (pref_id, day_of_week) | Khóa chính tổng hợp |

### 5.2.7 Bảng PersonalEvents (Lịch bận cá nhân)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| event_id | SERIAL | PRIMARY KEY | Mã sự kiện |
| student_id | VARCHAR(20) | FK → Students | Sinh viên sở hữu |
| title | VARCHAR(200) | NOT NULL | Tên sự kiện |
| day_of_week | SMALLINT | CHECK (2..8) | Thứ lặp lại (NULL nếu one-time) |
| start_time | TIME | NOT NULL | Giờ bắt đầu |
| end_time | TIME | NOT NULL, > start_time | Giờ kết thúc |
| is_recurring | BOOLEAN | DEFAULT FALSE | TRUE = lặp hàng tuần |
| note | TEXT | NULL | Ghi chú tùy chọn |

### 5.2.8 Bảng Schedules (Phương án thời khóa biểu)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| schedule_id | SERIAL | PRIMARY KEY | Mã phương án |
| student_id | VARCHAR(20) | FK → Students | Sinh viên sở hữu |
| semester_id | VARCHAR(10) | FK → Semesters | Học kỳ áp dụng |
| score_total | DECIMAL(5,4) | NOT NULL | Điểm tổng [0.0000–1.0000] |
| score_break | DECIMAL(5,4) | NOT NULL | Điểm thành phần khoảng nghỉ |
| score_pref | DECIMAL(5,4) | NOT NULL | Điểm thành phần sở thích |
| score_balance | DECIMAL(5,4) | NOT NULL | Điểm thành phần cân bằng |
| is_selected | BOOLEAN | DEFAULT FALSE | Sinh viên đã chọn phương án này |
| created_at | TIMESTAMP | DEFAULT NOW() | Thời điểm sinh phương án |

### 5.2.9 Bảng ScheduleClasses (Lớp trong phương án)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| schedule_id | INT | FK → Schedules | Phương án chứa lớp này |
| class_id | VARCHAR(20) | FK → Classes | Nhóm lớp được chọn |
|  |  | PRIMARY KEY (schedule_id, class_id) | Khóa chính tổng hợp |

## 5.3 Ràng buộc toàn vẹn dữ liệu bổ sung

- CHECK: Tổng ba trọng số w_break + w_preference + w_balance = 1.0 (thực thi bằng trigger hoặc validation tầng service).

- CHECK: end_time > start_time trong Classes và PersonalEvents.

- INDEX: Tạo index trên (semester_id, course_id) trong Classes để tăng tốc truy vấn lọc.

- CONSTRAINT: Mỗi sinh viên chỉ có 1 bản ghi is_selected = TRUE cho mỗi học kỳ (partial unique index).

# CHƯƠNG 6: THIẾT KẾ THUẬT TOÁN

## 6.1 Thuật toán phát hiện xung đột

### 6.1.1 Định nghĩa chính thức

Hai nhóm lớp A và B xung đột nếu và chỉ nếu thoả mãn đồng thời ba điều kiện:

**conflict(A, B) ≡  (A.day = B.day)  ∧  (A.start ****<**** B.end)  ∧  (B.start ****<**** A.end)**

Điều kiện biên quan trọng: Nếu A.end = B.start (lớp A kết thúc đúng lúc lớp B bắt đầu), biểu thức A.start < B.end = TRUE nhưng B.start < A.end = FALSE, vì vậy KHÔNG xung đột. Điều này đảm bảo lịch học liên tiếp không bị đánh dấu sai là xung đột.

### 6.1.2 Giải thích tại sao dùng thuật toán O(n²) đơn giản

Trong phạm vi đề tài, số nhóm lớp tối đa là 8 môn × 5 nhóm = 40 nhóm. Số cặp cần kiểm tra là C(40,2) = 780 phép so sánh – hoàn thành dưới 1ms. Thuật toán O(n log n) (Sweep Line) chỉ cần thiết khi n > 10.000. Sử dụng O(n²) ở đây là hợp lý, dễ cài đặt và dễ kiểm thử.

### 6.1.3 Mã giả (Pseudocode)

| **Mã giả thuật toán detect_conflicts(classes: List[Class]) → List[Pair]** |
| --- |
| conflicts = [] FOR i = 0 TO len(classes) - 2:     FOR j = i+1 TO len(classes) - 1:         A = classes[i]         B = classes[j]         IF A.day == B.day            AND A.start < B.end            AND B.start < A.end:             conflicts.append((A, B)) RETURN conflicts |

## 6.2 Hàm đánh giá Score(S)

### 6.2.1 Công thức tổng hợp

**Score(S) = w₁ × F_break(S) + w₂ × F_pref(S) + w₃ × F_balance(S)**

Trong đó: w₁ + w₂ + w₃ = 1.0; mặc định w₁ = 0.4, w₂ = 0.3, w₃ = 0.3

Mỗi thành phần F ∈ [0.0, 1.0]. Score(S) ∈ [0.0, 1.0]. Phương án tốt hơn có Score cao hơn.

### 6.2.2 Thành phần F_break – Chất lượng khoảng nghỉ

Đo lường mức độ phù hợp của khoảng nghỉ giữa các buổi học trong ngày so với ngưỡng nghỉ tối thiểu min_break của sinh viên.

Với mỗi ngày d có ít nhất 2 buổi học, sắp xếp các buổi theo giờ tăng dần, tính gap_i = start_{i+1} − end_i (đơn vị: phút).

f_break_d = mean( min(gap_i / (2 × min_break), 1.0)  for all gap_i )

F_break(S) = mean( f_break_d  for all d with ≥ 2 sessions )

*Nếu không có ngày nào có ≥ 2 buổi: F_break(S) = 1.0 (điểm tối đa, không bị phạt).*

### 6.2.3 Thành phần F_pref – Độ khớp sở thích

Đo lường mức độ khớp giữa lịch học và sở thích cá nhân (khung giờ ưa thích + ngày muốn tránh).

match_i = 1 nếu buổi học i thuộc khung giờ ưa thích VÀ không học vào ngày avoid; ngược lại = 0.

F_pref(S) = (số buổi match) / (tổng số buổi học trong tuần)

### 6.2.4 Thành phần F_balance – Cân bằng khối lượng

Đo lường mức độ phân bổ đều số buổi học trong tuần, tránh tình trạng dồn nhiều buổi vào một ngày.

n_d = số buổi học trong ngày d (chỉ tính các ngày từ T2 đến CN có ít nhất 1 buổi học)

σ = độ lệch chuẩn của {n_d}; n_max = max(n_d)

F_balance(S) = 1 − (σ / n_max)   [nếu n_max > 0; nếu chỉ 1 ngày học thì = 0.5]

### 6.2.5 Ví dụ tính Score minh họa

| **Phương án** | **F_break** | **F_pref** | **F_balance** | **Score (w=0.4/0.3/0.3)** |
| --- | --- | --- | --- | --- |
| PA-1 | 0.85 | 0.90 | 0.70 | 0.4×0.85 + 0.3×0.90 + 0.3×0.70 = 0.820 |
| PA-2 | 0.60 | 0.80 | 0.95 | 0.4×0.60 + 0.3×0.80 + 0.3×0.95 = 0.765 |
| PA-3 | 0.70 | 0.50 | 0.80 | 0.4×0.70 + 0.3×0.50 + 0.3×0.80 = 0.670 |

## 6.3 Thuật toán sinh tổ hợp TKB

### 6.3.1 Tại sao chọn thuật toán backtracking đơn giản

Kiến trúc Hybrid (OR-Tools + GA + XGBoost) đề xuất trong SRS gốc phức tạp vượt mức cần thiết cho 3 tháng triển khai. Phân tích thực tế: 7 môn × 5 nhóm = 78.125 tổ hợp tối đa. Sau lọc xung đột, thực tế còn dưới 500 tổ hợp hợp lệ. Tính điểm mỗi tổ hợp: ~0.01ms. Tổng: < 5ms. Thuật toán backtracking đơn giản hoàn toàn đủ và đáp ứng NFR-01.2 (≤ 3 giây). Kiến trúc phức tạp (XGBoost surrogate) sẽ là hướng phát triển tương lai khi quy mô tăng lên 20+ môn.

### 6.3.2 Mã giả

| **Mã giả generate_schedules(course_groups: Dict, conflicts: Set) → List[Schedule]** |
| --- |
| valid_schedules = [] courses = list(course_groups.keys())   # Danh sách môn học  DEF backtrack(idx, chosen_classes):     IF idx == len(courses):         valid_schedules.append(chosen_classes.copy())         RETURN     course = courses[idx]     FOR cls IN course_groups[course]:         # Kiểm tra cls không xung đột với bất kỳ lớp đã chọn         has_conflict = ANY conflict(cls, c) for c in chosen_classes                        where (cls.id, c.id) in conflicts_set         IF NOT has_conflict:             chosen_classes.append(cls)             backtrack(idx + 1, chosen_classes)             chosen_classes.pop()  backtrack(0, []) RETURN top_3_by_score(valid_schedules) |

## 6.4 Thiết kế API (REST)

| **Method** | **Endpoint** | **Mô tả** | **Auth** |
| --- | --- | --- | --- |
| POST | /api/auth/register | Đăng ký tài khoản mới | Public |
| POST | /api/auth/login | Đăng nhập, nhận JWT | Public |
| GET | /api/courses?semester_id= | Lấy danh sách môn theo học kỳ | JWT |
| GET | /api/courses/{id}/classes | Lấy nhóm lớp của 1 môn | JWT |
| POST | /api/enrollments | Lưu danh sách môn đã chọn | JWT |
| GET/PUT | /api/preferences | Xem / Cập nhật sở thích cá nhân | JWT |
| GET/POST/DELETE | /api/personal-events | Quản lý lịch bận cá nhân | JWT |
| POST | /api/schedules/generate | Kích hoạt sinh TKB, trả về top 3 | JWT |
| GET | /api/schedules?semester_id= | Lấy danh sách phương án đã sinh | JWT |
| PUT | /api/schedules/{id}/select | Chọn phương án TKB | JWT |
| POST | /api/study-sessions/generate | Sinh lịch tự học (UC-10) | JWT |

# CHƯƠNG 7: KẾ HOẠCH THỰC HIỆN 3 THÁNG (12 TUẦN)

## 7.1 Phân chia giai đoạn

| **Giai đoạn** | **Thời gian** | **Mục tiêu đầu ra chính** |
| --- | --- | --- |
| Phase 1: Nền tảng | Tuần 1–3 | Môi trường dev, CSDL, xác thực, quản lý dữ liệu môn học |
| Phase 2: Lõi hệ thống | Tuần 4–8 | Thuật toán xung đột + sinh TKB + hàm điểm + calendar UI |
| Phase 3: Hoàn thiện | Tuần 9–11 | Lịch tự học, kiểm thử toàn diện, sửa lỗi |
| Phase 4: Nghiệm thu | Tuần 12 | Deploy demo, hoàn thiện tài liệu, chuẩn bị bảo vệ |

## 7.2 Kế hoạch chi tiết theo tuần

| **Tuần** | **Nội dung công việc** | **Deliverable kiểm tra được** |
| --- | --- | --- |
| 1 | Cài đặt môi trường: Docker, PostgreSQL, FastAPI, React. Tạo repo GitHub. Phân công vai trò. | README cài đặt, repo có cấu trúc thư mục, DB chạy được |
| 2 | Cài đặt tất cả bảng CSDL (9 bảng). Viết migration script (Alembic). Seed dữ liệu test. | Script migration chạy thành công, dữ liệu seed có thể query |
| 3 | Triển khai UC-01, UC-02: Đăng ký, đăng nhập, JWT middleware. API /auth/*. | Postman test pass: đăng ký → đăng nhập → nhận token |
| 4 | Triển khai UC-03B, UC-04, UC-05: API chọn môn, sở thích, lịch bận. | API GET/POST /enrollments, /preferences, /personal-events pass test |
| 5 | Triển khai UC-06: Thuật toán phát hiện xung đột. Unit test đầy đủ (≥ 10 test case). | Unit test pass 100%; API /conflicts trả về đúng danh sách xung đột |
| 6 | Triển khai UC-07 (phần 1): Thuật toán backtracking sinh tổ hợp hợp lệ. | API generate trả về danh sách tổ hợp không xung đột |
| 7 | Triển khai UC-07 (phần 2): Hàm tính Score(S) theo 3 thành phần. Unit test hàm điểm. | Unit test hàm điểm pass; top 3 phương án được trả về đúng thứ tự |
| 8 | Triển khai UC-08, UC-09: Calendar UI (React), chọn phương án, hiển thị TKB. | UI hiển thị lịch tuần đúng màu sắc; chọn phương án lưu được vào DB |
| 9 | Triển khai UC-10: Thuật toán gợi ý lịch tự học. Tích hợp vào calendar. | Lịch tự học hiển thị trên calendar, không trùng lịch học và lịch bận |
| 10 | Kiểm thử tích hợp end-to-end: Thực hiện 5 luồng test từ đăng ký đến xem TKB. | Test report; ≥ 90% test case pass |
| 11 | Sửa lỗi, tối ưu UX, load test (Locust), viết tài liệu API. | Load test 50 user pass; API doc hoàn chỉnh |
| 12 | Deploy lên VPS/cloud (Render.com hoặc Railway free-tier). Hoàn thiện báo cáo, slide. | URL demo hoạt động; báo cáo + slide sẵn sàng |

## 7.3 Phân công vai trò nhóm (gợi ý cho nhóm 3–4 người)

| **Vai trò** | **Trách nhiệm chính** | **Phase tập trung** |
| --- | --- | --- |
| Backend Developer 1 | CSDL, Auth, API môn học / sở thích | Phase 1–2 |
| Backend Developer 2 | Thuật toán xung đột, sinh TKB, hàm điểm | Phase 2 |
| Frontend Developer | React UI, Calendar component, tích hợp API | Phase 2–3 |
| Full-stack / Tích hợp | UC-10 lịch tự học, kiểm thử, deploy, tài liệu | Phase 3–4 |

## 7.4 Ngưỡng rủi ro và phương án dự phòng

| **Rủi ro** | **Xác suất** | **Phương án xử lý** |
| --- | --- | --- |
| Thuật toán backtracking chậm với dữ liệu lớn | Thấp | Giới hạn input (≤ 8 môn × ≤ 5 nhóm). Thêm cắt tỉa sớm (early pruning). |
| React Calendar UI mất nhiều thời gian hơn dự kiến | Trung bình | Dùng thư viện có sẵn: react-big-calendar hoặc FullCalendar (MIT License). |
| Không kịp triển khai UC-10 (lịch tự học) | Trung bình | UC-10 là ưu tiên thấp – loại bỏ khỏi phạm vi nếu thiếu thời gian, thêm vào hướng phát triển. |
| Deploy gặp lỗi cấu hình | Thấp | Chuẩn bị Docker Compose để deploy nhanh; backup plan là demo trên localhost qua Ngrok. |

# CHƯƠNG 8: KẾ HOẠCH KIỂM THỬ

## 8.1 Kiểm thử đơn vị (Unit Test) – Thuật toán xung đột

| **ID** | **Mô tả test case** | **Input** | **Expected Output** |
| --- | --- | --- | --- |
| UT-01 | Hai lớp cùng ngày, giao nhau rõ ràng | A: T2 7:00–9:00 │ B: T2 8:00–10:00 | conflict = TRUE |
| UT-02 | Hai lớp cùng ngày, không giao nhau | A: T2 7:00–9:00 │ B: T2 9:30–11:30 | conflict = FALSE |
| UT-03 | Biên: A kết thúc đúng lúc B bắt đầu | A: T2 7:00–9:00 │ B: T2 9:00–11:00 | conflict = FALSE |
| UT-04 | Khác ngày, cùng khung giờ | A: T2 7:00–9:00 │ B: T3 7:00–9:00 | conflict = FALSE |
| UT-05 | Một lớp chứa hoàn toàn lớp kia | A: T2 7:00–11:30 │ B: T2 8:00–10:00 | conflict = TRUE |
| UT-06 | Danh sách 5 lớp, 1 cặp xung đột | L1..L5, L2 và L4 trùng T3 8:00–10:00 | conflicts = [(L2,L4)] |
| UT-07 | Không có xung đột nào | 4 lớp, mỗi lớp khác ngày | conflicts = [] |

## 8.2 Kiểm thử đơn vị – Hàm điểm Score(S)

| **ID** | **Mô tả** | **Input đặc trưng** | **Expected** |
| --- | --- | --- | --- |
| UT-08 | F_break = 1.0 khi chỉ 1 buổi/ngày | Mỗi ngày học 1 buổi | F_break = 1.0 |
| UT-09 | F_break = 0 khi nghỉ = 0 phút | Buổi học liên tiếp không nghỉ, min_break=30 | F_break < 0.5 |
| UT-10 | F_pref = 1.0 khi tất cả khớp sở thích | Tất cả buổi học buổi sáng, prefer=morning | F_pref = 1.0 |
| UT-11 | F_balance: 1 ngày tập trung tất cả | 5 buổi/ngày × 1 ngày | F_balance thấp (< 0.5) |
| UT-12 | Score tổng hợp đúng công thức | F_break=0.8, F_pref=0.6, F_balance=0.7 | Score = 0.4×0.8+0.3×0.6+0.3×0.7 = 0.71 |

## 8.3 Kiểm thử tích hợp (Integration Test)

| **ID** | **Luồng kiểm thử end-to-end** | **Kết quả kỳ vọng** |
| --- | --- | --- |
| IT-01 | Đăng ký → Đăng nhập → Nhận JWT | Status 200, token hợp lệ |
| IT-02 | Chọn 3 môn → Phát hiện xung đột → Nhận danh sách conflict | Danh sách đúng, không sai sót |
| IT-03 | Chọn 5 môn (không xung đột) → Sinh TKB → Nhận top 3 phương án | 3 phương án sắp xếp điểm giảm dần, thời gian ≤ 3s |
| IT-04 | Chọn phương án → Xem Calendar → Kiểm tra hiển thị đúng màu | Mỗi môn 1 màu riêng, không bị chồng lên nhau |
| IT-05 | Thêm lịch bận → Sinh TKB mới → Không trùng lịch bận | Kết quả không chứa nhóm lớp trùng PersonalEvents |

# KẾT LUẬN TÀI LIỆU

Tài liệu SRS này đặc tả đầy đủ các yêu cầu cho hệ thống Smart Schedule theo chuẩn IEEE 830-1998, được điều chỉnh để phù hợp với năng lực thực hiện trong 3 tháng của nhóm sinh viên. Các điểm cải tiến chính so với phiên bản gốc bao gồm: (1) bổ sung bảng Semesters và sửa lỗi avoid_days để đảm bảo 3NF/1NF; (2) đơn giản hóa thuật toán từ Hybrid Architecture thành backtracking O(n²) phù hợp quy mô thực tế; (3) làm rõ công thức toán học của từng thành phần Score(S); (4) xây dựng kế hoạch 12 tuần cụ thể với deliverable kiểm tra được; (5) bổ sung kế hoạch kiểm thử với test case rõ ràng.

Nhóm sinh viên cam kết thực hiện đúng phạm vi và thời hạn đã đề ra. Mọi thay đổi yêu cầu trong quá trình phát triển sẽ được cập nhật vào tài liệu và thông báo đến giảng viên hướng dẫn.

# PHỤ LỤC A: ROADMAP CHI TIẾT 12 TUẦN

Phụ lục này mở rộng Chương 7 với (i) lịch làm việc theo ngày trong từng tuần, (ii) Định nghĩa Hoàn thành (Definition of Done – DoD) cho từng tuần, (iii) các milestone demo M1–M4 gắn với cuối mỗi giai đoạn, và (iv) bản đồ phụ thuộc giữa các tuần để nhóm phát hiện sớm các tuần chặn (blocker week). Tất cả tham chiếu Use Case, NFR, và bảng CSDL trong phụ lục đều khớp với các chương từ 3 đến 6.

## A.1 Các milestone chính (M1–M4)

Mỗi milestone là một mốc demo nội bộ với giảng viên hướng dẫn hoặc trong nhóm, có tiêu chí chấp nhận rõ ràng. Nếu một milestone không đạt, nhóm phải họp khẩn và quyết định cắt phạm vi (xem mục 7.4).

| **Mốc** | **Cuối tuần** | **Tên** | **Tiêu chí chấp nhận (Acceptance)** |
| --- | --- | --- | --- |
| M1 | Tuần 3 | Foundation Ready | Repo có CI chạy; CSDL 9 bảng migrate sạch; UC-01/UC-02 chạy end-to-end qua Postman. |
| M2 | Tuần 8 | Core Engine Ready | Sinh được ≥ 1 phương án TKB hợp lệ từ input thực; Score(S) trả về top-3 ổn định; calendar UI hiển thị được TKB. |
| M3 | Tuần 11 | Feature Complete | Toàn bộ 10 UC chạy; ≥ 90% test case pass; load test 50 user đạt NFR-01. |
| M4 | Tuần 12 | Release & Defense | URL demo public; báo cáo + slide nộp; nhóm tổng duyệt bảo vệ. |

# PHỤ LỤC A: ROADMAP CHI TIẾT 12 TUẦN

Phụ lục này mở rộng Chương 7 với (i) lịch làm việc theo ngày trong từng tuần, (ii) Định nghĩa Hoàn thành (Definition of Done – DoD) cho từng tuần, (iii) các milestone demo M1–M4 gắn với cuối mỗi giai đoạn, và (iv) bản đồ phụ thuộc giữa các tuần để nhóm phát hiện sớm các tuần chặn (blocker week). Tất cả tham chiếu Use Case, NFR, và bảng CSDL trong phụ lục đều khớp với các chương từ 3 đến 6.

## A.1 Các milestone chính (M1–M4)

Mỗi milestone là một mốc demo nội bộ với giảng viên hướng dẫn hoặc trong nhóm, có tiêu chí chấp nhận rõ ràng. Nếu một milestone không đạt, nhóm phải họp khẩn và quyết định cắt phạm vi (xem mục 7.4).

| **Mốc** | **Cuối tuần** | **Tên** | **Tiêu chí chấp nhận (Acceptance)** |
| --- | --- | --- | --- |
| M1 | Tuần 3 | Foundation Ready | Repo có CI chạy; CSDL 9 bảng migrate sạch; UC-01/UC-02 chạy end-to-end qua Postman. |
| M2 | Tuần 8 | Core Engine Ready | Sinh được ≥ 1 phương án TKB hợp lệ từ input thực; Score(S) trả về top-3 ổn định; calendar UI hiển thị được TKB. |
| M3 | Tuần 11 | Feature Complete | Toàn bộ 10 UC chạy; ≥ 90% test case pass; load test 50 user đạt NFR-01. |
| M4 | Tuần 12 | Release & Defense | URL demo public; báo cáo + slide nộp; nhóm tổng duyệt bảo vệ. |

## A.2 Bản đồ phụ thuộc giữa các tuần

Mũi tên "⟶" đọc là "chặn" (blocks). Tuần ở bên trái phải hoàn thành DoD trước khi tuần bên phải khởi động. Các tuần không có mũi tên chỉ tới tức là có thể chạy song song.

T1 (Môi trường) ⟶ T2 (CSDL) ⟶ T3 (Auth) ⟶ T4 (Nhập dữ liệu/sở thích) ⟶ T5 (Xung đột)

T5 (Xung đột) ⟶ T6 (Sinh tổ hợp) ⟶ T7 (Score) ⟶ T8 (UI Calendar + chọn phương án)

T2 (CSDL) ⟶ T8 (UI cần model dữ liệu ổn định)

T8 (UI Calendar) ⟶ T9 (UC-10 lịch tự học – tích hợp lên cùng calendar)

T9 ⟶ T10 (Integration test) ⟶ T11 (Bug fix + load test) ⟶ T12 (Deploy + báo cáo)

Tuần chặn (blocker weeks): T2, T5, T6, T8. Bất kỳ chậm trễ nào tại các tuần này đều phải kích hoạt phương án dự phòng tại mục 7.4 trong vòng 24 giờ.

## A.3 Lịch làm việc theo ngày và Definition of Done

Mỗi tuần được trình bày dưới dạng: bảng lịch theo ngày (Thứ 2 – Thứ 6, giả định nhóm làm việc tập trung 5 buổi/tuần × 3 giờ; Thứ 7 dự phòng/họp tuần; Chủ nhật nghỉ) và một mục DoD liệt kê tiêu chí kiểm tra được. Vai trò viết tắt: BE1 (Backend Dev 1), BE2 (Backend Dev 2), FE (Frontend Dev), FS (Full-stack/Tích hợp).

## A.3.1 Phase 1 – Nền tảng (Tuần 1–3)

### Tuần 1 – Khởi tạo môi trường và quy ước nhóm

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **Cả nhóm** | **Họp kickoff: thống nhất phạm vi, công cụ (Git, Jira/Trello, Slack/Discord), quy ước commit, lịch họp.** | **Biên bản kickoff; bảng phân vai (mục 7.3) ký xác nhận.** |
| **T3** | **BE1+BE2** | **Tạo repo monorepo (backend/, frontend/, docs/). Cấu hình .gitignore, README, branch protection main.** | **Repo public/private trên GitHub; main được bảo vệ.** |
| **T3** | **FE** | **Khởi tạo project React (Vite + TypeScript). Cấu hình ESLint, Prettier.** | **frontend/ build thành công.** |
| **T4** | **BE1** | **Khởi tạo project FastAPI + uv/poetry. Cấu hình pre-commit (black, ruff, mypy).** | **backend/ chạy được endpoint /health.** |
| **T4** | **FS** | **Soạn Docker Compose: postgres, backend, frontend, adminer.** | **docker compose up đưa cả stack lên localhost.** |
| **T5** | **Cả nhóm** | **Cấu hình GitHub Actions CI: lint + test cho mỗi PR.** | **CI badge xanh trên README.** |
| **T6** | **Cả nhóm** | **Họp tuần (review + retro). Demo localhost stack hoạt động.** | **Ghi chú retro; backlog tuần 2 đã chia.** |

DoD Tuần 1: (a) docker compose up đưa lên 4 service; (b) CI pass trên main; (c) README có hướng dẫn setup ≤ 5 lệnh; (d) backlog tuần 2 đã chia trên Jira/Trello.

### Tuần 2 – Lược đồ CSDL và migration

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **BE1** | **Cài Alembic. Viết migration cho 3 bảng nền: Semesters, ****Students, Courses (Chương 5.2.1–5.2.3).** | **Migration 001 chạy lên/xuống được.** |
| **T3** | **BE1** | **Migration 002: Classes, Preferences, PreferenceAvoidDays (5.2.4–5.2.6).** | **Migration 002 pass.** |
| **T4** | **BE2** | **Migration 003: PersonalEvents, Schedules, ScheduleClasses (5.2.7–5.2.9). Bổ sung CHECK + UNIQUE từ mục 5.3.** | **Migration 003 pass; ràng buộc kiểm thử bằng INSERT lỗi.** |
| **T5** | **BE2** | **Viết script seed dữ liệu mẫu: 1 học kỳ, 8 môn, ~30 nhóm lớp, 2 sinh viên test.** | **Lệnh make seed nạp dữ liệu ****<**** 5 giây.** |
| **T6** | **FS+FE** | **Soạn ERD đầy đủ (dbdiagram.io hoặc Mermaid) đồng bộ với Chương 5.1. FE khởi tạo router skeleton.** | **ERD commit vào docs/erd.png; frontend có 4 route trống.** |

DoD Tuần 2: (a) make migrate up && make migrate down chạy sạch trên DB rỗng; (b) seed dữ liệu xong, query SELECT trên cả 9 bảng có kết quả; (c) ERD khớp 100% với Chương 5.

### Tuần 3 – Xác thực (UC-01, UC-02) — kết thúc Phase 1

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **BE1** | **Endpoint POST /auth/register: hash mật khẩu (bcrypt), validate email, ràng buộc UNIQUE.** | **Postman: đăng ký mới → 201; trùng email → 409.** |
| **T3** | **BE1** | **Endpoint POST /auth/login: trả JWT (access + refresh). Endpoint POST /auth/logout (blacklist token).** | **Login → token; logout → token bị thu hồi.** |
| **T4** | **BE2** | **JWT middleware: decode + verify, gắn current_user vào request. Endpoint GET /me.** | **API /me trả thông tin user đúng.** |
| **T5** | **FE** | **Trang Login + Register (form + validation). Lưu token vào httpOnly cookie hoặc localStorage có cảnh báo XSS.** | **FE đăng ký + đăng nhập gọi API thật thành công.** |
| **T6** | **Cả nhóm** | **Demo M1 nội bộ với giảng viên: chạy luồng đăng ký → đăng nhập → /me. Retro Phase 1.** | **Biên bản M1; danh sách action item cho Phase 2.** |

DoD Tuần 3 / Milestone M1: (a) UC-01, UC-02 pass tất cả test case; (b) JWT có hạn 60 phút, refresh 7 ngày, logout thu hồi đúng; (c) FE chạy được 2 trang Login/Register; (d) demo M1 đạt.

## A.3.2 Phase 2 – Lõi hệ thống (Tuần 4–8)

### Tuần 4 – Nhập dữ liệu, sở thích, lịch bận (UC-03, UC-04, UC-05)

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **BE1** | **API CRUD /courses và /classes (UC-03A) – admin-only.** | **Postman pass; chỉ user role admin truy cập được.** |
| **T3** | **BE1** | **API /enrollments (UC-03B): sinh viên chọn môn cho học kỳ hiện tại.** | **POST /enrollments lưu link Student–Course.** |
| **T4** | **BE2** | **API /preferences và /preferences/avoid-days (UC-04). Validate giờ start ****<**** end.** | **GET/POST/PUT /preferences pass test.** |
| **T5** | **BE2** | **API /personal-events (UC-05) — CRUD lịch bận, kiểm tra overlap khi tạo.** | **Tạo event trùng giờ → 409 với mã lỗi rõ ràng.** |
| **T6** | **FE** | **Form nhập sở thích + form thêm lịch bận. Tích hợp API.** | **FE: nhập preference → lưu DB → reload thấy đúng.** |

DoD Tuần 4: (a) 3 nhóm UC pass test; (b) DB constraint chặn dữ liệu sai (giờ âm, khoảng đảo ngược); (c) FE có 2 form đầy đủ validation.

### Tuần 5 – Thuật toán phát hiện xung đột (UC-06)

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **BE2** | **Cài đặt hàm has_conflict(a, b) theo định nghĩa 6.1.1 (cùng day_of_week + giao khoảng giờ).** | **Hàm thuần (pure) ≤ 20 dòng.** |
| **T3** | **BE2** | **Cài đặt detect_conflicts(classes) O(n²) theo mã giả 6.1.3.** | **Hàm trả về list[(class_a, class_b, reason)].** |
| **T3** | **BE2** | **Mở rộng: xung đột với PersonalEvents (lịch bận cá nhân).** | **Test case có lịch bận → trả xung đột đúng.** |
| **T4** | **BE2** | **Viết ≥ 10 unit test (pytest): cùng ngày khác giờ, khác ngày, biên (sát nhau), giao một phần, bao trùm, n=0, n=1, lịch bận.** | **pytest pass 100%; coverage ≥ 90% cho module.** |
| **T5** | **BE1** | **API GET /conflicts?schedule_id=… trả danh sách xung đột.** | **API pass test, response time ****<**** 50ms với n=20.** |
| **T6** | **Cả nhóm** | **Code review pair: BE1 review code BE2. Cập nhật doc thuật toán nếu khác mã giả.** | **PR merged; checklist review đính kèm.** |

DoD Tuần 5: (a) ≥ 10 unit test pass; (b) coverage module xung đột ≥ 90%; (c) API /conflicts trả đúng cấu trúc; (d) doc thuật toán khớp code thực tế.

### Tuần 6 – Sinh tổ hợp TKB bằng backtracking (UC-07 phần 1)

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **BE2** | **Cài đặt khung backtracking theo mã giả 6.3.2: chọn 1 nhóm cho mỗi môn, kiểm tra xung đột với tổ hợp đã chọn.** | **Hàm generate(courses) trả list tổ hợp.** |
| **T3** | **BE2** | **Thêm early pruning: cắt nhánh ngay khi nhóm mới xung đột với bất kỳ nhóm đã chọn.** | **Benchmark: 8 môn × 5 nhóm chạy ****<**** 2s.** |
| **T4** | **BE2** | **Giới hạn output: chỉ giữ tối đa 50 tổ hợp đầu (tránh OOM).** | **Test với input lớn không vượt 200MB RAM.** |
| **T5** | **BE1** | **API POST /schedules/generate: nhận semester_id, gọi generator, lưu tạm vào Schedules với is_draft=true.** | **API trả schedule_ids; DB có bản ghi draft.** |
| **T5** | **FS** | **Viết script benchmark đo thời gian generator theo n môn = 4, 6, 8.** | **Bảng benchmark commit vào docs/benchmark.md.** |
| **T6** | **Cả nhóm** | **Họp review: kiểm tra benchmark có vượt NFR-01 (≤ 5 giây) không.** | **Quyết định: tiếp tục hay tối ưu thêm.** |

DoD Tuần 6: (a) generator trả ≥ 1 tổ hợp hợp lệ với input mẫu; (b) benchmark 8 môn × 5 nhóm ≤ 5 giây (NFR-01); (c) draft schedules được lưu DB; (d) doc thuật toán cập nhật nếu pruning khác mã giả.

### Tuần 7 – Hàm Score(S) và xếp hạng (UC-07 phần 2)

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **BE2** | **Cài đặt F_break theo công thức 6.2.2.** | **Hàm thuần + 4 unit test biên.** |
| **T3** | **BE2** | **Cài đặt F_pref theo công thức 6.2.3 (đọc bảng Preferences + PreferenceAvoidDays).** | **Test: 3 sở thích khác nhau cho cùng tổ hợp → điểm khác nhau hợp lý.** |
| **T4** | **BE2** | **Cài đặt F_balance theo 6.2.4. Tổng hợp Score(S) = w1·F_break + w2·F_pref + w3·F_balance (mặc định w1=w2=w3=1/3).** | **Hàm score(s) trả số trong [0, 1].** |
| **T4** | **BE2** | **Test ví dụ minh họa 6.2.5: nhập đúng input, kết quả khớp ± 0.01.** | **Test pass.** |
| **T5** | **BE1** | **Cập nhật API /schedules/generate: trả top-K (mặc định K=3) đã sort theo score giảm dần.** | **Response chứa schedule + score, sort đúng.** |
| **T6** | **FE** | **Bắt đầu component danh sách phương án (card view), hiển thị score và badge top.** | **FE list-view hiển thị 3 card có điểm.** |

DoD Tuần 7: (a) test ví dụ 6.2.5 pass; (b) coverage hàm score ≥ 90%; (c) API trả top-3 ổn định; (d) FE đọc danh sách phương án.

### Tuần 8 – Calendar UI và lưu phương án (UC-08, UC-09) — kết thúc Phase 2

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **FE** | **Tích hợp react-big-calendar (hoặc FullCalendar). Mapping ScheduleClasses → events.** | **Calendar tuần render đúng các slot.** |
| **T3** | **FE** | **Phối màu môn học (ổn định theo course_id), tooltip thông tin lớp.** | **UX: hover hiện chi tiết; màu nhất quán giữa các tuần.** |
| **T4** | **FE** | **Trang so sánh 2–3 phương án song song (UC-08).** | **User chọn phương án A vs B → hiển thị calendar cạnh nhau.** |
| **T5** | **BE1** | **API POST /schedules/{id}/save (UC-08): chuyển is_draft=false, đánh dấu phương án chính.** | **API pass; DB chỉ có 1 phương án is_active=true mỗi user/semester.** |
| **T5** | **FS** | **Smoke test luồng E2E: login → chọn môn → set sở thích → generate → so sánh → lưu.** | **Luồng chạy không lỗi trên dữ liệu seed.** |
| **T6** | **Cả nhóm** | **Demo M2 với giảng viên. Retro Phase 2.** | **Biên bản M2; backlog Phase 3 đã chia.** |

DoD Tuần 8 / Milestone M2: (a) calendar hiển thị TKB đúng cho top-3; (b) lưu phương án persist qua reload; (c) E2E smoke test pass; (d) demo M2 đạt.

## A.3.3 Phase 3 – Hoàn thiện (Tuần 9–11)

### Tuần 9 – Lịch tự học (UC-10)

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **FS** | **Phân tích thuật toán đề xuất khe trống: lấy union (lịch học, lịch bận) → tính khe trống ≥ ngưỡng (mặc định 90 phút).** | **Spec ngắn ≤ 1 trang trong docs/uc10.md.** |
| **T3** | **FS** | **Cài đặt hàm suggest_self_study(student_id, semester_id) trả list khe trống ưu tiên (theo sở thích thời gian).** | **Hàm pure + 5 unit test.** |
| **T4** | **BE1** | **API GET /self-study/suggestions tích hợp vào Schedules.** | **API pass; trả ≥ 3 khe gợi ý.** |
| **T5** | **FE** | **Hiển thị khe tự học trên calendar với màu/style khác (ví dụ nét đứt).** | **Calendar render khe tự học không trùng lịch học/bận.** |
| **T6** | **Cả nhóm** | **Họp tuần. Quyết định cắt UC-10 nếu chưa xong (theo 7.4).** | **Quyết định ghi vào biên bản.** |

DoD Tuần 9: (a) UC-10 hoạt động end-to-end hoặc đã được chính thức cắt phạm vi (decision logged); (b) khe tự học không trùng lịch học/bận trong 100% test case.

### Tuần 10 – Kiểm thử tích hợp end-to-end

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **FS** | **Viết 5 kịch bản E2E (Playwright hoặc Cypress) theo Chương 8.3.** | **5 test file commit; chạy headless.** |
| **T3** | **FS** | **Tích hợp 5 kịch bản vào CI; chạy mỗi PR.** | **CI workflow chạy E2E ≤ 8 phút.** |
| **T4** | **BE2** | **Bổ sung integration test backend: pytest + httpx, mock DB bằng testcontainers.** | **≥ 15 integration test pass.** |
| **T5** | **Cả nhóm** | **Bug bash 2 giờ: cả nhóm cùng test thủ công, ghi bug vào Jira.** | **Danh sách bug có severity và assignee.** |
| **T6** | **Cả nhóm** | **Triage bug: chia bug cho tuần 11. Chỉ giữ bug Critical/High vào tuần 11; Low đẩy sang post-release.** | **Backlog tuần 11 chốt.** |

DoD Tuần 10: (a) ≥ 90% test case pass (mục tiêu Chương 8); (b) E2E chạy được trên CI; (c) bug Critical = 0 sau bug bash hoặc đã có owner và due date.

### Tuần 11 – Sửa lỗi, load test, tài liệu — kết thúc Phase 3

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **BE1+BE2** | **Fix bug Critical/High còn lại. Code review chéo.** | **Burn-down bug về 0 cho mức Critical.** |
| **T3** | **FS** | **Load test bằng Locust: 50 user đồng thời chạy luồng đăng nhập + generate (NFR-01).** | **Báo cáo p95 ****<**** 5s; biểu đồ throughput.** |
| **T4** | **FE** | **Tinh chỉnh UX: loading state, error toast, responsive mobile.** | **Lighthouse mobile score ≥ 80.** |
| **T5** | **BE1** | **Sinh tài liệu API tự động (FastAPI /docs Swagger + xuất HTML tĩnh).** | **docs/api/index.html commit.** |
| **T6** | **Cả nhóm** | **Demo M3 với giảng viên: chạy đầy đủ 10 UC. Khoá phạm vi (feature freeze).** | **Biên bản M3; chỉ còn fix bug, không thêm tính năng.** |

DoD Tuần 11 / Milestone M3: (a) load test 50 user đạt NFR-01; (b) Critical bug = 0; (c) API doc + README cập nhật; (d) feature freeze tuyên bố chính thức.

## A.3.4 Phase 4 – Nghiệm thu (Tuần 12)

### Tuần 12 – Deploy, báo cáo, bảo vệ

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| **T2** | **FS** | **Deploy backend lên Render.com / ****Railway; DB Postgres managed. Cấu hình biến môi trường.** | **URL backend public; /health 200.** |
| **T2** | **FE** | **Deploy frontend lên Vercel / Netlify; cấu hình API_BASE_URL.** | **URL frontend public; login chạy được.** |
| **T3** | **FS** | **Smoke test trên môi trường production. Tạo 2 tài khoản demo (sinh viên A, B).** | **Checklist 10 UC pass trên production.** |
| **T3** | **BE1+BE2** | **Hoàn thiện báo cáo đồ án: bổ sung kết quả thực nghiệm, screenshot.** | **Bản báo cáo nháp gửi GVHD đọc trước.** |
| **T4** | **FE** | **Quay video demo 5–7 phút theo kịch bản chuẩn.** | **video.mp4 upload Drive.** |
| **T5** | **Cả nhóm** | **Slide bảo vệ: 15–20 slide. Tổng duyệt nội bộ 2 lần.** | **Slide final commit; nhóm thuộc kịch bản.** |
| **T6** | **Cả nhóm** | **Tổng duyệt cuối + nộp tài liệu.** | **Hồ sơ bảo vệ đầy đủ.** |

DoD Tuần 12 / Milestone M4: (a) URL demo public chạy ổn định ≥ 24h; (b) báo cáo + slide + video nộp đúng hạn; (c) nhóm tổng duyệt bảo vệ ≥ 2 lần.

## A.4 Quỹ thời gian dự phòng (Buffer)

Mỗi phase có quỹ buffer ngầm là Thứ 7 hàng tuần. Ngoài ra, các tuần dưới đây được khuyến nghị giữ buffer cứng (không lập kế hoạch tính năng mới):

| **Phase** | **Buffer ngầm** | **Buffer cứng** | **Cách dùng** |
| --- | --- | --- | --- |
| Phase 1 (T1–3) | Thứ 7 mỗi tuần | Không có (giai đoạn ngắn) | Chạy bù migration nếu CSDL trượt. |
| Phase 2 (T4–8) | Thứ 7 mỗi tuần | ½ ngày Thứ 6 tuần 7 | Bù thuật toán nếu Score(S) trượt sang tuần 8. |
| Phase 3 (T9–11) | Thứ 7 mỗi tuần | 1 ngày Thứ 6 tuần 11 | Bù bug Critical còn sót. |
| Phase 4 (T12) | Thứ 7 | ½ ngày Thứ 5 | Bù lỗi deploy / sự cố hosting. |

Quy tắc dùng buffer: chỉ được tiêu khi (a) DoD tuần đó không đạt và (b) cả nhóm đồng ý ghi vào biên bản. Buffer không được dùng để "thêm tính năng" — sau feature freeze ở M3, mọi yêu cầu mới đều đẩy sang phase post-release.

## A.5 Chỉ số theo dõi tiến độ (KPI)

Nhóm cập nhật KPI vào cuối mỗi tuần (cuộc họp Thứ 6) và treo trên kênh chung. KPI vượt ngưỡng đỏ kích hoạt phương án dự phòng (mục 7.4).

| **KPI** | **Đo bằng** | **Ngưỡng xanh** | **Ngưỡng đỏ** |
| --- | --- | --- | --- |
| Velocity tuần | % công việc cam kết hoàn thành | ≥ 80% | < 60% hai tuần liên tiếp |
| Bug Critical mở | Số lượng cuối tuần | = 0 | ≥ 3 |
| Coverage thuật toán lõi | pytest --cov | ≥ 90% | < 75% |
| CI fail rate | % PR fail CI / tổng PR | ≤ 15% | ≥ 30% |
| DoD tuần đạt | Có/Không | Đạt 100% mục | Trượt ≥ 1 mục blocker |

**Hết Phụ lục A.**

Trang 1 / 1