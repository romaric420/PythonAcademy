import json

def save_json(sorted_years, stats, urls, logger):
    data = {
        "sorted_years": sorted_years,
        "top_frequent_years": stats.most_common(20),
        "urls": urls
    }

    with open("resultats.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logger.info("Fichier JSON généré : resultats.json")
