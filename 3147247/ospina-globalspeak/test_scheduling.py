from datetime import datetime, timedelta
import pytest

from scheduling import SchedulingManager, ClassEvent, SchedulingConflictError


def test_add_and_list_student(tmp_path):
    mgr = SchedulingManager()
    mgr.add_student("s1", "Ana Ospina")
    assert mgr._students["s1"].name == "Ana Ospina"


def test_schedule_class_and_list():
    mgr = SchedulingManager()
    mgr.add_student("s1", "Ana Ospina")

    start = datetime(2025, 9, 26, 9, 0)
    end = start + timedelta(hours=1)
    ev = ClassEvent(id="c1", student_id="s1", start=start, end=end, title="Inglés 101")
    mgr.schedule_class(ev)

    events = mgr.list_events("s1")
    assert len(events) == 1
    assert events[0].id == "c1"


def test_conflict_detection():
    mgr = SchedulingManager()
    mgr.add_student("s1", "Ana Ospina")

    s1 = datetime(2025, 9, 26, 10, 0)
    e1 = s1 + timedelta(hours=1)
    ev1 = ClassEvent(id="c1", student_id="s1", start=s1, end=e1)
    mgr.schedule_class(ev1)

    # evento que comienza antes y termina durante el primero -> conflicto
    s2 = datetime(2025, 9, 26, 9, 30)
    e2 = datetime(2025, 9, 26, 10, 30)
    ev2 = ClassEvent(id="c2", student_id="s1", start=s2, end=e2)

    with pytest.raises(SchedulingConflictError):
        mgr.schedule_class(ev2)


def test_no_conflict_different_student():
    mgr = SchedulingManager()
    mgr.add_student("s1", "Ana Ospina")
    mgr.add_student("s2", "Juan Perez")

    s1 = datetime(2025, 9, 26, 11, 0)
    e1 = s1 + timedelta(hours=1)
    ev1 = ClassEvent(id="c1", student_id="s1", start=s1, end=e1)
    mgr.schedule_class(ev1)

    # mismo horario, distinto estudiante -> permitido
    ev2 = ClassEvent(id="c2", student_id="s2", start=s1, end=e1)
    mgr.schedule_class(ev2)

    assert len(mgr.list_events()) == 2
