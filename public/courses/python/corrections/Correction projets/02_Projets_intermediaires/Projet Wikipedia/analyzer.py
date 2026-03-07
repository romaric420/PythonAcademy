from collections import Counter

def analyze_years(years, logger):
    # Convertir en entiers
    years_int = list(map(int, years))

    # Filtrer
    valid_years = list(filter(lambda y: 1000 <= y <= 2100, years_int))

    valid_years.sort()

    stats = Counter(valid_years)

    logger.debug(f"{len(valid_years)} années retenues après filtrage")

    return valid_years, stats
