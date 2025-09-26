from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict


class SchedulingConflictError(Exception):
    """Lanzada cuando se detecta un conflicto de programación."""


@dataclass
class Student:
    id: str
    name: str


@dataclass
class ClassEvent:
    id: str
    student_id: str
    start: datetime
    end: datetime
    title: str = "Clase"


class SchedulingManager:
    """Gestor simple para programar clases (Tipo B - programación temporal).

    Contrato mínimo:
    - add_student(id, name) -> crea estudiante
    - schedule_class(event) -> añade evento, detecta conflictos por estudiante
    - list_events(student_id=None) -> lista eventos

    Error modes:
    - SchedulingConflictError si hay solapamiento de horarios para el mismo estudiante
    """

    def __init__(self) -> None:
        self._students: Dict[str, Student] = {}
        self._events: Dict[str, ClassEvent] = {}

    def add_student(self, id: str, name: str) -> None:
        if id in self._students:
            return
        self._students[id] = Student(id=id, name=name)

    def schedule_class(self, event: ClassEvent) -> None:
        # validaciones básicas
        if event.student_id not in self._students:
            raise ValueError(f"Estudiante {event.student_id} no encontrado")
        if event.end <= event.start:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio")

        # comprobar conflictos solo contra eventos del mismo estudiante
        for e in self._events.values():
            if e.student_id != event.student_id:
                continue
            if self._overlaps(e.start, e.end, event.start, event.end):
                raise SchedulingConflictError(
                    f"Conflicto con evento {e.id} ({e.start} - {e.end})"
                )

        self._events[event.id] = event

    def list_events(self, student_id: str | None = None) -> List[ClassEvent]:
        if student_id is None:
            return sorted(self._events.values(), key=lambda e: e.start)
        return sorted([e for e in self._events.values() if e.student_id == student_id], key=lambda e: e.start)

    @staticmethod
    def _overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
        # True si los intervalos se solapan (intersección no vacía)
        return not (a_end <= b_start or b_end <= a_start)
