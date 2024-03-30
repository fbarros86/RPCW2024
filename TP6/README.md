# TP6  - App de Cinema
__Data:__ 28/2/2024

__Autor:__ Francisca Barros

__UC:__ RPCW

---

Este trabalho pode ser dividido em três partes: transformar o json (do TPC anterior) numa ontologia em `.ttl` e carregar para o endpoint disponibilizado pelo professor; fazer queries para responder a algumas perguntas sobre a ontologia; fazer uma aplicação web que mostra a informação obtida de uma forma organizada.


---

### JSON to Turtle

Para a primeira fase, criei uma script em python que usa a biblioteca `rdflib` para através da ontologia criada na aula, acrescentar os triplos correspondentes aos individuos que queremos acrescentar e as suas respetivas *data properties* e *object properties*.

Foi necessário ter em atenção algumas propriedades de ficheiros deste tipo, por exemplo, remover espaços e certos carateres, como `[` e `]` (optei por usar *snake case*).

---

### SPARQL queries


1. Quantos filmes existem no repositório?

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select (COUNT(?s) as ?nfilmes) where {
    ?s a :Film .
}
```


2. Qual a distribuição de filmes por ano de lançamento?



```sql
...
```

3. Qual a distribuição de filmes por género?



```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?genre (COUNT(?s) as ?nfilmes) where {
    ?s a :Film .
    ?s :hasGenre ?genre.
} 
GROUP BY (?genre)
ORDER BY DESC (?nfilmes)
```

4. Em que filmes participou o ator "Burt Reynolds"?


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?s where {
    ?s a :Film .
    ?s :hasActor :Burt_Reynolds.
} 
```

5. Produz uma lista de realizadores com o seu nome e o número de filmes que realizou.


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/cinema/>
select ?director (COUNT(?s) as ?nfilmes) where {
    ?s a :Film .
    ?s :hasDirector ?director.
} 
GROUP BY (?director)
ORDER BY DESC (?nfilmes)
```

6. Qual o título dos livros que aparecem associados aos filmes?


```sql
...
```

---

### Aplicação Web

Quanto à aplicação web, optei por ter 7 páginas diferentes:
-   `/` - mostra 3 opções que podem ser seguidas: filmes, realizadores e atores.
-   `/filmes` - mostra uma tabela com todos os filmes (o seu titulo e a sua duração). O título tem uma referência para a página do respetivo filme.
-  `/filmes/:titulo` - mostra a página do filme com a respetiva informação: título, descrição, duração, géneros, países, realizadores, atores,compositores, produtores e argumentistas
-  `/realizadores` - mostra uma tabela com todos os realizadores (o seu nome e o número de filmes que realizaram ordenados por ordem descrescente de filmes realizados). 
-  `/realizadores/:nome` - mostra a lista dos filmes que realizaram
-  `/atores` - mostra uma tabela com todos os atores (o seu nome e o número de filmes em que atuaram ordenados por ordem descrescente).
-  `/atores/:nome` - mostra a lista dos filmes em que atuaram


**Nota:** No futuro seria boa ideia utlizar paginação para mostrar os filmes, usando o conceito de limit e de offset






---

Lista de resultados: AppCinema, jsonToTTL.py, out.ttl

