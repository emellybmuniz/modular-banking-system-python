from .in_memory import InMemoryClientRepository, InMemoryAccountRepository

_client_repo: InMemoryClientRepository | None = None
_account_repo: InMemoryAccountRepository | None = None


def get_client_repo() -> InMemoryClientRepository:
    global _client_repo
    if _client_repo is None:
        _client_repo = InMemoryClientRepository()
    return _client_repo


def get_account_repo() -> InMemoryAccountRepository:
    global _account_repo
    if _account_repo is None:
        _account_repo = InMemoryAccountRepository()
    return _account_repo


def reset_repos() -> None:
    global _client_repo, _account_repo
    _client_repo = InMemoryClientRepository()
    _account_repo = InMemoryAccountRepository()

