# -- IMPORTACION DE MODULOS -- #
from datetime import datetime

# ------------------------------------------------------

# -- FUNCION -- #
# Descripcion: recibe la informacion (metricas) de los post de Instagram y retorna una lista con las locaciones de los ultimos posts.
# Input: lista de posts.
# Output: lista de locaciones.
def getLocations(metrics):
    ListaLugares = []
    for m in metrics:
        i_location = m['location']
        if i_location is not None:
            ListaLugares.append(i_location['name'])
    return ListaLugares
