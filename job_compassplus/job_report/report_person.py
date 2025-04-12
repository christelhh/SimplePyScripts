#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "ipetrash"


from functools import total_ordering


class ReportPerson:
    """Класс для описания сотрудника в отчете."""

    def __init__(self, tags: list[str]):
        # ФИО
        self.second_name, self.first_name, self.middle_name = tags[0].split(maxsplit=2)

        # Невыходов на работу
        self.absence_from_work = int(tags[1])

        # По календарю (смен / ч:мин)
        # Для точного значения посещенных дней, может быть указано как "3 = 4- (1 О)", поэтому
        # отсекаем правую, от знака равно, сторону, удаляем пробелы и переводим в число
        self.need_to_work_days = self.get_work_day(tags[2])
        self.need_to_work_on_time = self.get_work_time(tags[3])

        # Фактически (смен / ч:мин)
        self.worked_days = self.get_work_day(tags[4])
        self.worked_time = self.get_work_time(tags[5])

        # Отклонение (смен / ч:мин)
        self.deviation_of_day = self.get_work_day(tags[6])
        self.deviation_of_time = self.get_work_time(tags[7])

    @property
    def full_name(self) -> str:
        return f"{self.second_name} {self.first_name} {self.middle_name}"

    @staticmethod
    def get_work_day(day_str) -> int:
        return (
            int(day_str) if "=" not in day_str else int(day_str.split("=")[0].strip())
        )

    @total_ordering
    class Time:
        """Простой класс для хранения даты работы."""

        def __init__(self, time_str: str):
            self._hours, self._minutes, self._seconds = map(int, time_str.split(":"))

        @property
        def total(self) -> int:
            """Всего минут"""

            return self._hours * 60 + self._minutes

        def __repr__(self) -> str:
            return f"{self._hours:0>2}:{self._minutes:0>2}"

        def __eq__(self, other: "Time") -> bool:
            return self.total == other.total

        def __lt__(self, other: "Time") -> bool:
            return self.total < other.total

    @staticmethod
    def get_work_time(time_str: str) -> Time:
        return ReportPerson.Time(time_str)

    def __hash__(self) -> int:
        return hash(self.full_name)

    def __eq__(self, other: "ReportPerson") -> bool:
        return self.full_name == other.full_name

    def __repr__(self) -> str:
        return (
            f"{self.full_name}. Невыходов на работу: {self.absence_from_work}. "
            f"По календарю ({self.need_to_work_days} смен / {self.need_to_work_on_time} ч:мин). "
            f"Фактически ({self.worked_days} смен / {self.worked_time} ч:мин). "
            f"Отклонение ({self.deviation_of_day} смен / {self.deviation_of_time} ч:мин)"
        )
