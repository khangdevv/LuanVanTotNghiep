Smart Schedule – SRS v2.0	*Theo chuẩn IEEE 830-1998*

**TRƯỜNG ĐẠI HỌC CÔNG NGHỆ SÀI GÒN**

KHOA CÔNG NGHỆ THÔNG TIN

**ĐẶC TẢ YÊU CẦU PHẦN MỀM**

*(Software Requirements Specification)*

*Theo chuẩn IEEE 830-1998*

**SMART SCHEDULE**

Hệ Thống Tối Ưu Thời Khóa Biểu Cá Nhân

| **Phiên bản** | 2.0 |
| --- | --- |
| **Ngày tạo** | 01/06/2025 |
| **Ngày cập nhật** | 21/05/2026 |
| **Trạng thái** | Cập nhật theo thực tế triển khai |
| **Môn học** | Đồ án tốt nghiệp |

# LỊCH SỬ THAY ĐỔI TÀI LIỆU

| **Phiên bản** | **Ngày** | **Tác giả** | **Mô tả thay đổi** |
| --- | --- | --- | --- |
| 1.0 | 01/06/2025 | Nhóm sinh viên | Tạo tài liệu ban đầu – phiên bản hoàn chỉnh |
| 2.0 | 21/05/2026 | Nhóm sinh viên | Cập nhật theo thực tế triển khai: (1) Bổ sung 3 bảng CSDL mới (Enrollments, StudySessions, TokenBlacklist); (2) Cập nhật bảng Schedules (thêm is_draft, is_active); (3) Sửa công thức F_break, F_pref, F_balance khớp code thực tế; (4) Nâng cấp thuật toán từ backtracking đơn giản lên CSP đầy đủ (MRV + LCV + Forward Checking); (5) Bổ sung nguồn dữ liệu JSON và định dạng semester_id thực tế |

---

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

	5.2.1 Bảng Semesters (Học kỳ)	17

	5.2.2 Bảng Students (Sinh viên)	17

	5.2.3 Bảng Courses (Môn học)	17

	5.2.4 Bảng Classes (Nhóm lớp mở theo học kỳ)	18

	5.2.5 Bảng Preferences (Sở thích lịch học)	18

	5.2.6 Bảng PreferenceAvoidDays (Ngày muốn tránh)	19

	5.2.7 Bảng PersonalEvents (Lịch bận cá nhân)	19

	5.2.8 Bảng Schedules (Phương án thời khóa biểu)	19

	5.2.9 Bảng ScheduleClasses (Lớp trong phương án)	20

	5.2.10 Bảng Enrollments (Đăng ký môn học) – Bổ sung v2.0	20

	5.2.11 Bảng StudySessions (Lịch tự học) – Bổ sung v2.0	20

	5.2.12 Bảng TokenBlacklist (Thu hồi JWT) – Bổ sung v2.0	21

	5.3 Ràng buộc toàn vẹn dữ liệu bổ sung	21

	CHƯƠNG 6: THIẾT KẾ THUẬT TOÁN	22

	6.1 Thuật toán phát hiện xung đột	22

	6.2 Hàm đánh giá Score(S)	22

	6.3 Thuật toán sinh tổ hợp TKB – CSP với MRV + LCV + Forward Checking	24

	6.4 Thiết kế API (REST)	26

	CHƯƠNG 7: KẾ HOẠCH THỰC HIỆN 3 THÁNG (12 TUẦN)	27

	CHƯƠNG 8: KẾ HOẠCH KIỂM THỬ	29

	KẾT LUẬN TÀI LIỆU	31

	PHỤ LỤC A: ROADMAP CHI TIẾT 12 TUẦN	32

---

# CHƯƠNG 1: GIỚI THIỆU

## 1.1 Mục đích tài liệu

Tài liệu này là Đặc tả Yêu cầu Phần mềm (Software Requirements Specification – SRS) cho hệ thống Smart Schedule, được soạn thảo theo chuẩn IEEE 830-1998. Tài liệu mô tả đầy đủ các yêu cầu chức năng, phi chức năng, ràng buộc thiết kế và phạm vi triển khai của hệ thống, phục vụ làm căn cứ cho quá trình thiết kế, cài đặt, kiểm thử và nghiệm thu.

Tài liệu hướng đến các đối tượng đọc sau: (1) nhóm sinh viên phát triển hệ thống, (2) giảng viên hướng dẫn và hội đồng phản biện, (3) người dùng cuối (sinh viên đại học).

**Phiên bản 2.0** cập nhật các điều chỉnh phát sinh trong quá trình triển khai thực tế, bao gồm thiết kế CSDL, công thức hàm điểm và kiến trúc thuật toán. Tất cả thay đổi so với v1.0 được đánh dấu bằng chú thích *[Cập nhật v2.0]*.

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
| JTI | JWT ID – Định danh duy nhất của một JWT token |
| REST | Representational State Transfer – Kiến trúc API web |
| ORM | Object-Relational Mapping – Ánh xạ đối tượng-quan hệ |
| 3NF | Third Normal Form – Dạng chuẩn ba trong thiết kế CSDL |
| 1NF | First Normal Form – Dạng chuẩn một trong thiết kế CSDL |
| Score(S) | Hàm điểm tổng hợp đánh giá chất lượng phương án TKB |
| CSP | Constraint Satisfaction Problem – Bài toán thỏa mãn ràng buộc |
| MRV | Minimum Remaining Values – Chọn biến có miền giá trị nhỏ nhất |
| LCV | Least Constraining Value – Chọn giá trị gây ít ràng buộc nhất |
| FC | Forward Checking – Lan truyền ràng buộc tiến |
| Conflict | Xung đột lịch: hai lớp học cùng ngày, giao nhau về thời gian |
| Slot | Khung giờ học: (day_of_week, start_time, end_time) |
| Ca học | Phân chia buổi học theo khung giờ quy định của trường |
| Tiết | Đơn vị thời gian học (50 phút). Tiết 1–6: Ca 1–2 (07:00–12:05); Tiết 7–12: Ca 3–4 (12:35–17:40); Tiết 13–15: tối (17:45–20:15) |

## 1.4 Tài liệu tham khảo

- IEEE Std 830-1998, IEEE Recommended Practice for Software Requirements Specifications.

- Rossi, F. et al. (2006). Handbook of Constraint Programming. Elsevier.

- Russell, S. & Norvig, P. (2020). Artificial Intelligence: A Modern Approach, 4th Edition. Pearson. (Chương 6 – CSP)

- Sommerville, I. (2016). Software Engineering, 10th Edition. Pearson.

- PostgreSQL 14 Documentation. https://www.postgresql.org/docs/14/

- FastAPI Documentation. https://fastapi.tiangolo.com/

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

- *[Cập nhật v2.0]* Dữ liệu lịch mở lớp được nạp từ file JSON (`schedule_data_from_web.json`) chứa dữ liệu thực từ hệ thống đăng ký của trường, thay vì nhập thủ công qua giao diện quản trị. Tính năng import CSV và admin UI là hướng phát triển tương lai.

## 2.5 Giả định và phụ thuộc

- Giả định: Mỗi lớp học phần chỉ có một khung giờ cố định trong tuần (không phân chia ca). Lịch học không thay đổi trong suốt học kỳ.

- *[Cập nhật v2.0]* Định dạng mã học kỳ trong hệ thống thực tế là chuỗi dạng `"HK2-2025"` (thay vì `"20241"` như đề xuất ban đầu trong v1.0), phản ánh cách đặt tên học kỳ của Trường ĐH Công nghệ Sài Gòn.

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

*[Cập nhật v2.0]* Model Student trong code thực tế kiểm tra email bằng regex: `^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$`. Field `role` dùng enum `Role` với giá trị `student` / `admin`.

### UC-02: Đăng nhập / Đăng xuất

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-02 |
| Actor | Sinh viên |
| Điều kiện tiên quyết | Tài khoản đã tồn tại trong hệ thống |
| Kịch bản chính (Đăng nhập) | 1. Người dùng nhập Email và Mật khẩu. 2. Hệ thống xác thực: so sánh mật khẩu với hash bcrypt. 3. Nếu hợp lệ: phát hành JWT token (TTL = 24h), lưu vào localStorage. 4. Chuyển hướng về trang Dashboard. |
| Kịch bản thay thế | A1 – Sai mật khẩu ≥ 5 lần: khóa tài khoản 15 phút. A2 – Đăng xuất: xóa JWT khỏi localStorage, ghi JTI vào bảng TokenBlacklist, chuyển về trang đăng nhập. |
| Kết quả | Người dùng được xác thực; JWT token hợp lệ lưu phía client. |

