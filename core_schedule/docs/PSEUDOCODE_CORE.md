# Pseudocode Core Algorithm (UC-06/UC-07)

## Muc tieu
Xay loi thuat toan theo SRS:
- UC-06: Phat hien xung dot lich.
- UC-07: Sinh to hop TKB hop le + cham diem + tra top 3.
- Huong tim kiem: **Backtracking + MRV + Forward Checking + Pruning**.
- Chua dung surrogate model/ML.

---

## 1) Data Loader

```text
FUNCTION load_courses_by_ids(json_path, course_ids):
    raw = read_json(json_path)
    grouped = map[course_id][class_id] -> list(records)

    FOR record IN raw:
        IF record.ma_mh IN course_ids:
            grouped[record.ma_mh][record.nhom_to].append(record)

    result = []
    FOR cid IN course_ids:                   # giu thu tu dau vao
        IF cid NOT IN grouped:
            CONTINUE
        sections = []
        FOR class_id, records IN grouped[cid]:
            sec = build_section(class_id, records)
            sections.append(sec)
        result.append(sections)

    RETURN result
```

```text
FUNCTION build_section(class_id, records):
    first = records[0]
    schedules = []

    FOR rec IN records:
        IF rec.lich_hoc.so_tiet <= 0:
            CONTINUE

        (start_time, end_time) = tiet_to_time(rec.lich_hoc.tiet_bat_dau, rec.lich_hoc.so_tiet)
        (start_date, end_date) = parse_date_range(rec.lich_hoc.thoi_gian)

        schedules.append({
            day_of_week, tiet_bat_dau, so_tiet,
            start_time, end_time, room,
            start_date, end_date
        })

    RETURN {
        class_id, course_id, course_name, credits,
        teacher_name, schedules
    }
```

---

## 2) Conflict Detection

```text
FUNCTION date_ranges_overlap(a_start, a_end, b_start, b_end):
    # Neu thieu ngay thi conservative = overlap
    IF any value missing:
        RETURN TRUE
    RETURN (a_start <= b_end) AND (b_start <= a_end)
```

```text
FUNCTION sessions_overlap(sa, sb):
    IF sa.day_of_week != sb.day_of_week:
        RETURN FALSE

    IF NOT date_ranges_overlap(sa.start_date, sa.end_date, sb.start_date, sb.end_date):
        RETURN FALSE

    RETURN (sa.start_time < sb.end_time) AND (sb.start_time < sa.end_time)
```

```text
FUNCTION sections_conflict(secA, secB):
    FOR sa IN secA.schedules:
        FOR sb IN secB.schedules:
            IF sessions_overlap(sa, sb):
                RETURN TRUE
    RETURN FALSE
```

```text
FUNCTION precompute_conflict_map(courses):
    # courses[i] = list sections of course i
    conflicts = set()

    FOR i FROM 0 TO n-1:
        FOR k FROM i+1 TO n-1:
            FOR j FROM 0 TO len(courses[i])-1:
                FOR l FROM 0 TO len(courses[k])-1:
                    IF sections_conflict(courses[i][j], courses[k][l]):
                        conflicts.add((i,j,k,l))
                        conflicts.add((k,l,i,j))   # doi xung
    RETURN conflicts
```

---

## 3) CSP Generator (Backtracking + MRV + FC + Pruning)

### 3.1 Rang buoc tin chi theo `student_type`

```text
FUNCTION credit_bounds(student_type):
    IF student_type == "normal":
        RETURN (14, +INF)
    IF student_type == "weak":
        RETURN (10, 18)
    IF student_type == "summer":
        RETURN (0, 12)
```

### 3.2 Khoi tao mien gia tri

```text
FUNCTION init_domains(courses, avoid_days):
    domains = map course_idx -> list(section_idx)

    FOR i IN all courses:
        domains[i] = []
        FOR j IN all sections of courses[i]:
            days = section_days(courses[i][j])
            IF days intersects avoid_days:
                CONTINUE
            domains[i].append(j)

    RETURN domains
```

### 3.3 MRV + tie-break by degree

```text
FUNCTION choose_var_mrv(unassigned, domains, conflict_degree):
    min_size = +INF
    cands = []

    FOR v IN unassigned:
        size = len(domains[v])
        IF size < min_size:
            min_size = size
            cands = [v]
        ELSE IF size == min_size:
            cands.append(v)

    IF len(cands) == 1:
        RETURN cands[0]

    # tie-break: bien co degree cao hon
    best = cands[0]
    FOR c IN cands:
        IF conflict_degree[c] > conflict_degree[best]:
            best = c
    RETURN best
```

### 3.4 Forward Checking

