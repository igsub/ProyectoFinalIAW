# -- IMPORTACION DE MODULOS -- #
import googlemaps
import credentials

# ------------------------------------------------------

# -- INSTACIACION DE LA KEY PARA LOS SERVICIOS DE GOOGLEMAPS -- #
gmaps = googlemaps.Client(key=credentials.GOOGLEMAPS_KEY)

# ------------------------------------------------------

# -- FUNCION -- #
# Descripcion: a partir de una lista de locaciones obtiene la geolocalizacion de cada una de estas a traves del servicio de googlemaps.
# Input: Lista de locaciones.
# Output: Lista de coordenadas.
def getLocationsInfo(locations):
    coordinates = []
    for location in locations:
        print(location)
        try:
            geocode_result = gmaps.geocode(location)
            coordinates.append(geocode_result[0]['geometry']['location'])
        except:
            continue
    return coordinates
