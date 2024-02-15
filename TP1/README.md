# TP1  - Conversão de JSON para TTL
__Data:__ 10/2/2024

__Autor:__ Francisca Barros

__UC:__ RPCW

---

O objetivo deste trabalho era transformar o ficheiro plantas.json, fornecido pelo professor, numa ontologia (no formato ttl).

Para tal a primeira fase foi analisar o dataset e perceber a estrutura do mesmo de modo a perceber a melhor forma de construir a ontologia.

Após esta análise, concluí que deveriam ser criadas duas classes: rua e planta.
A classe rua tem associados os seguintes *data attributes* : Código de rua, Rua, Local, Freguesia.
A classe planta tem associados os seguintes *data attributes* : Id,Número de Registo,Espécie,Nome Científico,Origem,Data de Plantação,Estado,Caldeira,Tutor
Implantação,Gestor,Data de actualização,Número de intervenções.

Além disso, existe um *object atribute*: temRua que relaciona a planta com a rua.

Foi então criada esta estrutura no Protégé e foi feita uma script para adicionar todos os individuos que estão presentes no dataset.

Após correr a scipt percebi que o dataset tinha algum lixo:
* havia uma rua com uma aspa, sem sentido, optei por remover a aspa
* havia entradas em que os campos não estavam devidamente preennchidos, tinha datas em sitios que deveriam ser número por exemplo. Optei por remover estas entradas.
* havia ruas que o código não estava preenchido mas era possível deduzi-lo por outras entradas com a mesma rua (e mesmo local)
* havia no entanto uma rua que não existia informação do código, ignorei essa

---

Lista de resultados: jsonToTTL.py, plantas.ttl.