*[Cập nhật v2.0]* Đăng xuất ghi JTI (JWT ID) vào bảng `token_blacklist` kèm `expires_at` để middleware kiểm tra và từ chối token đã bị thu hồi. Bảng này được dọn dẹp định kỳ dựa trên `expires_at`.

### UC-03: Nhập dữ liệu môn học và nhóm lớp

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-03 |
| Actor | Sinh viên (chọn môn); Admin (nhập lịch mở lớp) |
| Mô tả | Phân thành 2 luồng: (A) Admin nhập danh mục môn học và lịch mở lớp vào hệ thống; (B) Sinh viên chọn các môn cần xếp lịch trong học kỳ hiện tại. |
| Kịch bản A – Admin | 1. Admin đăng nhập trang quản trị (route /admin). 2. Tạo môn học: nhập Mã môn, Tên môn, Số tín chỉ. 3. Tạo nhóm lớp: gán môn, nhập Thứ, Giờ bắt đầu, Giờ kết thúc, Phòng, Sĩ số tối đa. 4. Hệ thống lưu và hiển thị danh sách lớp đã nhập. |
| Kịch bản B – Sinh viên | 1. Sinh viên vào trang "Chọn môn học". 2. Chọn học kỳ hiện tại. 3. Tích chọn các môn cần đăng ký (tối đa 8 môn). 4. Hệ thống hiển thị tất cả nhóm lớp mở của các môn đã chọn. 5. Sinh viên xác nhận → lưu danh sách vào bảng Enrollments. |
| Kết quả | Dữ liệu đầu vào sẵn sàng cho UC-06 và UC-07. |

*[Cập nhật v2.0]* Luồng A trong thực tế v2.0 được thực hiện bằng cách nạp dữ liệu từ file JSON (`schedule_data_from_web.json`) qua hàm `load_course_groups()`. File JSON chứa dữ liệu thực từ hệ thống đăng ký của trường, gồm mã môn (`ma_mh`), nhóm/tổ (`nhom_to`), tiết bắt đầu, số tiết, phòng học và giảng viên. Dữ liệu được deduplicate theo (course_id, nhom_to, tiet_bat_dau) trước khi đưa vào CSP.

### UC-04: Thiết lập sở thích lịch học

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-04 |
| Actor | Sinh viên |
| Điều kiện tiên quyết | Đã đăng nhập |
| Kịch bản chính | 1. Sinh viên vào trang "Cài đặt sở thích". 2. Chọn khung giờ ưa thích: Sáng / Chiều / Tối. 3. Đánh dấu các ngày muốn tránh học (checkbox T2–CN). 4. Nhập thời gian nghỉ tối thiểu giữa 2 buổi liên tiếp (mặc định: 15 phút). 5. Nhấn "Lưu" → hệ thống cập nhật bảng Preferences. |
| Kết quả | Sở thích được lưu; được dùng trong hàm tính điểm Score(S). |

*[Cập nhật v2.0]* Ánh xạ khung giờ → Ca học trong code:
- `MORNING` → Ca 1 và Ca 2 (từ 07:00 đến trước 12:35)
- `AFTERNOON` → Ca 3 và Ca 4 (từ 12:35 đến trước 15:10, và từ 15:10 trở đi)
- `EVENING` → Ca 4 (từ 15:10 trở đi)

Ranh giới Ca học dựa trên phút từ 00:00: Ca1 < 575, Ca2 < 755, Ca3 < 910, Ca4 ≥ 910.

Trọng số mặc định: `w_break = 0.40`, `w_preference = 0.30`, `w_balance = 0.30`. Validator kiểm tra `w_break + w_preference + w_balance = 1.0` (sai số ≤ 1e-9).

### UC-05: Quản lý lịch bận cá nhân

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-05 |
| Mô tả | Sinh viên thêm, sửa, xóa các sự kiện bận cá nhân (làm thêm, câu lạc bộ, v.v.) để hệ thống tránh xếp lịch học và lịch tự học vào các khung giờ này. |
| Kịch bản chính | 1. Sinh viên nhấn "Thêm sự kiện". 2. Nhập: Tên sự kiện, Thứ (hoặc ngày cụ thể), Giờ bắt đầu, Giờ kết thúc, Lặp lại hàng tuần (toggle). 3. Nhấn "Lưu" → ghi vào bảng PersonalEvents. 4. Sự kiện hiển thị trên calendar dưới dạng ô màu xám. |
| Kết quả | Lịch bận được lưu; thuật toán CSP (UC-07) và thuật toán UC-10 tránh các khung giờ này. |

*[Cập nhật v2.0]* Thuật toán CSP chỉ lọc PersonalEvent có `is_recurring = True` **và** `day_of_week` không phải `None`. Sự kiện một lần (one-time, `is_recurring = False`) hoặc không có thứ cố định (`day_of_week = None`) không ảnh hưởng đến quá trình sinh TKB.

### UC-06: Phát hiện xung đột lịch

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-06 |
| Actor | Hệ thống (kích hoạt tự động sau UC-03) |
| Điều kiện tiên quyết | Sinh viên đã chọn ít nhất 2 môn học |
| Kịch bản chính | 1. Hệ thống lấy tất cả nhóm lớp của các môn đã chọn. 2. Với mỗi cặp (A, B): kiểm tra điều kiện xung đột. 3. Nếu phát hiện xung đột: ghi nhận cặp (classA_id, classB_id) vào conflict_set (lưu hai chiều). 4. Hiển thị danh sách xung đột kèm tên môn, thứ, giờ bị trùng. 5. conflict_set được truyền vào CSP để loại trừ tổ hợp không hợp lệ. |
| Điều kiện xung đột | Hai lớp A và B xung đột khi và chỉ khi: (A.day_of_week = B.day_of_week) AND (A.start_time < B.end_time) AND (B.start_time < A.end_time) |
| Lưu ý về điều kiện biên | Trường hợp A.end_time = B.start_time KHÔNG được tính là xung đột. |
| Cấu trúc conflict_set | *[Cập nhật v2.0]* conflict_set được lưu **hai chiều**: cả (A_id, B_id) và (B_id, A_id) đều có trong set. Lý do: MRV có thể xử lý các môn theo bất kỳ thứ tự nào, nên khi tra cứu `(cls.class_id, chosen_cls.class_id)`, cả hai hướng đều cần có mặt. |
| Độ phức tạp | O(n²) với n là tổng số nhóm lớp. Với n ≤ 50 (thực tế), thời gian < 1ms. |
| Kết quả | conflict_set sẵn sàng làm đầu vào cho CSP (UC-07). |

### UC-07: Sinh và xếp hạng phương án TKB

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-07 |
| Actor | Hệ thống |
| Điều kiện tiên quyết | UC-06 đã tạo conflict_set; sinh viên đã thiết lập sở thích (UC-04) |
| Kịch bản chính | 1. Hệ thống khởi tạo domain cho từng môn (loại trừ nhóm lớp thuộc avoid_days). 2. CSP với MRV+LCV+Forward Checking sinh tất cả tổ hợp hợp lệ (tối đa max_solutions). 3. Với mỗi tổ hợp hợp lệ: tính Score(S) theo công thức ở mục 6.2. 4. Sắp xếp giảm dần theo Score(S). 5. Lưu top 3 phương án vào bảng Schedules (is_draft=TRUE). 6. Trả về 3 phương án kèm điểm chi tiết từng thành phần. |
| Ràng buộc hiệu năng | Hoàn thành trong ≤ 3 giây với ≤ 8 môn, mỗi môn ≤ 5 nhóm. |
| Kết quả | Top 3 phương án TKB được lưu và sẵn sàng hiển thị ở UC-08. |

*[Cập nhật v2.0]* Tham số `max_solutions` mặc định là 200 (demo: 200.000). Hệ thống dừng sinh tổ hợp ngay khi đạt ngưỡng này mà không cần duyệt hết không gian tìm kiếm.

### UC-08: Xem, so sánh và lưu phương án TKB

| **Thuộc tính** | **Nội dung** |
| --- | --- |
| Mã | UC-08 |
| Actor | Sinh viên |
| Kịch bản chính | 1. Hiển thị 3 tab (Phương án 1, 2, 3), mỗi tab có điểm tổng và điểm thành phần. 2. Sinh viên chuyển tab để so sánh trực quan trên calendar. 3. Sinh viên chọn "Áp dụng phương án này" → cập nhật is_selected = TRUE, is_draft = FALSE trong DB. 4. Hệ thống xác nhận và chuyển sang màn hình calendar chính. |
| Kết quả | Một phương án được đánh dấu is_selected và is_active; dùng làm input cho UC-10. |

