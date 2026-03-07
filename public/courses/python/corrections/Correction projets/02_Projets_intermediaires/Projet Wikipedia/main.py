from logger_config import get_logger
from fetcher import fetch_page
from parser import extract_years, extract_urls
from analyzer import analyze_years
from exporter import save_json

URL = "https://fr.wikipedia.org/wiki/Intelligence_artificielle"

def main():
    logger = get_logger()

    html = fetch_page(URL, logger)

    years = extract_years(html, logger)
    urls = extract_urls(html, URL, logger)

    if not years:
        logger.warning("Aucune année trouvée !")
        return

    sorted_years, stats = analyze_years(years, logger)

    logger.info(f"Année min : {sorted_years[0]}")
    logger.info(f"Année max : {sorted_years[-1]}")
    logger.info(f"Top 10 années : {stats.most_common(10)}")
    logger.info(f"{len(urls)} URLs extraites.")

    save_json(sorted_years, stats, urls, logger)


if __name__ == "__main__":
    main()
