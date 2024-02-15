import json

f = open("plantas.json")
bd = json.load(f)
f.close()

ruasExistentes = set()
ttl = ""
for planta in bd:
    if planta["Código de rua"]!="" or planta["Rua"]!="":

        ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/plantas#planta_{planta["Id"]}
:planta_{planta["Id"]} rdf:type owl:NamedIndividual ;
                 :temRua :rua_{planta["Código de rua"]} ;
                 :caldeira "{planta["Caldeira"]}" ;
                 :data_de_atualizacao "{planta["Data de actualização"]}" ;
                 :data_de_plantacao "{planta["Data de Plantação"]}" ;
                 :especie "{planta["Espécie"]}" ;
                 :estado "{planta["Estado"]}" ;
                 :gestor "{planta["Gestor"]}" ;
                 :id {planta["Id"]} ;
                 :implantação "{planta["Implantação"]}" ;
                 :nome_cientifico "{planta["Nome Científico"]}" ;
                 :nr_intervencoes {planta["Número de intervenções"] if planta["Número de intervenções"]!="" else 0 } ;
                 :nr_registo {planta["Número de Registo"]} ;
                 :origem "{planta["Origem"]}" ;
                 :tutor "{planta["Tutor"]}" .
                 """
        if planta["Código de rua"] not in ruasExistentes:
            ruasExistentes.add(planta["Código de rua"])
            ttl+=f"""
###  http://rpcw.di.uminho.pt/2024/plantas#rua_{planta["Código de rua"]}
:rua_{planta["Código de rua"]} rdf:type owl:NamedIndividual ;
             :codigoRua {planta["Código de rua"]} ;
             :freguesia "{planta["Freguesia"]}" ;
             :local "{planta["Local"]}" ;
             :rua "{planta["Rua"]}" .
    """
print(ttl)