*[Cập nhật v2.0]* Bảng Schedules có thêm `is_draft` và `is_active`. Partial unique index đảm bảo mỗi sinh viên chỉ có 1 phương án `is_active=TRUE` cho mỗi học kỳ.

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

*[Cập nhật v2.0]* Bảng StudySessions không lưu `student_id` trực tiếp (đã sửa để tuân thủ 3NF). `student_id` có thể lấy qua `schedules.student_id` thông qua `schedule_id`.

# CHƯƠNG 4: YÊU CẦU PHI CHỨC NĂNG

## 4.1 Yêu cầu hiệu năng (NFR-01)

| **Mã** | **Chỉ tiêu** | **Giá trị mục tiêu** | **Phương pháp kiểm thử** |
| --- | --- | --- | --- |
| NFR-01.1 | Thời gian phản hồi API thông thường | ≤ 500ms (P95) | Dùng Locust hoặc k6 với 50 user đồng thời |
| NFR-01.2 | Thời gian sinh TKB (UC-07) | ≤ 3 giây với 8 môn × 5 nhóm | Unit test với input chuẩn |
| NFR-01.3 | Số người dùng đồng thời | ≥ 50 (mục tiêu tối thiểu) | Load test với Locust |
| NFR-01.4 | Thời gian tải trang chính | ≤ 3 giây trên kết nối 4G | Chrome DevTools Lighthouse |

*Lưu ý: Giá trị 50 người dùng đồng thời là mục tiêu thực tế khả thi trong 3 tháng. Nâng lên 100+ là hướng phát triển tương lai.*

## 4.2 Yêu cầu bảo mật (NFR-02)

| **Mã** | **Yêu cầu** | **Chi tiết kỹ thuật** |
| --- | --- | --- |
| NFR-02.1 | Mã hóa mật khẩu | bcrypt với cost factor = 10. Không bao giờ lưu plain-text. |
| NFR-02.2 | Truyền thông an toàn | HTTPS bắt buộc (TLS 1.2+). Redirect HTTP → HTTPS. |
| NFR-02.3 | Xác thực JWT | Token TTL = 24h. Payload chứa student_id và role. Ký bằng HS256. |
| NFR-02.4 | Thu hồi JWT | *[Cập nhật v2.0]* Khi đăng xuất, JTI ghi vào TokenBlacklist. Middleware kiểm tra blacklist trên mỗi request. Bảng dọn dẹp định kỳ theo expires_at. |
| NFR-02.5 | Chống SQL Injection | Dùng ORM (SQLAlchemy) với parameterized queries. Không dùng raw SQL string nối trực tiếp. |
| NFR-02.6 | Chống XSS | Escape toàn bộ output HTML. Dùng thư viện DOMPurify phía client. |
| NFR-02.7 | CORS | Chỉ cho phép origin của frontend đã cấu hình. |

## 4.3 Yêu cầu giao diện người dùng (NFR-03)

- Responsive design: hoạt động đúng trên màn hình ≥ 768px (tablet) và ≥ 1024px (desktop). Mobile là optional.

- Calendar grid: 7 cột (T2–CN), trục dọc hiển thị từng khung 30 phút từ 06:00 đến 21:00.

- Phân biệt màu sắc: mỗi môn học được gán 1 màu từ bảng màu cố định (tối thiểu 8 màu dễ phân biệt).

- Accessibility: văn bản có độ tương phản ≥ 4.5:1 theo WCAG 2.1 AA.

## 4.4 Yêu cầu độ tin cậy (NFR-04)

- Hệ thống xử lý đúng các trường hợp biên: sinh viên chọn 1 môn duy nhất, tất cả lớp bị xung đột, không có khung giờ trống cho tự học.

- *[Cập nhật v2.0]* Trường hợp domain rỗng ngay từ đầu (tất cả nhóm lớp thuộc avoid_days) → `generate_schedules()` trả về danh sách rỗng `[]` ngay lập tức mà không vào vòng lặp backtracking.

- Dữ liệu không bị mất khi trình duyệt reload (lưu phương án đã chọn vào DB, không chỉ lưu state phía client).

## 4.5 Yêu cầu bảo trì (NFR-05)

- Mã nguồn backend tổ chức theo cấu trúc: /routers, /models, /enums, /demo, /tests.

- Mỗi hàm logic phức tạp (thuật toán phát hiện xung đột, tính điểm, CSP) phải có unit test riêng với coverage ≥ 90%.

- README.md mô tả đầy đủ cách cài đặt và chạy dự án trong môi trường local.

# CHƯƠNG 5: THIẾT KẾ CƠ SỞ DỮ LIỆU

## 5.1 Tổng quan lược đồ

*[Cập nhật v2.0]* Cơ sở dữ liệu gồm **12 bảng** quan hệ (tăng từ 9 bảng trong v1.0), thiết kế theo dạng chuẩn hóa 3NF. Ba bảng bổ sung so với v1.0: `enrollments`, `study_sessions`, `token_blacklist`.

*Ghi chú ERD: Đường liền = quan hệ bắt buộc (NOT NULL FK); Đường đứt = tùy chọn (NULL FK).*

## 5.2 Mô tả chi tiết các bảng

### 5.2.1 Bảng Semesters (Học kỳ)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| semester_id | VARCHAR(10) | PRIMARY KEY | Mã học kỳ. *[v2.0]* Định dạng thực tế: `"HK2-2025"` |
| name | VARCHAR(50) | NOT NULL | Tên học kỳ, ví dụ: "Học kỳ 1 – 2024/2025" |
| start_date | DATE | NOT NULL | Ngày bắt đầu học kỳ |
| end_date | DATE | NOT NULL, > start_date | Ngày kết thúc học kỳ |
| is_active | BOOLEAN | DEFAULT FALSE | TRUE = học kỳ hiện tại đang diễn ra. Partial unique index đảm bảo chỉ 1 học kỳ active tại một thời điểm. |

### 5.2.2 Bảng Students (Sinh viên)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| student_id | VARCHAR(20) | PRIMARY KEY | Mã số sinh viên (MSSV) |
| name | VARCHAR(100) | NOT NULL | Họ và tên đầy đủ |
| email | VARCHAR(150) | UNIQUE, NOT NULL | Email đại học. *[v2.0]* Validate bằng regex tầng model. |
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

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| class_id | VARCHAR(20) | PRIMARY KEY | Mã nhóm lớp. *[v2.0]* Định dạng thực tế: `"CS03042_LT01_t1"` |
| course_id | VARCHAR(20) | FK → Courses, NOT NULL | Môn học tương ứng |
| semester_id | VARCHAR(10) | FK → Semesters, NOT NULL | Học kỳ mở lớp |
| day_of_week | SMALLINT | NOT NULL, CHECK (2..8) | Thứ (2=T2, 8=CN) |
| start_time | TIME | NOT NULL | Giờ bắt đầu |
| end_time | TIME | NOT NULL, > start_time | Giờ kết thúc |
| room | VARCHAR(50) | NULL | Phòng học |
| instructor | VARCHAR(100) | NULL | Giảng viên (tùy chọn) |
| max_students | SMALLINT | NOT NULL, > 0 | Sĩ số tối đa |

*[Cập nhật v2.0]* Model `ClassSection` trong code bổ sung hai computed field chỉ đọc: `duration_minutes` (tính từ start/end time) và `day_of_week_label` (ví dụ: "Thứ Hai"). Hai field này không lưu vào DB.

### 5.2.5 Bảng Preferences (Sở thích lịch học)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| pref_id | SERIAL | PRIMARY KEY | Mã bản ghi |
| student_id | VARCHAR(20) | FK → Students, UNIQUE | Mỗi sinh viên có 1 bản ghi sở thích |
| preferred_slot | ENUM | ('morning','afternoon','evening') | Khung giờ ưa thích |
| min_break_minutes | SMALLINT | DEFAULT 15, CHECK (≥ 0) | Nghỉ tối thiểu giữa 2 buổi (phút) |
| w_break | DECIMAL(3,2) | DEFAULT **0.40** | Trọng số thành phần khoảng nghỉ |
| w_preference | DECIMAL(3,2) | DEFAULT **0.30** | Trọng số thành phần sở thích |
| w_balance | DECIMAL(3,2) | DEFAULT **0.30** | Trọng số thành phần cân bằng |

*[Cập nhật v2.0]* Trọng số mặc định thay đổi từ `1/3 ≈ 0.33` (v1.0 Tuần 7) sang `w_break=0.40, w_preference=0.30, w_balance=0.30` theo quyết định thiết kế trong quá trình cài đặt. CHECK constraint: `ROUND(w_break + w_preference + w_balance, 2) = 1.00`.

