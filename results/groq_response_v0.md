# Resultados da detecção de conflitos semânticos

## c01_porcentagem_fracao

### Prompt: `prompt_intencao_estado`

SIM  

**1. INTENÇÃO**  
- **LEFT**: mudou a representação do desconto de “porcentagem (0‑100)” para “fração (0‑1)” e ajustou `preco_final` para usar a fração diretamente.  
- **RIGHT**: manteve a representação original (porcentagem) e adicionou a função `preco_frete`, que calcula o frete usando a mesma lógica de desconto baseada em porcentagem.

**2. ESTADO**  
| Elemento | Onde é lido/escrito | Ordem de uso nos trechos alterados |
|----------|----------------------|------------------------------------|
| `obter_desconto(cliente)` – valor retornado (desconto) | Lido por `preco_final` (ambos) e por `preco_frete` (apenas RIGHT/MERGE). | 1️⃣ `obter_desconto` → 2️⃣ cálculo do preço ou frete. |
| `produto.preco` | Lido por `preco_final`. | Após obter desconto. |
| `frete` (parâmetro de `preco_frete`) | Lido por `preco_frete`. | Após obter desconto. |
| Resultado de `preco_final` / `preco_frete` | Valor retornado das funções. | Não há escrita de estado externo. |

**3. TABELA**

| Elemento X                | BASE (porcentagem) | LEFT (fração) | RIGHT (porcentagem) | MERGE |
|---------------------------|--------------------|---------------|----------------------|-------|
| `obter_desconto(vip)`     | 15                 | 0.15          | 15                   | 0.15 |
| `obter_desconto(não‑vip)`| 0                  | 0             | 0                    | 0 |
| `preco_final` (vip)       | `p * 0.85`         | `p * 0.85`    | `p * 0.85`           | `p * 0.85` |
| `preco_frete` (vip)       | – (não existe)     | – (não existe) | `f * 0.85`          | `f * (1 - 0.15/100) = f * 0.9985` |
| `preco_frete` (não‑vip)   | –                  | –             | `f * 1.0`            | `f * (1 - 0/100) = f * 1.0` |

**4. CRITÉRIO**  

- **Condição (a)**: Não há elemento que seja igual em BASE, LEFT e RIGHT e diferente no MERGE.  
- **Condição (b)**: `obter_desconto` difere de BASE em RIGHT (mantém 15) e MERGE **não** preserva esse valor (passa a 0.15).  
  Também, a função `preco_frete` introduzida por RIGHT depende do desconto em porcentagem; no MERGE o desconto foi alterado para fração, portanto o comportamento de `preco_frete` mudou (de `f*0.85` para `f*0.9985`).  

Assim, há pelo menos um X que atende ao critério (b).

**5. Conclusão**  
O merge introduziu um conflito semântico: a mudança de unidade do desconto feita por LEFT quebra a lógica de `preco_frete` adicionada por RIGHT. Portanto, o merge **não** preserva o comportamento desejado por ambos os lados.

---

### Prompt: `prompt_one_shot_cleantext`

SIM  

**1. INTENÇÃO**  
- **LEFT**: mudar a API de `obter_desconto` para devolver a fração do desconto (0 → 1) e adaptar `preco_final` ao novo retorno.  
- **RIGHT**: manter o retorno em porcentagem (0 → 100) e acrescentar a função `preco_frete`, que calcula o preço do frete usando a mesma lógica percentual.

**2. ESTADO**  
| Elemento de estado                         | Onde é lido/escrito | Ordem de execução relevante |
|--------------------------------------------|---------------------|-----------------------------|
| Valor retornado por `obter_desconto(cliente)` (desconto) | Lido por `preco_final` e por `preco_frete` | `obter_desconto` → cálculo do preço |
| Cálculo de `preco_final` (produto × (1‑desconto)) | Escrita (valor retornado) | `obter_desconto` → multiplicação |
| Cálculo de `preco_frete` (frete × (1‑desconto/100)) | Escrita (valor retornado) | `obter_desconto` → divisão por 100 → multiplicação |

