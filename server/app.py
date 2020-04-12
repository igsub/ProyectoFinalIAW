# -- IMPORTACION DE MODULOS -- #
# FLASK 
# Microframework escrito en python que permite crear aplicaciones web facilmente.
from flask import Flask, jsonify, request
import json
from flask_cors import CORS

# INSTAGRAM
# Modulos utilizados para la obtecion de informacion
from scraper import InstagramScraper
from mapping import getLocationsInfo
from filterLocations import getLocations
from pprint import pprint

# TWITTER
from twitter_crawler import getTwitterLocations
# ------------------------------------------------------

# -- VARIABLES GLOBALES -- #
DEBUG = True
MARKERS = []
SUCCESS = False

# ------------------------------------------------------

# -- INSTACIACION DE LA APLICACION -- #
app = Flask(__name__)
app.config.from_object(__name__)
# Habilitar CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# ------------------------------------------------------

# -- RUTAS PARA EL MANEJO DE LOS MENSAJES HTTP -- #
@app.route('/map_locations', methods=['GET','POST'])
def map_locations():
    response_object = {'status': 'success'}
    global SUCCESS
    coordinates = []
    if request.method == 'POST':
        # Metodo POST
        print('POST')
        post_data = request.get_json()
        MARKERS.clear()
        if post_data.get('inputType') == '0':
            # Es un Usuario de Instagram
            print('INSTAGRAM')
            instagramUser = post_data.get('input')
            url = 'https://www.instagram.com/' + instagramUser
            try:
                # Obtengo el HTML de la pagina de instagram del usuario especificado                 
                instagram = InstagramScraper(url)
                # Obtengo los posteos con su respectiva informacion a partir del HTML anterior
                metrics = instagram.post_metrics()
                # Obtengo la locacion de cada posteo
                ArregloLugares = getLocations(metrics)
                # Obtengo las coordenadas de cada locacion
                coordinates = getLocationsInfo(ArregloLugares)
                # Seteo el estado de la operacion
                SUCCESS = True
                print('Instagram success')
            except:
                # Falla en el request a Instagram
                # Seteo el estado de la operacion
                SUCCESS = False
                print('Instagram error')
        else:
            # Es un Hashtag de Twitter
            print('TWITTER')
            hashtag = '#' + post_data.get('input')

            try:
                # Obtengo las locaciones de las menciones al hastag especificado
                print(hashtag)
                locations = getTwitterLocations(hashtag)
                # Obtengo las coordenadas de las locaciones
                coordinates = getLocationsInfo(locations)
                # Seteo el estado de la operacion
                SUCCESS = True
                print('Twitter success')                
            except:
                # Falla la API de Twitter
                # Seteo el estado de la operacion
                SUCCESS = False
                print(hashtag)
                print('Twitter error')
        # Agrego las coordenadas a un arreglo de marcadores
        for coordinate in coordinates:
            MARKERS.append({
                'lat': coordinate['lat'],
                'lng': coordinate['lng']
            })
    else:
        # Metodo GET
        print('GET')        
        if (SUCCESS and MARKERS):
            # Request exitosa y hay marcadores en la lista
            response_object['message'] = 'La solicitud se realizó correctamente.'
        else:
            response_object['message'] = 'La solicitud falló.'
            print('Failed')
    # Agrego los marcadores a la respuesta
    response_object['markers'] = MARKERS
    return jsonify(response_object)

# ------------------------------------------------------

# -- MAIN -- #
if __name__ == '__main__':
    app.run()

