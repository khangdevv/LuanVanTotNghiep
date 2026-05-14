# Ke hoach tich hop React, NestJS va Python Algorithm Service

## 1. Muc tieu kien truc

He thong du kien chia thanh 3 phan chinh:

- React: giao dien nguoi dung.
- NestJS: backend chinh, quan ly user, auth, database, ORM va API.
- Python: loi thuat toan xep thoi khoa bieu.

Nguyen tac quan trong la Python core chi nen giu vai tro thuat toan. Python khong can quan ly database relationship. Cac quan he du lieu nhu `Student - Preference`, `Course - ClassSection`, `Schedule - ScheduleClass` nen thuoc ve tang NestJS va ORM.

## 2. Vai tro tung tang

### React

React phu trach cac thao tac:

- Cho user chon mon hoc.
- Cho user nhap lich ban ca nhan.
- Cho user chon ngay muon tranh.
- Hien thi danh sach thoi khoa bieu duoc sinh ra.
- Hien thi diem danh gia tung thoi khoa bieu.

React khong nen goi truc tiep Python service. Tat ca request nen di qua NestJS de dam bao auth, phan quyen va thong nhat du lieu.

### NestJS

NestJS la backend trung tam:

- Quan ly authentication va authorization.
- Quan ly database bang ORM.
- Luu user, mon hoc, lop hoc, hoc ky, preference, personal event, schedule.
- Query du lieu lien quan den tung user.
- Chuan hoa du lieu thanh payload phang de gui sang Python.
- Nhan ket qua tu Python va tra ve React.
- Luu ket qua vao database neu can.

NestJS co the co ORM relationship day du, vi day la tang can hieu quan he du lieu trong database.

### Python Algorithm Service

Python chi nhan input da duoc chuan hoa, chay thuat toan va tra output.

Python khong can biet ORM relationship. Cac model Python co the tiep tuc doc lap nhu hien tai:

- `ClassSection`
- `PersonalEvent`
- `Preference`
- cac DTO phuc vu request/response

Thuat toan hien tai phu hop voi cach nay vi `generate_schedules(...)` nhan du lieu qua tham so rieng cho tung lan goi.

## 3. Luong giao tiep co ban

Luong de trien khai giai doan dau:

```text
React
  -> NestJS API
    -> Python FastAPI Algorithm Service
      -> NestJS
  -> React
```

Cac buoc xu ly:

1. User bam tao thoi khoa bieu tren React.
2. React goi NestJS API.
3. NestJS xac thuc user.
4. NestJS lay du lieu tu database.
5. NestJS tao payload rieng cho request do.
6. NestJS goi Python service.
7. Python chay thuat toan va tra ket qua.
8. NestJS map ket qua voi database/cache.
9. NestJS tra response ve React.

## 4. Payload giua NestJS va Python

NestJS nen gui payload nho gon, chi gom du lieu can thiet cho lan xep lich hien tai.

Vi du request:

```json
{
  "request_id": "uuid",
  "student_id": "SV001",
  "semester_id": "HK2-2025",
  "course_groups": {
    "CS03042": [
      {
        "class_id": "CS03042_01",
        "course_id": "CS03042",
        "semester_id": "HK2-2025",
        "day_of_week": 2,
        "start_time": "07:00",
        "end_time": "09:30",
        "room": "A101",
        "instructor": "Nguyen Van A",
        "max_students": 60
      }
    ]
  },
  "avoid_days": [6, 7],
  "personal_events": [
    {
      "event_id": 1,
      "student_id": "SV001",
      "title": "Di lam them",
      "day_of_week": 4,
      "start_time": "12:35",
      "end_time": "15:05",
      "is_recurring": true
    }
  ],
  "preferences": {
    "preferred_slot": "MORNING",
    "w_break": 0.4,
    "w_preference": 0.3,
    "w_balance": 0.3
  },
  "max_solutions": 50
}
```

Vi du response:

```json
{
  "request_id": "uuid",
  "schedules": [
    {
      "class_ids": ["CS03042_01", "CS03002_03"],
      "score": {
        "total": 0.86,
        "break_time": 0.9,
        "preference_match": 0.8,
        "workload_balance": 0.85
      }
    }
  ]
}
```

Python nen tra `class_id` thay vi tra lai toan bo object lop hoc neu NestJS da co san du lieu lop trong DB/cache. Cach nay giup response nhe hon va NestJS van la noi chiu trach nhiem ghep thong tin chi tiet de tra cho React.

## 5. Dam bao giao tiep rieng biet theo user

Moi lan user tao thoi khoa bieu, NestJS nen tao mot request/job rieng:

- Co `request_id` hoac `job_id`.
- Co `student_id`.
- Co bo `course_groups`, `avoid_days`, `personal_events`, `preferences` rieng.
- Khong dung chung bien runtime giua cac user.

Python service chi xu ly du lieu nam trong payload cua request do. Ket qua tra ve gan voi `request_id`/`job_id`, nen user A va user B khong bi lan du lieu.

Dieu kien can giu trong Python:

- Khong luu `chosen`, `domains`, `valid_schedules` bang bien global.
- Khong cache du lieu user neu khong co key ro rang theo `student_id` hoac `request_id`.
- Moi request phai tao model/input rieng.
- Cac bien bi mutate trong backtracking phai nam trong scope cua mot lan goi ham.

