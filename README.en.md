# Modular Banking System (Python)
[🇺🇸 English](./README.en.md) | [🇧🇷 Português](./README.md)

![GitHub License](https://img.shields.io/github/license/emellybmuniz/modular-banking-system-python)
![GitHub language count](https://img.shields.io/github/languages/count/emellybmuniz/modular-banking-system-python)
![GitHub last commit](https://img.shields.io/github/last-commit/emellybmuniz/modular-banking-system-python)
![GitHub repo size](https://img.shields.io/github/repo-size/emellybmuniz/modular-banking-system-python)
![Project Status](https://img.shields.io/badge/Status%20-%20Completed%20-%20%234BC21E )

This repository contains a didactic implementation of a modular banking system written in Python. The goal was to refactor a simple implementation that used dictionaries to store clients and accounts into an object-oriented design following a UML-like model, with a clear separation between domain, repository, services, and interface (CLI). The project focuses on class modeling (clients, accounts, transactions), banking operations (deposit, withdrawal), an in-memory repository, and a CLI menu for interaction.

---

### ✅ Checklist of completed items
- [x] Domain class modeling (Client, Account, History, Transaction, CheckingAccount).
- [x] In-memory repositories for clients and accounts.
- [x] Services that encapsulate business logic (create client/account, deposit, withdraw, statement, balance).
- [x] Basic CLI menu for interacting with the system (create user, create account, deposit, withdraw, view statement, list accounts).
- [x] Migration of stored data from dictionaries to objects (OOP) following the bootcamp requirements.
- [x] Automated tests (pytest) validating the main flows and business rules (`tests/test_integration.py`).

---

## 📋 Table of Contents
- [Challenge Description](#challenge-description)
- [Solution Overview](#solution-overview)
- [Project Structure](#project-structure)
- [How It Works (components)](#how-it-works-components)
- [What was changed / How the challenge was solved](#what-was-changed--how-the-challenge-was-solved)
- [How to Run (CLI and tests)](#how-to-run-cli-and-tests)
- [Prerequisites](#prerequisites)
- [Contributing](#contributing)
- [License and Author](#license-and-author)

---

## 📌 Challenge Description
Provided by the Luizalabs bootcamp - Back-end with Python (DIO):

General Objective
- Start modeling a banking system in OOP. Add classes for client and basic banking operations: deposit and withdrawal.

Challenge
- Update the banking system implementation to store clients and bank accounts as objects (class instances) instead of dictionaries.
- Follow the provided UML class model (domain modeling).
- After completing the class modeling and implementing the methods, update the menu option handlers so they work with the modeled classes.

---

## 🧭 Solution Overview
The solution adopts a simple, modular architecture with clearly defined responsibilities:
- domain/: model classes (Client, Account, CheckingAccount, History, Transaction).
- repository/: in-memory repositories (InMemory) and a small persistence helper to obtain repositories (singletons during execution).
- services/: business orchestration (AccountService, TransactionService, UserService).
- cli/: terminal-based user interface (menu and handlers that use services).
- tests/: automated tests (pytest) covering main flows.

Design principles applied:
- Single responsibility and separation of concerns: domain, repository, services and interface are decoupled.
- Dependency injection: services accept repository instances for easier testing and swapping of implementations.
- Object-oriented design: clients, accounts and history are represented by objects instead of dictionaries.

---

## 📂 Project Structure (detailed)
Root layout (simplified):

```
modular-banking-system-python/
├── app.py                     # CLI application: orchestrates menu and services
├── cli/                       # CLI helpers and menu
│   └── menu.py
├── domain/                    # Domain models
│   ├── account.py
│   ├── checking_account.py
│   ├── client.py
│   ├── natural_person.py
│   ├── history.py
│   └── transaction.py
├── repository/                # In-memory repositories and persistence helpers
│   ├── in_memory.py
│   └── persistence.py
├── services/                  # Application services
│   ├── account_service.py
│   ├── transaction_service.py
│   └── user_service.py
├── tests/                     # Integration tests (pytest)
│   └── test_integration.py
├── README.md
└── pytest.ini
```

Each package has a clear responsibility: `domain` contains business entities; `repository` abstracts storage; `services` implement business operations; `cli` handles user interaction.

---

## ⚙️ How It Works (components and responsibilities)

Domain (models)
- Client / NaturalPerson: represent the account holder. They keep basic fields and a reference to a `History` (statement) and their accounts.
- Account / CheckingAccount: represent bank accounts. They contain `agency`, `number`, `_balance`, `history`, and methods for deposit/withdraw (implemented via `Transaction`).
- Transaction / Deposito / Saque: objects that encapsulate value, type, date and know how to register themselves on an `Account` (update balance and add an entry to `History`).
- History: collection of transactions and a formatted statement generator.

Repository
- InMemoryClientRepository / InMemoryAccountRepository: simple implementations that store objects in-memory and expose methods (add, get, list, remove, find).
- persistence.py: provides singleton accessors for repositories and a `reset_repos()` function used by tests to ensure a clean state between runs.

Services
- AccountService: creates clients and accounts, lists accounts and finds accounts by client. When creating a client, it attaches a `History` so transactions are recorded.
- TransactionService: manages deposit, withdraw, get_balance, get_statement and get_transactions. It validates the account existence and operation values.
- UserService: alternative helper for managing users directly via repository.

CLI
- `app.py` (class `BankingCLI`) provides an interactive menu: create user, create account, deposit, withdraw, view statement, list accounts, remove user.
- The CLI uses the services and repositories to perform operations. Inputs are validated and exceptions are handled with user-friendly messages.

---

## 🛠️ What was changed to solve the challenge
Summary of modifications and design decisions:

1. Class modeling
   - Converted client and account records from dictionary-based structures to domain classes (`NaturalPerson`, `CheckingAccount`, `Account`, `History`, `Transaction`).
   - The modeling follows typical UML concepts for Client, Account, Transaction and History.

2. In-memory repositories
   - Implemented `InMemoryClientRepository` and `InMemoryAccountRepository` that hold objects in private structures and expose simple CRUD-like methods.
   - `persistence.py` provides singleton accessors and `reset_repos()` to reinitialize state for tests.

3. Services
   - `AccountService` validates business rules when creating clients/accounts (e.g., duplicate CPF or account) and ensures a `History` is associated with each created client.
   - `TransactionService` validates account existence and amounts, creates `Deposito`/`Saque` transactions, and registers them in account history.

4. CLI
   - Menu handlers in `app.py` were updated to work with domain objects and use service APIs instead of manipulating dictionaries or raw IDs.

5. Tests
   - Added `tests/test_integration.py` with integration tests that exercise services using in-memory repositories.
   - `tests/conftest.py` ensures the project root is on `sys.path` during tests.
   - Registered a custom `integration` marker in `pytest.ini`.

---

## 🧪 Example flows (step-by-step)

1) Create a user and an account
- CLI asks for CPF, full name, birth date and address.
- `AccountService.create_customer()` checks CPF uniqueness and creates a `NaturalPerson` with an attached `History`.
- `AccountService.create_checking_account()` creates a `CheckingAccount` and associates it with the client (the client's history is propagated to the account).

2) Deposit
- `TransactionService.deposit()` finds the account by `agency` and `number`, validates the amount and creates a `Deposito` transaction.
- `Deposito.registrar()` increases the account `_balance` and appends the transaction to the account `History`.

3) Withdraw
- `TransactionService.withdraw()` validates sufficient funds and creates a `Saque` transaction.
- `Saque.registrar()` decreases the account `_balance` and appends the transaction to the account `History`.

4) Statement
- `TransactionService.get_statement()` returns `history.statement()` — a formatted string of transaction lines.

---

## 🚀 How to Run
Follow the steps below to run the CLI and tests locally.

### Prerequisites
- Python 3.10+ (recommended)
- pip

### Install dependencies for tests (optional)
This project only relies on the standard library and `pytest` for tests. Create a virtual environment and install pytest:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -U pip
pip install pytest
```

### Run the application (CLI)
From the project root in PowerShell:

```powershell
python app.py
```

Follow the interactive menu to create users, create accounts, and perform operations.

### Run tests

```powershell
pytest -q
# For a full report:
pytest -q -rA
```

---

## 🔍 Notes and important technical decisions
- The in-memory repository choice keeps the project simple and didactic; swapping to a persistent storage (SQLite, Postgres) only requires implementing repositories compatible with the current repository API.
- Transaction classes (`Deposito`/`Saque`) prefer to manipulate the account's `_balance` directly when registering for simplicity; validation and error handling occur in `TransactionService` and in transaction classes.
- `AccountService.create_customer()` now automatically attaches a `History` to each client — this ensures that all accounts for a client share a history and that statements work as expected.

---

## ♻️ Tests and quality
- Integration tests are located at `tests/test_integration.py` and cover main flows and validations.
- Use `reset_repos()` from `repository.persistence` in tests to ensure a clean state between test cases.

---

## 🤝 Contributing
Contributions are welcome. Feel free to open issues and submit pull requests.

Suggested workflow:
1. Fork the repository
2. Create a feature branch
3. Test locally before opening a PR

---

## 🔑 License
This repository is provided for educational purposes and is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## ✍️ Author

Developed by Emelly Beatriz ❤️

📬 Contact:

📧 emellybmuniz@gmail.com
💼 [LinkedIn](https://www.linkedin.com/in/emellybmuniz)
🐙 [Github](https://github.com/emellybmuniz)


