# Plano Estratégico — Modelagem e Modularização do Sistema Bancário (POO)

## 1. Objetivo curto
Transformar dados em **objetos** e separar responsabilidades de forma clara:
- **Domínio (models)** → regras e entidades do negócio  
- **Serviços** → orquestração das regras  
- **Interface (CLI)** → entrada e saída do usuário  
- **Infraestrutura** → armazenamento e persistência  

O foco é **arquitetura e caminho mental**, não implementação pronta.

---

## 2. Estrutura de pastas sugerida
banking/
├─ app.py # ponto de entrada do sistema
├─ cli/
│ ├─ init.py
│ └─ menu.py # apenas input/output
├─ domain/
│ ├─ init.py
│ ├─ cliente.py
│ ├─ pessoa_fisica.py
│ ├─ conta.py
│ ├─ conta_corrente.py
│ ├─ historico.py
│ └─ transacao.py # interface/abstração
├─ services/
│ ├─ init.py
│ ├─ usuario_service.py
│ ├─ conta_service.py
│ └─ transacao_service.py
├─ repository/
│ ├─ init.py
│ ├─ in_memory.py
│ └─ persistence.py # opcional
├─ tests/
│ ├─ test_conta.py
│ └─ test_services.py
└─ README.md

yaml
Copy code

**Racional:** cada camada tem um motivo único para mudar.

---

## 3. Leitura do UML → responsabilidades
### Cliente / PessoaFisica
- Dono das contas
- Guarda dados pessoais
- Gerencia **referências** às contas (não lógica bancária)

### Conta (classe base)
- Mantém saldo (protegido)
- Executa depósito e saque
- Registra histórico
- Não conhece menu nem armazenamento

### ContaCorrente
- Especialização da Conta
- Regras adicionais: limite, número de saques

### Histórico
- Guarda transações
- Gera extrato
- Não executa regras bancárias

### Transação (interface)
- Contrato comum para ações bancárias
- Implementações: Saque, Depósito
- Cada transação sabe **como se registrar**

---

## 4. Interfaces e abstrações
- Use `ABC` ou `Protocol` para:
  - `Transacao`
  - (opcional) `Repository`
- Interface só quando há **variação de comportamento**
- Evite abstração por esporte

---

## 5. Público vs Privado (regra de ouro)
- **Métodos públicos:** ações do domínio  
  - `depositar()`, `sacar()`, `extrato()`
- **Métodos privados (`_`)**:
  - validações
  - detalhes internos
- **Atributos sensíveis protegidos**
  - `saldo` → apenas leitura via `@property`

---

## 6. Assinaturas
```python
class Conta(ABC):
    def depositar(self, valor: float) -> bool: ...
    def sacar(self, valor: float) -> bool: ...
    @property
    def saldo(self) -> float: ...

class Transacao(ABC):
    def registrar(self, conta: Conta) -> bool: ...

```
Essas assinaturas guiam seu código sem resolver o exercício.


7. Onde ficam as regras de negócio

Validação de saldo -> Conta
Limite de saque ->	ContaCorrente
Criação de contas -> ContaService
Associação cliente-conta -> UsuarioService
Fluxo de menu -> CLI


8. Repositório (armazenamento)
Substitui listas/dicionários globais

Interface simples:

add(obj)

remove(obj)

get_all()

find(predicate)

Comece com InMemory, troque depois sem dor

9. Roteiro de execução (ordem segura)
Criar skeletons das classes (sem lógica)

Implementar Conta + testes

Implementar Historico e Transacao

Substituir dicionários por objetos

Criar Repository

Criar Services

Refatorar menu para usar services

Adicionar persistência (opcional)

10. Refatoração de funções antigas
Antes (procedural)	Depois (POO)
depositar(saldo)	conta.depositar(valor)
sacar()	conta.sacar(valor)
extrato()	conta.extrato()

11. Testes mínimos esperados
Depósito altera saldo

Saque inválido falha

Histórico registra trans

12. Critérios de aceitação

Nenhum dicionário representando cliente ou conta

Menu funciona chamando serviços

Regras isoladas do CLI

Código legível e extensível

13. Armadilhas comuns

Expor saldo para escrita direta

Colocar lógica no menu

Usar herança onde composição resolve

Misturar persistência com domínio

14. Extensões futuras (opcional)

Persistência em JSON

Padrão Command para transações

Logs e auditoria

Transferência entre contas