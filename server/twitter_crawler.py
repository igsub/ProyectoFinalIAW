# Tener en cuenta que seran obtenidos unicamente los tweets con antiguedad de una semana o menos. Si los tweets pertenecen a fechas anteriores no seran recolectados.

# -- IMPORTACION DE MODULOS -- #
import tweepy
import credentials

# ------------------------------------------------------

# -- INSTACIACION DEL MODULO -- #
# Conexion con la API de Twitter
auth = tweepy.OAuthHandler(credentials.TWITTER_CONSUMER_KEY, credentials.TWITTER_CONSUMER_SECRET)
auth.set_access_token(credentials.TWITTER_ACCESS_TOKEN, credentials.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)

# ------------------------------------------------------

# -- FUNCION -- #
# Descripcion: a partir de un hastag, retorna las locaciones de los ultimos usuarios que twittearon mencionandolo.
# Input: hastag.
# Output: Lista de Locaciones.
def getTwitterLocations(hashtag):
    response = []
    for tweet in tweepy.Cursor(api.search,q=hashtag).items(20):
        location = tweet.author.location
        response.append(location)
    return response