**3. TABELA**

| X (elemento)                               | BASE                                   | LEFT                                   | RIGHT                                  | MERGE (resultado)                                 |
|--------------------------------------------|----------------------------------------|----------------------------------------|----------------------------------------|---------------------------------------------------|
| `obter_desconto(cliente)` (valor)          | 15  (percentual) se VIP, 0 caso contrário | 0.15 (fração) se VIP, 0 caso contrário | 15  (percentual) se VIP, 0 caso contrário | 0.15 (fração) – valor escolhido por LEFT          |
| Cálculo de `preco_final`                    | `preco * (1‑obter_desconto/100)`       | `preco * (1‑obter_desconto)`           | idem ao BASE                           | `preco * (1‑obter_desconto)` – mantém intenção LEFT |
| Cálculo de `preco_frete` (nova função)     | — (não existe)                         | — (não existe)                         | `frete * (1‑obter_desconto/100)`       | `frete * (1‑obter_desconto/100)` – usa desconto em fração |

**4. CRITÉRIO**  

- Para o elemento **desconto**, LEFT e RIGHT divergiam de BASE; MERGE adotou a versão LEFT, portanto o valor do desconto mudou em relação à intenção de RIGHT.  
- Mais importante, para **`preco_frete`** (introduzido por RIGHT) a expectativa era:  
  `frete * (1‑desconto_percentual/100)` → 15 % de redução quando o cliente é VIP.  
  No MERGE, o mesmo código usa `obter_desconto` que agora devolve **fração** (0.15), produzindo:  
  `frete * (1‑0.15/100) = frete * 0.9985` → **0,15 %** de redução.  

Assim, existe um X (o cálculo de `preco_frete`) que era idêntico em BASE e RIGHT, mas ficou **diferente** no MERGE (critério a), ou, visto que RIGHT alterou o comportamento de `preco_frete` em relação a BASE e o MERGE **não preservou** essa alteração (critério b).  

Portanto, o merge introduziu um conflito semântico.

---

### Prompt: `prompt_teste_mental`

**SIM**

---

## PASSO 1 – ENTENDER O CÓDIGO  

| Versão | O que o código faz | O que mudou | Intenção provável do desenvolvedor |
|--------|-------------------|-------------|------------------------------------|
| **BASE** | `obter_desconto` devolve **porcentagem** (0‑100). `preco_final` calcula o preço com desconto usando `valor * (1 - desconto/100)`. `formatar_preco` apenas formata o número. | – | O desconto deve ser especificado em **porcentagem**; todas as funções que calculam valores com desconto esperam esse formato. |
| **LEFT** | Alterou `obter_desconto` para devolver **fração** (0‑1). Ajustou `preco_final` para usar a fração diretamente (`valor * (1 - desconto)`). | Mudança de unidade de retorno (porcentagem → fração) e adaptação do cálculo em `preco_final`. | O desenvolvedor queria simplificar a API, usando a forma já “normalizada” (0‑1) que é comum em cálculos matemáticos. |
| **RIGHT** | Mantém tudo igual ao BASE e **adiciona** a função `preco_frete`, que calcula o frete com desconto usando a mesma lógica de porcentagem (`frete * (1 - obter_desconto(cliente) / 100)`). | Introdução de nova funcionalidade (cálculo de frete). | O desenvolvedor pretende que o frete seja descontado **na mesma base percentual** usada para o preço do produto. |
| **MERGE** | Herdou as mudanças de LEFT (desconto como fração) **e** a nova função de RIGHT (`preco_frete`). Porém `preco_frete` continua dividindo o valor retornado por 100, assumindo que `obter_desconto` ainda devolve porcentagem. | Combinação das duas alterações sem ajuste de compatibilidade. | O merge automático juntou as modificações, mas não reconciliou a diferença de unidade entre `obter_desconto` e a fórmula de `preco_frete`. |

**Ordem de execução no MERGE:**  
1. `obter_desconto` (versão LEFT) – retorna fração.  
2. `preco_final` (versão LEFT) – usa a fração corretamente.  
3. `preco_frete` (versão RIGHT) – usa a mesma chamada a `obter_desconto`, porém ainda aplica a divisão por 100, acreditando que o retorno é percentual.

