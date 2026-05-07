# Pseudocode Core Algorithm (UC-06 / UC-07)

## Mục tiêu
- UC-06: Phát hiện xung đột lịch.
- UC-07: Sinh tổ hợp TKB hợp lệ + chấm điểm + trả top 3.
- Hướng tìm kiếm: **Backtracking + MRV + Forward Checking + Pruning**.
- Dữ liệu đầu vào: lấy từ DB (Classes, Preferences, PersonalEvents) qua service layer.

---

## Kiến trúc 3 tầng tuần tự

```text
[DB] → Tầng 1: build_conflict_set()
     → Tầng 2: generate_schedules() — Backtracking + MRV + FC
     → Tầng 3: score_schedule() → top 3 → lưu DB
```

---

## 1) Tầng 1 — Xây dựng conflict_set (UC-06)

Tính một lần trước khi backtracking, dùng trong suốt quá trình sinh tổ hợp.

```text
FUNCTION build_conflict_set(all_classes: list[ClassSection]) -> set[tuple]:
    """
    UC-06 / SRS 6.1.1: conflict(A,B) khi và chỉ khi
        A.day_of_week == B.day_of_week
        AND A.start_time < B.end_time
        AND B.start_time < A.end_time

    Điều kiện biên: A.end_time == B.start_time → KHÔNG xung đột (dùng strict <).
    Độ phức tạp: O(n²), n ≤ 40 → < 1ms.
    """
    conflict_set = set()

    FOR i FROM 0 TO len(all_classes) - 1:
        FOR j FROM i+1 TO len(all_classes) - 1:
            a = all_classes[i]
            b = all_classes[j]
            IF (a.day_of_week == b.day_of_week
                    AND a.start_time < b.end_time
                    AND b.start_time < a.end_time):
                conflict_set.add((a.class_id, b.class_id))
                conflict_set.add((b.class_id, a.class_id))  # cả hai chiều

    RETURN conflict_set
```

---

## 2) Tầng 2 — Sinh tổ hợp TKB (UC-07 phần 1)

### 2.1 Kiểm tra xung đột với lịch bận cá nhân (UC-05)

```text
FUNCTION conflicts_with_personal_events(cls: ClassSection,
                                        personal_events: list[PersonalEvent]) -> bool:
    FOR event IN personal_events:
        IF event.day_of_week IS NULL:
            CONTINUE                          # sự kiện one-time, bỏ qua
        IF (cls.day_of_week == event.day_of_week
                AND cls.start_time < event.end_time
                AND event.start_time < cls.end_time):
            RETURN TRUE
    RETURN FALSE
```

### 2.2 Khởi tạo domain (lọc avoid_days)

```text
FUNCTION init_domains(course_groups: dict, avoid_days: set[int]) -> dict:
    """
    course_groups: {course_id: list[ClassSection]}
    avoid_days:    set của day_of_week cần tránh (từ PreferenceAvoidDays)
    """
    domains = {}

    FOR course_id, sections IN course_groups:
        domains[course_id] = []
        FOR cls IN sections:
            IF cls.day_of_week NOT IN avoid_days:
                domains[course_id].append(cls)

    RETURN domains
```

### 2.3 MRV — chọn môn ưu tiên

```text
FUNCTION choose_next_course(unassigned: list, domains: dict) -> str:
    """
    MRV (Minimum Remaining Values): chọn môn có ít lựa chọn hợp lệ nhất.
    Phát hiện dead-end sớm, cắt nhánh trước.
    """
    RETURN min(unassigned, key=lambda c: len(domains[c]))
```

### 2.4 Forward Checking

