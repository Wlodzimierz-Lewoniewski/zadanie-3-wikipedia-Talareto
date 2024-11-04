import requests
from bs4 import BeautifulSoup


def get_articles_from_category(category):
    # Krok 1: Pobranie kodu HTML kategorii
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{category.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Krok 2: Ekstrakcja adresów URL i nazw artykułów
    articles = []
    for link in soup.select('div.mw-category-group a'):
        title = link.get('title')
        if title and not title.startswith("Kategoria:"):
            articles.append(link.get('href'))

    return articles[:2]  # Zwracamy tylko pierwsze dwa artykuły


def extract_article_info(article_url):
    # Krok 3: Pobranie kodu HTML artykułu
    url = f"https://pl.wikipedia.org{article_url}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Krok 4: Ekstrakcja odnośników wewnętrznych
    internal_links = [a.get('title') for a in soup.select('a[href^="/wiki/"]')][:5]

    # Krok 5: Ekstrakcja URL obrazków
    images = [img.get('src') for img in soup.select('img')][:3]

    # Krok 6: Ekstrakcja źródeł
    references = [ref.get('href') for ref in soup.select('ol.references a[href^="http"]')][:3]

    # Krok 7: Ekstrakcja kategorii
    categories = [cat.text for cat in soup.select('div#catlinks a')][:3]

    return internal_links, images, references, categories


def format_output(articles_info):
    output_lines = []

    for internal_links, images, references, categories in articles_info:
        output_lines.append(" | ".join(internal_links) if internal_links else "")
        output_lines.append(" | ".join(images) if images else "")
        output_lines.append(" | ".join(references) if references else "")
        output_lines.append(" | ".join(categories) if categories else "")

    return "\n".join(output_lines)


def main():
    category = input("Podaj nazwę kategorii w polskojęzycznej Wikipedii (np. 'Miasta na prawach powiatu'): ")

    articles = get_articles_from_category(category)

    articles_info = []

    for article in articles:
        internal_links, images, references, categories = extract_article_info(article)
        articles_info.append((internal_links, images, references, categories))

    result = format_output(articles_info)

    print(result)


if __name__ == "__main__":
    main()
