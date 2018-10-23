import pymongo
from flask import Flask, jsonify, request

# Flask  nos permite manejar un servidor web
# Jsonify  Utilizar las librerias de json
# request  peticiones a travez del cliente por modo query

def get_db_connection(uri):
    client = pymongo.MongoClient(uri)
    return client.cryptongo

app = Flask(__name__)
db_connection = get_db_connection('mongodb://localhost:27017/')

def get_documents(): #Obtener todo los documentos de nuestra base de datos.
    params = {}
    name = request.args.get('name', '') # Variable de la base de datos nombre
    limit = int(request.args.get('limit', 0)) #Variable limit mongo
    if name :
        params.update({ 'name': name})
    cursor = db_connection.ticker.find(
        params, {'_id': 0, 'ticker_hash':0}
    ).limit(limit) # variable que traemos de mongo
    return list(cursor) #Lista nombre funcion de python
 
def get_top20(): #Permite traer el top20 de las monedas
    params = {}
    name = request.args.get('name', '') # Variable de la base de datos nombre
    limit = int(request.args.get('limit', 0)) #Variable limit mongo
    if name :
        params.update({ 'name': name})
    params.update({ 'rank': {'$lte': 20}}) # Los primeros 20
    cursor = db_connection.ticker.find(
        params, {'_id': 0, 'ticker_hash': 0}
    ).limit(limit) # variable que traemos de mongo
    return list(cursor) #Lista nombre funcion de python

def remove_currency(): # Remover un tiques de una moneda
    params = {}
    name = request.args.get('name', '')
    if name:
        params.update({'name': name})
    else:
        return False
    return db_connection.tickers.delete_many(
        params
    ).deleted_count
    
# Ruta inicial
@app.route("/")
def index():
     return jsonify(
         {
             'name' : 'Cryptongo API'
         }
     )
@app.route("/top20", methods=['GET']) #EXPLICAR el metodo que vamos a utilizar
def top20():
    return jsonify(
        get_top20()
    )