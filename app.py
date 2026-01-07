"""
Modular Banking System - CLI Application
Integrates with AccountService and TransactionService
"""
import textwrap
from datetime import datetime
from cli.menu import menu
from services.account_service import AccountService
from services.transaction_service import TransactionService
from repository.persistence import get_client_repo, get_account_repo

class BankingCLI:
    AGENCY = "0001"
    
    def __init__(self):
        self.account_service = AccountService()
        self.transaction_service = TransactionService()
        self.client_repo = get_client_repo()
        self.account_repo = get_account_repo()
        self.current_account = None

    def deposit(self):
        if not self._select_account_if_needed():
            return
        
        try:
            value = float(input("Digite o valor do depósito: "))
            self.transaction_service.deposit(
                agency=self.current_account.agency,
                number=self.current_account.number,
                value=value,
                description="Depósito via CLI"
            )
            print("\n=== Depósito realizado com sucesso! ===")
        except ValueError as e:
            print(f"\n@@@ Operação falhou! {e} @@@")
        except Exception as e:
            print(f"\n@@@ Erro: {e} @@@")

    def withdraw(self):
        if not self._select_account_if_needed():
            return

        try:
            value = float(input("Digite o valor do saque: "))
            self.transaction_service.withdraw(
                agency=self.current_account.agency,
                number=self.current_account.number,
                value=value,
                description="Saque via CLI"
            )
            print("\n=== Saque realizado com sucesso! ===")
        except ValueError as e:
            print(f"\n@@@ Operação falhou! {e} @@@")
        except Exception as e:
            print(f"\n@@@ Erro: {e} @@@")

    def show_statement(self):
        if not self._select_account_if_needed():
            return

        try:
            statement = self.transaction_service.get_statement(
                agency=self.current_account.agency,
                number=self.current_account.number
            )
            balance = self.transaction_service.get_balance(
                agency=self.current_account.agency,
                number=self.current_account.number
            )

            print("\n================ EXTRATO ================")
            if statement:
                print(statement)
            else:
                print("Nenhuma transação realizada.")
            print(f"\nSaldo:\t$ {balance:.2f}")
            print("==========================================")
        except Exception as e:
            print(f"\n@@@ Erro: {e} @@@")

    def create_user(self):
        cpf = input("Digite o CPF (apenas números): ")
        if not cpf.isdigit():
            print("\n@@@ CPF inválido! Digite apenas números. @@@")
            return

        name = input("Digite o nome completo: ")
        birth_date_str = input("Digite a data de nascimento (dd-mm-aaaa): ")
        address = input("Digite o endereço (rua, nº - bairro - cidade/estado): ")

        try:
            day, month, year = birth_date_str.split("-")
            birth_date = datetime(int(year), int(month), int(day)).date()

            customer = self.account_service.create_customer(
                name=name,
                cpf=cpf,
                birth_date=birth_date,
                address=address
            )
            print("\n=== Usuário criado com sucesso! ===")
        except ValueError as e:
            print(f"\n@@@ Operação falhou! {e} @@@")
        except Exception as e:
            print(f"\n@@@ Erro ao criar usuário: {e} @@@")

    def delete_user(self):
        cpf = input("Digite o CPF do usuário a ser removido: ")
        if not cpf.isdigit():
            print("\n@@@ CPF inválido! Digite apenas números. @@@")
            return

        customers = self.client_repo.find(lambda c: getattr(c, 'cpf', None) == cpf)
        if not customers:
            print("\n@@@ Usuário não encontrado! @@@")
            return

        customer = customers[0]

        accounts = self.account_service.find_accounts_by_customer(customer)
        for acc in accounts:
            self.account_repo.remove(acc.agency, acc.number)

        for key, client in self.client_repo._store.items():
            if client is customer:
                self.client_repo.remove(key)
                break

        if accounts:
            print(f"\n--- {len(accounts)} conta(s) associada(s) ao usuário foram removidas. ---")

        print("\n=== Usuário removido com sucesso! ===")

    def create_account(self):
        cpf = input("Digite o CPF do usuário: ")
        if not cpf.isdigit():
            print("\n@@@ CPF inválido! Digite apenas números. @@@")
            return

        customers = self.client_repo.find(lambda c: getattr(c, 'cpf', None) == cpf)
        if not customers:
            print("\n@@@ Usuário não encontrado, criação de conta abortada! @@@")
            return

        customer = customers[0]

        all_accounts = self.account_repo.list()
        account_number = len(all_accounts) + 1

        try:
            account = self.account_service.create_checking_account(
                customer=customer,
                number=account_number,
                agency=self.AGENCY,
                initial_balance=0.0
            )
            print("\n=== Conta criada com sucesso! ===")
        except ValueError as e:
            print(f"\n@@@ Operação falhou! {e} @@@")
        except Exception as e:
            print(f"\n@@@ Erro ao criar conta: {e} @@@")

    def list_accounts(self):
        accounts = self.account_service.list_accounts()

        if not accounts:
            print("\n@@@ Nenhuma conta registrada. @@@")
            return

        for account in accounts:
            client_name = account.client.name if account.client else "N/A"
            line = f"""\
                Agência:\t{account.agency}
                Conta:\t\t{account.number}
                Titular:\t{client_name}
                Saldo:\t$ {account.balance:.2f}
            """
            print("=" * 100)
            print(textwrap.dedent(line))

    def _select_account_if_needed(self):
        accounts = self.account_repo.list()

        if not accounts:
            print("\n@@@ Nenhuma conta registrada. Crie uma conta primeiro. @@@")
            return False

        if len(accounts) == 1:
            self.current_account = accounts[0]
            return True

        print("\n=== Selecionar uma conta ===")
        for idx, acc in enumerate(accounts, 1):
            client_name = acc.client.name if acc.client else "N/A"
            print(f"[{idx}] Agência: {acc.agency}, Conta: {acc.number}, Titular: {client_name}")

        try:
            choice = int(input("Digite o número da conta: "))
            if 1 <= choice <= len(accounts):
                self.current_account = accounts[choice - 1]
                return True
            else:
                print("\n@@@ Conta inválida! @@@")
                return False
        except (ValueError, IndexError):
            print("\n@@@ Seleção inválida! @@@")
            return False

    def run(self):
        print("\n=== Sistema Bancário Modular ===")
        print("Bem-vindo!")

        while True:
            option = menu()

            if option == "d":
                self.deposit()

            elif option == "s":
                self.withdraw()

            elif option == "e":
                self.show_statement()

            elif option == "n":
                self.create_user()

            elif option == "r":
                self.delete_user()

            elif option == "c":
                self.create_account()

            elif option == "l":
                self.list_accounts()

            elif option == "q":
                print("\n=== Encerrando. Até logo! ===")
                break

            else:
                print("\n@@@ Operação inválida, selecione novamente. @@@")


def main():
    cli = BankingCLI()
    cli.run()


if __name__ == "__main__":
    main()