---

## PASSO 2 – IDENTIFICAR AS VARIÁVEIS DE ESTADO  

Variáveis/leitura/escrita afetadas pelos trechos alterados:

| Variável / Campo | Onde é lida/escrita | Impacto nas duas branches |
|------------------|---------------------|----------------------------|
| `cliente.vip`   | Lida em `obter_desconto` (LEFT & RIGHT) | Base comum a ambos. |
| **Valor retornado por `obter_desconto`** (desconto) | Lido por `preco_final` (BASE, LEFT, RIGHT) e por `preco_frete` (RIGHT, MERGE) | **Criticamente diferente** entre LEFT (fração) e RIGHT (porcentagem). |
| `produto.preco`  | Lido em `preco_final` | Não alterado nas branches; uso consistente. |
| `frete`          | Lido em `preco_frete` | Só existe em RIGHT/MERGE. |
| Resultado de `preco_frete` | Valor calculado e retornado | Só LEFT não tem, RIGHT tem cálculo correto, MERGE tem cálculo incorreto. |

A variável de maior relevância para o conflito semântico é **o desconto retornado por `obter_desconto`**, pois sua unidade mudou e isso afeta diretamente `preco_frete`.

---

## PASSO 3 – SIMULAR UM CASO QUE SATISFAÇA OS CRITÉRIOS  

Escolha de estado inicial:  

- `cliente.vip = True` (cliente VIP).  
- `produto.preco = 100.0` (valor qualquer).  
- `frete = 20.0`.

### Execução

| Versão | `obter_desconto(cliente)` | Cálculo de `preco_frete(frete, cliente)` | Valor obtido |
|--------|---------------------------|------------------------------------------|--------------|
| **BASE** | `15` (porcentagem) | `20 * (1 - 15/100)` = `20 * 0.85` | **17.00** |
| **LEFT** | `0.15` (fração) | *função inexistente* | – |
| **RIGHT** | `15` (porcentagem) | `20 * (1 - 15/100)` = `20 * 0.85` | **17.00** |
| **MERGE** | `0.15` (fração) | `20 * (1 - 0.15/100)` = `20 * 0.9985` | **19.97** (aprox.) |

### Análise dos critérios  

- **Critério (a):** Não há variável que mantenha o mesmo valor em BASE, LEFT e RIGHT e mude no MERGE.  
- **Critério (b):** O valor retornado por `preco_frete` **difere** de BASE/RIGHT (`17.00`) e **não preserva** o valor que RIGHT introduziu (`17.00`). No MERGE o valor é `≈19.97`, portanto a mudança feita por RIGHT foi violada.

---

## PASSO 4 – CONCLUIR  

A simulação demonstra que a alteração de LEFT (mudança da unidade de desconto) rompeu a suposição feita por RIGHT ao implementar `preco_frete`. No merge, `preco_frete` continua usando a lógica de porcentagem (divide por 100) enquanto `obter_desconto` já devolve fração.  

**Resultado:** há conflito semântico. A intenção do desenvolvedor da **branch RIGHT** (aplicar o mesmo desconto percentual ao frete) foi violada pelo ajuste de unidade introduzido na **branch LEFT**.  

---

---

## n02_nova_view_sem_duplicar

### Prompt: `prompt_intencao_estado`

NAO  

**1. INTENÇÃO**  
- **LEFT:** Quer registrar, além do log, a métrica de acesso (`metricas.incrementar`) para toda página visitada.  
- **RIGHT:** Quer expor a página de categoria, adicionando a view `view_categoria` que registra o acesso (log) e renderiza o template correspondente.

