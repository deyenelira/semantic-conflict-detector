# acessos.py
import logging

from servicos import metricas, render

log = logging.getLogger(__name__)


def registrar_acesso(usuario, pagina):
    log.info(f"{usuario} acessou {pagina}")
    metricas.incrementar(f"acessos:{pagina}")


def view_produto(request, produto_id):
    registrar_acesso(request.user, f"/produto/{produto_id}")
    return render(request, "produto.html", {"id": produto_id})


def view_categoria(request, slug):
    registrar_acesso(request.user, f"/categoria/{slug}")
    return render(request, "categoria.html", {"slug": slug})
