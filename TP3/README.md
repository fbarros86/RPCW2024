# TP2  - Conversão de JSON para TTL - Escola de música
__Data:__ 25/2/2024

__Autor:__ Francisca Barros

__UC:__ RPCW

---

O objetivo deste trabalho era transformar o ficheiro mapa-virtual.json, fornecido pelo professor, numa ontologia (no formato ttl) e posteriormente carregá-lo para o GraphDB e fazer algumas queries.

Após uma análise do dataset,  destacam-se 2 tipos de entidades: cidades e ligações. Optei por criar uma classe para cada uma delas.


A classe cidade vai ter então as seguintes *data properties*:
- id
- nome
- população
- descrição
- distrito
  
  


A classe ligação tem as seguintes *data properties*: 
- id
- distancia


E tem duas *object properties*: origem e destino (ligação &rarr; cidade)



Depois de ter a ontologia criada, criei uma script para a povoar.

Finalmente, o resultado foi importado para o GraphDB, e foram criadas queries para responder às perguntas apresentadas.







1. Quais as cidades de um determinado distrito?

```sql

PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select ?nome where { 
	?s :distrito "Porto" .
    ?s :nome ?nome
}


```


2. Distribuição de cidades por distrito?


```sql

PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select ?distrito (COUNT(distinct ?cidade) as ?ncidades) where { 
    ?cidade :distrito ?distrito .
}
group by ?distrito

```

3. Quantas cidades se podem atingir a partir do Porto? (Diretamente)
```sql
    PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>

    SELECT distinct ?cidade WHERE {
        ?porto :distrito "Porto" .
        ?ligacao :origem ?porto .
        ?ligacao :destino ?c .
        ?c :nome ?cidade
    }
```


4. Quais as cidades com população acima de um determinado valor?


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>

SELECT ?nome ?populacao WHERE {
    ?cidade a :cidade .
    ?cidade :nome ?nome .
    ?cidade :populacao ?populacao .
    FILTER (100000 < ?populacao).
}
```


---

Lista de resultados: jsonToTTL.py, mapa-virtual.ttl.

