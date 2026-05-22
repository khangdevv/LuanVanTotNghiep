# SmartSchedule — Kiến trúc, Phân công & Quy ước làm việc

> **Phiên bản:** 3 repo · 2 người · 12 tuần
> **Cập nhật:** dựa trên code thực tế `core_schedule/` đã có

---

## Mục lục

1. [Phân vai & phạm vi trách nhiệm](#1-phân-vai--phạm-vi-trách-nhiệm)
2. [Cấu trúc 3 repo](#2-cấu-trúc-3-repo)
3. [Kiến trúc hệ thống](#3-kiến-trúc-hệ-thống)
4. [Quy ước Git — Branch, Commit, Merge](#4-quy-ước-git--branch-commit-merge)
5. [Quy tắc tránh xung đột trong NestJS](#5-quy-tắc-tránh-xung-đột-trong-nestjs)
6. [Chuẩn API — Response format & Error codes](#6-chuẩn-api--response-format--error-codes)
7. [NestJS — Cấu trúc module chi tiết](#7-nestjs--cấu-trúc-module-chi-tiết)
8. [FastAPI Engine — Cấu trúc chi tiết](#8-fastapi-engine--cấu-trúc-chi-tiết)
9. [React — Cấu trúc chi tiết](#9-react--cấu-trúc-chi-tiết)
10. [API Contract Engine ↔ Backend](#10-api-contract-engine--backend)
11. [Kế hoạch theo tuần](#11-kế-hoạch-theo-tuần)

---

## 1. Phân vai & phạm vi trách nhiệm

### Tổng quan

| | **Person A** | **Person B** |
|---|---|---|
| **Đã làm** | — | Python algorithms (CSP, conflicts, scoring) ✅ |
| **Repo chính** | `smartschedule-frontend` | `smartschedule-engine` |
| **Repo phụ** | `smartschedule-backend` (Auth layer) | `smartschedule-backend` (Business layer) |
| **Tech** | React + TypeScript, NestJS Auth | Python FastAPI, NestJS CRUD/Orchestrator |

### Nhiệm vụ Person B — 8 hạng mục còn lại

| # | Hạng mục | Repo | UC |
|---|---|---|---|
| 1 | `main.py` + FastAPI app, CORS, `/health` | engine | — |
| 2 | `routers/schedules.py` — `POST /generate`, `POST /conflicts` | engine | UC-06, UC-07 |
| 3 | `routers/self_study.py` — `POST /suggest-self-study` | engine | UC-10 |
| 4 | `pyproject.toml` + `Dockerfile` | engine | — |
| 5 | `PersonalEventsModule` — CRUD lịch bận | backend | UC-05 |
| 6 | `CoursesModule` + `ClassesModule` — CRUD admin | backend | UC-03 |
| 7 | `SchedulesModule` — orchestrator gọi Engine, lưu kết quả | backend | UC-07, UC-08, UC-10 |
| 8 | `docker-compose.yml` + Deploy NestJS + Engine | backend/infra | — |

### Nhiệm vụ Person A — 17 hạng mục

| # | Hạng mục | Repo | UC |
|---|---|---|---|
| 1 | `nest new backend` + config (`@nestjs/config`, Prisma client) | backend | — |
| 2 | `AuthModule` — register, login, logout, JWT Guards | backend | UC-01, UC-02 |
| 3 | `EnrollmentsModule` — `POST /enrollments` | backend | UC-03 |
| 4 | `PreferencesModule` — `/preferences` + `/avoid-days` | backend | UC-04 |
| 5 | Prisma `schema.prisma` + migrations + `seed.ts` | backend | — |
| 6 | Jest integration tests + Swagger export | backend | — |
| 7 | Vite + TypeScript setup + Router skeleton | frontend | — |
| 8 | `LoginPage` + `RegisterPage` — React Hook Form + Zod | frontend | UC-01, UC-02 |
| 9 | `PreferencesPage` — form sở thích + avoid-days + lịch bận | frontend | UC-04, UC-05 |
| 10 | `GeneratePage` + `CourseSelector` | frontend | UC-07 |
| 11 | `ScheduleCardList` — Top-3, score, badge, `ConflictAlert` | frontend | UC-06, UC-07 |
| 12 | `Calendar` — react-big-calendar, màu theo `course_id` | frontend | UC-08 |
| 13 | `CompareView` — so sánh song song 2–3 phương án | frontend | UC-08 |
| 14 | Lưu phương án — `POST /schedules/:id/save` | frontend | UC-09 |
| 15 | `SelfStudyLayer` — khe tự học nét đứt, toggle | frontend | UC-10 |
| 16 | UX polish — loading skeleton, error toast, Lighthouse ≥ 80 | frontend | — |
| 17 | Playwright E2E (5 kịch bản) + Demo video + Deploy Vercel | frontend | — |

---

## 2. Cấu trúc 3 repo

### Tại sao tách 3 repo?

| Lý do | Chi tiết |
|---|---|
| **Tách ngôn ngữ** | Python (engine) và TypeScript (backend + frontend) là 2 hệ sinh thái khác nhau — không chia sẻ gì |
| **Tách quyền sở hữu** | B chỉ push vào `engine`. A chỉ push vào `frontend`. `backend` chia rõ module ownership |
| **CI độc lập** | Mỗi repo có workflow riêng, không bị trigger nhầm |
| **Deploy độc lập** | Engine → Railway. Backend → Render. Frontend → Vercel |
| **Git history sạch** | Không lẫn commit Python với TypeScript |

### 3 repo trên GitHub

```
GitHub Organization (hoặc personal):
├── smartschedule-engine    ← Person B (Python FastAPI)
├── smartschedule-backend   ← Person A + B (NestJS, module ownership rõ ràng)
└── smartschedule-frontend  ← Person A (React)
```

### `smartschedule-engine` (Person B)

```
smartschedule-engine/
│
├── .github/workflows/ci.yml      ← ruff + mypy + pytest --cov
│
├── csp_generator.py              ← ĐÃ CÓ
├── detect_conflicts.py           ← ĐÃ CÓ
├── scoring_function.py           ← ĐÃ CÓ
├── data_loader.py                ← ĐÃ CÓ (chỉ dùng cho demo)
│
├── models/                       ← ĐÃ CÓ (Pydantic v2)
│   ├── classes.py
│   ├── preferences.py
│   ├── personal_events.py
│   └── ...
│
├── enums/                        ← ĐÃ CÓ
│   └── preferred_slot.py         ← PreferredSlot.MORNING | AFTERNOON
│
├── demo/                         ← ĐÃ CÓ (giữ để test nhanh)
│   └── main.py
│
├── tests/                        ← ĐÃ CÓ (+ thêm test route)
│   ├── conftest.py
│   ├── test_csp_generator.py
│   └── test_routes.py            ← THÊM MỚI
│
├── main.py                       ← THÊM MỚI — FastAPI app entrypoint
├── routers/                      ← THÊM MỚI
│   ├── __init__.py
│   ├── schedules.py              ← POST /generate, POST /conflicts
│   └── self_study.py             ← POST /suggest-self-study
│
├── Dockerfile                    ← THÊM MỚI
├── pyproject.toml                ← THÊM MỚI
└── README.md
```

### `smartschedule-backend` (NestJS — A + B)

```
smartschedule-backend/
│
├── .github/workflows/ci.yml      ← eslint + jest
│
├── src/
│   ├── main.ts                   ← A (bootstrap)
│   ├── app.module.ts             ← A đăng ký module của A, B đăng ký module của B
│   │
│   ├── common/                   ← A khởi tạo — CẢ HAI dùng, KHÔNG tự ý sửa
│   │   ├── decorators/
│   │   │   ├── current-user.decorator.ts
│   │   │   └── roles.decorator.ts
│   │   ├── filters/
│   │   │   └── http-exception.filter.ts
│   │   ├── guards/
│   │   │   ├── jwt-auth.guard.ts
│   │   │   └── roles.guard.ts
│   │   └── interceptors/
│   │       └── response.interceptor.ts   ← chuẩn hóa response format
│   │
│   ├── config/                   ← A khởi tạo
│   │   └── config.module.ts
│   │
│   ├── database/                 ← A khởi tạo (Prisma service)
│   │   ├── prisma.module.ts
│   │   └── prisma.service.ts
│   │
│   │   ── PERSON A SỞ HỮU ────────────────────────────────
│   ├── auth/                     ← A ONLY
│   ├── students/                 ← A ONLY
│   ├── preferences/              ← A ONLY
│   └── enrollments/              ← A ONLY
│   │
│   │   ── PERSON B SỞ HỮU ────────────────────────────────
│   ├── personal-events/          ← B ONLY
│   ├── courses/                  ← B ONLY
│   ├── classes/                  ← B ONLY
│   └── schedules/                ← B ONLY
│       └── engine/
│           └── engine.service.ts ← gọi HTTP đến smartschedule-engine
│
├── prisma/                       ← A khởi tạo
│   ├── schema.prisma
│   ├── seed.ts
│   └── migrations/
│
├── test/                         ← A viết integration tests
├── docker-compose.yml            ← B tạo (dev environment)
├── nest-cli.json
├── tsconfig.json
└── package.json
```

### `smartschedule-frontend` (Person A)

```
smartschedule-frontend/
│
├── .github/workflows/ci.yml      ← eslint + vite build + playwright
│
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── pages/
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── PreferencesPage.tsx
│   │   ├── GeneratePage.tsx
│   │   └── CalendarPage.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── schedule/
│   │   │   ├── ScheduleCardList.tsx
│   │   │   ├── ScheduleCard.tsx
│   │   │   └── ConflictAlert.tsx
│   │   ├── calendar/
│   │   │   ├── ScheduleCalendar.tsx
│   │   │   ├── CompareView.tsx
│   │   │   └── SelfStudyLayer.tsx
│   │   └── forms/
│   │       ├── CourseSelector.tsx
│   │       ├── PreferencesForm.tsx
│   │       └── PersonalEventForm.tsx
│   ├── hooks/
│   ├── services/                 ← axios calls đến smartschedule-backend
│   └── types/
│
├── e2e/                          ← Playwright
├── vite.config.ts
└── package.json
```

---

## 3. Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────┐
│   smartschedule-frontend  (React :5173)                 │
│   Person A                                              │
└──────────────────────────┬──────────────────────────────┘
                           │  HTTPS /api/v1/*
                           │
┌──────────────────────────▼──────────────────────────────┐
│   smartschedule-backend  (NestJS :3000)                 │
│                                                         │
│   A owns: AuthModule, PreferencesModule,                │
│           PersonalEventsModule, EnrollmentsModule        │
│   B owns: CoursesModule, ClassesModule,                 │
│           SchedulesModule → engine.service              │
│                                                         │
│   PrismaService ◄──────────── PostgreSQL :5432          │
└──────────────────────────┬──────────────────────────────┘
                           │  Internal HTTP (JSON)
                           │  POST /generate
                           │  POST /conflicts
                           │  POST /suggest-self-study
┌──────────────────────────▼──────────────────────────────┐
│   smartschedule-engine   (FastAPI :8001)                │
│   Person B                                              │
│                                                         │
│   routers/schedules.py  → csp_generator.py             │
│                            detect_conflicts.py          │
│                            scoring_function.py          │
│   routers/self_study.py → (UC-10)                       │
│                                                         │
│   Stateless — không kết nối DB                          │
└─────────────────────────────────────────────────────────┘
```

### Local dev — Docker Compose (trong `smartschedule-backend/`)

```yaml
# docker-compose.yml
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: smartschedule
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5

  engine:
    build:
      context: ../smartschedule-engine   # clone cạnh nhau
    ports:
      - "8001:8001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 10s
      retries: 3

  backend:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      postgres:
        condition: service_healthy
      engine:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@postgres:5432/smartschedule
      ENGINE_URL: http://engine:8001
      JWT_SECRET: ${JWT_SECRET}
      JWT_EXPIRES_IN: 60m
      JWT_REFRESH_EXPIRES_IN: 7d
    command: ["npm", "run", "start:dev"]
```

---

## 4. Quy ước Git — Branch, Commit, Merge

### 4.1 Mô hình nhánh (Git Flow đơn giản)

```
main          ← production, tag tại mỗi Milestone, KHÔNG push thẳng
│
└── develop   ← integration, tất cả feature merge vào đây
    │
    ├── feature/<mô-tả>          ← task thông thường
    ├── fix/<mô-tả-lỗi>          ← sửa bug trong develop
    ├── hotfix/<mô-tả-lỗi>       ← fix khẩn từ production (main)
    └── release/v<x.y>           ← chuẩn bị Milestone
```

**Quy tắc bảo vệ nhánh:**

| Nhánh | Rule |
|---|---|
| `main` | Chỉ merge từ `release/*` hoặc `hotfix/*`. Require 1 approval. CI phải xanh. |
| `develop` | Merge từ `feature/*` hoặc `fix/*`. Require 1 approval. CI phải xanh. |

### 4.2 Đặt tên nhánh

**Format:** `<type>/<phạm-vi-ngắn>` — viết thường, dùng dấu `-`, không dùng dấu `/` trong phần mô tả.

| Type | Khi nào | Ví dụ |
|---|---|---|
| `feature/` | Tính năng mới | `feature/auth-register-endpoint` |
| `fix/` | Sửa bug trong develop | `fix/calendar-wrong-color-on-reload` |
| `hotfix/` | Fix khẩn từ production | `hotfix/generate-api-500-empty-semester` |
| `release/` | Chuẩn bị Milestone | `release/v0.1` |

> **Quy tắc đặt tên:** Đọc tên nhánh là hiểu ngay làm gì. Không dùng tên chung chung như `feature/update`, `fix/bug`.

### 4.3 Quy ước Commit (Conventional Commits)

**Format:** `<type>(<scope>): <mô tả ngắn, tiếng Anh, viết thường>`

```
feat(auth): add bcrypt hashing on POST /auth/register
fix(calendar): slot color resets after page reload
test(csp): cover adjacent interval edge case n=1
docs(api): update engine contract for generate response
chore(deps): upgrade fastapi to 0.115
refactor(scoring): extract weight constants to config
perf(backtracking): early pruning reduces search by 60%
```

| Type | Khi nào |
|---|---|
| `feat` | Tính năng mới |
| `fix` | Sửa bug |
| `test` | Thêm / sửa test |
| `docs` | Tài liệu, contract |
| `chore` | Config, dependencies, tooling |
| `refactor` | Cải cấu trúc, không đổi hành vi |
| `perf` | Tối ưu hiệu năng |
| `style` | Format, linting (không đổi logic) |

**Scope gợi ý:**

| Repo | Scopes |
|---|---|
| engine | `csp`, `conflict`, `scoring`, `self-study`, `router`, `model` |
| backend | `auth`, `courses`, `classes`, `enrollments`, `preferences`, `events`, `schedules`, `prisma` |
| frontend | `auth`, `calendar`, `schedule`, `preferences`, `form`, `ui` |

> **Commit nhỏ và thường xuyên.** Mỗi commit chỉ làm 1 việc. Không commit "nhiều thứ cùng lúc".

### 4.4 Quy trình làm việc hàng ngày

```bash
# 1. Bắt đầu ngày — đồng bộ develop
git checkout develop && git pull origin develop

# 2. Tạo nhánh cho task hôm nay
git checkout -b feature/auth-login-jwt

# 3. Làm việc, commit thường xuyên
git add -p                                    # stage từng chunk, không add .
git commit -m "feat(auth): add JWT access token on login"

# 4. Cuối ngày — push
git push origin feature/auth-login-jwt

# 5. Khi task xong — mở Pull Request vào develop
#    Title  : [feat] Add JWT login endpoint
#    Body   : checklist, cách test, screenshot nếu UI
#    Label  : person-A hoặc person-B
#    Assign : người kia để review
```

### 4.5 Pull Request — Quy tắc Review

```
Checklist trước khi mở PR:
  □ CI xanh (lint + test pass)
  □ Không có console.log / print bỏ quên
  □ Tên hàm, biến rõ nghĩa
  □ Không commit .env, node_modules, __pycache__
  □ Test đã bao phủ happy path + ít nhất 1 edge case

Quy tắc review:
  • Phải có ít nhất 1 approval trước khi merge
  • Reviewer cần review trong 24h
  • Dùng "Squash and merge" — giữ lịch sử develop gọn
  • Xóa nhánh sau khi merge
```

### 4.6 Merge vào `main` tại Milestone

```bash
# Milestone M1 — cuối Tuần 3
git checkout develop && git pull
git checkout -b release/v0.1
# Fix nhỏ nếu cần, không thêm tính năng
git checkout main
git merge --no-ff release/v0.1
git tag v0.1
git push origin main --tags
git branch -d release/v0.1
```

| Milestone | Thời điểm | Tag | Nội dung |
|---|---|---|---|
| M1 | Cuối Tuần 3 | `v0.1` | Auth hoàn chỉnh |
| M2 | Cuối Tuần 8 | `v0.2` | Generate + Calendar + Save |
| M3 | Cuối Tuần 11 | `v1.0` | Feature freeze |
| M4 | Cuối Tuần 12 | `v1.0-final` | Deploy production |

---

## 5. Quy tắc tránh xung đột trong NestJS

### 5.1 Ownership matrix — ai được sửa file nào

| Thư mục / File | Person A | Person B | Ghi chú |
|---|---|---|---|
| `src/auth/**` | ✅ | ❌ | A ONLY |
| `src/students/**` | ✅ | ❌ | A ONLY |
| `src/preferences/**` | ✅ | ❌ | A ONLY |
| `src/personal-events/**` | ❌ | ✅ | B ONLY |
| `src/courses/**` | ❌ | ✅ | B ONLY |
| `src/classes/**` | ❌ | ✅ | B ONLY |
| `src/enrollments/**` | ✅ | ❌ | A ONLY |
| `src/schedules/**` | ❌ | ✅ | B ONLY |
| `src/database/**` | ✅ | ❌ | A ONLY (Prisma service) |
| `prisma/**` | ✅ | ❌ | A ONLY |
| `src/common/**` | 🤝 | 🤝 | Báo trước khi sửa |
| `src/app.module.ts` | 🤝 | 🤝 | Xem quy tắc bên dưới |
| `src/main.ts` | ✅ | ❌ | A setup ban đầu |
| `src/config/**` | ✅ | ❌ | A setup ban đầu |

### 5.2 Quy tắc `app.module.ts` — tránh merge conflict

```typescript
// app.module.ts — A và B đăng ký module ở 2 block riêng biệt
@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),

    // ── PERSON A MODULES ──────────────────────
    AuthModule,
    StudentsModule,
    PreferencesModule,
    EnrollmentsModule,

    // ── PERSON B MODULES ──────────────────────
    PersonalEventsModule,
    CoursesModule,
    ClassesModule,
    SchedulesModule,
  ],
})
export class AppModule {}
```

> **Quy tắc:** A chỉ thêm/sửa trong block A. B chỉ thêm/sửa trong block B. Không ai sửa block của người kia.

### 5.3 Quy tắc dùng service của nhau

B cần biết student có enrolled môn nào để generate TKB. Thay vì B import trực tiếp `EnrollmentsService` (của A), B định nghĩa interface:

```typescript
// src/schedules/ports/enrollment-reader.interface.ts  (B tạo)
export interface IEnrollmentReader {
  findEnrolledCourseIds(studentId: string, semesterId: string): Promise<string[]>
}

// src/enrollments/enrollments.service.ts  (A implement)
@Injectable()
export class EnrollmentsService implements IEnrollmentReader {
  async findEnrolledCourseIds(studentId: string, semesterId: string) { ... }
}
```

→ B gọi qua interface, không phụ thuộc implementation của A.

### 5.4 Quy tắc Prisma schema

B sở hữu `prisma/schema.prisma`. Khi A cần thêm model liên quan đến Auth:

```
B định nghĩa model nền: Student, Course, Class, ...
A chỉ thêm field vào model Student nếu cần (ví dụ: tokenVersion)
A KHÔNG tự tạo model mới — phải báo B trước
Mọi thay đổi schema cần PR review chéo
```

---

## 6. Chuẩn API — Response format & Error codes

### 6.1 Base URL & Versioning

```
Development : http://localhost:3000/api/v1
Production  : https://api.smartschedule.app/api/v1
Engine      : http://localhost:8001   (nội bộ, không expose ra ngoài)
```

### 6.2 Response format chuẩn

**Thành công:**
```json
{
  "success": true,
  "data": { ... },
  "message": "OK"
}
```

**Lỗi:**
```json
{
  "success": false,
  "error": {
    "code": "AUTH_EMAIL_ALREADY_EXISTS",
    "message": "Email này đã được đăng ký"
  }
}
```

**Danh sách có phân trang:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "total": 32,
    "page": 1,
    "limit": 20
  }
}
```

### 6.3 HTTP Status Codes

| Code | Khi nào |
|---|---|
| `200 OK` | GET / PUT / PATCH thành công |
| `201 Created` | POST tạo mới thành công |
| `204 No Content` | DELETE thành công |
| `400 Bad Request` | Validation lỗi (sai format, thiếu field) |
| `401 Unauthorized` | Không có token hoặc token hết hạn |
| `403 Forbidden` | Có token nhưng không đủ quyền (wrong role) |
| `404 Not Found` | Resource không tồn tại |
| `409 Conflict` | Duplicate (email, enrollment đã tồn tại) |
| `422 Unprocessable` | Logic lỗi (giờ end < start, weights ≠ 1.0) |
| `500 Internal Error` | Server lỗi không xử lý được |

### 6.4 Error codes (quy ước đặt tên)

Format: `<MODULE>_<DESCRIPTION>` — UPPER_SNAKE_CASE

```
AUTH_EMAIL_ALREADY_EXISTS
AUTH_INVALID_CREDENTIALS
AUTH_TOKEN_EXPIRED
AUTH_INSUFFICIENT_PERMISSIONS

ENROLLMENT_ALREADY_EXISTS
ENROLLMENT_SEMESTER_NOT_FOUND
ENROLLMENT_MAX_COURSES_EXCEEDED

SCHEDULE_GENERATION_FAILED
SCHEDULE_NO_VALID_COMBINATION
SCHEDULE_ENGINE_UNAVAILABLE

PREFERENCE_WEIGHTS_INVALID        ← tổng không bằng 1.0
EVENT_TIME_OVERLAP                 ← lịch bận trùng giờ
CLASS_TIME_INVALID                 ← end_time <= start_time
```

### 6.5 Quy ước đặt tên endpoint

```
GET    /api/v1/courses              ← danh sách
GET    /api/v1/courses/:id          ← chi tiết
POST   /api/v1/courses              ← tạo mới
PATCH  /api/v1/courses/:id          ← cập nhật một phần
DELETE /api/v1/courses/:id          ← xóa

POST   /api/v1/schedules/generate   ← action (động từ cuối)
POST   /api/v1/schedules/:id/save   ← sub-action
GET    /api/v1/schedules/conflicts  ← query action
```

---

## 7. NestJS — Cấu trúc module chi tiết

### Module của Person A

```
src/auth/
├── auth.module.ts
├── auth.controller.ts     ← POST /api/v1/auth/register|login|logout
│                             GET  /api/v1/auth/me
├── auth.service.ts
├── strategies/
│   └── jwt.strategy.ts
└── dto/
    ├── register.dto.ts
    └── login.dto.ts

src/preferences/
├── preferences.module.ts
├── preferences.controller.ts  ← GET|PUT  /api/v1/preferences
│                                 POST|DELETE /api/v1/preferences/avoid-days
├── preferences.service.ts
└── dto/
    └── upsert-preferences.dto.ts

src/enrollments/
├── enrollments.module.ts
├── enrollments.controller.ts  ← GET|POST|DELETE /api/v1/enrollments
├── enrollments.service.ts     ← implements IEnrollmentReader
└── dto/
    └── create-enrollment.dto.ts
```

### Module của Person B

```
src/personal-events/
├── personal-events.module.ts
├── personal-events.controller.ts  ← GET|POST|PATCH|DELETE /api/v1/personal-events
├── personal-events.service.ts
└── dto/
    ├── create-personal-event.dto.ts
    └── update-personal-event.dto.ts

src/courses/
├── courses.module.ts
├── courses.controller.ts  ← GET|POST|PATCH|DELETE /api/v1/courses
│                             GET /api/v1/courses/:id/classes
├── courses.service.ts
└── dto/

src/classes/
├── classes.module.ts
├── classes.controller.ts  ← GET|POST|PATCH|DELETE /api/v1/classes
├── classes.service.ts
└── dto/

src/schedules/
├── schedules.module.ts
├── schedules.controller.ts    ← POST /api/v1/schedules/generate
│                                 GET  /api/v1/schedules
│                                 GET  /api/v1/schedules/conflicts
│                                 POST /api/v1/schedules/:id/save
│                                 GET  /api/v1/schedules/self-study/suggestions
├── schedules.service.ts       ← đọc DB → gọi Engine → lưu kết quả
├── engine/
│   └── engine.service.ts      ← HTTP client, serialize ClassSection[]
└── dto/
    ├── generate-schedule.dto.ts
    └── save-schedule.dto.ts
```

### Luồng `POST /schedules/generate`

```
Request → SchedulesController.generate(studentId, semesterId)
  │
  ▼ SchedulesService.generate()
  │  1. enrollmentService.findEnrolledCourseIds()  → ['CS101', 'MATH101', ...]
  │  2. classesService.findBySemesterAndCourses()  → ClassSection[]
  │  3. preferencesService.findByStudent()         → Preference
  │  4. personalEventsService.findByStudent()      → PersonalEvent[]
  │  5. engineService.generate({ classes, preference,
  │                              avoid_days, personal_events, top_k: 3 })
  │     → { schedules: [{rank, assignment, scores}], total_found }
  │  6. prisma.schedule.createMany(is_draft=true)  → lưu draft
  │
  ▼ Response: { data: { scheduleIds[], schedules[{rank, scores, classIds}] } }
```

---

## 8. FastAPI Engine — Cấu trúc chi tiết

> Thuật toán đã hoàn chỉnh. Chỉ cần thêm HTTP layer.

### Files đã có

| File | Hàm chính |
|---|---|
| `csp_generator.py` | `generate_schedules(course_groups, conflict_set, avoid_days, personal_events, max_solutions=200)` |
| `detect_conflicts.py` | `build_conflict_set(classes)` — cho CSP; `detect_conflicts(classes)` — cho display |
| `scoring_function.py` | `calculate_total_score(schedule, preferences, avoid_days)` → `{total, break_time, preference_match, workload_balance}` |
| `models/classes.py` | `ClassSection` — Pydantic v2, validate `end_time > start_time` |
| `models/preferences.py` | `Preference` — validate `w_break + w_preference + w_balance == 1.0` |
| `enums/preferred_slot.py` | `PreferredSlot.MORNING \| AFTERNOON \| EVENING` — values lowercase (`"morning"`, `"afternoon"`, `"evening"`) |

### Files cần thêm

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import schedules, self_study

app = FastAPI(title="SmartSchedule Engine", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"])
app.include_router(schedules.router, prefix="/schedules", tags=["schedules"])
app.include_router(self_study.router, prefix="/self-study", tags=["self-study"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "smartschedule-engine"}
```

```python
# routers/schedules.py
@router.post("/generate", response_model=GenerateResponse)
def generate_schedules(req: GenerateRequest):
    # 1. Gom classes → course_groups
    # 2. build_conflict_set(all_classes)
    # 3. generate_schedules(course_groups, conflict_set, avoid_days, personal_events)
    # 4. calculate_total_score cho mỗi schedule
    # 5. sort + top_k
    ...

@router.post("/conflicts", response_model=ConflictResponse)
def detect(req: ConflictRequest):
    conflicts = detect_conflicts(req.classes)
    ...
```

---

## 9. React — Cấu trúc chi tiết

```
src/
├── pages/
│   ├── LoginPage.tsx
│   ├── RegisterPage.tsx
│   ├── PreferencesPage.tsx     ← form sở thích + avoid-days + lịch bận
│   ├── GeneratePage.tsx        ← CourseSelector + card list kết quả
│   └── CalendarPage.tsx        ← calendar + compare + self-study
│
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── schedule/
│   │   ├── ScheduleCardList.tsx
│   │   ├── ScheduleCard.tsx         ← score, badge Top 1/2/3
│   │   └── ConflictAlert.tsx        ← warning xung đột
│   ├── calendar/
│   │   ├── ScheduleCalendar.tsx     ← react-big-calendar wrapper
│   │   ├── CompareView.tsx          ← side-by-side 2-3 phương án
│   │   └── SelfStudyLayer.tsx       ← khe tự học nét đứt
│   ├── forms/
│   │   ├── CourseSelector.tsx       ← multi-select môn học
│   │   ├── PreferencesForm.tsx
│   │   └── PersonalEventForm.tsx
│   └── ui/
│       ├── LoadingSkeleton.tsx
│       ├── ErrorToast.tsx
│       └── ProtectedRoute.tsx
│
├── hooks/
│   ├── useAuth.ts
│   ├── useSchedule.ts
│   └── useConflicts.ts
│
├── services/                        ← axios calls
│   ├── api.ts                       ← axios instance + interceptors
│   ├── auth.service.ts
│   ├── schedule.service.ts
│   └── preferences.service.ts
│
└── types/                           ← TypeScript interfaces
    ├── auth.types.ts
    ├── schedule.types.ts
    └── api.types.ts
```

### Axios instance chuẩn

```typescript
// services/api.ts
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL + '/api/v1' })

// Request interceptor — đính token
api.interceptors.request.use(config => {
  const token = getCookie('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Response interceptor — tự refresh khi 401
api.interceptors.response.use(
  res => res,
  async err => {
    if (err.response?.status === 401 && !err.config._retry) {
      err.config._retry = true
      await refreshToken()
      return api(err.config)
    }
    return Promise.reject(err)
  }
)
```

---

## 10. API Contract Engine ↔ Backend

> Dựa trực tiếp trên Pydantic models trong `smartschedule-engine/models/`.

### `POST /schedules/generate`

```typescript
// NestJS gửi
interface GenerateRequest {
  classes: ClassSection[]
  preference: {
    student_id: string
    preferred_slot: "morning" | "afternoon" | "evening"   // ← lowercase, khớp DB enum
    min_break_minutes: number                  // default 15
    w_break: number                            // default 0.40
    w_preference: number                       // default 0.30
    w_balance: number                          // default 0.30
    // w_break + w_preference + w_balance = 1.0 (Engine validate)
  }
  avoid_days: number[]                         // [6, 7]
  personal_events: PersonalEvent[]
  top_k?: number                               // default 3
  max_solutions?: number                       // default 200
}

// Engine trả về
interface GenerateResponse {
  schedules: Array<{
    rank: number
    assignment: Record<string, ClassSection>   // {course_id: ClassSection}
    scores: {
      total: number           // ∈ [0.0000, 1.0000]
      break_time: number
      preference_match: number
      workload_balance: number
    }
  }>
  total_found: number
}
```

### `ClassSection` — kiểu dùng chung

```typescript
interface ClassSection {
  class_id: string       // "CS101_01_t1"
  course_id: string      // "CS101"
  semester_id: string    // "20241"
  day_of_week: number    // 2=T2 … 8=CN
  start_time: string     // "07:30"  ← string HH:MM
  end_time: string       // "10:30"
  room?: string
  instructor?: string
  max_students: number
}
```

### `POST /schedules/conflicts`

```typescript
// NestJS gửi
interface ConflictRequest { classes: ClassSection[] }

// Engine trả về
interface ConflictResponse {
  conflicts: Array<{ class_a: ClassSection; class_b: ClassSection }>
  total: number
}
```

### Quy trình khi thay đổi contract

```
B thay đổi Engine API → mở 2 PR liên kết:
  PR-1 trong smartschedule-engine:
    → routers/schedules.py  (sửa endpoint)
    → models/*.py           (sửa Pydantic schema)
    → tests/test_routes.py  (cập nhật test)

  PR-2 trong smartschedule-backend:
    → src/schedules/engine/engine.service.ts  (cập nhật HTTP call)
    → docs/engine-api-contract.md             (cập nhật contract doc)

  Cả 2 PR phải merge trước khi A deploy frontend sử dụng data mới.
```

---

## 11. Kế hoạch theo tuần

**Ký hiệu:** 🔵 Person A · 🟢 Person B · 🟡 Cả hai

---

## Phase 1 — Nền tảng (Tuần 1–3)

---

### Tuần 1 — Setup 3 repo + FastAPI wrap

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2 | 🟡 | Họp kickoff: thống nhất quy ước Git, commit, API format, lịch họp T6. Tạo 3 repo GitHub. | 3 repo có `main` + `develop`, branch protection bật. | — |
| T3 | 🟢 B | `smartschedule-engine`: thêm `pyproject.toml`, `main.py`, `routers/__init__.py`. `GET /health` chạy được. | `uvicorn main:app` → port 8001. | `feature/fastapi-app-entrypoint` |
| T3 | 🔵 A | `smartschedule-frontend`: Vite + React + TS. ESLint, Prettier, path aliases. | `npm run build` — 0 error. | `feature/vite-react-typescript-setup` |
| T4 | 🟢 B | Engine: `routers/schedules.py` — `POST /generate` gọi đúng pipeline (gom classes → conflict_set → generate → score → sort). | Postman: gửi payload mẫu → trả top-3 schedules. | `feature/router-generate-endpoint` |
| T4 | 🔵 A | `smartschedule-backend`: `nest new backend`. ESLint, Prettier, `@nestjs/config`, Prisma cài đặt. `GET /health`. | `GET /api/v1/health → 200`. | `feature/nestjs-project-init` |
| T5 | 🟢 B | Engine: `POST /conflicts` + `routers/self_study.py` stub. `Dockerfile`. | 3 endpoints hoạt động. | `feature/router-conflicts-selfstudy` |
| T5 | 🟢 B | `docker-compose.yml` trong `smartschedule-backend/` — postgres + engine + backend. | `docker compose up` → 3 service healthy. | `feature/docker-compose-dev` |
| T6 | 🟡 | Họp: test Postman toàn bộ Engine endpoints. Thống nhất `ClassSection` TypeScript interface. | Engine API xác nhận; interface commit vào `types/`. | — |

> ✅ **DoD T1:** Engine 3 endpoint hoạt động; `docker compose up` lên được; CI xanh cả 3 repo.

---

### Tuần 2 — DB Schema + Auth setup

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2 | 🔵 A | Prisma `schema.prisma` — 12 model, enums, relations, indexes. Migration 001. | `npx prisma migrate dev` pass; 12 bảng lên DB. | `feature/prisma-schema-migrations` |
| T3 | 🔵 A | `seed.ts` — 1 HK, 8 môn, 32 nhóm, 2 SV, preferences, events. | `npm run seed` < 5s; SELECT 9 bảng có data. | `feature/prisma-seed-data` |
| T4 | 🔵 A | `AuthModule` skeleton: `POST /auth/register` — bcrypt, email unique. | 201 email mới; 409 trùng. | `feature/auth-register-endpoint` |
| T5 | 🔵 A | `POST /auth/login` (JWT access + refresh) + `POST /auth/logout` (token_version++). | Login → token pair; logout → token cũ → 401. | `feature/auth-login-logout-jwt` |
| T6 | 🟡 | Họp: test Auth + DB. ERD commit vào `docs/`. | ERD khớp schema; auth endpoints pass. | — |

> ✅ **DoD T2:** Migrations pass; seed pass; register/login/logout hoạt động.

---

### Tuần 3 — Auth hoàn thiện + M1

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2 | 🔵 A | `JwtStrategy` + `JwtAuthGuard` + `RolesGuard`. `GET /auth/me`. `@nestjs/throttler` cho `/auth/*`. | `/auth/me` → user info; no token → 401. | `feature/auth-jwt-guard-strategy` |
| T3 | 🔵 A | React: `LoginPage` + `RegisterPage` — React Hook Form + Zod. Axios interceptor tự refresh. Cookie storage. | FE auth flow hoàn chỉnh gọi NestJS thật. | `feature/frontend-login-register-pages` |
| T4 | 🟢 B | `CoursesModule` + `ClassesModule` — CRUD admin-only. `GET /courses/:id/classes`. | CRUD pass; user thường → 403. | `feature/courses-classes-crud-module` |
| T5 | 🟡 | Demo M1: đăng ký → login → `/auth/me` → logout. Merge `develop` → `release/v0.1` → `main`. `git tag v0.1`. | Tag `v0.1` push cả 3 repo. | — |

> ✅ **DoD T3 / M1:** UC-01, UC-02 pass; FE auth hoàn chỉnh; tag `v0.1`.

---

## Phase 2 — Lõi hệ thống (Tuần 4–8)

---

### Tuần 4 — Data APIs + Preferences + Events

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2 | 🟢 B | `EnrollmentsModule` — `POST /enrollments` (validate semester + chưa enroll). | POST lưu đúng; duplicate → 409. | `feature/enrollments-module` |
| T3 | 🔵 A | `PreferencesModule` — `GET/PUT /preferences` + `POST/DELETE /preferences/avoid-days`. | Upsert pass; giờ đảo ngược → 422. | `feature/preferences-module` |
| T4 | 🟢 B | `PersonalEventsModule` — CRUD `/personal-events`, overlap check. | Trùng giờ → 409. | `feature/personal-events-module` |
| T5 | 🔵 A | React: `PreferencesPage` — form sở thích + avoid-days + lịch bận. Tích hợp API. | FE: nhập → lưu → reload thấy đúng. | `feature/preferences-page-forms` |
| T6 | 🟡 | Review API integration. Retro. | 5 modules (auth, courses, classes, enrollments, prefs, events) pass. | — |

---

### Tuần 5 — SchedulesModule + Generate flow

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2 | 🟢 B | `SchedulesModule` skeleton + `engine.service.ts` — HTTP client gọi Engine. | NestJS → Engine: stub call 200. | `feature/schedules-module-engine-client` |
| T3 | 🟢 B | `POST /schedules/generate` — đọc DB (enrollments → classes → preferences → events) → gọi Engine → lưu draft. | `is_draft=true` trong DB; response có schedule_ids. | `feature/schedules-generate-endpoint` |
| T4 | 🟢 B | `GET /schedules/conflicts` — đọc classes → gọi Engine `/conflicts` → trả FE. | Response < 50ms, n=20. | `feature/schedules-conflicts-endpoint` |
| T5 | 🔵 A | React: `GeneratePage` + `CourseSelector` — multi-select môn + gọi `/generate`. `ScheduleCardList` + `ConflictAlert`. | 3 card score thực từ NestJS; warning xung đột. | `feature/generate-page-card-list` |
| T6 | 🟡 | Code review chéo. | Generate pipeline end-to-end pass. | — |

---

### Tuần 6–7 — Calendar UI + Save

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2–T3 | 🔵 A | React: `ScheduleCalendar` — react-big-calendar, mapping, màu theo `course_id`. | Calendar render đúng slot. | `feature/calendar-react-big-calendar` |
| T4 | 🔵 A | React: `CompareView` — side-by-side 2–3 phương án. Tooltip thông tin lớp. | So sánh rõ ràng, hover → chi tiết. | `feature/calendar-compare-view` |
| T5 | 🟢 B | `POST /schedules/:id/save` — `is_draft=false`, `is_active=true`, partial unique enforce. | 1 active/student/semester. | `feature/schedules-save-endpoint` |
| T6 | 🔵 A | React: nút Lưu phương án → gọi `POST /schedules/:id/save`. Persist qua reload. | Lưu thành công; reload vẫn thấy. | `feature/frontend-save-schedule` |

---

### Tuần 8 — M2

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2–T4 | 🟡 | Bug fix, integration test thủ công toàn luồng. | Luồng không lỗi trên seed data. | — |
| T5 | 🟡 | Demo M2: generate → calendar → compare → save. Merge → `release/v0.2` → `main`. `git tag v0.2`. | Tag `v0.2`. | — |

> ✅ **DoD T8 / M2:** Calendar top-3 đúng; lưu persist; tag `v0.2`.

---

## Phase 3 — Hoàn thiện (Tuần 9–11)

---

### Tuần 9 — Self-Study + UX

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2–T3 | 🟢 B | Engine: `routers/self_study.py` hoàn chỉnh — `POST /suggest-self-study`. NestJS: `GET /schedules/self-study/suggestions`. | API trả ≥ 3 khe không trùng lịch. | `feature/self-study-endpoint` |
| T4–T5 | 🔵 A | React: `SelfStudyLayer` trên Calendar. UX polish — loading skeleton, error toast. | Khe tự học hiển thị; Lighthouse mobile ≥ 80. | `feature/self-study-calendar-ux-polish` |

---

### Tuần 10 — Testing

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2–T3 | 🔵 A | Playwright: 5 kịch bản E2E. Tích hợp CI `smartschedule-frontend`. | 5 test headless pass; CI ≤ 8 phút. | `feature/e2e-playwright-5-specs` |
| T4 | 🟢 B | Jest integration tests NestJS: ≥ 15 test (auth, generate, save). | ≥ 15 pass. | `feature/nestjs-integration-tests` |
| T5–T6 | 🟡 | Bug bash + triage. | Bug list có severity + assignee. | — |

---

### Tuần 11 — M3

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2 | 🟡 | Fix Critical/High bugs. | Critical = 0. | `fix/<mô-tả>` |
| T3–T4 | 🔵 A | Swagger export `docs/api/`. React responsive final pass. | API docs commit; Lighthouse ≥ 80. | `feature/swagger-docs-responsive-final` |
| T5 | 🟡 | Demo M3: 10 UC. Feature freeze. Merge → `release/v1.0` → `main`. `git tag v1.0`. | Tag `v1.0`; feature freeze. | — |

---

## Phase 4 — Deploy (Tuần 12)

| Ngày | Người | Công việc | Output | Nhánh |
|---|---|---|---|---|
| T2 | 🟢 B | Deploy NestJS (Render) + Engine (Railway). Postgres managed. | `/health` 2 service → 200. | `feature/deploy-backend-engine` |
| T2 | 🔵 A | Deploy React (Vercel). `VITE_API_BASE_URL` → production NestJS. | URL frontend; Login chạy được. | `feature/deploy-frontend-vercel` |
| T3 | 🟡 | Smoke test production: 10 UC. Báo cáo nháp → GVHD. | Checklist 10 UC pass. | — |
| T4 | 🔵 A | Video demo 5–7 phút. | Upload Drive; link trong README. | — |
| T5–T6 | 🟡 | Slide + tổng duyệt 2 lần. `git tag v1.0-final`. Nộp hồ sơ. | Hồ sơ đầy đủ. | — |

> ✅ **DoD M4:** 3 URL public stable ≥ 24h; hồ sơ nộp đúng hạn.

---

## Tổng hợp nhánh Git theo tuần

| Tuần | Person A 🔵 | Person B 🟢 |
|---|---|---|
| 1 | `feature/vite-react-typescript-setup` · `feature/nestjs-project-init` | `feature/fastapi-app-entrypoint` · `feature/router-generate-endpoint` · `feature/router-conflicts-selfstudy` · `feature/docker-compose-dev` |
| 2 | `feature/prisma-schema-migrations` · `feature/prisma-seed-data` · `feature/auth-register-endpoint` · `feature/auth-login-logout-jwt` | — |
| 3 | `feature/auth-jwt-guard-strategy` · `feature/frontend-login-register-pages` | `feature/courses-classes-crud-module` |
| 4 | `feature/preferences-module` · `feature/preferences-page-forms` | `feature/enrollments-module` · `feature/personal-events-module` |
| 5 | `feature/generate-page-card-list` | `feature/schedules-module-engine-client` · `feature/schedules-generate-endpoint` · `feature/schedules-conflicts-endpoint` |
| 6–7 | `feature/calendar-react-big-calendar` · `feature/calendar-compare-view` · `feature/frontend-save-schedule` | `feature/schedules-save-endpoint` |
| 9 | `feature/self-study-calendar-ux-polish` | `feature/self-study-endpoint` |
| 10 | `feature/e2e-playwright-5-specs` | `feature/nestjs-integration-tests` |
| 11 | `feature/swagger-docs-responsive-final` | `fix/<tên-lỗi>` |
| 12 | `feature/deploy-frontend-vercel` | `feature/deploy-backend-engine` |

---

# PROJECT CONTEXT — Dành cho AI

> Paste section này vào đầu chat với bất kỳ AI nào.

## Tên & Mục tiêu
**SmartSchedule** — Sinh viên nhập môn đăng ký + sở thích + lịch bận → hệ thống sinh top-3 TKB không xung đột, xếp hạng theo điểm, hiển thị trên calendar.

## Trạng thái
| Phần | Trạng thái |
|---|---|
| Python algorithms (`csp_generator`, `detect_conflicts`, `scoring_function`) | ✅ Xong |
| FastAPI HTTP layer (`main.py`, `routers/`) | ⏳ Person B làm |
| NestJS Auth + Prefs + Enrollments + Prisma/seed | ⏳ Person A làm |
| NestJS PersonalEvents + Courses + Schedules | ⏳ Person B làm |
| React frontend (toàn bộ) | ⏳ Person A làm |

## 3 Repo
- `smartschedule-engine` — Person B (Python FastAPI, port 8001)
- `smartschedule-backend` — A+B (NestJS, port 3000, PostgreSQL)
- `smartschedule-frontend` — Person A (React, port 5173)

## Tech Stack
React 18 + TS + Vite · NestJS + Prisma + PostgreSQL 16 · Python 3.14 + FastAPI

## Kiến trúc
```
React → NestJS(:3000) → PostgreSQL
              ↓ HTTP
         FastAPI Engine(:8001) — stateless
```

## Core Algorithms (đã xong)
- `generate_schedules(course_groups, conflict_set, avoid_days, personal_events)` — CSP backtracking MRV+LCV+FC
- `build_conflict_set(classes)` → set[(id_A, id_B)]
- `calculate_total_score(schedule, preferences, avoid_days)` → {total, break_time, preference_match, workload_balance}

## Pydantic Models (API contract)
- `ClassSection`: class_id, course_id, semester_id, day_of_week(2-8), start_time("HH:MM"), end_time
- `Preference`: preferred_slot(**morning**|**afternoon**|**evening** — lowercase, khớp DB enum), min_break_minutes, w_break+w_preference+w_balance=1.0
- `PersonalEvent`: event_id, student_id, day_of_week(nullable), start_time, end_time, is_recurring

## NestJS Modules
- **A owns**: AuthModule, PreferencesModule, EnrollmentsModule, Prisma schema/seed, DatabaseModule
- **B owns**: PersonalEventsModule, CoursesModule, ClassesModule, SchedulesModule, docker-compose

## API Response Format
```json
{ "success": true, "data": {...} }
{ "success": false, "error": { "code": "AUTH_EMAIL_ALREADY_EXISTS", "message": "..." } }
```

## Git Quy ước

- **Branch:** `feature/<mô-tả>` · `fix/<mô-tả>` · `hotfix/<mô-tả>` · `release/v<x.y>`
- **Commit:** `feat(scope): mô tả` — Conventional Commits
- **Merge:** Squash and merge vào `develop`; `--no-ff` merge vào `main`
- **Milestone tags:** `v0.1` (M1 T3) · `v0.2` (M2 T8) · `v1.0` (M3 T11) · `v1.0-final` (M4 T12)