### 5.2.6 Bảng PreferenceAvoidDays (Ngày muốn tránh)

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
| day_of_week | SMALLINT | NULL, CHECK (2..8) | Thứ lặp lại (NULL nếu one-time) |
| start_time | TIME | NOT NULL | Giờ bắt đầu |
| end_time | TIME | NOT NULL, > start_time | Giờ kết thúc |
| is_recurring | BOOLEAN | DEFAULT FALSE | TRUE = lặp hàng tuần |
| note | TEXT | NULL | Ghi chú tùy chọn |

### 5.2.8 Bảng Schedules (Phương án thời khóa biểu) – *[Cập nhật v2.0]*

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| schedule_id | SERIAL | PRIMARY KEY | Mã phương án |
| student_id | VARCHAR(20) | FK → Students | Sinh viên sở hữu |
| semester_id | VARCHAR(10) | FK → Semesters | Học kỳ áp dụng |
| score_total | DECIMAL(5,4) | NOT NULL, [0–1] | Điểm tổng (snapshot tại thời điểm generate) |
| score_break | DECIMAL(5,4) | NOT NULL, [0–1] | Điểm thành phần khoảng nghỉ |
| score_pref | DECIMAL(5,4) | NOT NULL, [0–1] | Điểm thành phần sở thích |
| score_balance | DECIMAL(5,4) | NOT NULL, [0–1] | Điểm thành phần cân bằng |
| **is_draft** | **BOOLEAN** | **DEFAULT TRUE** | **TRUE = chưa lưu chính thức (bản nháp)** |
| is_selected | BOOLEAN | DEFAULT FALSE | Sinh viên đã chọn phương án này |
| **is_active** | **BOOLEAN** | **DEFAULT FALSE** | **Phương án đang hiển thị chính** |
| created_at | TIMESTAMP | DEFAULT NOW() | Thời điểm sinh phương án |

*Ghi chú thiết kế (Denormalization có chủ đích)*: score_total được lưu snapshot vì `w_break`, `w_preference`, `w_balance` trong Preferences có thể thay đổi sau khi generate. Tính lại sau sẽ cho kết quả sai. Đây là vi phạm 3NF có chủ ý và được ghi chú rõ trong code.

Partial unique index: `(student_id, semester_id) WHERE is_active = TRUE` – mỗi sinh viên chỉ có 1 phương án active cho mỗi học kỳ.

### 5.2.9 Bảng ScheduleClasses (Lớp trong phương án)

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| schedule_id | INT | FK → Schedules, ON DELETE CASCADE | Phương án chứa lớp này |
| class_id | VARCHAR(20) | FK → Classes, ON DELETE RESTRICT | Nhóm lớp được chọn |
|  |  | PRIMARY KEY (schedule_id, class_id) | Khóa chính tổng hợp |

### 5.2.10 Bảng Enrollments (Đăng ký môn học) – *[Bổ sung v2.0]*

Bảng này hiện thực hóa luồng UC-03B: sinh viên đăng ký môn học cho học kỳ cụ thể.

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| student_id | VARCHAR(20) | FK → Students, ON DELETE CASCADE | Sinh viên đăng ký |
| course_id | VARCHAR(20) | FK → Courses, ON DELETE RESTRICT | Môn học được đăng ký |
| semester_id | VARCHAR(10) | FK → Semesters, ON DELETE RESTRICT | Học kỳ đăng ký |
| enrolled_at | TIMESTAMP | DEFAULT NOW() | Thời điểm đăng ký |
|  |  | PRIMARY KEY (student_id, course_id, semester_id) | Khóa chính tổng hợp |

### 5.2.11 Bảng StudySessions (Lịch tự học) – *[Bổ sung v2.0, sửa 3NF]*

Lưu các buổi tự học được gợi ý bởi UC-10.

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| session_id | SERIAL | PRIMARY KEY | Mã buổi tự học |
| schedule_id | INT | FK → Schedules, ON DELETE CASCADE | Phương án TKB liên quan |
| course_id | VARCHAR(20) | FK → Courses, ON DELETE RESTRICT | Môn cần tự học |
| day_of_week | SMALLINT | NOT NULL, CHECK (2..8) | Thứ tự học |
| start_time | TIME | NOT NULL | Giờ bắt đầu |
| end_time | TIME | NOT NULL, > start_time | Giờ kết thúc |

*Sửa 3NF*: Cột `student_id` đã được **xóa** khỏi bảng này so với thiết kế ban đầu. Lý do: `student_id` phụ thuộc bắc cầu `session_id → schedule_id → student_id`, vi phạm 3NF. Để lấy `student_id`, dùng JOIN: `SELECT s.student_id FROM schedules s WHERE s.schedule_id = ?`.

### 5.2.12 Bảng TokenBlacklist (Thu hồi JWT) – *[Bổ sung v2.0]*

Lưu các JTI (JWT ID) đã bị thu hồi khi đăng xuất (UC-02).

| **Tên cột** | **Kiểu dữ liệu** | **Ràng buộc** | **Mô tả** |
| --- | --- | --- | --- |
| jti | VARCHAR(36) | PRIMARY KEY | UUID từ JWT payload |
| student_id | VARCHAR(20) | FK → Students, ON DELETE CASCADE | Sinh viên đã đăng xuất |
| revoked_at | TIMESTAMP | DEFAULT NOW() | Thời điểm thu hồi |
| expires_at | TIMESTAMP | NOT NULL | TTL của token gốc – dùng để dọn dẹp định kỳ |

Index trên `expires_at` hỗ trợ cleanup job xóa token hết hạn định kỳ.

## 5.3 Ràng buộc toàn vẹn dữ liệu bổ sung

- CHECK: Tổng ba trọng số `ROUND(w_break + w_preference + w_balance, 2) = 1.00` (thực thi tầng DB và tầng model Pydantic).

- CHECK: `end_time > start_time` trong Classes, PersonalEvents, StudySessions.

- CHECK: `end_date > start_date` trong Semesters.

- CHECK: `day_of_week BETWEEN 2 AND 8` trong Classes, PersonalEvents, PreferenceAvoidDays, StudySessions.

- INDEX: Tạo index trên `(semester_id, course_id)` trong Classes để tăng tốc truy vấn lọc.

- PARTIAL UNIQUE INDEX: `(student_id, semester_id) WHERE is_active = TRUE` trong Schedules – mỗi sinh viên chỉ có 1 phương án active.

- PARTIAL UNIQUE INDEX: `(is_active) WHERE is_active = TRUE` trong Semesters – chỉ 1 học kỳ active tại một thời điểm.

# CHƯƠNG 6: THIẾT KẾ THUẬT TOÁN

## 6.1 Thuật toán phát hiện xung đột

### 6.1.1 Định nghĩa chính thức

Hai nhóm lớp A và B xung đột nếu và chỉ nếu thoả mãn đồng thời ba điều kiện:

**conflict(A, B) ≡  (A.day = B.day)  ∧  (A.start < B.end)  ∧  (B.start < A.end)**

Điều kiện biên: Nếu A.end = B.start → B.start < A.end = FALSE → KHÔNG xung đột.

### 6.1.2 Cấu trúc conflict_set *[Cập nhật v2.0]*

`conflict_set` là `set[tuple[str, str]]` lưu **hai chiều**: khi A xung đột B, cả `(A.class_id, B.class_id)` và `(B.class_id, A.class_id)` đều được thêm vào set. Lý do: MRV có thể chọn môn A trước môn B hoặc ngược lại. Khi tra cứu `(cls.class_id, chosen_cls.class_id)` trong bước backtracking, cả hai thứ tự đều cần trả `True`.

### 6.1.3 Mã giả

```
build_conflict_set(all_sections: List[ClassSection]) → Set[Tuple[str, str]]:
    conflict_set = set()
    FOR i = 0 TO len(all_sections) - 2:
        FOR j = i+1 TO len(all_sections) - 1:
            A = all_sections[i]
            B = all_sections[j]
            IF A.day_of_week == B.day_of_week
               AND A.start_time < B.end_time
               AND B.start_time < A.end_time:
                conflict_set.add((A.class_id, B.class_id))
                conflict_set.add((B.class_id, A.class_id))  # lưu hai chiều
    RETURN conflict_set
```

Độ phức tạp: O(n²). Với n ≤ 50 nhóm lớp thực tế, hoàn thành < 1ms.

## 6.2 Hàm đánh giá Score(S)

### 6.2.1 Công thức tổng hợp

**Score(S) = w_break × F_break(S) + w_preference × F_pref(S) + w_balance × F_balance(S)**

