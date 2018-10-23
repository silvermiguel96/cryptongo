import requests #Librería para capturar peticiones rest
import pymongo #Librería para comunicarse con la bd mongodb

API_URL = 'https://api.coinmarketcap.com/v1/ticker/'

#Función para crear conexión a la bd
def get_db_connection(uri):
	client = pymongo.MongoClient(uri) #Crear una conexión a la bd
	return client.cryptongo #Devolver bd cryptongo

#Función para obtener datos del api externa
def get_cryptocurrencies_from_api():
    r = requests.get(API_URL)
    if r.status_code == 200:
        result = r.json()
        return result

    raise Exception('API Error')

def first_element(elemets): # tuplas para utilizar la memoria ram
    return elemets[0]

def get_hash(value):
    from hashlib import sha512
    return sha512(
        value.encode('utf-8')
    ).hexdigest()
    
def get_ticker_hash(ticker_data):
    from collections import OrderedDict
    #Trae elementos Ticker data
    ticker_data = OrderedDict(
        sorted( # Funcion para ordenar elementos
            ticker_data.items(),
            key= first_element # lo que resive la funcion sorted ciclo for para ordenarlo
        )
    )
    ticker_value = ''
    for _, value in ticker_data.items():
        ticker_value += str(value)
    
    return get_hash(ticker_value)

def check_if_exists(db_connection, ticker_data):
    ticker_hash = get_ticker_hash(ticker_data)
    
    if db_connection.ticker.find_one(
        {'ticker_hash': ticker_hash}):
        return True

    return False

def save_ticker(db_connection, ticker_data = None):
    if not ticker_data:
        return False

    if check_if_exists(db_connection, ticker_data):
        return False
    
    ticker_hash = get_ticker_hash(ticker_data)
    ticker_data['ticker_hash'] = ticker_hash
    ticker_data['rank'] = int(ticker_data['rank'])
    ticker_data['last_updated'] = int(ticker_data['last_updated'])

    db_connection.ticker.insert_one(ticker_data)
    return True

if __name__ == "__main__":
    connection = get_db_connection('mongodb://localhost:27017/')
    tickers = get_cryptocurrencies_from_api()

    for ticker in tickers:
        save_ticker(connection, ticker)

    print("Tickers almacenados")
    