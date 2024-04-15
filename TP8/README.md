# TP8  - XML to TTL
__Data:__ 15/4/2024

__Autor:__ Francisca Barros

__UC:__ RPCW

---

Este trabalho consistia em pegar num de dois ficheiros XML, um sobre a bíblia e outro sobre a família real, sendo que ambos continham informação sobre pessoas e os respetivos pais e filhos. O objetivo era transformar esta informação numa ontologia simples com apenas uma classe - `Pessoa` - e duas *object properties* - `temPai` e `temMae`.

Escolhi o ficheiro da biblia, o primeiro passo foi selecionar todos os elementos do tipo `Person`, e para cada um, utilizando a biblioteca `rdflib`, foi criado um *Individual* com a respetiva *data property* - `nome`. Além disso, a informação desta pessoa é guardada - id, nome, pais, sexo - para mais tarde associar as pessoas de acordo com o seu sexo.






---

Lista de resultados: xmlToTTL.py, familia.ttl

