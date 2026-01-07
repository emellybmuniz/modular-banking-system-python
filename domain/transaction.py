from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from .account import Account


@runtime_checkable
class TransactionProtocol(Protocol):
    """Protocol for transactions used by the domain.

    Properties (English names):
      - value: float
      - date: datetime
      - kind: str  # e.g., 'deposit', 'withdraw', 'transfer'
      - description: Optional[str]

    Method:
      - registrar(conta: Account) -> None  # register the transaction on the provided account
    """

    value: float
    date: datetime
    kind: str
    description: Optional[str]

    def registrar(self, conta: "Account") -> None:
        ...


@dataclass
class Transaction:
    """Base transaction implementation that satisfies TransactionProtocol.
    """

    value: float
    kind: str  # e.g., 'deposit', 'withdraw', 'transfer'
    description: Optional[str] = None
    date: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        desc = f" - {self.description}" if self.description else ""
        date_str = self.date.strftime("%Y-%m-%d %H:%M:%S")
        sign = "+" if self.value >= 0 else "-"
        return f"{date_str} | {self.kind.title():10s} | {sign}{abs(self.value):.2f}{desc}"

    def registrar(self, conta: "Account") -> None:
        """Default registration: add to account history if available (does not change balance).
        Concrete subclasses should override to modify balance where appropriate.
        """
        if getattr(conta, "history", None) is not None:
            try:
                conta.history.add(self)
            except Exception:
                pass


@dataclass
class Deposito(Transaction):
    def __post_init__(self) -> None:
        # ensure a default kind if not provided
        self.kind = self.kind or "deposit"

    def registrar(self, conta: "Account") -> None:
        if self.value <= 0:
            return

        # Prefer direct balance manipulation if present (fast path)
        if hasattr(conta, "_balance"):
            try:
                conta._balance += self.value
            except Exception:
                pass
        else:
            # Fallback to public API if available
            try:
                conta.deposit(self.value)
            except Exception:
                pass

        # register in history if present
        if getattr(conta, "history", None) is not None:
            try:
                conta.history.add(self)
            except Exception:
                pass


@dataclass
class Saque(Transaction):
    def __post_init__(self) -> None:
        self.kind = self.kind or "withdraw"

    def registrar(self, conta: "Account") -> None:
        # determine current balance if possible
        balance = getattr(conta, "_balance", None)
        if balance is None:
            try:
                balance = conta.balance
            except Exception:
                balance = None

        if self.value <= 0 or (balance is not None and self.value > balance):
            return

        if hasattr(conta, "_balance"):
            try:
                conta._balance -= self.value
            except Exception:
                pass
        else:
            try:
                conta.withdraw(self.value)
            except Exception:
                pass

        # register in history if present
        if getattr(conta, "history", None) is not None:
            try:
                conta.history.add(self)
            except Exception:
                pass
