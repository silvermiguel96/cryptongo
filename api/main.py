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
    cursor = db_connection.tickers.find(
        params, {'_id': 0, 'ticker_hash':0}
    ).limit(limit) # variable que traemos de mongo
    return list(cursor) #Lista nombre funcion de python
 
def get_top20(): #Permite traer el top20 de las monedas
    pass

def remove_currency(): # Remover un tiques de una moneda
    pass