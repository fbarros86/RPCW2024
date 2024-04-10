# Queries em SPARQL





1. Lista de cidades, ordenada alfabeticamente pelo nome;

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select ?nome where { 
	?s a :cidade .
    ?s :nome ?nome
}
ORDER BY ?nome
```


2. Distribuição das cidades por distrito: lista de distritos ordenada alfabeticamente em que para cada um se indica quantas cidades tem;

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select ?distrito (COUNT(?s) AS ?ncidades) where { 
	?s a :cidade .
    ?s :distrito ?distrito
}
GROUP BY ?distrito
ORDER BY ?distrito
```


3. Que cidades têm ligações diretas com Braga? (Considera Braga como origem mas também como destino)

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select distinct (COUNT(?cidade) as ?ncidades) where { 
	?braga a :cidade .
    ?braga :nome "Braga".
    ?ligacao a :ligacao.
    
{?ligacao :origem ?braga.
    ?ligacao :destino ?cidade.}
UNION
{?ligacao :destino ?braga.
    ?ligacao :origem ?cidade.}

}

```


4. Partindo de Braga, que cidades se conseguem visitar? (Apresenta uma lista de cidades ordenada alfabeticamente)

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/mapa-virtual/>
select (COUNT(?cena) AS ?ncidades) where { 
	?braga a :cidade .
    ?braga :nome "Braga".
    ?l :origem ?braga.
    ?l :destino ?cena.
}
```