**2. ESTADO**  
| Elemento / Ação                     | Tipo                | Onde é lido / escrito |
|-------------------------------------|---------------------|-----------------------|
| `log.info`                          | efeito colateral (log) | `registrar_acesso` (BASE, LEFT, RIGHT, MERGE) |
| `metricas.incrementar`              | efeito colateral (contagem) | `registrar_acesso` (apenas em LEFT e MERGE) |
| Chamada a `render`                  | retorno de resposta HTTP | `view_produto` (BASE, LEFT, RIGHT, MERGE) e `view_categoria` (RIGHT, MERGE) |
| Argumentos de `registrar_acesso` (`usuario`, `pagina`) | parâmetros de entrada | passado por `view_produto` e `view_categoria` |
| Dicionário passado a `render` (`{"id": …}` ou `{"slug": …}`) | valor retornado ao cliente | construído em `view_produto` / `view_categoria` |

**3. TABELA**

| Elemento X                | BASE                               | LEFT (inclui métrica)                              | RIGHT (nova view)                              | MERGE (ambas)                                   |
|---------------------------|------------------------------------|---------------------------------------------------|------------------------------------------------|-------------------------------------------------|
| Log de acesso             | `log.info("user acessou /produto/...")` | mesmo log + métrica                                 | mesmo log (sem métrica)                         | mesmo log + métrica (para ambas views)          |
| Métrica de acesso         | **não existe**                     | `metricas.incrementar("acessos:/produto/...")`   | **não existe**                                 | `metricas.incrementar("acessos:/produto/...")`<br>`metricas.incrementar("acessos:/categoria/...")` |
| Render da página produto  | `render(..., {"id": produto_id})`  | idêntico                                          | idêntico                                        | idêntico                                         |
| Render da página categoria| **não existe**                     | **não existe**                                    | `render(..., {"slug": slug})`                  | `render(..., {"slug": slug})`                   |

**4. CRITÉRIO**  

- Não há nenhum elemento X que seja idêntico em BASE, LEFT e RIGHT e que mude no MERGE (condição a).  
- Para o elemento `metricas.incrementar`, ele foi introduzido apenas em LEFT; o MERGE **preserva** essa alteração (condição b).  
- A nova view `view_categoria` foi adicionada apenas em RIGHT; o MERGE também a preserva.  

Portanto, nenhuma das condições de conflito semântico foi violada.  

**5. CONCLUSÃO**  
Não há conflito semântico introduzido pelo merge.

---

### Prompt: `prompt_one_shot_cleantext`

**NAO**

---

### 1. INTENÇÃO
- **LEFT**: ampliar `registrar_acesso` para também registrar a contagem de acessos em `metricas` (incrementar a métrica `"acessos:{pagina}"`).
- **RIGHT**: introduzir nova view `view_categoria`, que também registra o acesso (usando a mesma função) e renderiza a página de categoria.

### 2. ESTADO
Elementos de estado observados nos trechos alterados:

| Elemento                         | Tipo de acesso | Onde ocorre                                    | Ordem de execução relevante |
|----------------------------------|----------------|------------------------------------------------|------------------------------|
| `log.info`                       | escrita (log)  | `registrar_acesso` (BASE, LEFT, RIGHT, MERGE)  | primeira dentro da função   |
| `metricas.incrementar`           | escrita (contagem) | `registrar_acesso` – **apenas em LEFT e MERGE** | logo após o log              |
| Função `view_produto`            | leitura (chama `registrar_acesso`) | BASE, LEFT, RIGHT, MERGE | chamada direta ao retornar |
| Função `view_categoria`          | leitura (chama `registrar_acesso`) | **apenas em RIGHT e MERGE** | chamada direta ao retornar |
| Dicionário de contexto passado ao `render` | leitura/escrita (passagem de dados) | Cada view passa seu próprio dicionário | não interfere entre si |

### 3. TABELA DE VALORES/COMPORTAMENTO