Code hien tai phu hop voi huong nay vi `generate_schedules(...)` nhan input qua tham so va tao `domains`, `chosen`, `valid_schedules` rieng trong moi lan goi.

## 6. Dam bao toc do he thong

### 6.1. Khong gui thua du lieu

NestJS khong nen gui toan bo du lieu hoc ky sang Python. Chi gui:

- Cac mon user da chon.
- Cac nhom lop cua cac mon do.
- Lich ban cua user do.
- Ngay muon tranh.
- Preference cua user do.
- Gioi han `max_solutions`.

### 6.2. Cache conflict_set

`build_conflict_set()` co the ton chi phi cao vi phai so sanh tung cap lop.

Nen tinh truoc `conflict_set` theo hoc ky:

```text
semester_id -> all class sections -> conflict_set -> cache/DB/Redis
```

Khi user gui request, NestJS hoac Python chi lay phan conflict lien quan den cac `class_id` trong request.

Day la diem toi uu quan trong vi xung dot giua cac lop trong mot hoc ky thuong khong thay doi theo tung user.

### 6.3. Chay Python nhu service rieng

Khong nen moi request lai spawn mot process Python moi:

```text
NestJS -> spawn python script
```

Cach nay cham vi ton thoi gian khoi dong process va kho quan ly timeout/log/error.

Nen chay Python bang FastAPI:

```text
NestJS -> HTTP POST /generate-schedules -> Python FastAPI
```

Python service luon chay san, nhan request va tra response.

### 6.4. Dung queue khi tac vu lau

Neu viec xep lich co the mat vai giay hoac co nhieu user chay cung luc, nen dung queue.

Kien truc nang cap:

```text
React
  -> NestJS
    -> Redis Queue
      -> Python Workers
        -> Redis/DB
  -> React poll/WebSocket
```

Luong xu ly:

1. React gui yeu cau.
2. NestJS tao `job_id`.
3. NestJS day job vao queue.
4. Python worker lay job va chay thuat toan.
5. Ket qua duoc luu vao Redis hoac DB.
6. React lay ket qua bang polling hoac WebSocket.

Cach nay giup API NestJS khong bi treo request HTTP lau.

### 6.5. Scale Python workers

Vi moi request/job doc lap, co the chay nhieu Python worker song song:

```text
Python worker 1
Python worker 2
Python worker 3
```

Moi worker xu ly mot job rieng. Dieu kien la Python algorithm khong dung global state cho du lieu user.

### 6.6. Gioi han khong gian tim kiem

Can gioi han de he thong co toc do on dinh:

- Gioi han `max_solutions`.
- Gioi han so mon user co the xep trong mot lan.
- Dat timeout cho job.
- Loc `avoid_days` truoc khi backtracking.
- Loc `personal_events` som.
- Dung MRV, LCV va Forward Checking nhu hien tai.

## 7. Thong nhat du lieu giua NestJS va Python

Can dinh nghia contract ro rang giua hai tang.

Phia NestJS nen co DTO TypeScript:

- `ClassSectionInputDto`
- `PersonalEventInputDto`
- `PreferenceInputDto`
- `GenerateScheduleRequestDto`
- `GeneratedScheduleDto`
- `ScoreDto`

Phia Python nen co Pydantic model tuong ung:

- `ClassSectionInput`
- `PersonalEventInput`
- `PreferenceInput`
- `GenerateScheduleRequest`
- `GeneratedScheduleResult`
- `ScoreResult`

Hai ben phai thong nhat cac quy uoc:

- `day_of_week`: tu 2 den 8.
- `start_time`, `end_time`: dinh dang `"HH:mm"`.
- `class_id`: duy nhat trong hoc ky.
- `course_id`: dung lam key trong `course_groups`.
- `semester_id`: dung de cache du lieu hoc ky.
- `preferred_slot`: dung enum thong nhat, vi du `"MORNING"` va `"AFTERNOON"`.

## 8. Lo trinh trien khai de xuat

### Giai doan 1: Demo dong bo

Dung kien truc:

```text
React -> NestJS -> Python FastAPI -> NestJS -> React
```

Phu hop khi:

- So user con it.
- Thuat toan chay nhanh.
- Can demo ro rang cho do an.

### Giai doan 2: Toi uu hieu nang

Them:

- Cache `conflict_set` theo `semester_id`.
- Giam kich thuoc request/response.
- Timeout cho Python request.
- Log `request_id`.

### Giai doan 3: Xu ly bat dong bo

Dung kien truc:

```text
React -> NestJS -> Redis Queue -> Python Workers -> DB/Redis -> React
```

Phu hop khi:

- Nhieu user chay cung luc.
- Thuat toan co the mat nhieu giay.
- Can scale so luong Python worker.

## 9. Ket luan

Huong thiet ke de xuat la giu Python core doc lap va de NestJS chiu trach nhiem ORM relationship.

Cach nay co cac loi ich:

- Tach biet ro giua logic thuat toan va logic database.
- Python core de test doc lap.
- NestJS van quan ly du lieu day du va thong nhat.
- Co the phuc vu nhieu user neu moi request/job co payload rieng.
- Co the mo rong hieu nang bang cache, FastAPI service va queue worker.

Tom lai, Python model doc lap van phu hop cho loi thuat toan. Su thong nhat du lieu nam o contract request/response giua NestJS va Python, khong nam o viec Python phai co ORM relationship.
