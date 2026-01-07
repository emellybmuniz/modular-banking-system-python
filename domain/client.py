from abc import ABC
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from domain.account import Account
    from domain.natural_person import NaturalPerson
    from .history import History


class Client(ABC):
    def __init__(self, name: str = "", cpf: str = "", birth_date: str = "", address: str = "", history: Optional["History"] = None):
        self._name = name
        self._cpf = cpf
        self._birth_date = birth_date
        self._address = address
        self._accounts: List["Account"] = []
        self.history: Optional["History"] = history

    @property
    def name(self) -> str:
        return self._name

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def birth_date(self) -> str:
        return self._birth_date

    @property
    def address(self) -> str:
        return self._address

    @property
    def accounts(self) -> List["Account"]:
        return list(self._accounts)

    def add_account(self, account: "Account") -> None:
        # attach client reference and client's history to the account
        account.client = self
        if self.history is not None:
            account.history = self.history
        self._accounts.append(account)

    def remove_account(self, account: "Account") -> None:
        if account in self._accounts:
            # detach references
            account.client = None
            account.history = None
            self._accounts.remove(account)

    def attach_history(self, history: "History") -> None:
        """Attach a History to this client and propagate to existing accounts."""
        self.history = history
        for acc in self._accounts:
            acc.history = history

    def statement(self) -> str:
        """Return the client's history statement as string; empty string if none."""
        if self.history is None:
            return ""
        return self.history.generate_statement()