| Elemento                | BASE                                 | LEFT (após mudança)                                            | RIGHT (após mudança)                                            | MERGE (resultado)                                               |
|-------------------------|--------------------------------------|----------------------------------------------------------------|------------------------------------------------------------------|-----------------------------------------------------------------|
| `log.info`              | registra `"usuario acessou pagina"` | idem                                                          | idem                                                            | idem                                                            |
| `metricas.incrementar`  | **não existe**                       | **executado** → incrementa `"acessos:{pagina}"`               | **não existe**                                                  | **executado** (preservado)                                      |
| `view_produto`          | existe, chama `registrar_acesso`     | idem (chama a versão de `registrar_acesso` que inclui métrica) | idem (chama a mesma versão)                                     | idem                                                            |
| `view_categoria`        | **não existe**                       | **não existe**                                                | **existe** → registra acesso e renderiza categoria                | **existe** (preservado)                                         |
| Dicionário de contexto  | `{ "id": produto_id }`               | idem                                                          | `{ "slug": slug }` (apenas na nova view)                         | idem em cada respectiva view                                    |

### 4. CRITÉRIO DE CONFLITO
- **(a) Igual em BASE, LEFT e RIGHT, diferente em MERGE**:  
  Nenhum elemento atende a esse caso. O único elemento que muda ( `metricas.incrementar` ) não está presente nem em BASE nem em RIGHT.
- **(b) Diferença de LEFT (ou RIGHT) em relação a BASE que não é preservada no MERGE**:  
  - `metricas.incrementar` foi adicionado em LEFT e **preservado** no MERGE.  
  - `view_categoria` foi adicionada em RIGHT e **preservada** no MERGE.  

Portanto, nenhum dos critérios de conflito semântico foi satisfeito.

---  

**Conclusão:** o merge não introduziu um conflito semântico.

---

### Prompt: `prompt_teste_mental`

SIM  

**PASSO 1 – ENTENDER O CÓDIGO**  

| Versão | O que o código faz | O que mudou | Intenção provável do desenvolvedor |
|--------|-------------------|-------------|------------------------------------|
| **BASE** | `registrar_acesso` grava no log que *usuário* acessou *página*. <br>`view_produto` chama `registrar_acesso` e devolve o template *produto.html*. | – | Apenas registrar a visita no log. |
| **LEFT** | Mesma coisa que BASE, porém `registrar_acesso` também chama `metricas.incrementar` para contar o acesso. | Adição de `metricas.incrementar(f"acessos:{pagina}")` dentro de `registrar_acesso`. | O desenvolvedor quer que **todas** as visitas (produto, categoria, etc.) sejam contabilizadas em métricas. |
| **RIGHT** | Mantém o comportamento de BASE e ainda acrescenta uma nova view `view_categoria`, que também usa `registrar_acesso` e devolve *categoria.html*. | Nova função `view_categoria`. | O desenvolvedor só quer expor a página de categoria, sem mudar a lógica de registro de acesso. |
| **MERGE** | Contém a mudança de LEFT (contagem de métricas) **e** a nova view de RIGHT. Não há conflito textual; o merge escolheu a implementação de `registrar_acesso` de LEFT e adicionou `view_categoria` de RIGHT. | – | O código resultante registra no log **e** incrementa métricas para **todas** as páginas, incluindo a nova categoria. |

**PASSO 2 – IDENTIFICAR AS VARIÁVEIS DE ESTADO**  

1. **`metricas`** – objeto (ou módulo) que recebe chamadas `incrementar(chave)`.  
2. **`log`** – logger que recebe `info`.  
3. **`request.user`** – usuário que está fazendo a requisição (lido).  
4. **Argumentos `pagina`/`slug`** – strings usadas para montar a chave da métrica.  

As duas mudanças afetam a primeira: **`metricas`**. O log continua igual, portanto não gera conflito.

**PASSO 3 – SIMULAR UM CASO QUE SATISFAÇA OS CRITÉRIOS**  

Escolha de entrada:  

```python
request.user = "alice"
produto_id = 42
slug = "eletronics"
```

Estado inicial das métricas (supondo que todas as contagens comecem em 0):

| Métrica                     | Valor inicial |
|-----------------------------|---------------|
| "acessos:/produto/42"       | 0 |
| "acessos:/categoria/eletronics" | 0 |

Execução passo a passo:

