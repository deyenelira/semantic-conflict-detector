# pedidos.py
from servicos import db, enviar_nota_fiscal


def listar_pedidos(cliente_id):
    return [p for p in db.pedidos() if p.cliente_id == cliente_id]


def reenviar_notas(cliente_id):
    for pedido in listar_pedidos(cliente_id):
        enviar_nota_fiscal(pedido)


def gerar_extrato(cliente_id):
    pedidos = listar_pedidos(cliente_id)
    total = sum(p.valor for p in pedidos)
    linhas = [f"{p.id}: R$ {p.valor:.2f}" for p in pedidos]
    return {"total": total, "linhas": linhas}
