from datetime import date
from domain.natural_person import NaturalPerson


class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def create_user(
        self,
        name: str,
        cpf: str,
        birth_date: date,
        address: str
    ) -> NaturalPerson:
        existing_user = self._user_repository.find(
            lambda u: u.cpf == cpf
        )

        if existing_user:
            raise ValueError("User already registered")

        user = NaturalPerson(
            name=name,
            cpf=cpf,
            birth_date=birth_date,
            address=address
        )

        self._user_repository.add(user)
        return user

    def list_users(self) -> list[NaturalPerson]:
        return self._user_repository.get_all()

    def get_by_cpf(self, cpf: str) -> NaturalPerson | None:
        return self._user_repository.find(
            lambda u: u.cpf == cpf
        )
