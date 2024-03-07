from flask import Flask, render_template, url_for
from datetime import datetime
import requests
 
app = Flask(__name__)

# data do sistema no formato ISO
data_hora_atual = datetime.now()
data_iso_formatada = data_hora_atual.strftime("%Y-%m-%dT%H:%M:%S")


#GraphDB endpoint
graphdb_endpoint = "http://localhost:7200/repositories/tabPeriodica"

@app.route("/")
def index():
    return render_template('index.html',data = {"data":data_iso_formatada})

@app.route("/elementos")
def elementos():
    sparql_query = """
prefix tp:  <http://www.daml.org/2003/01/periodictable/PeriodicTable#>

select * where {
    ?s a tp:Element ;
    tp:name ?nome;
    tp:symbol ?simb;
    tp:atomicNumber ?n;
    tp:group ?group. 
}
ORDER BY ?n
    """
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        return render_template("elementos.html", data = dados)
    else:
        return render_template("empty.html",data = {"data":data_iso_formatada})
    

@app.route("/grupos")
def grupos():
    sparql_query = """
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
SELECT ?s ?n ?nome WHERE {
    ?s a :Group.
    optional { ?s :number ?n.}
    optional {?s :name ?nome.}
    
}
    """
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        return render_template("grupos.html", data = dados)
    else:
        return render_template("empty.html",data = {"data":data_iso_formatada})



@app.route("/elemento/<string:name>")
def elemento(name):
    sparql_query = f"""
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
SELECT * WHERE {{
    ?elem :name "{name}" ;
          :atomicNumber ?na;
          :atomicWeight ?aw;
          :block ?block;
          :casRegistryID ?rid;
          :classification ?class;
          :color ?color;
          :group ?group;
          :name ?name;
          :period ?per;
          :standardState ?state;
          :symbol ?symbol.
    ?per :number ?period.
    
}}
    """
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        print(dados[0])
        return render_template("elemento.html", data = dados[0])
    else:
        return render_template("empty.html",data = {"data":data_iso_formatada})

@app.route("/grupo/<string:idGrupo>")
def grupo(idGrupo):
    sparql_query = f"""
PREFIX : <http://www.daml.org/2003/01/periodictable/PeriodicTable#>
SELECT ?n ?nome ?nomeElem ?simbElem ?nElem WHERE {{
    :{idGrupo} a :Group.
    optional {{ :{idGrupo} :number ?n.}}
    optional {{:{idGrupo} :name ?nome.}}
    :{idGrupo} :element ?elemento.
    ?elemento :name ?nomeElem.
    ?elemento :symbol ?simbElem.
    ?elemento :atomicNumber ?nElem.
    
}}
    """
    resposta = requests.get(graphdb_endpoint,params = {"query":sparql_query},headers = {"Accept":"application/sparql-results+json"})
    if resposta.status_code == 200:
        dados = resposta.json()["results"]["bindings"]
        return render_template("grupo.html", data = {"dados":dados,"id":idGrupo})
    else:
        return render_template("empty.html",data = {"data":data_iso_formatada})

if __name__=="__main__":
    app.run(debug=True)