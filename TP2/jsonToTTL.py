import json

f = open("musica.json")
bd = json.load(f)
f.close()


ttl = ""
for instrumento in bd["instrumentos"]:
    instrumento["#text"] = instrumento["#text"].replace(" ", "_")
    ttl+=f"""

###  http://rpcw.di.uminho.pt/2024/musica#{instrumento["#text"]}
:{instrumento["#text"]} rdf:type owl:NamedIndividual ,
                    :instrumento ;
           :nomeInstrumento "{instrumento["#text"]}" .
    """
    
for curso in bd["cursos"]:
    curso["instrumento"]["#text"] = curso["instrumento"]["#text"].replace(" ", "_")
    curso["designacao"] = curso["designacao"].replace(" ", "_")
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/musica#{curso["id"]}
:{curso["id"]} rdf:type owl:NamedIndividual ,
              :curso ;
     :ensina :{curso["instrumento"]["#text"]} ;
     :designacao "{curso["designacao"]}" ;
     :duracao {curso["duracao"]} ;
     :id "{curso["id"]}" .


"""
  
    
for aluno in bd["alunos"]:
    aluno["nome"]=aluno["nome"].replace(" ", "_")
    aluno["instrumento"] = aluno["instrumento"].replace(" ", "_")
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/musica#{aluno["id"]}
:{aluno["id"]} rdf:type owl:NamedIndividual ,
                 :aluno ;
        :inscrito :{aluno["curso"]} ;
        :toca :{aluno["instrumento"]} ;
        :anoCurso {aluno["anoCurso"]} ;
        :dataNasc "{aluno["dataNasc"]}" ;
        :id "{aluno["id"]}" ;
        :nome "{aluno["nome"]}" ."""


print(ttl)