Trong đó: `w_break + w_preference + w_balance = 1.0`; mặc định `w_break = 0.40`, `w_preference = 0.30`, `w_balance = 0.30`.

Mỗi thành phần F ∈ [0.0, 1.0]. Score(S) ∈ [0.0, 1.0]. Phương án tốt hơn có Score cao hơn. Kết quả được làm tròn đến 4 chữ số thập phân.

### 6.2.2 Thành phần F_break – Chất lượng khoảng nghỉ *[Cập nhật v2.0]*

**Bước 1 – Tính gap:** Với mỗi ngày có ≥ 2 buổi học, sắp xếp các buổi theo `start_time` tăng dần, tính:

`gap_i = start_time_{i+1} − end_time_i   (đơn vị: phút)`

**Bước 2 – Nhận dạng khoảng nghỉ thiết kế:** Trường ĐH Công nghệ Sài Gòn có 3 khoảng nghỉ cố định giữa các ca học (tính theo phút từ 00:00):
- Ca 2 → Ca 3: khoảng (570, 575) → nghỉ 5 phút (12:10–12:35)
- Ca 3 → Ca 4: khoảng (725, 755) → nghỉ 30 phút (12:05–12:35)
- Ca 4 → cuối: khoảng (905, 910) → nghỉ 5 phút

Nếu `(end_minute, start_minute)` thuộc một trong các khoảng trên → `gap_score = 1.0` (không áp dụng công thức phạt).

**Bước 3 – Hàm gap_score cho khoảng nghỉ thông thường:**

| **Điều kiện** | **gap_score** | **Ý nghĩa** |
| --- | --- | --- |
| gap < 0 | 0.0 | Xung đột (không hợp lệ) |
| 0 ≤ gap < min_break | gap / min_break | Chưa đủ nghỉ, tăng tuyến tính |
| min_break ≤ gap ≤ 90 | 1.0 | Vùng lý tưởng |
| 90 < gap ≤ 180 | 0.7 | Bỏ trống ~1 ca |
| 180 < gap ≤ 300 | 0.4 | Bỏ trống ~2 ca |
| gap > 300 | 0.1 | Khoảng nghỉ quá dài |

**Bước 4 – Tổng hợp:**

`F_break(S) = clamp(mean(gap_score_i cho tất cả gap), 0.0, 1.0)`

*Nếu không có ngày nào có ≥ 2 buổi (không có gap nào): F_break(S) = 1.0.*

*So sánh với v1.0*: v1.0 dùng `min(gap_i / (2 × min_break), 1.0)` không có phân biệt vùng lý tưởng và không nhận dạng khoảng nghỉ thiết kế của trường.

### 6.2.3 Thành phần F_pref – Độ khớp sở thích *[Cập nhật v2.0]*

Với mỗi nhóm lớp trong phương án:

```
ca_num = số ca của start_time (Ca1: <575 phút, Ca2: <755 phút, Ca3: <910 phút, Ca4: ≥910 phút)
time_score = 1.0 nếu ca_num ∈ preferred_cas; ngược lại = 0.0
day_score  = 0.0 nếu day_of_week ∈ avoid_days; ngược lại = 1.0
class_score = (time_score + day_score) / 2
```

`F_pref(S) = clamp(mean(class_score_i cho tất cả lớp), 0.0, 1.0)`

Ánh xạ preferred_slot → preferred_cas:
- `MORNING` → {Ca1, Ca2} (07:00–12:35)
- `AFTERNOON` → {Ca3, Ca4} (12:35–cuối)
- `EVENING` → {Ca4} (≥ 15:10)

*So sánh với v1.0*: v1.0 dùng binary match (0 hoặc 1 cho mỗi lớp). v2.0 kết hợp time_score và day_score theo trọng số đều (0.5/0.5) cho từng lớp, cho kết quả mịn hơn khi một trong hai tiêu chí được đáp ứng một phần.

### 6.2.4 Thành phần F_balance – Cân bằng khối lượng *[Cập nhật v2.0]*

Đếm số lớp trong mỗi ngày học (`by_day[day] = count`).

```
counts = [by_day[d] for d in active_days]

Nếu len(counts) ≤ 1:
    Nếu tổng số lớp ≤ 1: F_balance = 1.0
    Ngược lại (nhiều lớp dồn 1 ngày): F_balance = 0.0

Ngược lại (≥ 2 ngày học):
    avg      = mean(counts)
    variance = mean((c - avg)² cho mọi c trong counts)   # phương sai quần thể
    F_balance = clamp(max(0.0, 1.0 − variance / 9.0), 0.0, 1.0)
```

Hằng số chuẩn hóa `9.0` tương ứng với trường hợp xấu nhất: 3 lớp dồn 1 ngày trong khi ngày còn lại có 0 lớp, variance = (1.5)² + (1.5)² ≈ ... (thực tế chọn 9.0 là giá trị thực nghiệm cho bài toán 8 môn ÷ 2 ngày cực đoan).

*So sánh với v1.0*: v1.0 dùng `1 − (σ / n_max)` (độ lệch chuẩn chia max). v2.0 dùng `1 − variance / 9.0` (phương sai quần thể với hằng chuẩn hóa), cho kết quả ổn định hơn với số lớp thay đổi.

### 6.2.5 Ví dụ tính Score minh họa

| **Phương án** | **F_break** | **F_pref** | **F_balance** | **Score (w=0.40/0.30/0.30)** |
| --- | --- | --- | --- | --- |
| PA-1 | 0.85 | 0.90 | 0.70 | 0.40×0.85 + 0.30×0.90 + 0.30×0.70 = **0.8200** |
| PA-2 | 0.60 | 0.80 | 0.95 | 0.40×0.60 + 0.30×0.80 + 0.30×0.95 = **0.7650** |
| PA-3 | 0.70 | 0.50 | 0.80 | 0.40×0.70 + 0.30×0.50 + 0.30×0.80 = **0.6700** |

## 6.3 Thuật toán sinh tổ hợp TKB – CSP với MRV + LCV + Forward Checking *[Cập nhật v2.0]*

### 6.3.1 Lý do nâng cấp từ backtracking đơn giản lên CSP đầy đủ

v1.0 đề xuất backtracking đơn giản không có heuristic. Trong quá trình cài đặt, nhóm nhận thấy với 8 môn × 5 nhóm và nhiều ràng buộc avoid_days + PersonalEvents, không gian tìm kiếm có thể lớn hơn dự kiến. CSP với MRV + LCV + Forward Checking giải quyết bằng cách:

- **MRV** (Minimum Remaining Values): Chọn môn có ít nhóm lớp hợp lệ nhất để xử lý trước. Môn có domain nhỏ nhất có khả năng dẫn đến điểm chết cao nhất – xử lý sớm giúp phát hiện nhánh vô nghĩa trước khi đi sâu.
- **LCV** (Least Constraining Value): Sắp xếp nhóm lớp của môn đang xét theo số lượng xung đột với các môn chưa gán, ưu tiên nhóm lớp gây ít ràng buộc nhất cho các môn còn lại.
- **Forward Checking**: Sau mỗi lần gán, loại ngay các nhóm lớp xung đột khỏi domain của các môn chưa xét. Nếu domain nào rỗng → phát hiện dead-end sớm, backtrack ngay.

Thuật toán CSP đầy đủ vẫn hoàn thành trong < 3 giây với 8 môn × 5 nhóm, đáp ứng NFR-01.2.

### 6.3.2 Các kiểu dữ liệu chính

```python
CourseGroups = dict[str, list[ClassSection]]   # {course_id: [tất cả nhóm lớp]}
Domains      = dict[str, list[ClassSection]]   # {course_id: [nhóm lớp còn hợp lệ]}
ConflictSet  = set[tuple[str, str]]            # {(class_id_A, class_id_B)} – hai chiều
Schedule     = dict[str, ClassSection]         # {course_id: nhóm đã chọn}
Removed      = dict[str, list[ClassSection]]   # snapshot để restore sau FC
```

### 6.3.3 Mã giả đầy đủ

