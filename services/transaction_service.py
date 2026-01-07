from typing import List

from domain.transaction import Deposito, Saque, Transaction
from repository.persistence import get_account_repo


class TransactionService:
    def __init__(self, account_repo=None):
        self.account_repo = account_repo or get_account_repo()

    def deposit(self, agency: str, number: int, value: float, description: str = "Deposit") -> bool:
        """Execute a deposit transaction on the specified account.

        Args:
            agency: Account agency
            number: Account number
            value: Deposit amount
            description: Optional transaction description

        Returns:
            True if successful, False otherwise
        """
        account = self.account_repo.get(agency, number)
        if account is None:
            raise ValueError("Account not found")

        if value <= 0:
            raise ValueError("Deposit value must be positive")

        transaction = Deposito(value=value, kind='deposit', description=description)
        transaction.registrar(account)
        return True

    def withdraw(self, agency: str, number: int, value: float, description: str = "Withdraw") -> bool:
        """Execute a withdrawal transaction on the specified account.

        Args:
            agency: Account agency
            number: Account number
            value: Withdrawal amount
            description: Optional transaction description

        Returns:
            True if successful, False otherwise
        """
        account = self.account_repo.get(agency, number)
        if account is None:
            raise ValueError("Account not found")

        if value <= 0:
            raise ValueError("Withdrawal value must be positive")

        if value > account.balance:
            raise ValueError("Insufficient balance")

        transaction = Saque(value=value, kind='withdraw', description=description)
        transaction.registrar(account)
        return True

    def get_statement(self, agency: str, number: int) -> str:
        """Get the statement for the specified account.

        Args:
            agency: Account agency
            number: Account number

        Returns:
            Formatted statement string
        """
        account = self.account_repo.get(agency, number)
        if account is None:
            raise ValueError("Account not found")

        return account.statement()

    def get_balance(self, agency: str, number: int) -> float:
        """Get the current balance for the specified account.

        Args:
            agency: Account agency
            number: Account number

        Returns:
            Current balance
        """
        account = self.account_repo.get(agency, number)
        if account is None:
            raise ValueError("Account not found")

        return account.balance

    def get_transactions(self, agency: str, number: int) -> List[Transaction]:
        """Get all transactions for the specified account.

        Args:
            agency: Account agency
            number: Account number

        Returns:
            List of Transaction objects
        """
        account = self.account_repo.get(agency, number)
        if account is None:
            raise ValueError("Account not found")

        if account.history is None:
            return []

        return account.history.transactions

