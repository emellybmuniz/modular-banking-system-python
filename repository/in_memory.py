from typing import Any, Dict, List, Optional, Callable, Tuple


class InMemoryClientRepository:

    def __init__(self) -> None:
        self._store: Dict[int, Any] = {}
        self._next_id = 1

    def add(self, client: Any) -> int:
        key = self._next_id
        self._next_id += 1
        self._store[key] = client
        return key

    def get(self, key: int) -> Optional[Any]:
        return self._store.get(key)

    def list(self) -> List[Any]:
        return list(self._store.values())

    def remove(self, key: int) -> bool:
        if key in self._store:
            del self._store[key]
            return True
        return False

    def find(self, predicate: Callable[[Any], bool]) -> List[Any]:
        return [v for v in self._store.values() if predicate(v)]

    def clear(self) -> None:
        self._store.clear()
        self._next_id = 1


class InMemoryAccountRepository:

    def __init__(self) -> None:
        self._store: Dict[Tuple[str, int], Any] = {}

    def _key(self, account: Any) -> Tuple[str, int]:
        return getattr(account, "agency"), int(getattr(account, "number"))

    def add(self, account: Any) -> Tuple[str, int]:
        k = self._key(account)
        self._store[k] = account
        return k

    def get(self, agency: str, number: int) -> Optional[Any]:
        return self._store.get((agency, int(number)))

    def list(self) -> List[Any]:
        return list(self._store.values())

    def remove(self, agency: str, number: int) -> bool:
        k = (agency, int(number))
        if k in self._store:
            del self._store[k]
            return True
        return False

    def find_by_client(self, client: Any) -> List[Any]:
        return [acc for acc in self._store.values() if getattr(acc, "client", None) is client]

    def clear(self) -> None:
        self._store.clear()