```
generate_schedules(course_groups, conflict_set, avoid_days, personal_events,
                   max_solutions=200) → List[Schedule]:

    IF course_groups rỗng: RETURN []

    domains = init_domains(course_groups, avoid_days)
    IF bất kỳ domain nào rỗng: RETURN []   # early exit

    valid_schedules = []
    backtrack({}, list(course_groups.keys()), domains, ...)
    RETURN valid_schedules


init_domains(course_groups, avoid_days):
    domains = {}
    FOR course_id, sections IN course_groups:
        domains[course_id] = [cls FOR cls IN sections
                              IF cls.day_of_week NOT IN avoid_days]
    RETURN domains


choose_next_course(unassigned, domains) → str:   # MRV
    RETURN argmin(len(domains[c]) FOR c IN unassigned)


choose_sections_lcv(course_id, domains, unassigned, conflict_set) → List[ClassSection]:
    FOR cls IN domains[course_id]:
        conflict_count = COUNT(other_cls
                               FOR other_id IN unassigned IF other_id ≠ course_id
                               FOR other_cls IN domains[other_id]
                               IF (cls.class_id, other_cls.class_id) IN conflict_set)
    RETURN sorted by conflict_count ascending


forward_check(cls, unassigned, domains, conflict_set) → (bool, Removed):
    removed = {}
    FOR other_id IN unassigned:
        removed[other_id] = []
        FOR g IN domains[other_id]:
            IF (cls.class_id, g.class_id) IN conflict_set:
                domains[other_id].remove(g)
                removed[other_id].append(g)
        IF domains[other_id] rỗng:
            RETURN False, removed   # dead-end phát hiện sớm
    RETURN True, removed


backtrack(chosen, unassigned, domains, conflict_set, personal_events,
          valid_schedules, max_solutions):

    IF len(valid_schedules) >= max_solutions: RETURN
    IF unassigned rỗng:
        valid_schedules.append(copy(chosen))
        RETURN

    course_id = choose_next_course(unassigned, domains)         # MRV
    next_unassigned = unassigned − {course_id}
    ordered_sections = choose_sections_lcv(course_id, domains,  # LCV
                                           next_unassigned, conflict_set)

    FOR cls IN ordered_sections:
        IF conflicts_with_personal_events(cls, personal_events): CONTINUE
        IF ANY (cls.class_id, chosen[c].class_id) IN conflict_set FOR c IN chosen: CONTINUE

        chosen[course_id] = cls
        ok, removed = forward_check(cls, next_unassigned, domains, conflict_set)  # FC
        IF ok:
            backtrack(chosen, next_unassigned, domains, ...)
        restore_domains(removed, domains)
        DEL chosen[course_id]
        IF len(valid_schedules) >= max_solutions: RETURN
```

### 6.3.4 Lọc PersonalEvents

Chỉ lọc sự kiện thỏa mãn đồng thời: `event.is_recurring == True` **VÀ** `event.day_of_week is not None`. Điều kiện xung đột với lớp học giống UC-06:

`cls.day_of_week == event.day_of_week AND cls.start_time < event.end_time AND event.start_time < cls.end_time`

## 6.4 Thiết kế API (REST)

| **Method** | **Endpoint** | **Mô tả** | **Auth** |
| --- | --- | --- | --- |
| POST | /api/auth/register | Đăng ký tài khoản mới | Public |
| POST | /api/auth/login | Đăng nhập, nhận JWT | Public |
| POST | /api/auth/logout | Đăng xuất, thu hồi JWT vào TokenBlacklist | JWT |
| GET | /api/courses?semester_id= | Lấy danh sách môn theo học kỳ | JWT |
| GET | /api/courses/{id}/classes | Lấy nhóm lớp của 1 môn | JWT |
| POST | /api/enrollments | Lưu danh sách môn đã chọn (Bảng Enrollments) | JWT |
| GET/PUT | /api/preferences | Xem / Cập nhật sở thích cá nhân | JWT |
| GET/POST/DELETE | /api/personal-events | Quản lý lịch bận cá nhân | JWT |
| POST | /api/schedules/generate | Kích hoạt sinh TKB bằng CSP, trả về top 3 | JWT |
| GET | /api/schedules?semester_id= | Lấy danh sách phương án đã sinh | JWT |
| PUT | /api/schedules/{id}/select | Chọn phương án TKB (is_selected=TRUE, is_draft=FALSE) | JWT |
| POST | /api/study-sessions/generate | Sinh lịch tự học (UC-10), lưu vào StudySessions | JWT |

# CHƯƠNG 7: KẾ HOẠCH THỰC HIỆN 3 THÁNG (12 TUẦN)

## 7.1 Phân chia giai đoạn

| **Giai đoạn** | **Thời gian** | **Mục tiêu đầu ra chính** |
| --- | --- | --- |
| Phase 1: Nền tảng | Tuần 1–3 | Môi trường dev, CSDL, xác thực, quản lý dữ liệu môn học |
| Phase 2: Lõi hệ thống | Tuần 4–8 | Thuật toán xung đột + CSP sinh TKB + hàm điểm + calendar UI |
| Phase 3: Hoàn thiện | Tuần 9–11 | Lịch tự học, kiểm thử toàn diện, sửa lỗi |
| Phase 4: Nghiệm thu | Tuần 12 | Deploy demo, hoàn thiện tài liệu, chuẩn bị bảo vệ |

## 7.2 Kế hoạch chi tiết theo tuần