```text
FUNCTION forward_check(cls: ClassSection,
                       unassigned: list,
                       domains: dict,
                       conflict_set: set) -> tuple[bool, dict]:
    """
    Sau khi gán cls cho môn hiện tại, loại các nhóm lớp xung đột
    khỏi domain của các môn chưa xét.

    Dùng restore dict thay vì deep_copy — nhanh hơn, ít tốn bộ nhớ hơn.
    """
    removed = {}

    FOR other_id IN unassigned:
        removed[other_id] = []
        FOR g IN list(domains[other_id]):
            IF (cls.class_id, g.class_id) IN conflict_set:
                domains[other_id].remove(g)
                removed[other_id].append(g)

        IF len(domains[other_id]) == 0:
            RETURN (FALSE, removed)     # dead-end → báo backtrack ngay

    RETURN (TRUE, removed)


FUNCTION restore_domains(removed: dict, domains: dict):
    FOR course_id, classes IN removed:
        domains[course_id].extend(classes)
```

### 2.5 Pruning tín chỉ và ngày (optional — yêu cầu student_type, max_days_per_week)

> **Lưu ý:** Hai hàm này cần `student_type` và `max_days_per_week` chưa có trong bảng
> `Preferences`. Bỏ qua cho đến khi bổ sung hai trường này vào DB.

```text
FUNCTION prune_credit(assigned: dict, unassigned: list,
                      domains: dict, courses_data: dict,
                      credit_min: int, credit_max: int) -> bool:
    current = SUM(courses_data[c][s].credits FOR (c, s) IN assigned)

    IF current > credit_max:
        RETURN TRUE

    min_add = SUM(MIN(cls.credits FOR cls IN domains[u]) FOR u IN unassigned)
    max_add = SUM(MAX(cls.credits FOR cls IN domains[u]) FOR u IN unassigned)

    IF current + min_add > credit_max: RETURN TRUE
    IF current + max_add < credit_min: RETURN TRUE

    RETURN FALSE


FUNCTION prune_days(assigned: dict, unassigned: list,
                    domains: dict, max_days_per_week: int) -> bool:
    used_days = SET(cls.day_of_week FOR cls IN assigned.values())

    IF len(used_days) > max_days_per_week:
        RETURN TRUE

    RETURN FALSE
```

### 2.6 Backtracking chính

```text
FUNCTION backtrack(chosen: dict,
                   unassigned: list,
                   domains: dict,
                   conflict_set: set,
                   personal_events: list,
                   courses: list,
                   valid_schedules: list,
                   max_solutions: int):

    IF len(valid_schedules) >= max_solutions:
        RETURN

    IF unassigned is empty:
        valid_schedules.append(copy(chosen))
        RETURN

    # MRV: chọn môn có domain nhỏ nhất
    course_id = choose_next_course(unassigned, domains)
    next_unassigned = unassigned - {course_id}

    FOR cls IN list(domains[course_id]):

        # Lọc PersonalEvents (UC-05)
        IF conflicts_with_personal_events(cls, personal_events):
            CONTINUE

        # Kiểm tra xung đột với các môn đã gán
        IF ANY (cls.class_id, chosen[c].class_id) IN conflict_set FOR c IN chosen:
            CONTINUE

        chosen[course_id] = cls

        # Forward Checking: lan truyền ràng buộc
        (ok, removed) = forward_check(cls, next_unassigned, domains, conflict_set)

        IF ok:
            backtrack(chosen, next_unassigned, domains, conflict_set,
                      personal_events, courses, valid_schedules, max_solutions)

        restore_domains(removed, domains)
        DEL chosen[course_id]

        IF len(valid_schedules) >= max_solutions:
            RETURN
```

### 2.7 API cho generator

```text
FUNCTION generate_schedules(course_groups: dict,
                             conflict_set: set,
                             preferences: Preference,
                             personal_events: list,
                             max_solutions: int = 200) -> list[dict]:

    avoid_days = {pad.day_of_week FOR pad IN preferences.avoid_days}
    domains = init_domains(course_groups, avoid_days)

    IF ANY len(domains[c]) == 0 FOR c IN domains:
        RETURN []   # domain rỗng → không có nghiệm

    courses = list(course_groups.keys())
    valid_schedules = []

    backtrack(
        chosen          = {},
        unassigned      = courses,
        domains         = domains,
        conflict_set    = conflict_set,
        personal_events = personal_events,
        courses         = courses,
        valid_schedules = valid_schedules,
        max_solutions   = max_solutions,
    )

    RETURN valid_schedules
```

