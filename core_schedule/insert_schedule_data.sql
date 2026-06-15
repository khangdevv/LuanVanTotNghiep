-- ============================================================
--  INSERT THOI KHOA BIEU - schedule_data_from_web.json
--  2 hoc ki: HK1-2025 (Hoc ki 1) va HK2-2025 (Hoc ki 2)
--  max_students: random 70-90, giong nhau theo tung mon hoc
-- ============================================================

-- ------------------------------------------------------------
-- 1. Semesters
-- ------------------------------------------------------------
INSERT INTO semesters (semester_id, name, start_date, end_date, is_active)
VALUES ('HK1-2025', 'Hoc ky 1 (2025-2026)', '2026-01-26', '2026-02-28', FALSE)
ON CONFLICT (semester_id) DO NOTHING;
INSERT INTO semesters (semester_id, name, start_date, end_date, is_active)
VALUES ('HK2-2025', 'Hoc ky 2 (2025-2026)', '2026-03-01', '2026-06-15', FALSE)
ON CONFLICT (semester_id) DO NOTHING;

-- ------------------------------------------------------------
-- 2. Courses (17 mon hoc)
-- (max_students theo tung mon: cung mon = cung so)
-- ------------------------------------------------------------
-- Kỹ thuật số -> max_students = 90
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS03001', 'Kỹ thuật số', 2)
ON CONFLICT (course_id) DO NOTHING;
-- Thí nghiệm Kỹ thuật số -> max_students = 73
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS03002', 'Thí nghiệm Kỹ thuật số', 1)
ON CONFLICT (course_id) DO NOTHING;
-- Triển khai hệ thống thông tin -> max_students = 70
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS03042', 'Triển khai hệ thống thông tin', 3)
ON CONFLICT (course_id) DO NOTHING;
-- Xây dựng phần mềm Web -> max_students = 78
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS03043', 'Xây dựng phần mềm Web', 3)
ON CONFLICT (course_id) DO NOTHING;
-- Xây dựng phần mềm Windows -> max_students = 77
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS03044', 'Xây dựng phần mềm Windows', 3)
ON CONFLICT (course_id) DO NOTHING;
-- AI cơ bản và ứng dụng -> max_students = 77
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS03057', 'AI cơ bản và ứng dụng', 3)
ON CONFLICT (course_id) DO NOTHING;
-- Xây dựng phần mềm thiết bị di động -> max_students = 74
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS03058', 'Xây dựng phần mềm thiết bị di động', 3)
ON CONFLICT (course_id) DO NOTHING;
-- Nhập môn lập trình -> max_students = 73
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS09001', 'Nhập môn lập trình', 3)
ON CONFLICT (course_id) DO NOTHING;
-- Thực hành Nhập môn lập trình -> max_students = 87
INSERT INTO courses (course_id, course_name, credits)
VALUES ('CS09002', 'Thực hành Nhập môn lập trình', 1)
ON CONFLICT (course_id) DO NOTHING;
-- Tiếng Anh 2 -> max_students = 72
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS19008', 'Tiếng Anh 2', 2)
ON CONFLICT (course_id) DO NOTHING;
-- Tiếng Anh 4 -> max_students = 88
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS19010', 'Tiếng Anh 4', 2)
ON CONFLICT (course_id) DO NOTHING;
-- Toán A2 (Hàm nhiều biến, giải tích vec tơ) -> max_students = 83
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS33002', 'Toán A2 (Hàm nhiều biến, giải tích vec tơ)', 4)
ON CONFLICT (course_id) DO NOTHING;
-- Vật lý 2 -> max_students = 71
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS43002', 'Vật lý 2', 4)
ON CONFLICT (course_id) DO NOTHING;
-- Thí nghiệm Vật lý_Phần 2 -> max_students = 70
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS49005', 'Thí nghiệm Vật lý_Phần 2', 1)
ON CONFLICT (course_id) DO NOTHING;
-- Triết học Mác - Lênin -> max_students = 72
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS79005', 'Triết học Mác - Lênin', 3)
ON CONFLICT (course_id) DO NOTHING;
-- Kinh tế chính trị Mác - Lênin -> max_students = 76
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS79006', 'Kinh tế chính trị Mác - Lênin', 2)
ON CONFLICT (course_id) DO NOTHING;
-- Giáo dục thể chất 1 -> max_students = 77
INSERT INTO courses (course_id, course_name, credits)
VALUES ('GS93005', 'Giáo dục thể chất 1', 1)  -- so_tc goc = 0, doi thanh 1 de thoa man CHECK (credits > 0)
ON CONFLICT (course_id) DO NOTHING;

