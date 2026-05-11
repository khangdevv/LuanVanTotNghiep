from models import ClassSection, PersonalEvent

CourseGroups = dict[str, list[ClassSection]]    # {course_id: [ClassSection]}
Domains = dict[str, list[ClassSection]]         # {course_id: [ClassSection còn hợp lệ]}
ConflictSet = set[tuple[str, str]]              # {(class_id_A, class_id_B)}
Schedule = dict[str, ClassSection]              # {course_id: ClassSection đã chọn}
Removed = dict[str, list[ClassSection]]         # snapshot để restore sau FC


# 1. Lọc PersonalEvents
def _conflicts_with_personal_events(cls: ClassSection, personal_events: list[PersonalEvent]) -> bool:
    """
    Trả True nếu nhóm lớp trùng giờ với ít nhất một sự kiện cá nhân lặp lại hàng tuần.
    Chỉ xét sự kiện có day_of_week (is_recurring hoặc có thứ cố định).
    """
    for event in personal_events:
        if event.day_of_week is None:
            continue
        if (cls.day_of_week == event.day_of_week
            and cls.start_time < event.end_time
            and event.start_time < cls.end_time):
            return True
    return False


# 2. Khởi tạo domain (lọc avoid_days)
def _init_domains(course_groups: CourseGroups, avoid_days: set[int]) -> Domains:
    """
    Với mỗi môn, loại bỏ ngay các nhóm lớp nằm vào ngày sinh viên muốn tránh.
    Domain còn lại là các lựa chọn hợp lệ trước khi sử dụng backtracking.
    """
    domains: Domains = {}
    for course_id, sections in course_groups.items():
        domains[course_id] = []
        for cls in sections:
            if cls.day_of_week not in avoid_days:
                domains[course_id].append(cls)
    return domains


# 3. MRV : chọn môn ưu tiên
def _choose_next_course(unassigned: list[str], domains: Domains,) -> str:
    """
    MRV chọn môn có ít lựa chọn hợp lệ nhất.
    Môn có domain nhỏ nhất có khả năng dẫn đến điểm chết cao nhất.
    Gán nó sớm sẽ giúp phát hiện và cắt nhánh vô nghĩa trước khi đi sâu.
    """
    min_course = unassigned[0]
    min_size = len(domains[min_course])
    
    for course in unassigned[1:]:
        size = len(domains[course])
        if size < min_size:
            min_size = size
            min_course = course
    return min_course 


# chọn lớp có ít xung đột nhất với các lớp của môn khác
def _choose_next_section_of_course(course_id : str, domains: Domains, unassigned: list[str], conflict_set: ConflictSet) -> list[ClassSection]:
    candidates = domains[course_id]
    
    scored = []
    
    # duyệt nhóm lớp của môn
    for cls in candidates:
        conflict_count = 0
        
        # duyệt các môn chưa được giao
        for other_id in unassigned:
            if other_id == course_id:
                continue
            
            # duyệt nhóm lớp của môn chưa dc giao
            for other_cls in domains[other_id]:
                
                # xung đột thì tính điểm
                if (cls.class_id, other_cls.class_id) in conflict_set:
                    conflict_count += 1
        scored.append((conflict_count, cls))
    
    # sắp xếp theo các lớp có ít xung đột nhất
    scored.sort(key=lambda x: x[0])
    
    # trả về danh sách với môn ít xung đột từ nhỏ đến lớn
    result = []
    for conflict_count, cls in scored:
        result.append(cls)
    return result


# 4. Forward Checking
def _forward_check(cls: ClassSection, unassigned: list[str], domains: Domains, conflict_set: ConflictSet,
) -> tuple[bool, Removed]:
    """
    Sau khi gán một lớp cho môn hiện tại, loại các nhóm lớp xung đột
    khỏi domain của các môn chưa xét (lan truyền ràng buộc).

    Dùng restore dict thay vì deep_copy:
      - Chỉ ghi lại những gì bị xóa
      - restore_domains hoàn tác chính xác, không ảnh hưởng phần tử khác

    Trả về:
      (True,  removed) nếu mọi domain còn ≥ 1 lựa chọn thì sẽ tiếp tục
      (False, removed) nếu có domain rỗng thì sẽ dẫn đến điểm chết, backtrack ngay
    """
    removed: Removed = {}

    for other_id in unassigned:
        removed[other_id] = []
        for g in list(domains[other_id]):
            if (cls.class_id, g.class_id) in conflict_set:
                domains[other_id].remove(g)
                removed[other_id].append(g)

        if len(domains[other_id]) == 0:
            # Dead-end phát hiện sớm giúp trả về ngay, không cần duyệt tiếp
            return False, removed

    return True, removed


