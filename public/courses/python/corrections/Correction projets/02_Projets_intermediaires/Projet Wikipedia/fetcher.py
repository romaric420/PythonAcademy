import requests

def fetch_page(url, logger):
    logger.debug(f"Téléchargement : {url}")
    response = requests.get(url)

    logger.debug(f"Statut HTTP reçu : {response.status_code}")
    logger.debug(f"Taille du contenu : {len(response.text)} caractères")

    return response.text