-- ------------------------------------------------------------
-- 3. Classes (251 ban ghi = lop x hoc ki)
-- class_id suffix: _s1 = HK1-2025, _s2 = HK2-2025
-- ------------------------------------------------------------

-- -- Hoc ki: HK1-2025
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_01_t7_s1', 'CS03001', 'HK1-2025', 5, '12:35:00', '15:05:00', 'C601', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_02_t10_s1', 'CS03001', 'HK1-2025', 5, '15:10:00', '17:40:00', 'C805', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_03_t7_s1', 'CS03001', 'HK1-2025', 3, '12:35:00', '15:05:00', 'C805', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_04_t10_s1', 'CS03001', 'HK1-2025', 3, '15:10:00', '17:40:00', 'C804', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_05_t4_s1', 'CS03001', 'HK1-2025', 6, '09:35:00', '12:05:00', 'C608', 'T.T.H.Trang', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_06_t4_s1', 'CS03001', 'HK1-2025', 6, '09:35:00', '12:05:00', 'C605', 'N.T.Đê', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_01_t7_s1', 'CS03042', 'HK1-2025', 5, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_03_t1_s1', 'CS03042', 'HK1-2025', 2, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_05_t1_s1', 'CS03042', 'HK1-2025', 3, '07:00:00', '12:05:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_07_t1_s1', 'CS03042', 'HK1-2025', 6, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_09_t7_s1', 'CS03042', 'HK1-2025', 4, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_11_t7_s1', 'CS03042', 'HK1-2025', 3, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_13_t1_s1', 'CS03042', 'HK1-2025', 5, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_15_t1_s1', 'CS03042', 'HK1-2025', 7, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_16_t1_s1', 'CS03042', 'HK1-2025', 5, '07:00:00', '12:05:00', 'PM09_B305', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_18_t7_s1', 'CS03042', 'HK1-2025', 6, '12:35:00', '17:40:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_20_t7_s1', 'CS03042', 'HK1-2025', 4, '12:35:00', '17:40:00', 'PM09_B305', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_22_t7_s1', 'CS03042', 'HK1-2025', 2, '12:35:00', '17:40:00', 'PM09_B305', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_23_t1_s1', 'CS03042', 'HK1-2025', 4, '07:00:00', '12:05:00', 'PM09_B305', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_01_t7_s1', 'CS03043', 'HK1-2025', 2, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_02_t7_s1', 'CS03043', 'HK1-2025', 3, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_03_t7_s1', 'CS03043', 'HK1-2025', 4, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_04_t7_s1', 'CS03043', 'HK1-2025', 5, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_05_t7_s1', 'CS03043', 'HK1-2025', 6, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_06_t1_s1', 'CS03043', 'HK1-2025', 4, '07:00:00', '11:15:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03044_01_t2_s1', 'CS03044', 'HK1-2025', 5, '07:50:00', '12:05:00', 'C703', 'N.T.Tùng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03044_02_t2_s1', 'CS03044', 'HK1-2025', 2, '07:50:00', '12:05:00', 'C705', 'N.T.Tùng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03044_03_t2_s1', 'CS03044', 'HK1-2025', 3, '07:50:00', '12:05:00', 'C703', 'N.T.Tùng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_01_t7_s1', 'CS03057', 'HK1-2025', 4, '12:35:00', '16:50:00', 'C705', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_02_t7_s1', 'CS03057', 'HK1-2025', 2, '12:35:00', '16:50:00', 'C705', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_03_t7_s1', 'CS03057', 'HK1-2025', 3, '12:35:00', '16:50:00', 'C705', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_04_t8_s1', 'CS03057', 'HK1-2025', 7, '13:25:00', '17:40:00', 'C703', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_05_t2_s1', 'CS03057', 'HK1-2025', 5, '07:50:00', '12:05:00', 'C705', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_06_t1_s1', 'CS03057', 'HK1-2025', 2, '07:00:00', '11:15:00', 'C703', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_07_t1_s1', 'CS03057', 'HK1-2025', 5, '07:00:00', '11:15:00', 'C803', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_01_t7_s1', 'CS03058', 'HK1-2025', 3, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_03_t7_s1', 'CS03058', 'HK1-2025', 6, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_05_t1_s1', 'CS03058', 'HK1-2025', 4, '07:00:00', '12:05:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_07_t1_s1', 'CS03058', 'HK1-2025', 3, '07:00:00', '11:15:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_09_t8_s1', 'CS03058', 'HK1-2025', 4, '13:25:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_11_t1_s1', 'CS03058', 'HK1-2025', 6, '07:00:00', '12:05:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_01_t10_s1', 'CS09001', 'HK1-2025', 5, '15:10:00', '17:40:00', 'C601', 'T.Q.Trường', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_02_t7_s1', 'CS09001', 'HK1-2025', 5, '12:35:00', '15:05:00', 'C805', 'T.Q.Trường', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_03_t10_s1', 'CS09001', 'HK1-2025', 3, '15:10:00', '17:40:00', 'C805', 'N.T.N.Hà', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_04_t7_s1', 'CS09001', 'HK1-2025', 3, '12:35:00', '15:05:00', 'C804', 'N.T.N.Hà', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_05_t7_s1', 'CS09001', 'HK1-2025', 4, '12:35:00', '15:05:00', 'C708', 'B.N.Bằng', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_06_t1_s1', 'CS09001', 'HK1-2025', 6, '07:00:00', '09:30:00', 'C605', 'T.T.N.ý', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_15_t4_s1', 'GS19008', 'HK1-2025', 6, '09:35:00', '12:05:00', 'C305', 'P.T.Ngọc', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_16_t1_s1', 'GS19008', 'HK1-2025', 6, '07:00:00', '09:30:00', 'C305', 'P.T.Ngọc', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_17_t4_s1', 'GS19008', 'HK1-2025', 6, '09:35:00', '12:05:00', 'C303', 'N.H.M.Thanh', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_18_t1_s1', 'GS19008', 'HK1-2025', 7, '07:00:00', '09:30:00', 'C303', 'T.L.Tâm', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_19_t4_s1', 'GS19008', 'HK1-2025', 7, '09:35:00', '12:05:00', 'C303', 'T.L.Tâm', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_20_t7_s1', 'GS19008', 'HK1-2025', 7, '12:35:00', '15:05:00', 'C303', 'T.X.N.Bách', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_21_t1_s1', 'GS19008', 'HK1-2025', 2, '07:00:00', '09:30:00', 'C305', 'V.B.Khanh', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_22_t4_s1', 'GS19008', 'HK1-2025', 2, '09:35:00', '12:05:00', 'C305', 'V.B.Khanh', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_23_t4_s1', 'GS19008', 'HK1-2025', 2, '09:35:00', '12:05:00', 'C307', 'T.V.Viễn', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19010_07_t1_s1', 'GS19010', 'HK1-2025', 4, '07:00:00', '09:30:00', 'C303', 'N.H.M.Thanh', 88)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_03_t2_s1', 'GS33002', 'HK1-2025', 3, '07:50:00', '11:15:00', 'C601', 'N.T.T.Phương', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_04_t2_s1', 'GS33002', 'HK1-2025', 7, '07:50:00', '11:15:00', 'C803', 'N.T.T.Phương', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_05_t7_s1', 'GS33002', 'HK1-2025', 6, '12:35:00', '16:00:00', 'C805', 'T.N.Hội', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_06_t8_s1', 'GS33002', 'HK1-2025', 4, '13:25:00', '16:50:00', 'C804', 'T.N.An', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_07_t1_s1', 'GS33002', 'HK1-2025', 4, '07:00:00', '10:25:00', 'C806', 'T.N.Hội', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_08_t8_s1', 'GS33002', 'HK1-2025', 2, '13:25:00', '16:50:00', 'C808', 'T.N.An', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_01_t2_s1', 'GS43002', 'HK1-2025', 7, '07:50:00', '11:15:00', 'C601', 'H.A.Tấn', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_02_t8_s1', 'GS43002', 'HK1-2025', 4, '13:25:00', '16:50:00', 'C803', 'C.T.M.Dung', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_03_t8_s1', 'GS43002', 'HK1-2025', 5, '13:25:00', '16:50:00', 'C605', 'N.N.Phương', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_04_t8_s1', 'GS43002', 'HK1-2025', 6, '13:25:00', '16:50:00', 'C804', 'P.N.T.(ly)', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_05_t8_s1', 'GS43002', 'HK1-2025', 2, '13:25:00', '16:50:00', 'C804', 'P.N.T.(ly)', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_06_t2_s1', 'GS43002', 'HK1-2025', 5, '07:50:00', '11:15:00', 'C808', 'N.N.Phương', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_01_t1_s1', 'GS49005', 'HK1-2025', 4, '07:00:00', '09:30:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_02_t4_s1', 'GS49005', 'HK1-2025', 4, '09:35:00', '12:05:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_03_t4_s1', 'GS49005', 'HK1-2025', 6, '09:35:00', '12:05:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_04_t4_s1', 'GS49005', 'HK1-2025', 3, '09:35:00', '12:05:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_05_t7_s1', 'GS49005', 'HK1-2025', 6, '12:35:00', '15:05:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_07_t7_s1', 'GS79005', 'HK1-2025', 2, '12:35:00', '16:50:00', 'C601', 'P.T.B.Trâm', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_08_t8_s1', 'GS79005', 'HK1-2025', 3, '13:25:00', '17:40:00', 'C803', 'V.V.Mười', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_09_t1_s1', 'GS79005', 'HK1-2025', 2, '07:00:00', '11:15:00', 'C601', 'D.T.T.Thơ', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_10_t7_s1', 'GS79005', 'HK1-2025', 5, '12:35:00', '16:50:00', 'C804', 'A.T.N.Trinh', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_11_t7_s1', 'GS79005', 'HK1-2025', 7, '12:35:00', '16:50:00', 'C806', 'N.T.H.Phương', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_14_t2_s1', 'GS79005', 'HK1-2025', 7, '07:50:00', '12:05:00', 'C808', 'N.V.H.(cb)', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_15_t8_s1', 'GS93005', 'HK1-2025', 4, '13:25:00', '16:50:00', 'SAN_1', 'T.V.Tú', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_16_t2_s1', 'GS93005', 'HK1-2025', 2, '07:50:00', '11:15:00', 'SAN_1', 'N.V.Hồng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_17_t2_s1', 'GS93005', 'HK1-2025', 5, '07:50:00', '11:15:00', 'SAN_1', 'L.G.Hán', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_18_t8_s1', 'GS93005', 'HK1-2025', 2, '13:25:00', '16:50:00', 'SAN_1', 'T.V.Tú', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_19_t2_s1', 'GS93005', 'HK1-2025', 3, '07:50:00', '11:15:00', 'SAN_1', 'T.V.Tú', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_20_t8_s1', 'GS93005', 'HK1-2025', 4, '13:25:00', '16:50:00', 'SAN_2', 'T.B.Hoài', 77)
ON CONFLICT (class_id) DO NOTHING;