| **Tuần** | **Nội dung công việc** | **Deliverable kiểm tra được** |
| --- | --- | --- |
| 1 | Cài đặt môi trường: Docker, PostgreSQL, FastAPI, React. Tạo repo GitHub. Phân công vai trò. | README cài đặt, repo có cấu trúc thư mục, DB chạy được |
| 2 | Cài đặt tất cả bảng CSDL (12 bảng). Viết migration script (Alembic). Seed dữ liệu test. | Script migration chạy thành công, dữ liệu seed có thể query |
| 3 | Triển khai UC-01, UC-02: Đăng ký, đăng nhập, JWT middleware, TokenBlacklist. API /auth/*. | Postman test pass: đăng ký → đăng nhập → đăng xuất → token bị thu hồi |
| 4 | Triển khai UC-03B (Enrollments), UC-04, UC-05: API chọn môn, sở thích, lịch bận. | API GET/POST /enrollments, /preferences, /personal-events pass test |
| 5 | Triển khai UC-06: build_conflict_set (hai chiều). Unit test ≥ 10 test case. | Unit test pass 100%; conflict_set đúng hai chiều |
| 6 | Triển khai UC-07 phần 1: CSP với MRV + Forward Checking. Sinh tổ hợp hợp lệ. | Generator trả ≥ 1 phương án với input mẫu 8 môn |
| 7 | Triển khai UC-07 phần 2: LCV + hàm Score(S) 3 thành phần. Unit test hàm điểm. | Top 3 phương án sắp xếp đúng; unit test hàm điểm pass |
| 8 | Triển khai UC-08, UC-09: Calendar UI (React), chọn phương án, lưu DB. | UI hiển thị lịch tuần; chọn phương án lưu is_active đúng |
| 9 | Triển khai UC-10: Sinh lịch tự học, lưu StudySessions (không có student_id – 3NF). | Lịch tự học hiển thị trên calendar, không trùng lịch học và lịch bận |
| 10 | Kiểm thử tích hợp end-to-end: Thực hiện 5 luồng test từ đăng ký đến xem TKB. | Test report; ≥ 90% test case pass |
| 11 | Sửa lỗi, tối ưu UX, load test (Locust), viết tài liệu API. | Load test 50 user pass; API doc hoàn chỉnh |
| 12 | Deploy lên VPS/cloud (Render.com hoặc Railway free-tier). Hoàn thiện báo cáo, slide. | URL demo hoạt động; báo cáo + slide sẵn sàng |

## 7.3 Phân công vai trò nhóm (gợi ý cho nhóm 3–4 người)

| **Vai trò** | **Trách nhiệm chính** | **Phase tập trung** |
| --- | --- | --- |
| Backend Developer 1 | CSDL (12 bảng), Auth + TokenBlacklist, API môn học / sở thích / Enrollments | Phase 1–2 |
| Backend Developer 2 | Thuật toán: build_conflict_set, CSP (MRV+LCV+FC), hàm Score(S) | Phase 2 |
| Frontend Developer | React UI, Calendar component, tích hợp API | Phase 2–3 |
| Full-stack / Tích hợp | UC-10 lịch tự học (StudySessions), kiểm thử, deploy, tài liệu | Phase 3–4 |

## 7.4 Ngưỡng rủi ro và phương án dự phòng

| **Rủi ro** | **Xác suất** | **Phương án xử lý** |
| --- | --- | --- |
| CSP chậm với dữ liệu lớn | Thấp | Giới hạn max_solutions (≤ 200 mặc định). MRV+FC đã giảm không gian tìm kiếm đáng kể. |
| React Calendar UI mất nhiều thời gian | Trung bình | Dùng thư viện: react-big-calendar hoặc FullCalendar (MIT License). |
| Không kịp triển khai UC-10 | Trung bình | UC-10 ưu tiên thấp – loại bỏ nếu thiếu thời gian. |
| Deploy gặp lỗi cấu hình | Thấp | Docker Compose để deploy nhanh; backup là demo qua Ngrok. |

# CHƯƠNG 8: KẾ HOẠCH KIỂM THỬ

## 8.1 Kiểm thử đơn vị – Thuật toán xung đột

| **ID** | **Mô tả test case** | **Input** | **Expected Output** |
| --- | --- | --- | --- |
| UT-01 | Hai lớp cùng ngày, giao nhau rõ ràng | A: T2 7:00–9:00 │ B: T2 8:00–10:00 | conflict = TRUE |
| UT-02 | Hai lớp cùng ngày, không giao nhau | A: T2 7:00–9:00 │ B: T2 9:30–11:30 | conflict = FALSE |
| UT-03 | Biên: A kết thúc đúng lúc B bắt đầu | A: T2 7:00–9:00 │ B: T2 9:00–11:00 | conflict = FALSE |
| UT-04 | Khác ngày, cùng khung giờ | A: T2 7:00–9:00 │ B: T3 7:00–9:00 | conflict = FALSE |
| UT-05 | Một lớp chứa hoàn toàn lớp kia | A: T2 7:00–11:30 │ B: T2 8:00–10:00 | conflict = TRUE |
| UT-06 | Danh sách 5 lớp, 1 cặp xung đột | L1..L5, L2 và L4 trùng T3 8:00–10:00 | conflicts = [(L2,L4),(L4,L2)] |
| UT-07 | Không có xung đột nào | 4 lớp, mỗi lớp khác ngày | conflicts = [] |
| UT-08 *[v2.0]* | conflict_set lưu hai chiều | A xung đột B | (A,B) và (B,A) đều trong set |

## 8.2 Kiểm thử đơn vị – Hàm điểm Score(S) *[Cập nhật v2.0]*

| **ID** | **Mô tả** | **Input đặc trưng** | **Expected** |
| --- | --- | --- | --- |
| UT-09 | F_break = 1.0 khi chỉ 1 buổi/ngày | Mỗi ngày học 1 buổi (không có gap) | F_break = 1.0 |
| UT-10 | F_break vùng lý tưởng | gap = 45 phút, min_break = 30 | F_break = 1.0 |
| UT-11 | F_break gap < min_break | gap = 10 phút, min_break = 30 | F_break = 10/30 ≈ 0.333 |
| UT-12 | F_break khoảng nghỉ thiết kế | end=570, start=575 (gap thiết kế) | gap_score = 1.0 |
| UT-13 | F_break gap quá dài | gap = 350 phút | gap_score = 0.1 |
| UT-14 | F_pref = 1.0 tất cả khớp | Tất cả buổi Ca1, prefer=MORNING, không avoid | F_pref = 1.0 |
| UT-15 | F_pref kết hợp time + day | 1 lớp: Ca đúng, ngày tránh | class_score = (1.0+0.0)/2 = 0.5 |
| UT-16 | F_balance = 1.0 phân bổ đều | 4 lớp / 4 ngày (1 lớp/ngày) | variance=0, F_balance=1.0 |
| UT-17 | F_balance = 0.0 dồn 1 ngày | 4 lớp cùng 1 ngày | F_balance = 0.0 |
| UT-18 | Score tổng hợp đúng công thức | F_break=0.8, F_pref=0.6, F_balance=0.7 | Score = 0.40×0.8+0.30×0.6+0.30×0.7 = 0.71 |

## 8.3 Kiểm thử tích hợp CSP *[Cập nhật v2.0]*

| **ID** | **Mô tả** | **Expected** |
| --- | --- | --- |
| IT-CSP-01 | generate_schedules với dữ liệu thực (8 môn) | Trả danh sách, mỗi TKB có đủ 8 môn |
| IT-CSP-02 | Mọi TKB trong kết quả không có xung đột nội bộ | Không tồn tại cặp (A,B) nào trong conflict_set |
| IT-CSP-03 | Không có nhóm lớp thuộc avoid_days | Không có lớp nào có day_of_week ∈ avoid_days |
| IT-CSP-04 | Không có nhóm lớp trùng PersonalEvent lặp lại | Kiểm tra giao nhau với tất cả recurring events |
| IT-CSP-05 | Tôn trọng max_solutions | len(result) ≤ max_solutions |
| IT-CSP-06 | Trả [] khi tất cả ngày đều là avoid_days | avoid_days = [2,3,4,5,6,7,8] → [] |
| IT-CSP-07 | Mỗi phương án là duy nhất | Không có 2 TKB giống hệt nhau |
| IT-CSP-08 | MRV chọn đúng môn ít lựa chọn nhất | Môn có 1 nhóm lớp được gán đầu tiên |
| IT-CSP-09 | Forward Checking phát hiện dead-end | Khi FC loại hết domain → không tiếp tục đệ quy |

## 8.4 Kiểm thử tích hợp end-to-end

| **ID** | **Luồng kiểm thử end-to-end** | **Kết quả kỳ vọng** |
| --- | --- | --- |
| IT-01 | Đăng ký → Đăng nhập → Nhận JWT | Status 200, token hợp lệ |
| IT-02 | Đăng xuất → Token bị thu hồi → Gọi API lại | Status 401 Unauthorized |
| IT-03 | Chọn 3 môn → Phát hiện xung đột → Nhận danh sách conflict | Danh sách đúng, hai chiều |
| IT-04 | Chọn 5 môn (không xung đột) → Sinh TKB → Nhận top 3 phương án | 3 phương án sắp xếp điểm giảm dần, thời gian ≤ 3s |
| IT-05 | Chọn phương án → Xem Calendar → Kiểm tra hiển thị đúng màu | Mỗi môn 1 màu riêng, không bị chồng lên nhau |
| IT-06 | Thêm lịch bận (is_recurring=True) → Sinh TKB mới | Kết quả không chứa nhóm lớp trùng PersonalEvents |
| IT-07 | Thêm lịch bận (is_recurring=False) → Sinh TKB mới | Lịch bận này không ảnh hưởng TKB |

# KẾT LUẬN TÀI LIỆU

Tài liệu SRS v2.0 này cập nhật các điều chỉnh thực tế phát sinh trong quá trình triển khai hệ thống Smart Schedule. Các điểm thay đổi chính so với v1.0:

1. **Cơ sở dữ liệu** – Bổ sung 3 bảng mới: `enrollments` (UC-03B), `study_sessions` (UC-10, sửa 3NF), `token_blacklist` (UC-02 đăng xuất). Bảng `schedules` bổ sung `is_draft` và `is_active`. Tổng 9 → 12 bảng.

2. **Hàm điểm F_break** – Cập nhật theo code thực tế: nhận dạng 3 khoảng nghỉ thiết kế của trường, bảng phân loại gap 5 vùng, hàm `_gap_score()` tuyến tính trong vùng thiếu nghỉ.

3. **Hàm điểm F_pref** – Cập nhật: kết hợp time_score và day_score theo trọng số đều (0.5/0.5), ánh xạ EVENING → Ca4.

4. **Hàm điểm F_balance** – Cập nhật: dùng phương sai quần thể / 9.0 thay vì σ/n_max.

5. **Thuật toán CSP** – Nâng cấp từ backtracking đơn giản lên CSP đầy đủ: MRV (chọn môn ít domain nhất) + LCV (sắp xếp lựa chọn theo ít xung đột) + Forward Checking (lan truyền ràng buộc, phát hiện dead-end sớm).

6. **Nguồn dữ liệu** – Tải từ JSON (`schedule_data_from_web.json`) thay vì nhập thủ công. Định dạng `semester_id` là `"HK2-2025"`.

7. **Trọng số mặc định** – Điều chỉnh từ `1/3` sang `w_break=0.40, w_preference=0.30, w_balance=0.30`.

Nhóm sinh viên cam kết cập nhật tài liệu liên tục song song với quá trình phát triển.

# PHỤ LỤC A: ROADMAP CHI TIẾT 12 TUẦN

Phụ lục này mở rộng Chương 7 với (i) lịch làm việc theo ngày trong từng tuần, (ii) Định nghĩa Hoàn thành (Definition of Done – DoD) cho từng tuần, (iii) các milestone demo M1–M4 gắn với cuối mỗi giai đoạn, và (iv) bản đồ phụ thuộc giữa các tuần. Tất cả tham chiếu Use Case, NFR, và bảng CSDL trong phụ lục đều khớp với các chương từ 3 đến 6.

## A.1 Các milestone chính (M1–M4)

| **Mốc** | **Cuối tuần** | **Tên** | **Tiêu chí chấp nhận (Acceptance)** |
| --- | --- | --- | --- |
| M1 | Tuần 3 | Foundation Ready | Repo có CI chạy; CSDL 12 bảng migrate sạch; UC-01/UC-02 (kể cả logout + TokenBlacklist) chạy end-to-end qua Postman. |
| M2 | Tuần 8 | Core Engine Ready | CSP sinh được ≥ 1 phương án TKB hợp lệ từ input thực; Score(S) trả về top-3 ổn định; calendar UI hiển thị được TKB. |
| M3 | Tuần 11 | Feature Complete | Toàn bộ 10 UC chạy; ≥ 90% test case pass; load test 50 user đạt NFR-01. |
| M4 | Tuần 12 | Release & Defense | URL demo public; báo cáo + slide nộp; nhóm tổng duyệt bảo vệ. |

## A.2 Bản đồ phụ thuộc giữa các tuần

T1 (Môi trường) ⟶ T2 (CSDL 12 bảng) ⟶ T3 (Auth + TokenBlacklist) ⟶ T4 (Enrollments/sở thích/lịch bận)

T4 ⟶ T5 (build_conflict_set hai chiều) ⟶ T6 (CSP MRV+FC) ⟶ T7 (LCV + Score) ⟶ T8 (UI Calendar)

T2 (CSDL) ⟶ T8 (UI cần model ổn định)

T8 ⟶ T9 (UC-10 StudySessions 3NF) ⟶ T10 (Integration test) ⟶ T11 (Bug fix + load test) ⟶ T12

Tuần chặn (blocker weeks): T2, T5, T6, T8.

## A.3 Lịch làm việc theo ngày và Definition of Done

### A.3.1 Phase 1 – Nền tảng (Tuần 1–3)

**Tuần 1 – Khởi tạo môi trường**

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| T2 | Cả nhóm | Họp kickoff: phạm vi, công cụ, quy ước commit | Biên bản kickoff; bảng phân vai |
| T3 | BE1+BE2 | Tạo repo monorepo. Cấu hình .gitignore, README, branch protection | Repo trên GitHub; main được bảo vệ |
| T3 | FE | Khởi tạo React (Vite + TypeScript). ESLint, Prettier | frontend/ build thành công |
| T4 | BE1 | Khởi tạo FastAPI. pre-commit (black, ruff, mypy) | backend/ chạy /health |
| T4 | FS | Docker Compose: postgres, backend, frontend, adminer | docker compose up chạy đủ stack |
| T5 | Cả nhóm | GitHub Actions CI: lint + test cho mỗi PR | CI badge xanh |
| T6 | Cả nhóm | Họp tuần. Demo localhost stack | Ghi chú retro; backlog T2 chia xong |

DoD T1: (a) docker compose up đủ 4 service; (b) CI pass trên main; (c) README ≤ 5 lệnh setup; (d) backlog T2 chia trên Jira/Trello.

**Tuần 2 – CSDL 12 bảng**

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| T2 | BE1 | Migration 001: Semesters, Students, Courses (5.2.1–5.2.3) | Migration 001 chạy up/down |
| T3 | BE1 | Migration 002: Classes, Preferences, PreferenceAvoidDays | Migration 002 pass |
| T4 | BE2 | Migration 003: PersonalEvents, Schedules (+ is_draft, is_active), ScheduleClasses | Migration 003 pass; partial unique index is_active |
| T5 | BE2 | Migration 004: Enrollments, StudySessions (không có student_id), TokenBlacklist | Migration 004 pass; 12 bảng tổng |
| T5 | BE2 | Seed dữ liệu: 1 học kỳ HK2-2025, 8 môn, ~30 nhóm lớp, 2 sinh viên test | make seed chạy < 5 giây |
| T6 | FS+FE | ERD đầy đủ 12 bảng (dbdiagram.io). FE router skeleton | ERD commit vào docs/; 4 route FE trống |

DoD T2: (a) make migrate up && down sạch; (b) seed 12 bảng có dữ liệu; (c) ERD khớp 100% Ch.5.

**Tuần 3 – Auth + TokenBlacklist (UC-01, UC-02)**

| **Ngày** | **Người** | **Công việc** | **Output** |
| --- | --- | --- | --- |
| T2 | BE1 | POST /auth/register: bcrypt, validate email regex, UNIQUE | 201 mới; 409 trùng email |
| T3 | BE1 | POST /auth/login: JWT. POST /auth/logout: ghi JTI vào TokenBlacklist | Login → token; logout → token bị thu hồi |
| T4 | BE2 | JWT middleware: decode, kiểm tra blacklist, gắn current_user. GET /me | /me trả đúng user; token trong blacklist → 401 |
| T5 | FE | Trang Login + Register. Lưu token vào httpOnly cookie | FE đăng ký + đăng nhập + đăng xuất thành công |
| T6 | Cả nhóm | Demo M1 với GVHD | Biên bản M1; action items Phase 2 |

DoD T3/M1: (a) UC-01, UC-02 pass; (b) đăng xuất thu hồi JTI đúng; (c) FE 2 trang hoạt động; (d) demo M1 đạt.

### A.3.2 Phase 2 – Lõi hệ thống (Tuần 4–8)

**Tuần 4 – Enrollments, Sở thích, Lịch bận (UC-03B, UC-04, UC-05)**

DoD T4: 3 nhóm UC pass; Enrollments lưu đúng; Preferences validate tổng weights = 1.0.

**Tuần 5 – build_conflict_set hai chiều (UC-06)**

DoD T5: ≥ 10 unit test pass; conflict_set lưu (A,B) và (B,A); coverage ≥ 90%.

**Tuần 6 – CSP MRV + Forward Checking (UC-07 phần 1)**

DoD T6: Generator trả ≥ 1 TKB hợp lệ; MRV chọn môn ít domain; FC phát hiện dead-end; benchmark 8 môn ≤ 5s.

**Tuần 7 – LCV + Score(S) (UC-07 phần 2)**

DoD T7: LCV sắp xếp đúng; test ví dụ 6.2.5 pass; coverage hàm điểm ≥ 90%; top-3 sort đúng.

**Tuần 8 – Calendar UI + lưu phương án (UC-08, UC-09)**

DoD T8/M2: Calendar hiển thị đúng; is_active partial unique index hoạt động; E2E smoke pass; demo M2 đạt.

### A.3.3 Phase 3 – Hoàn thiện (Tuần 9–11)

**Tuần 9 – StudySessions UC-10 (3NF – không có student_id)**

DoD T9: UC-10 hoạt động hoặc chính thức cắt phạm vi; StudySessions không có student_id; lịch tự học không trùng lịch học/bận.

**Tuần 10 – Kiểm thử tích hợp end-to-end**

DoD T10: ≥ 90% test case pass; E2E chạy trên CI; bug Critical = 0 sau bug bash.

**Tuần 11 – Sửa lỗi, load test, tài liệu**

DoD T11/M3: Load test 50 user đạt NFR-01; Critical bug = 0; API doc + README cập nhật; feature freeze.

### A.3.4 Phase 4 – Nghiệm thu (Tuần 12)

DoD T12/M4: URL demo public ≥ 24h; báo cáo + slide + video nộp đúng hạn; tổng duyệt ≥ 2 lần.

## A.4 Quỹ thời gian dự phòng (Buffer)

| **Phase** | **Buffer ngầm** | **Buffer cứng** | **Cách dùng** |
| --- | --- | --- | --- |
| Phase 1 (T1–3) | Thứ 7 mỗi tuần | Không có | Chạy bù migration nếu CSDL trượt |
| Phase 2 (T4–8) | Thứ 7 mỗi tuần | ½ ngày Thứ 6 tuần 7 | Bù LCV/Score nếu trượt sang tuần 8 |
| Phase 3 (T9–11) | Thứ 7 mỗi tuần | 1 ngày Thứ 6 tuần 11 | Bù bug Critical còn sót |
| Phase 4 (T12) | Thứ 7 | ½ ngày Thứ 5 | Bù lỗi deploy / sự cố hosting |

## A.5 Chỉ số theo dõi tiến độ (KPI)

| **KPI** | **Đo bằng** | **Ngưỡng xanh** | **Ngưỡng đỏ** |
| --- | --- | --- | --- |
| Velocity tuần | % công việc cam kết hoàn thành | ≥ 80% | < 60% hai tuần liên tiếp |
| Bug Critical mở | Số lượng cuối tuần | = 0 | ≥ 3 |
| Coverage thuật toán lõi | pytest --cov | ≥ 90% | < 75% |
| CI fail rate | % PR fail CI / tổng PR | ≤ 15% | ≥ 30% |
| DoD tuần đạt | Có/Không | Đạt 100% mục | Trượt ≥ 1 mục blocker |

**Hết Phụ lục A.**

Trang 1 / 1
