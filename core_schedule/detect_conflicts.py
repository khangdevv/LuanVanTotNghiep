from models import ClassSection


def _overlaps(a: ClassSection, b: ClassSection) -> bool:
    return (
        a.day_of_week == b.day_of_week
        and a.start_time < b.end_time
        and b.start_time < a.end_time
    )


def detect_conflicts(classes: list[ClassSection],) -> list[tuple[ClassSection, ClassSection]]:
    # Trả danh sách cặp xung đột để hiển thị cho người dùng.
    conflicts: list[tuple[ClassSection, ClassSection]] = []

    for i in range(len(classes) - 1):
        for j in range(i + 1, len(classes)):
            if classes[i].course_id == classes[j].course_id:
                continue
            if _overlaps(classes[i], classes[j]):
                conflicts.append((classes[i], classes[j]))

    return conflicts


def build_conflict_set(classes: list[ClassSection]) -> set[tuple[str, str]]:
    conflict_set: set[tuple[str, str]] = set()

    for i in range(len(classes) - 1):
        for j in range(i + 1, len(classes)):
            if _overlaps(classes[i], classes[j]):
                a_id = classes[i].class_id
                b_id = classes[j].class_id
                conflict_set.add((a_id, b_id))
                conflict_set.add((b_id, a_id))

    return conflict_set
