import re
from urllib.parse import urljoin


# -------------------------
# Extraction des années
# -------------------------

def extract_years(text, logger):
    pattern = r"\b(1|2)\d{3}\b"
    matches = re.findall(pattern, text)

    logger.debug(f"{len(matches)} années trouvées (brut)")

    # matches contient seulement '1' ou '2' car mauvaise capture → corriger :
    fixed = re.findall(r"\b((?:1|2)\d{3})\b", text)

    logger.debug(f"{len(fixed)} années extraites (corrigé)")
    return fixed


# -------------------------
# Extraction des URLs
# -------------------------

def extract_urls(text, base_url, logger):
    url_pattern = r'href="([^"]+)"'
    raw_urls = re.findall(url_pattern, text)

    logger.debug(f"{len(raw_urls)} liens bruts trouvés")

    absolute_urls = []
    for u in raw_urls:
        absolute = urljoin(base_url, u)
        absolute_urls.append(absolute)

    # Élimination des doublons
    unique_urls = list(set(absolute_urls))

    logger.debug(f"{len(unique_urls)} liens uniques après nettoyage")

    return unique_urls
