import pytest
from datetime import date

from repository.persistence import reset_repos, get_client_repo, get_account_repo
from services.account_service import AccountService
from services.transaction_service import TransactionService
from domain.natural_person import NaturalPerson


@pytest.fixture(autouse=True)
def reset_repositories():
    reset_repos()


@pytest.fixture
def account_service() -> AccountService:
    return AccountService(client_repo=get_client_repo(), account_repo=get_account_repo())


@pytest.fixture
def transaction_service() -> TransactionService:
    return TransactionService(account_repo=get_account_repo())


@pytest.fixture
def customer(account_service: AccountService) -> NaturalPerson:
    return account_service.create_customer(
        name="Alice",
        cpf="12345678900",
        birth_date=date(1990, 1, 1),
        address="Rua A, 123"
    )


@pytest.fixture
def checking_account(account_service: AccountService, customer: NaturalPerson):
    return account_service.create_checking_account(
        customer=customer,
        number=1001,
        agency="0001",
        initial_balance=0.0,
    )


# Tests
@pytest.mark.integration
def test_create_customer_and_account(account_service: AccountService):
    cust = account_service.create_customer(
        name="Bob",
        cpf="98765432100",
        birth_date=date(1985, 5, 20),
        address="Rua B, 456",
    )
    assert isinstance(cust, NaturalPerson)
    assert cust.cpf == "98765432100"

    acc = account_service.create_checking_account(
        customer=cust,
        number=2002,
        agency="0001",
        initial_balance=50.0,
    )
    assert acc.agency == "0001"
    assert acc.number == 2002
    assert acc.balance == 50.0


@pytest.mark.integration
def test_deposit_and_balance(transaction_service: TransactionService, checking_account):
    # Happy path deposit
    ok = transaction_service.deposit(agency=checking_account.agency, number=checking_account.number, value=200.0)
    assert ok is True
    balance = transaction_service.get_balance(agency=checking_account.agency, number=checking_account.number)
    assert balance == 200.0

    # Invalid deposit value
    with pytest.raises(ValueError):
        transaction_service.deposit(agency=checking_account.agency, number=checking_account.number, value=-10.0)


@pytest.mark.integration
def test_withdraw_and_balance(transaction_service: TransactionService, checking_account):
    # Seed with a deposit
    transaction_service.deposit(agency=checking_account.agency, number=checking_account.number, value=150.0)
    assert transaction_service.get_balance(checking_account.agency, checking_account.number) == 150.0

    ok = transaction_service.withdraw(agency=checking_account.agency, number=checking_account.number, value=40.0)
    assert ok is True
    assert transaction_service.get_balance(checking_account.agency, checking_account.number) == 110.0

    with pytest.raises(ValueError):
        transaction_service.withdraw(agency=checking_account.agency, number=checking_account.number, value=-5.0)

    with pytest.raises(ValueError):
        transaction_service.withdraw(agency=checking_account.agency, number=checking_account.number, value=999.0)


@pytest.mark.integration
def test_transactions_list_and_statement(transaction_service: TransactionService, checking_account):
    txs = transaction_service.get_transactions(agency=checking_account.agency, number=checking_account.number)
    assert isinstance(txs, list)
    assert len(txs) == 0

    transaction_service.deposit(agency=checking_account.agency, number=checking_account.number, value=100.0, description="Depósito inicial")
    transaction_service.withdraw(agency=checking_account.agency, number=checking_account.number, value=30.0, description="Saque pequeno")

    txs = transaction_service.get_transactions(agency=checking_account.agency, number=checking_account.number)
    assert len(txs) == 2
    kinds = [t.kind for t in txs]
    assert kinds == ["deposit", "withdraw"]

    stmt = transaction_service.get_statement(agency=checking_account.agency, number=checking_account.number)
    assert isinstance(stmt, str)
    assert "Deposit" in stmt or "Deposito" in stmt or "deposit" in stmt
    assert "Withdraw" in stmt or "Saque" in stmt or "withdraw" in stmt


@pytest.mark.integration
def test_error_on_unknown_account(transaction_service: TransactionService):
    with pytest.raises(ValueError):
        transaction_service.get_balance(agency="9999", number=999999)
    with pytest.raises(ValueError):
        transaction_service.deposit(agency="9999", number=999999, value=10.0)
    with pytest.raises(ValueError):
        transaction_service.withdraw(agency="9999", number=999999, value=10.0)
    with pytest.raises(ValueError):
        transaction_service.get_statement(agency="9999", number=999999)
    with pytest.raises(ValueError):
        transaction_service.get_transactions(agency="9999", number=999999)


@pytest.mark.integration
def test_duplicate_cpf_not_allowed(account_service: AccountService):
    account_service.create_customer(name="Carol", cpf="11122233344", birth_date=date(1992, 7, 15), address="Rua C, 789")
    with pytest.raises(ValueError):
        account_service.create_customer(name="Carol 2", cpf="11122233344", birth_date=date(1992, 7, 15), address="Rua D, 101")


@pytest.mark.integration
def test_duplicate_account_not_allowed(account_service: AccountService, customer: NaturalPerson):
    account_service.create_checking_account(customer=customer, number=3003, agency="0002", initial_balance=0.0)
    with pytest.raises(ValueError):
        account_service.create_checking_account(customer=customer, number=3003, agency="0002", initial_balance=0.0)

