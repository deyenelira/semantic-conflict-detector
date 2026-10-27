# precos.py


def obter_desconto(cliente):
    """Retorna o desconto como fração (0 a 1)."""
    return 0.15 if cliente.vip else 0


def preco_final(produto, cliente):
    return produto.preco * (1 - obter_desconto(cliente))


def formatar_preco(valor):
    return f"R$ {valor:.2f}"
