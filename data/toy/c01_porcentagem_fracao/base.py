# precos.py


def obter_desconto(cliente):
    """Retorna o desconto em porcentagem (0 a 100)."""
    return 15 if cliente.vip else 0


def preco_final(produto, cliente):
    return produto.preco * (1 - obter_desconto(cliente) / 100)


def formatar_preco(valor):
    return f"R$ {valor:.2f}"