-- -- Hoc ki: HK2-2025
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_01_t7_s2', 'CS03001', 'HK2-2025', 5, '12:35:00', '15:05:00', 'C601', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_02_t10_s2', 'CS03001', 'HK2-2025', 5, '15:10:00', '17:40:00', 'C805', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_03_t7_s2', 'CS03001', 'HK2-2025', 3, '12:35:00', '15:05:00', 'C805', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_04_t10_s2', 'CS03001', 'HK2-2025', 3, '15:10:00', '17:40:00', 'C804', 'V.X.Thịnh', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_05_t4_s2', 'CS03001', 'HK2-2025', 6, '09:35:00', '12:05:00', 'C608', 'T.T.H.Trang', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03001_06_t4_s2', 'CS03001', 'HK2-2025', 6, '09:35:00', '12:05:00', 'C605', 'N.T.Đê', 90)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_01_t1_s2', 'CS03002', 'HK2-2025', 2, '07:00:00', '09:30:00', 'B202', 'T.H.P.Thuận', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_02_t4_s2', 'CS03002', 'HK2-2025', 2, '09:35:00', '12:05:00', 'B202', 'H.X.Dương', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_03_t1_s2', 'CS03002', 'HK2-2025', 4, '07:00:00', '09:30:00', 'B202', 'T.H.P.Thuận', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_04_t7_s2', 'CS03002', 'HK2-2025', 2, '12:35:00', '15:05:00', 'B202', 'T.H.P.Thuận', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_05_t10_s2', 'CS03002', 'HK2-2025', 2, '15:10:00', '17:40:00', 'B202', 'T.H.P.Thuận', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_06_t7_s2', 'CS03002', 'HK2-2025', 4, '12:35:00', '15:05:00', 'A307', 'N.V.Thùy', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_07_t10_s2', 'CS03002', 'HK2-2025', 4, '15:10:00', '17:40:00', 'A307', 'N.V.Thùy', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_08_t4_s2', 'CS03002', 'HK2-2025', 4, '09:35:00', '12:05:00', 'B202', 'T.H.P.Thuận', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_09_t1_s2', 'CS03002', 'HK2-2025', 6, '07:00:00', '09:30:00', 'A307', 'H.X.Dương', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_10_t4_s2', 'CS03002', 'HK2-2025', 6, '09:35:00', '12:05:00', 'A307', 'H.X.Dương', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_11_t1_s2', 'CS03002', 'HK2-2025', 5, '07:00:00', '09:30:00', 'B202', 'Đ.Đ.Quang', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_12_t4_s2', 'CS03002', 'HK2-2025', 5, '09:35:00', '12:05:00', 'B202', 'Đ.Đ.Quang', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_13_t7_s2', 'CS03002', 'HK2-2025', 3, '12:35:00', '15:05:00', 'B202', 'H.X.Dương', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_14_t1_s2', 'CS03002', 'HK2-2025', 3, '07:00:00', '09:30:00', 'A307', 'T.T.H.Trang', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03002_15_t4_s2', 'CS03002', 'HK2-2025', 3, '09:35:00', '12:05:00', 'A307', 'T.T.H.Trang', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_01_t7_s2', 'CS03042', 'HK2-2025', 5, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_02_t7_s2', 'CS03042', 'HK2-2025', 5, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_03_t1_s2', 'CS03042', 'HK2-2025', 2, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_03_t2_s2', 'CS03042', 'HK2-2025', 2, '07:50:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_04_t1_s2', 'CS03042', 'HK2-2025', 2, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_05_t1_s2', 'CS03042', 'HK2-2025', 3, '07:00:00', '12:05:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_05_t2_s2', 'CS03042', 'HK2-2025', 3, '07:50:00', '12:05:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_06_t1_s2', 'CS03042', 'HK2-2025', 3, '07:00:00', '12:05:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_06_t2_s2', 'CS03042', 'HK2-2025', 3, '07:50:00', '12:05:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_07_t1_s2', 'CS03042', 'HK2-2025', 6, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_07_t2_s2', 'CS03042', 'HK2-2025', 6, '07:50:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_08_t1_s2', 'CS03042', 'HK2-2025', 6, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_09_t7_s2', 'CS03042', 'HK2-2025', 4, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_10_t7_s2', 'CS03042', 'HK2-2025', 4, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_10_t8_s2', 'CS03042', 'HK2-2025', 4, '13:25:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_11_t7_s2', 'CS03042', 'HK2-2025', 3, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_12_t7_s2', 'CS03042', 'HK2-2025', 3, '12:35:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_12_t8_s2', 'CS03042', 'HK2-2025', 3, '13:25:00', '17:40:00', 'PM10_B303', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_13_t1_s2', 'CS03042', 'HK2-2025', 5, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_13_t2_s2', 'CS03042', 'HK2-2025', 5, '07:50:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_14_t1_s2', 'CS03042', 'HK2-2025', 5, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_15_t1_s2', 'CS03042', 'HK2-2025', 7, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_15_t2_s2', 'CS03042', 'HK2-2025', 7, '07:50:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_16_t1_s2', 'CS03042', 'HK2-2025', 5, '07:00:00', '12:05:00', 'PM09_B305', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_16_t2_s2', 'CS03042', 'HK2-2025', 5, '07:50:00', '12:05:00', 'PM09_B305', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_17_t1_s2', 'CS03042', 'HK2-2025', 5, '07:00:00', '12:05:00', 'PM09_B305', 'N.L.A.Thư', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_18_t7_s2', 'CS03042', 'HK2-2025', 6, '12:35:00', '17:40:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_19_t7_s2', 'CS03042', 'HK2-2025', 6, '12:35:00', '17:40:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_20_t7_s2', 'CS03042', 'HK2-2025', 4, '12:35:00', '17:40:00', 'PM09_B305', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_21_t1_s2', 'CS03042', 'HK2-2025', 7, '07:00:00', '12:05:00', 'PM10_B303', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_22_t7_s2', 'CS03042', 'HK2-2025', 2, '12:35:00', '17:40:00', 'PM09_B305', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_23_t1_s2', 'CS03042', 'HK2-2025', 4, '07:00:00', '12:05:00', 'PM09_B305', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03042_23_t2_s2', 'CS03042', 'HK2-2025', 4, '07:50:00', '12:05:00', 'PM09_B305', 'L.T.M.Dung', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_01_t7_s2', 'CS03043', 'HK2-2025', 2, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_02_t7_s2', 'CS03043', 'HK2-2025', 3, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_03_t7_s2', 'CS03043', 'HK2-2025', 4, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_04_t7_s2', 'CS03043', 'HK2-2025', 5, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_05_t7_s2', 'CS03043', 'HK2-2025', 6, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_06_t1_s2', 'CS03043', 'HK2-2025', 4, '07:00:00', '11:15:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03043_07_t7_s2', 'CS03043', 'HK2-2025', 2, '12:35:00', '16:50:00', 'C703', 'T.V.Hùng', 78)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03044_01_t2_s2', 'CS03044', 'HK2-2025', 5, '07:50:00', '12:05:00', 'C703', 'N.T.Tùng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03044_02_t2_s2', 'CS03044', 'HK2-2025', 2, '07:50:00', '12:05:00', 'C705', 'N.T.Tùng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03044_03_t2_s2', 'CS03044', 'HK2-2025', 3, '07:50:00', '12:05:00', 'C703', 'N.T.Tùng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_01_t7_s2', 'CS03057', 'HK2-2025', 4, '12:35:00', '16:50:00', 'C705', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_02_t7_s2', 'CS03057', 'HK2-2025', 2, '12:35:00', '16:50:00', 'C705', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_03_t7_s2', 'CS03057', 'HK2-2025', 3, '12:35:00', '16:50:00', 'C705', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_04_t8_s2', 'CS03057', 'HK2-2025', 7, '13:25:00', '17:40:00', 'C703', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_05_t2_s2', 'CS03057', 'HK2-2025', 5, '07:50:00', '12:05:00', 'C705', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_06_t1_s2', 'CS03057', 'HK2-2025', 2, '07:00:00', '11:15:00', 'C703', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_07_t1_s2', 'CS03057', 'HK2-2025', 5, '07:00:00', '11:15:00', 'C803', 'L.A.Vinh', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_08_t1_s2', 'CS03057', 'HK2-2025', 2, '07:00:00', '11:15:00', 'C703', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03057_08_t2_s2', 'CS03057', 'HK2-2025', 5, '07:50:00', '12:05:00', 'C705', 'H.Khuê', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_01_t7_s2', 'CS03058', 'HK2-2025', 3, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_01_t8_s2', 'CS03058', 'HK2-2025', 3, '13:25:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_02_t7_s2', 'CS03058', 'HK2-2025', 3, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_02_t8_s2', 'CS03058', 'HK2-2025', 3, '13:25:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_03_t7_s2', 'CS03058', 'HK2-2025', 6, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_03_t8_s2', 'CS03058', 'HK2-2025', 6, '13:25:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_04_t7_s2', 'CS03058', 'HK2-2025', 6, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_05_t1_s2', 'CS03058', 'HK2-2025', 4, '07:00:00', '12:05:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_06_t1_s2', 'CS03058', 'HK2-2025', 4, '07:00:00', '12:05:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_07_t1_s2', 'CS03058', 'HK2-2025', 3, '07:00:00', '11:15:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_08_t1_s2', 'CS03058', 'HK2-2025', 3, '07:00:00', '11:15:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_09_t7_s2', 'CS03058', 'HK2-2025', 4, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_09_t8_s2', 'CS03058', 'HK2-2025', 4, '13:25:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_10_t7_s2', 'CS03058', 'HK2-2025', 4, '12:35:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_10_t8_s2', 'CS03058', 'HK2-2025', 4, '13:25:00', '17:40:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_11_t1_s2', 'CS03058', 'HK2-2025', 6, '07:00:00', '12:05:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS03058_11_t2_s2', 'CS03058', 'HK2-2025', 6, '07:50:00', '12:05:00', 'PM11_B301', 'H.Khuê', 74)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_01_t10_s2', 'CS09001', 'HK2-2025', 5, '15:10:00', '17:40:00', 'C601', 'T.Q.Trường', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_02_t7_s2', 'CS09001', 'HK2-2025', 5, '12:35:00', '15:05:00', 'C805', 'T.Q.Trường', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_03_t10_s2', 'CS09001', 'HK2-2025', 3, '15:10:00', '17:40:00', 'C805', 'N.T.N.Hà', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_04_t7_s2', 'CS09001', 'HK2-2025', 3, '12:35:00', '15:05:00', 'C804', 'N.T.N.Hà', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_05_t7_s2', 'CS09001', 'HK2-2025', 4, '12:35:00', '15:05:00', 'C708', 'B.N.Bằng', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09001_06_t1_s2', 'CS09001', 'HK2-2025', 6, '07:00:00', '09:30:00', 'C605', 'T.T.N.ý', 73)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_01_t4_s2', 'CS09002', 'HK2-2025', 2, '09:35:00', '12:05:00', 'PM02_B308', 'T.Q.Trường', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_02_t1_s2', 'CS09002', 'HK2-2025', 2, '07:00:00', '09:30:00', 'PM02_B308', 'T.Q.Trường', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_03_t4_s2', 'CS09002', 'HK2-2025', 4, '09:35:00', '12:05:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_04_t10_s2', 'CS09002', 'HK2-2025', 2, '15:10:00', '17:40:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_05_t7_s2', 'CS09002', 'HK2-2025', 2, '12:35:00', '15:05:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_06_t10_s2', 'CS09002', 'HK2-2025', 4, '15:10:00', '17:40:00', 'PM02_B308', 'T.Q.Trường', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_07_t7_s2', 'CS09002', 'HK2-2025', 4, '12:35:00', '15:05:00', 'PM02_B308', 'T.Q.Trường', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_08_t1_s2', 'CS09002', 'HK2-2025', 4, '07:00:00', '09:30:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_09_t4_s2', 'CS09002', 'HK2-2025', 6, '09:35:00', '12:05:00', 'PM02_B308', 'T.Q.Trường', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_10_t1_s2', 'CS09002', 'HK2-2025', 6, '07:00:00', '09:30:00', 'PM02_B308', 'T.Q.Trường', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_11_t4_s2', 'CS09002', 'HK2-2025', 5, '09:35:00', '12:05:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_12_t1_s2', 'CS09002', 'HK2-2025', 5, '07:00:00', '09:30:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_13_t10_s2', 'CS09002', 'HK2-2025', 3, '15:10:00', '17:40:00', 'PM02_B308', 'T.Q.Trường', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_14_t4_s2', 'CS09002', 'HK2-2025', 3, '09:35:00', '12:05:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('CS09002_15_t1_s2', 'CS09002', 'HK2-2025', 3, '07:00:00', '09:30:00', 'PM02_B308', 'T.T.M.Huỳnh', 87)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_15_t4_s2', 'GS19008', 'HK2-2025', 6, '09:35:00', '12:05:00', 'C305', 'P.T.Ngọc', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_16_t1_s2', 'GS19008', 'HK2-2025', 6, '07:00:00', '09:30:00', 'C305', 'P.T.Ngọc', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_18_t1_s2', 'GS19008', 'HK2-2025', 7, '07:00:00', '09:30:00', 'C303', 'T.L.Tâm', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_19_t4_s2', 'GS19008', 'HK2-2025', 7, '09:35:00', '12:05:00', 'C303', 'T.L.Tâm', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_20_t7_s2', 'GS19008', 'HK2-2025', 7, '12:35:00', '15:05:00', 'C303', 'T.X.N.Bách', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_21_t1_s2', 'GS19008', 'HK2-2025', 2, '07:00:00', '09:30:00', 'C305', 'V.B.Khanh', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_22_t4_s2', 'GS19008', 'HK2-2025', 2, '09:35:00', '12:05:00', 'C305', 'V.B.Khanh', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19008_23_t4_s2', 'GS19008', 'HK2-2025', 2, '09:35:00', '12:05:00', 'C307', 'T.V.Viễn', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS19010_07_t1_s2', 'GS19010', 'HK2-2025', 4, '07:00:00', '09:30:00', 'C303', 'V.B.Khanh', 88)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_03_t2_s2', 'GS33002', 'HK2-2025', 3, '07:50:00', '11:15:00', 'C601', 'N.T.T.Phương', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_04_t2_s2', 'GS33002', 'HK2-2025', 7, '07:50:00', '11:15:00', 'C803', 'N.T.T.Phương', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_05_t7_s2', 'GS33002', 'HK2-2025', 6, '12:35:00', '16:00:00', 'C805', 'N.T.T.Phương', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_06_t8_s2', 'GS33002', 'HK2-2025', 4, '13:25:00', '16:50:00', 'C804', 'T.N.An', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_07_t1_s2', 'GS33002', 'HK2-2025', 4, '07:00:00', '10:25:00', 'C806', 'T.N.Hội', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS33002_08_t8_s2', 'GS33002', 'HK2-2025', 2, '13:25:00', '16:50:00', 'C808', 'T.N.An', 83)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_01_t2_s2', 'GS43002', 'HK2-2025', 7, '07:50:00', '11:15:00', 'C601', 'H.A.Tấn', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_02_t8_s2', 'GS43002', 'HK2-2025', 4, '13:25:00', '16:50:00', 'C803', 'C.T.M.Dung', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_03_t8_s2', 'GS43002', 'HK2-2025', 5, '13:25:00', '16:50:00', 'C605', 'N.N.Phương', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_04_t8_s2', 'GS43002', 'HK2-2025', 6, '13:25:00', '16:50:00', 'C804', 'P.N.T.(ly)', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_05_t8_s2', 'GS43002', 'HK2-2025', 2, '13:25:00', '16:50:00', 'C804', 'P.N.T.(ly)', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS43002_06_t2_s2', 'GS43002', 'HK2-2025', 5, '07:50:00', '11:15:00', 'C808', 'N.N.Phương', 71)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_01_t1_s2', 'GS49005', 'HK2-2025', 4, '07:00:00', '09:30:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_02_t4_s2', 'GS49005', 'HK2-2025', 4, '09:35:00', '12:05:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_03_t4_s2', 'GS49005', 'HK2-2025', 6, '09:35:00', '12:05:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_04_t4_s2', 'GS49005', 'HK2-2025', 3, '09:35:00', '12:05:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_05_t7_s2', 'GS49005', 'HK2-2025', 6, '12:35:00', '15:05:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_06_t1_s2', 'GS49005', 'HK2-2025', 4, '07:00:00', '09:30:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_07_t4_s2', 'GS49005', 'HK2-2025', 4, '09:35:00', '12:05:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_08_t4_s2', 'GS49005', 'HK2-2025', 6, '09:35:00', '12:05:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_09_t1_s2', 'GS49005', 'HK2-2025', 2, '07:00:00', '09:30:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_10_t4_s2', 'GS49005', 'HK2-2025', 2, '09:35:00', '12:05:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_11_t1_s2', 'GS49005', 'HK2-2025', 6, '07:00:00', '09:30:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_12_t7_s2', 'GS49005', 'HK2-2025', 6, '12:35:00', '15:05:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_13_t4_s2', 'GS49005', 'HK2-2025', 6, '09:35:00', '12:05:00', 'F104', 'H.A.Tấn', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_14_t4_s2', 'GS49005', 'HK2-2025', 4, '09:35:00', '12:05:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS49005_15_t1_s2', 'GS49005', 'HK2-2025', 4, '07:00:00', '09:30:00', 'F104', 'P.N.T.(ly)', 70)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_07_t7_s2', 'GS79005', 'HK2-2025', 2, '12:35:00', '16:50:00', 'C601', 'P.T.B.Trâm', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_08_t8_s2', 'GS79005', 'HK2-2025', 3, '13:25:00', '17:40:00', 'C803', 'V.V.Mười', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_09_t1_s2', 'GS79005', 'HK2-2025', 2, '07:00:00', '11:15:00', 'C601', 'D.T.T.Thơ', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_10_t7_s2', 'GS79005', 'HK2-2025', 5, '12:35:00', '16:50:00', 'C804', 'A.T.N.Trinh', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_11_t7_s2', 'GS79005', 'HK2-2025', 7, '12:35:00', '16:50:00', 'C806', 'N.T.H.Phương', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79005_14_t2_s2', 'GS79005', 'HK2-2025', 7, '07:50:00', '12:05:00', 'C808', 'N.V.H.(cb)', 72)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79006_12_t7_s2', 'GS79006', 'HK2-2025', 2, '12:35:00', '16:50:00', 'C601', 'P.T.B.Trâm', 76)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79006_13_t8_s2', 'GS79006', 'HK2-2025', 3, '13:25:00', '17:40:00', 'C803', 'P.T.B.Trâm', 76)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79006_14_t2_s2', 'GS79006', 'HK2-2025', 2, '07:50:00', '12:05:00', 'C601', 'V.V.Mười', 76)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79006_15_t8_s2', 'GS79006', 'HK2-2025', 5, '13:25:00', '17:40:00', 'C804', 'V.V.Mười', 76)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79006_16_t8_s2', 'GS79006', 'HK2-2025', 7, '13:25:00', '17:40:00', 'C806', 'N.V.H.(cb)', 76)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS79006_19_t2_s2', 'GS79006', 'HK2-2025', 7, '07:50:00', '12:05:00', 'C808', 'N.V.H.(cb)', 76)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_15_t8_s2', 'GS93005', 'HK2-2025', 4, '13:25:00', '16:50:00', 'SAN_1', 'T.V.Tú', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_16_t2_s2', 'GS93005', 'HK2-2025', 2, '07:50:00', '11:15:00', 'SAN_1', 'N.V.Hồng', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_17_t2_s2', 'GS93005', 'HK2-2025', 5, '07:50:00', '11:15:00', 'SAN_1', 'L.G.Hán', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_18_t8_s2', 'GS93005', 'HK2-2025', 2, '13:25:00', '16:50:00', 'SAN_1', 'T.V.Tú', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_19_t2_s2', 'GS93005', 'HK2-2025', 3, '07:50:00', '11:15:00', 'SAN_1', 'T.V.Tú', 77)
ON CONFLICT (class_id) DO NOTHING;
INSERT INTO classes (class_id, course_id, semester_id, day_of_week, start_time, end_time, room, instructor, max_students)
VALUES ('GS93005_20_t8_s2', 'GS93005', 'HK2-2025', 4, '13:25:00', '16:50:00', 'SAN_2', 'T.B.Hoài', 77)
ON CONFLICT (class_id) DO NOTHING;