def _restore_domains(removed: Removed, domains: Domains) -> None:
    # Hoàn tác forward_check để đưa các nhóm lớp bị loại trở lại domain
    for course_id, classes in removed.items():
        domains[course_id].extend(classes)


# 5. Backtracking chính
def _backtrack(
    chosen: Schedule,
    unassigned: list[str],
    domains: Domains,
    conflict_set: ConflictSet,
    personal_events: list[PersonalEvent],
    valid_schedules: list[Schedule],
    max_solutions: int,
) -> None:
    """
    Đệ quy backtracking với MRV + Forward Checking.
    Luồng mỗi bước:
      1. Nếu đủ max_solutions thì dừng sớm.
      2. Nếu đã gán hết môn thì lưu nghiệm.
      3. MRV chọn môn tiếp theo.
      4. Với mỗi nhóm lớp trong domain của môn đó:
           a. Bỏ qua nếu xung đột PersonalEvents.
           b. Bỏ qua nếu xung đột với môn đã gán (tra conflict_set để kiếm các cặp xung đột).
           c. Gán thử bằng Forward Checking lan truyền ràng buộc.
           d. Nếu môn được chọn chạy được thì đệ quy sâu hơn.
           e. Restore domain rồi thử nhóm lớp tiếp theo (backtrack).
    """
    if len(valid_schedules) >= max_solutions:
        return

    if not unassigned:
        valid_schedules.append(dict(chosen))
        return

    # Bước 3 MRV
    course_id = _choose_next_course(unassigned, domains)
    next_unassigned = [c for c in unassigned if c != course_id]
    
    # Bước 4 - Sử dụng thêm LCV để lựa chọn nhóm lớp có ít xung đột với nhóm lớp các môn khác
    lcv_classess = _choose_next_section_of_course(course_id, domains, next_unassigned, conflict_set)

    for cls in lcv_classess:

        # Bước 4a lọc PersonalEvents
        if _conflicts_with_personal_events(cls, personal_events):
            continue

        # Bước 4b kiểm tra conflict_set với các môn đã gán
        if any((cls.class_id, chosen[c].class_id) in conflict_set for c in chosen):
            continue

        # Bước 4c gán và Forward Checking
        chosen[course_id] = cls
        ok, removed = _forward_check(cls, next_unassigned, domains, conflict_set)

        # Bước 4d đệ quy nếu không có dead-end
        if ok:
            _backtrack(
                chosen, next_unassigned, domains,
                conflict_set, personal_events,
                valid_schedules, max_solutions,
            )

        # Bước 4e restore và thử lựa chọn khác
        _restore_domains(removed, domains)
        del chosen[course_id]

        if len(valid_schedules) >= max_solutions:
            return


# 6. Entry point 
def generate_schedules(
    course_groups: CourseGroups,
    conflict_set: ConflictSet,
    avoid_days: set[int],
    personal_events: list[PersonalEvent],
    max_solutions: int = 200,
) -> list[Schedule]:
    """
    Tham số:
        course_groups   {course_id: [ClassSection]} — tất cả nhóm lớp theo môn
        conflict_set    output của build_conflict_set()
        avoid_days      set day_of_week cần tránh (từ PreferenceAvoidDay)
        personal_events danh sách lịch bận cá nhân (PersonalEvent)
        max_solutions   giới hạn số nghiệm thu thập (tránh bùng nổ tổ hợp)

    Trả về:
        list[dict[course_id → ClassSection]] — mỗi phần tử là một TKB hợp lệ.
        Trả [] nếu không có nghiệm.
    """
    if not course_groups:
        return []

    domains = _init_domains(course_groups, avoid_days)

    # Domain rỗng ngay từ đầu thì sẽ không thể có nghiệm
    if any(len(domains[c]) == 0 for c in domains):
        return []

    valid_schedules: list[Schedule] = []
    _backtrack(
        chosen          = {},
        unassigned      = list(course_groups.keys()),
        domains         = domains,
        conflict_set    = conflict_set,
        personal_events = personal_events,
        valid_schedules = valid_schedules,
        max_solutions   = max_solutions,
    )
    return valid_schedules
