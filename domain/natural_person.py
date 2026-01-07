from datetime import date
from typing import Optional
from domain.client import Client


class NaturalPerson(Client):
    def __init__(self, name: str, cpf: str, birth_date: date, address: str, history: Optional["History"] = None):
        super().__init__(name=name, cpf=cpf, birth_date=birth_date, address=address, history=history)

    @property
    def name(self) -> str:
        return self._name

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def birth_date(self) -> date:
        return self._birth_date

    @birth_date.setter
    def birth_date(self, birth_date: date) -> None:
        if not isinstance(birth_date, date):
            raise TypeError("birth_date must be a datetime.date")
        today = date.today()
        if birth_date > today:
            raise ValueError("birth_date cannot be in the future")
        self._birth_date = birth_date

