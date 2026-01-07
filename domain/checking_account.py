# python
from .account import Account
from typing import Optional, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import Client
    from .history import History


class CheckingAccount(Account):
    def __init__(
        self,
        number: int,
        agency: str,
        balance: float = 0.0,
        client: Optional["Client"] = None,
        history: Optional["History"] = None,
    ) -> None:
        super().__init__(number, agency, balance, client, history)

    # Inherits deposit, withdraw, statement from Account