| Versão | Operação executada | Efeito em `metricas` |
|--------|--------------------|----------------------|
| **BASE** | `view_produto(request,42)` → `registrar_acesso` (apenas log) | Nenhum incremento. |
| **LEFT** | `view_produto(request,42)` → `registrar_acesso` (log + `metricas.incrementar("acessos:/produto/42")`) | `"acessos:/produto/42"` passa de 0 → 1. |
| **RIGHT** | `view_categoria(request,"eletronics")` → `registrar_acesso` (apenas log) | Nenhum incremento. |
| **MERGE** | `view_categoria(request,"eletronics")` → `registrar_acesso` (log + `metricas.incrementar("acessos:/categoria/eletronics")`) | `"acessos:/categoria/eletronics"` passa de 0 → 1. |

Resultado das contagens para a métrica da categoria:

- **BASE** : 0  
- **LEFT** : (não existe `view_categoria`) – não aplicável.  
- **RIGHT** : 0  
- **MERGE** : 1  

Isso corresponde ao critério **(b)**: a variável de estado *contador de métricas para a página de categoria* difere de BASE/RIGHT, e o MERGE **não preserva** o valor esperado (0).

**PASSO 4 – CONCLUIR**  

Foi encontrada uma variável de estado (`metricas` – contagem de acessos) que satisfaz o critério (b). O comportamento introduzido pelo merge (incremento da métrica para a nova view de categoria) **não** corresponde ao que o desenvolvedor da branch RIGHT pretendia, já que ele não alterou `registrar_acesso` nem mencionou a necessidade de métricas adicionais. Portanto, há um **conflito semântico** e a intenção do desenvolvedor da branch RIGHT foi violada.

---

## c05_lista_vira_gerador

### Prompt: `prompt_intencao_estado`

**SIM**

---

### 1. INTENÇÃO  
- **LEFT**: substituir a lista retornada por `listar_pedidos` por um *generator* para evitar carregar todos os pedidos em memória.  
- **RIGHT**: introduzir a nova função `gerar_extrato` que soma os valores dos pedidos e gera uma lista de linhas formatadas, assumindo que `listar_pedidos` devolve uma coleção reutilizável (lista).

### 2. ESTADO  
| Elemento de estado | Onde é lido/escrito | Observação de ordem |
|--------------------|---------------------|----------------------|
| **Resultado de `listar_pedidos`** (coleção de pedidos) | - `reenviar_notas` (itera uma vez) <br> - `gerar_extrato` (itera duas vezes: `sum` e depois compreensão de lista) | Em `gerar_extrato` a mesma variável `pedidos` é consumida duas vezes sequencialmente. |
| **Variável `total`** | Escrita em `gerar_extrato` (`sum`) | Depende da primeira iteração sobre `pedidos`. |
| **Variável `linhas`** | Escrita em `gerar_extrato` (compreensão de lista) | Depende da segunda iteração sobre `pedidos`. |
| **Saída de `gerar_extrato`** (`{"total": ..., "linhas": [...]}`) | Retorno da função | Deve conter todas as linhas formatadas. |

### 3. TABELA DE VALORES/COMPORTAMENTO  

| Elemento X | BASE | LEFT | RIGHT | MERGE |
|------------|------|------|-------|-------|
| **`listar_pedidos` retorna** | **lista** (ex.: `[p1, p2, …]`) | **generator** (`(p for …)`) | **lista** | **generator** (mesmo código de LEFT) |
| **Iteração 1 sobre `pedidos` (para `sum`)** | Percorre toda a lista → soma correta | Consome o generator → soma correta | Percorre a lista → soma correta | Consome o generator → soma correta |
| **Iteração 2 sobre `pedidos` (para `linhas`)** | Percorre a lista novamente → linhas completas | Generator já está esgotado → **nenhum elemento** → `linhas = []` | Percorre a lista novamente → linhas completas | Generator já está esgotado → **nenhum elemento** → `linhas = []` |
| **`gerar_extrato` devolve** | *não existe* | *não existe* | `{"total": soma, "linhas": ["id: R$ valor", …]}` (linhas completas) | `{"total": soma, "linhas": []}` (linhas vazias) |

### 4. CRITÉRIO DE CONFLITO  

