import json

f = open("aval-alunos.json")
bd = json.load(f)
f.close()


ttl = ""
for aluno in bd["alunos"]:
    ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/avaliacao_alunos#{aluno["idAluno"]}
:{aluno["idAluno"]} rdf:type owl:NamedIndividual ,
                  :Aluno ;"""
    if "normal" in aluno["exames"]:
        ttl+=f"""
        :temExame :{aluno["idAluno"]}_exame_normal ;""" 
    if "recurso" in aluno["exames"]:
        ttl+=f"""
        :temExame :{aluno["idAluno"]}_exame_recurso ;""" 
    if "expecial" in aluno["exames"]:
        ttl+=f"""
        :temExame :{aluno["idAluno"]}_exame_ee ;"""  
    for tpc in aluno["tpc"]:
        ttl+=f"""
        :temTPC :{aluno["idAluno"]}_{tpc["tp"]} ;"""
    ttl+=f""" 
        :curso"{aluno["curso"]}"  ;
         :idAluno "{aluno["idAluno"]}" ;
         :nome "{aluno["nome"]}"  ;
         :notaProjeto {aluno["projeto"]} ."""
    if "normal" in aluno["exames"]:
        ttl+=f"""
        ###  http://rpcw.di.uminho.pt/2024/avaliacao_alunos#{aluno["idAluno"]}_exame_normal
                    :{aluno["idAluno"]}_exame_normal rdf:type owl:NamedIndividual ,
                               :Exame_Normal ;
                      :nota {aluno["exames"]["normal"]} .
        """
    if "recurso" in aluno["exames"]:
        ttl+=f"""
        ###  http://rpcw.di.uminho.pt/2024/avaliacao_alunos#{aluno["idAluno"]}_exame_recurso
                    :{aluno["idAluno"]}_exame_recurso rdf:type owl:NamedIndividual ,
                               :Exame_Recurso ;
                      :nota {aluno["exames"]["recurso"]} .
        """
        
    if "especial" in aluno["exames"]:
        ttl+=f"""
        ###  http://rpcw.di.uminho.pt/2024/avaliacao_alunos#{aluno["idAluno"]}_exame_ee
                    :{aluno["idAluno"]}_exame_ee rdf:type owl:NamedIndividual ,
                               :Exame_EE ;
                      :nota {aluno["exames"]["especial"]} .
        """
        
    for tpc in aluno["tpc"]:
        ttl+=f"""
        ###  http://rpcw.di.uminho.pt/2024/avaliacao_alunos#{aluno["idAluno"]}_{tpc["tp"]}
                    :{aluno["idAluno"]}_{tpc["tp"]} rdf:type owl:NamedIndividual ,
                               :TPC ;
                      :nota {tpc["nota"]} .
        """
    
  



print(ttl)