```text
FUNCTION forward_check(var_i, sec_j, domains, unassigned, conflict_map):
    next_domains = deep_copy(domains)

    FOR v IN unassigned:
        IF v == var_i:
            CONTINUE

        filtered = []
        FOR s IN next_domains[v]:
            IF (var_i, sec_j, v, s) NOT IN conflict_map:
                filtered.append(s)

        next_domains[v] = filtered

        IF len(filtered) == 0:
            RETURN (FALSE, null)

    RETURN (TRUE, next_domains)
```

### 3.5 Pruning

```text
FUNCTION prune_credit(assigned, domains, courses, credit_min, credit_max):
    current = sum_credits(assigned)

    IF current > credit_max:
        RETURN TRUE

    min_add = 0
    max_add = 0
    FOR u IN unassigned variables:
        credit_candidates = [credits(courses[u][s]) for s IN domains[u]]
        min_add += min(credit_candidates)
        max_add += max(credit_candidates)

    IF current + min_add > credit_max:
        RETURN TRUE

    IF current + max_add < credit_min:
        RETURN TRUE

    RETURN FALSE
```

```text
FUNCTION prune_days(assigned, max_days_per_week):
    used = union_days(assigned)
    IF len(used) > max_days_per_week:
        RETURN TRUE
    RETURN FALSE
```

### 3.6 Backtracking chinh

```text
FUNCTION backtrack(
    assigned, unassigned, domains,
    conflict_map, courses,
    credit_min, credit_max, max_days,
    solutions, max_solutions, conflict_degree
):
    IF len(solutions) >= max_solutions:
        RETURN

    IF unassigned is empty:
        IF credits_ok(assigned, credit_min, credit_max) AND days_ok(assigned, max_days):
            solutions.append(materialize_schedule(assigned, courses))
        RETURN

    IF prune_credit(...):
        RETURN

    IF prune_days(...):
        RETURN

    var = choose_var_mrv(unassigned, domains, conflict_degree)

    FOR sec IN domains[var]:
        ok = TRUE
        FOR (v_assigned -> s_assigned) IN assigned:
            IF (var, sec, v_assigned, s_assigned) IN conflict_map:
                ok = FALSE
                BREAK
        IF NOT ok:
            CONTINUE

        assigned[var] = sec
        next_unassigned = unassigned - {var}

        (fc_ok, next_domains) = forward_check(var, sec, domains, next_unassigned, conflict_map)

        IF fc_ok:
            backtrack(
                assigned, next_unassigned, next_domains,
                conflict_map, courses,
                credit_min, credit_max, max_days,
                solutions, max_solutions, conflict_degree
            )

        remove assigned[var]

        IF len(solutions) >= max_solutions:
            RETURN
```

### 3.7 API cho generator

```text
FUNCTION find_valid_combinations(courses, preferences, max_solutions):
    IF courses invalid OR empty:
        RETURN []

    (credit_min, credit_max) = credit_bounds(preferences.student_type)
    domains = init_domains(courses, preferences.avoid_days)

    IF any domain empty:
        RETURN []

    conflict_map = precompute_conflict_map(courses)
    conflict_degree = compute_conflict_degree(conflict_map, len(courses))

    solutions = []
    backtrack(
        assigned = {},
        unassigned = all course indices,
        domains = domains,
        conflict_map = conflict_map,
        courses = courses,
        credit_min = credit_min,
        credit_max = credit_max,
        max_days = preferences.max_days_per_week,
        solutions = solutions,
        max_solutions = max_solutions,
        conflict_degree = conflict_degree
    )

    RETURN solutions
```

---

## 4) Scoring Function (Rule-based theo SRS)

```text
FUNCTION F_break(schedule, preferences):
    # SRS 6.2.2: f_break_d = mean( min(gap_i / (2 * min_break), 1.0) )
    min_break = preferences.min_break_minutes   # default = 15 (phut)

    day_scores = []

    FOR each day d WITH sessions sorted by start_time (only days with >= 2 sessions):
        gap_scores_d = []
        FOR each adjacent pair (a, b):
            gap = b.start_time - a.end_time     # don vi: phut
            score = min(gap / (2 * min_break), 1.0)
            gap_scores_d.append(score)
        day_scores.append(mean(gap_scores_d))

    IF day_scores empty:
        RETURN 1.0                              # khong co ngay nao >= 2 buoi → khong bi phat
    RETURN mean(day_scores)
```