---

## 3) Tầng 3 — Chấm điểm và xếp hạng (UC-07 phần 2)

### 3.1 Ánh xạ giờ → ca học

```text
FUNCTION map_time_to_slot(start_time: time) -> str:
    IF start_time < 12:00: RETURN "morning"
    IF start_time < 17:30: RETURN "afternoon"
    RETURN "evening"
```

### 3.2 F_break — Chất lượng khoảng nghỉ (SRS 6.2.2)

```text
FUNCTION calc_f_break(classes: list[ClassSection],
                      min_break_minutes: int) -> float:
    """
    Với mỗi ngày có ≥ 2 buổi:
        gap_i = start_{i+1} - end_i  (phút)
        f_break_day = mean( min(gap_i / (2 × min_break), 1.0) )
    F_break = mean(f_break_day cho tất cả ngày có ≥ 2 buổi)
    Nếu không có ngày nào ≥ 2 buổi → F_break = 1.0
    """
    sessions_by_day = GROUP classes BY day_of_week, SORT BY start_time

    day_scores = []
    FOR day, sessions IN sessions_by_day:
        IF len(sessions) < 2:
            CONTINUE
        gaps = []
        FOR i FROM 0 TO len(sessions) - 2:
            gap = (sessions[i+1].start_time - sessions[i].end_time).minutes
            gaps.append(min(gap / (2 * min_break_minutes), 1.0))
        day_scores.append(mean(gaps))

    IF day_scores is empty:
        RETURN 1.0
    RETURN mean(day_scores)
```

### 3.3 F_pref — Độ khớp sở thích (SRS 6.2.3)

```text
FUNCTION calc_f_pref(classes: list[ClassSection],
                     preferred_slot: str,
                     avoid_days: set[int]) -> float:
    """
    match_i = 1 nếu buổi học i thuộc khung giờ ưa thích VÀ không học ngày avoid
    F_pref  = (số buổi match) / (tổng số buổi)
    """
    IF classes is empty:
        RETURN 1.0

    match_count = 0
    FOR cls IN classes:
        slot  = map_time_to_slot(cls.start_time)
        day_ok  = cls.day_of_week NOT IN avoid_days
        time_ok = (slot == preferred_slot)
        IF day_ok AND time_ok:
            match_count += 1

    RETURN match_count / len(classes)
```

### 3.4 F_balance — Cân bằng khối lượng (SRS 6.2.4)

```text
FUNCTION calc_f_balance(classes: list[ClassSection]) -> float:
    """
    SRS 6.2.4:
        n_d   = số buổi học trong ngày d
        σ     = độ lệch chuẩn của {n_d}
        n_max = max(n_d)
        F_balance = 1 - (σ / n_max)
        Nếu chỉ 1 ngày học → 0.5
    """
    counts_by_day = COUNT classes GROUP BY day_of_week

    IF len(counts_by_day) <= 1:
        RETURN 0.5

    n_max = max(counts_by_day.values())
    sigma = std_dev(counts_by_day.values())

    RETURN 1.0 - (sigma / n_max)
```

### 3.5 Score tổng hợp (SRS 6.2.1)

```text
FUNCTION score_schedule(chosen: dict, preferences: Preference) -> dict:
    """Score(S) = 0.4×F_break + 0.3×F_pref + 0.3×F_balance"""
    classes   = list(chosen.values())
    avoid_days = {pad.day_of_week FOR pad IN preferences.avoid_days}

    f_break   = calc_f_break(classes, preferences.min_break_minutes)
    f_pref    = calc_f_pref(classes, preferences.preferred_slot, avoid_days)
    f_balance = calc_f_balance(classes)

    total = (preferences.w_break   * f_break
           + preferences.w_preference * f_pref
           + preferences.w_balance * f_balance)

    RETURN {
        total:    total,
        f_break:  f_break,
        f_pref:   f_pref,
        f_balance: f_balance,
    }
```

