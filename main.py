import requests
from bs4 import BeautifulSoup

def fetch_article_data(article_path):
    # Budowanie pełnego URL
    url = f'https://pl.wikipedia.org{article_path}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Błąd: Nie udało się pobrać artykułu {article_path}")
        return []

    # Parsowanie HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find("div", class_="mw-body-content")
    
    # Zbieranie danych: linki wewnętrzne
    internal_links = [a['title'] for a in content_div.find_all('a', href=True) if a['href'].startswith('/wiki/') and ':' not in a['href'][6:]][:5]
    
    # Zbieranie danych: obrazki
    images = [img['src'] for img in content_div.find_all('img', src=True) if '/wiki/' not in img['src']][:3]

    # Zbieranie danych: linki zewnętrzne (źródła)
    references = []
    for ref in soup.find_all("li", class_="references"):
        links = ref.find_all('a', href=True)
        for link in links:
            if "http" in link['href']:
                references.append(link['href'])
        if len(references) >= 3:
            break

    # Zbieranie danych: kategorie
    categories_div = soup.find("div", class_="mw-normal-catlinks")
    categories = [cat.text.strip() for cat in categories_div.find_all('a')[:3]] if categories_div else []

    return {
        'internal_links': " | ".join(internal_links),
        'images': " | ".join(images),
        'references': " | ".join(references[:3]),
        'categories': " | ".join(categories)
    }

def main():
    search_term = input("Wprowadź kategorię: ").replace(" ", "_")
    base_url = f'https://pl.wikipedia.org/wiki/Kategoria:{search_term}'
    
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Błąd: Nie udało się pobrać strony kategorii dla {search_term}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find("div", class_="mw-category").find_all("a", href=True)

    # Przetwarzanie pierwszych 2 artykułów z kategorii
    for link in links[:2]:
        article_data = fetch_article_data(link['href'])
        if article_data:
            print(f"\nArtykuł: {link['title']}")
            for key, value in article_data.items():
                print(f"{key.capitalize()}: {value}")

if __name__ == "__main__":
    main()