```text
FUNCTION F_pref(schedule, preferences):
    # SRS 6.2.3: match_i = 1 neu (buoi i thuoc khung gio ua thich VA khong hoc ngay avoid)
    # Tinh per SESSION (toan bo buoi hoc), khong phai per class
    preferred_slot = preferences.preferred_slot   # 'morning' | 'afternoon' | 'evening'
    avoid_days     = preferences.avoid_days       # list ngay muon tranh

    all_sessions = flatten all sessions from every class_item in schedule
    total = len(all_sessions)

    IF total == 0:
        RETURN 1.0

    match_count = 0
    FOR session IN all_sessions:
        slot = time_to_slot(session.start_time)
        # 'morning'   : 06:00–11:30
        # 'afternoon' : 12:00–17:30
        # 'evening'   : 17:30–21:00

        in_preferred = (slot == preferred_slot)
        not_avoided  = (session.day_of_week NOT IN avoid_days)

        IF in_preferred AND not_avoided:        # dieu kien AND, khong phai trung binh
            match_count += 1

    RETURN match_count / total
```

```text
FUNCTION F_balance(schedule):
    # SRS 6.2.4: F_balance = 1 - (sigma / n_max)
    counts = {day: count_sessions(day) for day in study_days(schedule)}

    IF len(counts) == 0:
        RETURN 1.0
    IF len(counts) == 1:
        RETURN 0.5                  # chi 1 ngay hoc → diem trung binh (SRS quy dinh)

    n_max = max(counts.values())
    sigma = std_dev(counts.values())    # do lech chuan (khong phai variance)

    RETURN clamp(1 - sigma / n_max, 0, 1)
```

```text
FUNCTION Score(schedule, preferences):
    b = F_break(schedule, preferences)      # can preferences de doc min_break
    p = F_pref(schedule, preferences)
    w = F_balance(schedule)

    # Trong so lay tu preferences (luu trong bang Preferences o DB)
    # mac dinh: w1=0.4, w2=0.3, w3=0.3; rang buoc: w1+w2+w3 = 1.0
    w1 = preferences.w_break       OR 0.4
    w2 = preferences.w_preference  OR 0.3
    w3 = preferences.w_balance     OR 0.3

    total = w1*b + w2*p + w3*w

    RETURN {
        total,
        break_time: b,
        preference_match: p,
        workload_balance: w
    }
```

---

## 5) Ranking Top 3

```text
FUNCTION rank_schedules(candidates, preferences, top_n = 3):
    scored = []

    FOR idx, sch IN candidates:
        s = Score(sch, preferences)
        scored.append({
            candidate_index: idx,
            score: s.total,
            breakdown: s,
            schedule: sch
        })

    sort scored by score DESC
    RETURN first top_n entries
```

---

## 6) End-to-End Optimize Flow

```text
FUNCTION optimize(request):
    courses = load_courses_by_ids(DATA_PATH, request.course_ids)
    IF courses empty:
        RETURN HTTP 404

    candidates = find_valid_combinations(
        courses = courses,
        preferences = request.preferences,
        max_solutions = request.max_solutions
    )

    IF candidates empty:
        RETURN HTTP 422

    ranked = rank_schedules(candidates, request.preferences, top_n = 3)

    response = {
        total_valid: len(candidates),
        top_n: 3,
        schedules: ranked
    }

    RETURN HTTP 200, response
```

---

## 7) Test Checklist (core-only)

- Conflict:
  - cung thu + giao gio + overlap date range => conflict
  - khac thu => non-conflict
  - cung thu, khong overlap date range => non-conflict
- Generator:
  - co nghiem => tra >= 1 lich
  - vo nghiem => tra rong
  - dung dung `max_solutions`
  - moi lich output deu khong xung dot
- Credit/day constraints:
  - `normal`, `weak`, `summer` dung nguong
  - khong vuot `max_days_per_week`
- Score:
  - tung thanh phan trong [0,1]
  - tong dung w1*b + w2*p + w3*w voi w1+w2+w3=1.0 (mac dinh 0.4/0.3/0.3)
  - sort giam dan dung top 3
  - UT-08: moi ngay chi 1 buoi → F_break = 1.0
  - UT-09: gap=0 phut, min_break=30 → score_gap = min(0/60, 1)=0.0 → F_break = 0.0 < 0.5
  - UT-10: tat ca session khop preferred_slot va khong hoc ngay avoid → F_pref = 1.0
  - UT-11: tat ca session don tu 1 ngay (len(counts)==1) → F_balance = 0.5
           [Luu y: SRS quy dinh 0.5 cho truong hop nay; test case goc ghi "< 0.5" la mau thuan noi bo]
  - UT-12: F_break=0.8, F_pref=0.6, F_balance=0.7 → Score = 0.4*0.8+0.3*0.6+0.3*0.7 = 0.71