- **X = comportamento de `gerar_extrato` (conteúdo de `linhas`)**  
  - Em **RIGHT**, `linhas` contém uma entrada para **cada** pedido.  
  - No **MERGE**, `linhas` está vazia porque o generator foi consumido na primeira iteração.  

Isso corresponde ao caso **(b)**: `X` difere de **RIGHT** (valor esperado) e o **MERGE** não preserva o valor introduzido por RIGHT.  

Portanto, há **conflito semântico**.

---

### Prompt: `prompt_one_shot_cleantext`

**SIM**

---

### 1. INTENÇÃO  
- **LEFT:** Alterar `listar_pedidos` para retornar um **gerador**, evitando carregar todos os pedidos na memória.  
- **RIGHT:** Introduzir a nova funcionalidade **`gerar_extrato`**, que devolve o total e linhas formatadas a partir da lista de pedidos.

### 2. ESTADO  
| Elemento / Operação                     | Onde é usado                              |
|----------------------------------------|-------------------------------------------|
| `listar_pedidos(cliente_id)` – retorno | - `reenviar_notas` (iteração única) <br> - `gerar_extrato` (duas iterações: `sum` e compreensão de lista) |
| Tipo do retorno de `listar_pedidos`   | `list` (BASE & RIGHT) → permite múltiplas iterações <br> `generator` (LEFT & MERGE) → só uma iteração |
| Consumo de `pedido` em `reenviar_notas`| Chama `enviar_nota_fiscal(pedido)` para cada elemento. |
| Consumo de `pedido` em `gerar_extrato`| 1️⃣ `sum(p.valor for p in pedidos)` <br> 2️⃣ `[f"{p.id}: R$ {p.valor:.2f}" for p in pedidos]` |

### 3. TABELA DE VALORES/COMPORTAMENTO  

| Elemento X                              | BASE                              | LEFT                               | RIGHT (com `gerar_extrato`)                                 | MERGE (gerador + `gerar_extrato`)                               |
|----------------------------------------|-----------------------------------|------------------------------------|------------------------------------------------------------|-----------------------------------------------------------------|
| `listar_pedidos` → tipo de retorno      | `list`                            | `generator`                        | `list` (não mudou)                                         | `generator` (mantido da LEFT)                                   |
| `reenviar_notas` (iterações)            | Funciona (lista)                  | Funciona (gerador – iterável uma vez) | Funciona (lista)                                            | Funciona (gerador – ok, só uma iteração)                        |
| `gerar_extrato` – `total`                | **não existe**                    | **não existe**                     | `total = sum(p.valor for p in lista)` → soma correta        | `total = sum(p.valor for p in gerador)` → soma correta          |
| `gerar_extrato` – `linhas`               | **não existe**                    | **não existe**                     | `linhas` = lista de strings para **todos** os pedidos      | `linhas` = **lista vazia** (gerador já consumido por `sum`)    |

### 4. CRITÉRIO DE CONFLITO  

- **X = comportamento de `gerar_extrato`** (valor de `linhas`).  
- Em **RIGHT**, `linhas` contém uma entrada para **cada** pedido.  
- Em **MERGE**, por causa do gerador, `linhas` fica **vazia** (o gerador é consumido na primeira iteração).  

Condição (a):  
- `linhas` tem o mesmo valor em **BASE** (não existe) → não se aplica.  
Condição (b):  
- **RIGHT** introduz `gerar_extrato` cujo comportamento difere de **BASE**.  
- O **MERGE** **não preserva** esse comportamento (as linhas desaparecem).  

Portanto, há um conflito semântico.

---

---

### Prompt: `prompt_teste_mental`

SIM  

**PASSO 1 – ENTENDER O CÓDIGO**  

- **BASE**  
  - `listar_pedidos(cliente_id)` devolve **uma lista** com todos os pedidos do cliente (carrega tudo em memória).  
  - `reenviar_notas(cliente_id)` itera sobre essa lista e chama `enviar_nota_fiscal` para cada pedido.  
  - Não há `gerar_extrato`.  

