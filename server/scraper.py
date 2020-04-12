# -- IMPORTACION DE MODULOS -- #
from random import choice
import json
import requests
from bs4 import BeautifulSoup

# ------------------------------------------------------

# -- VARIABLES GLOBALES -- #
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']

# ------------------------------------------------------

# -- CLASE -- #
# Descripcion: Modulo encargado de la obtencion de informacion de Instagram.
class InstagramScraper:

    # -- CONSTRUCTOR -- #
    # Descripcion: Inicializa las variables a ser utilizadas en la instancia creada.
    def __init__(self, url, user_agents=None, proxy=None):
        self.url = url
        self.user_agents = user_agents
        self.proxy = proxy

    # ------------------------------------------------------

    def __random_agent(self):
        if self.user_agents and isinstance(self.user_agents, list):
            return choice(self.user_agents)
        return choice(USER_AGENTS)

    # ------------------------------------------------------

    # -- FUNCION -- #
    # Descripcion: Genera el mensaje HTTP (GET) a la url especificada y retorna la respuesta del mismo.
    # Input: Instacia actual del objeto InstagramScraper y url destino.
    # Output: respuesta del mensaje HTTP (GET)
    def __request_url(self, url):
        try:
            response = requests.get(
                url,
                headers={'User-Agent': self.__random_agent()},
                proxies={'http': self.proxy, 'https': self.proxy})
            response.raise_for_status()
        except requests.HTTPError:
            raise requests.HTTPError(
                'Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response.text

    # ------------------------------------------------------

    # -- FUNCION -- #
    # Descripcion: A partir de la respuesta en formato HTML, extrae la informacion en el cuerpo del mensaje.
    # Input: pagina HTML.
    # Output: JSON con la informacion.
    @staticmethod
    def extract_json(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace(
            'window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    # ------------------------------------------------------

    # -- FUNCION --#
    # Descripcion: A partir de la url instanciada en el constructor, genera el mensage GET, extrae la informacion (metricas) de la respuesta y retorna los posts obtenidos en una lista.
    # Input: Instancia actual del objeto InstagramScraper
    # Output: Lista de posts de Instagram.
    def post_metrics(self):
        results = []
        try:
            response = self.__request_url(self.url)
            json_data = self.extract_json(response)
            metrics = json_data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node)
        return results

