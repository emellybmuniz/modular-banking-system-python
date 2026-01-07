import textwrap

def menu():
    menu_text = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [c]\tNova conta
    [l]\tListar contas
    [n]\tNovo usuário
    [r]\tRemover usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu_text))