### 3.6 Xếp hạng Top 3

```text
FUNCTION rank_schedules(valid_schedules: list, preferences: Preference,
                        top_n: int = 3) -> list:
    scored = []
    FOR idx, chosen IN valid_schedules:
        s = score_schedule(chosen, preferences)
        scored.append({
            index:    idx,
            score:    s.total,
            breakdown: s,
            schedule: chosen,
        })

    SORT scored BY score DESC
    RETURN scored[:top_n]
```

---

## 4) End-to-End Flow (service layer)

```text
FUNCTION generate_top3(student_id: str, semester_id: str, db) -> list:

    # 1. Lấy dữ liệu từ DB
    enrollments    = db.query(Enrollment).filter(student_id, semester_id)
    course_groups  = build_course_groups(enrollments, db)   # {course_id: [ClassSection]}
    all_classes    = FLATTEN course_groups.values()
    preferences    = db.query(Preference).filter(student_id).first()
    avoid_days_rows = db.query(PreferenceAvoidDay).filter(pref_id=preferences.pref_id)
    personal_events = db.query(PersonalEvent).filter(student_id)

    IF course_groups is empty:
        RAISE HTTP 404

    # 2. Tầng 1: conflict set
    conflict_set = build_conflict_set(all_classes)

    # 3. Tầng 2: backtracking
    valid_schedules = generate_schedules(
        course_groups   = course_groups,
        conflict_set    = conflict_set,
        preferences     = preferences,   # có .avoid_days từ avoid_days_rows
        personal_events = personal_events,
    )

    IF valid_schedules is empty:
        RAISE HTTP 422

    # 4. Tầng 3: score + top 3
    top3 = rank_schedules(valid_schedules, preferences, top_n=3)

    # 5. Lưu vào Schedules + ScheduleClasses
    FOR rank, entry IN top3:
        save_to_db(student_id, semester_id, entry.schedule,
                   entry.breakdown, rank, db)

    RETURN top3
```

---

## 5) API Endpoint (FastAPI)

```text
POST /api/schedules/generate
    Auth: JWT required
    Body: { semester_id: str }
    SLA:  ≤ 3 giây (NFR-01.2)

FUNCTION handle_generate(semester_id, current_user, db):
    top3 = generate_top3(current_user.student_id, semester_id, db)
    RETURN HTTP 200, { total_valid: len(valid_schedules), top_n: 3, schedules: top3 }
```

---

## 6) Test Checklist

### Tầng 1 — Conflict Detection

- [ ] Cùng thứ + giao giờ → conflict
- [ ] Khác thứ → non-conflict
- [ ] `A.end_time == B.start_time` → non-conflict (điều kiện biên SRS 6.1.1)
- [ ] Kết quả có cả hai chiều `(a,b)` và `(b,a)`

### Tầng 2 — Backtracking

- [ ] Có nghiệm → trả ≥ 1 lịch
- [ ] Vô nghiệm → trả rỗng
- [ ] Mọi lịch output đều không xung đột
- [ ] Không có lịch nào trùng PersonalEvents
- [ ] avoid_days lọc đúng
- [ ] Dừng đúng khi đủ `max_solutions`

### Tầng 3 — Scoring

- [ ] F_break, F_pref, F_balance ∈ [0, 1]
- [ ] Tổng trọng số = 1.0
- [ ] Kết quả sort giảm dần, đúng top 3
- [ ] F_break = 1.0 khi mọi ngày chỉ có 1 buổi
- [ ] F_balance = 0.5 khi chỉ có 1 ngày học
