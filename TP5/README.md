# TP5  - Criar base de dados de filmes
__Data:__ 07/3/2024

__Autor:__ Francisca Barros

__UC:__ RPCW

---

O objetivo deste trabalho era criar uma base de dados com informação sobre filmes disponíveis na Linnked Open Data.

Inicialmente foi seguida uma estratégia que consistia em fazer múltiplas queries: uma querie inicial para ir buscar os filmes, e para cada filme, queries para cada elemento que pode ter múltiplos valores. No entanto, este método obrigava a muitas chamadas ao end-point do SPARQL.

Assim, foi seguida uma segunda estratégia que consistia em pedir tudo numa query e depois os dados duplicados eram tratados posteriormente, localmente.

---

Lista de resultados: getFilmes2.py, filmes2.json.
