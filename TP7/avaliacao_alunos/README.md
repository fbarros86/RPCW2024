# Queries

1. Quantos alunos estão registados?
   
   299

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT (COUNT(?aluno) as ?nalunos) WHERE {
    ?aluno a :Aluno
}
```

2. Quantos alunos frequentam o curso "LCC"?

    44

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT (COUNT(?aluno) as ?nalunos) WHERE {
    ?aluno a :Aluno.
    ?aluno :curso "LCC"
}
```

3. Que alunos tiveram nota positiva no exame de época normal? (lista ordenada alfabeticamente por nome com: idAluno, nome, curso, nota do exame);

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?idAluno ?nome ?curso ?nota_exame WHERE {
    ?aluno a :Aluno;
     :curso ?curso;
     :nome ?nome;
     :idAluno ?idAluno;
     :temExame ?exame.
   ?exame a :Exame_Normal;
          :nota ?nota_exame.
    FILTER(?nota_exame>9).

}
ORDER BY ?nome
```

4. Qual a distribuição dos alunos pelas notas do projeto? (lista com: nota e número de alunos que obtiveram essa nota)

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?nota (COUNT(?aluno) as ?nalunos) WHERE {
    ?aluno a :Aluno;
     :notaProjeto ?nota;

}
GROUP BY ?nota
```

5. Quais os alunos mais trabalhadores durante o semestre? (lista ordenada por ordem decrescente do total: idAluno, nome, curso, total = somatório dos resultados dos TPC)


```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?idAluno ?nome ?curso (SUM(?nota) AS ?total) WHERE {
      ?aluno a :Aluno;
     :curso ?curso;
     :nome ?nome;
     :idAluno ?idAluno;
     :temTPC ?tpc.
   ?tpc :nota ?nota.

}
GROUP BY ?aluno ?curso ?nome ?idAluno
ORDER BY DESC (?total)
```

6. Qual a distribuição dos alunos pelos vários cursos? (lista de cursos, ordenada alfabeticamente
por curso, com: curso, número de alunos nesse curso)

```sql
PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?curso (COUNT(?aluno) AS ?nalunos) WHERE {
      ?aluno a :Aluno;
     :curso ?curso;
 
}
GROUP BY ?curso
ORDER BY ?curso
```