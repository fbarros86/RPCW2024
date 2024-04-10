from flask import Flask, render_template, url_for,request
from datetime import datetime
import requests
 
app = Flask(__name__)

# data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime("%Y-%m-%dT%H:%M:%S")



def trataAlunos(dados):
    alunos = {}
    for linha in dados:
        idAluno = linha["idAluno"]["value"]
        if idAluno not in alunos:
            alunos[idAluno] = {}
        if "nome" not in alunos[idAluno]:
            alunos[idAluno]["nome"] = linha["nome"]["value"]
        if "curso" not in alunos[idAluno]:
            alunos[idAluno]["curso"] = linha["curso"]["value"]
        if "notaProjeto" not in alunos[idAluno]:
            alunos[idAluno]["notaProjeto"] = float(linha["notaProjeto"]["value"])
        if "exames" not in alunos[idAluno]:
            alunos[idAluno]["exames"] = {}
        if "tpcs" not in alunos[idAluno]:
            alunos[idAluno]["tpcs"] = {}
        exame = linha["exame"]["value"].split("_")[-1]
        tpc = linha["tpc"]["value"].split("_")[-1]
        if exame not in alunos[idAluno]["exames"]:
            alunos[idAluno]["exames"][exame] = float(linha["notaExame"]["value"])
        if tpc not in alunos[idAluno]["tpcs"]:
            alunos[idAluno]["tpcs"][tpc] = float(linha["notaTPC"]["value"])
    for aluno in alunos:
        notaFinal = 0
        if alunos[aluno]["notaProjeto"] < 10:
            notaFinal = "R"
        else:
            notaExame = max(alunos[aluno]["exames"].values())
            if (notaExame) < 10:
                notaFinal = "R"
            else:
                for tpc in alunos[aluno]["tpcs"]:
                    notaFinal += alunos[aluno]["tpcs"][tpc]
                notaFinal += 0.4*alunos[aluno]["notaProjeto"]
                notaFinal += 0.4*notaExame
                if notaFinal < 10:
                    notaFinal = "R"
                else:
                    notaFinal = round(notaFinal,2)
        alunos[aluno]["notaFinal"] = notaFinal
        alunos[aluno].pop("exames")
        alunos[aluno].pop("tpcs")
        alunos[aluno].pop("notaProjeto")
    return alunos

def trataAluno(dados):
    aluno = {}
    exames = {}
    tpcs = {}
    aluno["nome"] = dados[0]["nome"]["value"]
    aluno["curso"] = dados[0]["curso"]["value"]
    aluno["idAluno"] = dados[0]["idAluno"]["value"]
    aluno["notaProjeto"] = dados[0]["notaProjeto"]["value"]
    for linha in dados:
        exame = linha["exame"]["value"].split("_")[-1]
        tpc = linha["tpc"]["value"].split("_")[-1]
        if exame not in exames:
            exames[exame] = linha["notaExame"]["value"]
        if tpc not in tpcs:
            tpcs[tpc] = linha["notaTPC"]["value"]
    aluno["exames"] = exames
    aluno["tpcs"] = tpcs
    
    return aluno

#GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/Alunos"

@app.route("/api/alunos")
def alunos(): 
    if "curso" in request.args:
        curso = request.args["curso"]
        sparql_query = f""" 
    PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?idAluno ?nome  WHERE {{
      ?aluno a :Aluno;
     :curso "{curso}";
     :nome ?nome;
     :idAluno ?idAluno;
}}
ORDER BY (?nome)
    """
    elif "groupBy" in request.args:
        if request.args["groupBy"] == "curso":
            sparql_query = """
                PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?curso (COUNT(?aluno) AS ?nalunos)  WHERE {{
      ?aluno a :Aluno;
     :curso ?curso.
}}
GROUP BY ?curso
ORDER BY (?curso)
            """
        elif request.args["groupBy"] == "projeto":
            sparql_query = """
                PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?projeto (COUNT(?aluno) AS ?nalunos)  WHERE {{
      ?aluno a :Aluno;
     :notaProjeto ?projeto.
}}
GROUP BY ?projeto
ORDER BY DESC (?projeto)
            """
        elif request.args["groupBy"] == "recurso":
            sparql_query = """
                PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT  ?idAluno ?nome ?curso ?notaExame  WHERE {{
      ?aluno a :Aluno;
     :curso ?curso;
     :nome ?nome;
     :idAluno ?idAluno;
     :temExame ?exame.
    ?exame :nota ?notaExame.
    ?exame a :Exame_Recurso.   
}}
            """
    else:
        sparql_query = """ 
    PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?idAluno ?nome ?curso  WHERE {
      ?aluno a :Aluno;
     :curso ?curso;
     :nome ?nome;
     :idAluno ?idAluno;
}
ORDER BY (?nome)
    """
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        for dado in dados:
            for key,value in dado.items():
                dado[key] = value["value"]
        return dados
    else:
        return "erro"


@app.route("/api/alunos/tpc")
def tpc():
    sparql_query = """ 
   PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?idAluno ?nome ?curso (COUNT(?tpc) AS ?ntpcs) WHERE {
      ?aluno a :Aluno;
     :curso ?curso;
     :nome ?nome;
     :idAluno ?idAluno;
     :temTPC ?tpc.

}
GROUP BY ?curso ?nome ?idAluno"""
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        for dado in dados:
            for key,value in dado.items():
                dado[key] = value["value"]
        return dados
    else:
        return "erro"

 
@app.route("/api/alunos/avaliados")
def avaliados():
    sparql_query = """ 
        PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?nome ?curso ?idAluno ?notaProjeto ?exame ?tpc ?notaExame ?notaTPC WHERE {{
      ?aluno a :Aluno;
     :curso ?curso;
     :nome ?nome;
     :idAluno ?idAluno;
     :notaProjeto ?notaProjeto;
     :temExame ?exame;
     :temTPC ?tpc.
    ?exame :nota ?notaExame.
    ?tpc :nota ?notaTPC.
}}"""
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        dados = trataAlunos(dados)
        return dados
#render_template("alunos.html", data = dados)
    else:
        return "erro"


@app.route("/api/alunos/<string:id>")
def aluno(id):
    sparql_query = f""" 
    PREFIX : <http://rpcw.di.uminho.pt/2024/avaliacao_alunos/>
SELECT ?nome ?curso ?idAluno ?notaProjeto ?exame ?tpc ?notaExame ?notaTPC WHERE {{
      ?aluno a :Aluno;
     :curso ?curso;
     :nome ?nome;
     :idAluno "{id}";
     :notaProjeto ?notaProjeto;
     :idAluno ?idAluno;
     :temExame ?exame;
     :temTPC ?tpc.
    ?exame :nota ?notaExame.
    ?tpc :nota ?notaTPC.
}}
    """
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        dados = trataAluno(dados)
        return dados
    else:
        return "erro"

if __name__=="__main__":
    app.run(debug=True)