- **LEFT** (alteração)  
  - Mudou `listar_pedidos` para **gerador** (`(p for …)`), mantendo a mesma lógica de filtragem, porém evitando o carregamento completo em memória.  
  - A intenção provável: melhorar performance/memória, sem mudar o resultado lógico da iteração.  

- **RIGHT** (alteração)  
  - Mantém `listar_pedidos` como lista (como em BASE).  
  - Acrescenta a nova função `gerar_extrato`, que **chama `listar_pedidos` duas vezes**:  
    1. `total = sum(p.valor for p in pedidos)` – consome o iterável.  
    2. `linhas = [...] for p in pedidos` – espera poder iterar novamente.  
  - A intenção provável: fornecer um extrato completo (total + linhas) usando a lista retornada por `listar_pedidos`.  

- **MERGE**  
  - O merge manteve a mudança de LEFT (gerador) e a nova função de RIGHT.  
  - Ordem de execução:  
    1. `listar_pedidos` agora devolve um gerador.  
    2. `gerar_extrato` usa esse gerador duas vezes sequencialmente.  

**PASSO 2 – IDENTIFICAR AS VARIÁVEIS DE ESTADO**  

| Variável / Campo | Onde aparece | Influência das mudanças (LEFT & RIGHT) |
|------------------|--------------|----------------------------------------|
| `pedidos` (resultado de `listar_pedidos`) | `reenviar_notas`, `gerar_extrato` | LEFT → gera *generator*; RIGHT → espera *lista* reutilizável. |
| `p.valor` | cálculo de `total` | Dependente da forma de iteração. |
| `p.id` | montagem de `linhas` | idem. |
| `total` | retorno de `gerar_extrato` | Deve refletir soma de todos os valores. |
| `linhas` | retorno de `gerar_extrato` | Deve conter uma linha por pedido. |
| `enviar_nota_fiscal(pedido)` | `reenviar_notas` | Não afeta o conflito (não depende da forma da coleção). |

A variável crítica que sofre efeito das duas mudanças é **`pedidos`** (o iterável retornado por `listar_pedidos`), pois sua natureza (lista vs gerador) altera o comportamento de `gerar_extrato`.

**PASSO 3 – SIMULAR UM CASO QUE SATISFAÇA OS CRITÉRIOS**  

Supomos que `db.pedidos()` retorne dois objetos:

```python
Pedido(id=1, valor=10.0, cliente_id=42)
Pedido(id=2, valor=20.0, cliente_id=42)
```

| Versão | `pedidos` (tipo) | `total` (após sum) | `linhas` (após list comprehension) |
|--------|------------------|--------------------|--------------------------------------|
| **BASE** (não tem `gerar_extrato`) | — | — | — |
| **LEFT** (gerador, sem `gerar_extrato`) | generator | — | — |
| **RIGHT** (lista) | list | `30.0` | `["1: R$ 10.00", "2: R$ 20.00"]` |
| **MERGE** (gerador + `gerar_extrato`) | generator | `30.0` (consome o generator) | `[]` (generator já está exausto) |

- **Critério (a)** não se aplica porque não há variável que tenha o mesmo valor em BASE, LEFT e RIGHT e mude em MERGE.  
- **Critério (b)** se aplica a `linhas`:  
  - Em **RIGHT**, `linhas` contém duas strings (comportamento desejado).  
  - Em **MERGE**, `linhas` fica vazia, **não preservando** o valor que RIGHT introduziu.  

Portanto, a mudança de LEFT que transformou `listar_pedidos` em gerador fez com que a nova lógica de RIGHT deixasse de funcionar corretamente.

**PASSO 4 – CONCLUIR**  

Existe conflito semântico.  
- O desenvolvedor que escreveu **RIGHT** pretendia que `gerar_extrato` retornasse **todas** as linhas do extrato.  
- O merge, ao incorporar a alteração de LEFT (gerador), violou essa intenção, produzindo `linhas = []`.  

**Conclusão:** há conflito; a intenção do desenvolvedor de RIGHT foi quebrada.

---
