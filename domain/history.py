from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .transaction import Transaction


class History:
    def __init__(self, transactions: Optional[List["Transaction"]] = None):
        self._transactions: List["Transaction"] = transactions or []

    @property
    def transactions(self) -> List["Transaction"]:
        return list(self._transactions)

    def add_transaction(self, transaction: "Transaction") -> None:
        self._transactions.append(transaction)


    def add(self, transaction: "Transaction") -> None:
        self.add_transaction(transaction)

    def list(self) -> None:
        print(self.generate_statement())

    def generate_statement(self) -> str:
        lines: List[str] = []
        for t in self._transactions:
            try:
                lines.append(str(t))
            except Exception:
                lines.append(repr(t))

        return "\n".join(lines)

    def statement(self) -> str:
        return self.generate_statement()
