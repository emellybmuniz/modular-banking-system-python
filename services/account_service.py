from datetime import date
from typing import List

from domain.natural_person import NaturalPerson
from domain.checking_account import CheckingAccount
from repository.persistence import get_client_repo, get_account_repo
from domain.history import History


class AccountService:
    def __init__(self, client_repo=None, account_repo=None):
        self.client_repo = client_repo or get_client_repo()
        self.account_repo = account_repo or get_account_repo()

    def create_customer(self, name: str, cpf: str, birth_date: date, address: str) -> NaturalPerson:
        # check for existing cpf
        existing = self.client_repo.find(lambda u: getattr(u, 'cpf', None) == cpf)
        if existing:
            raise ValueError("Customer with given CPF already exists")

        customer = NaturalPerson(name=name, cpf=cpf, birth_date=birth_date, address=address)
        customer.attach_history(History())
        self.client_repo.add(customer)
        return customer

    def create_checking_account(self, customer: NaturalPerson, number: int, agency: str, initial_balance: float = 0.0) -> CheckingAccount:
        if self.account_repo.get(agency, number) is not None:
            raise ValueError("Account already exists")

        acc = CheckingAccount(number=number, agency=agency, balance=initial_balance, client=customer, history=customer.history)
        self.account_repo.add(acc)
        customer.add_account(acc)
        return acc

    def list_accounts(self) -> List[CheckingAccount]:
        return self.account_repo.list()

    def find_accounts_by_customer(self, customer: NaturalPerson) -> List[CheckingAccount]:
        return self.account_repo.find_by_client(customer)
