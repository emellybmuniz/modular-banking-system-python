# python
from abc import ABC
from typing import Optional, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import Client
    from .history import History

class Account(ABC):
    def __init__(
        self,
        number: int,
        agency: str,
        balance: float = 0.0,
        client: Optional["Client"] = None,
        history: Optional["History"] = None,
    ) -> None:
        self.number = number
        self.agency = agency
        self._balance = float(balance)
        self.client = client
        self.history = history

    @property
    def balance(self) -> float:
        return self._balance

    def deposit(self, value: float) -> bool:
        if value <= 0:
            return False
        # use transaction implementation
        from .transaction import Deposito

        prev = self._balance
        t = Deposito(value=value, kind='deposit', description='Deposit')
        t.registrar(self)
        return self._balance > prev

    def withdraw(self, value: float) -> bool:
        if value <= 0 or value > self._balance:
            return False
        # use transaction implementation
        from .transaction import Saque

        prev = self._balance
        t = Saque(value=value, kind='withdraw', description='Withdraw')
        t.registrar(self)
        return self._balance < prev

    def statement(self) -> Any:
        """
        Return the account statement from the associated History.
        If no history is attached, returns an empty list.
        """
        if self.history is None:
            return "Nenhuma transação registrada."
        return self.history.statement()
