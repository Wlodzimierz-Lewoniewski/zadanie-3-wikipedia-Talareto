import requests
from bs4 import BeautifulSoup
import html

def fetch_article_details(article_path):
    url = f'https://pl.wikipedia.org{article_path}'
    response = requests.get(url)
    if response.status_code != 200:
        print("Błąd podczas pobierania strony artykułu:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    details = []

    # Find main content area
    body_content = soup.find("div", class_="mw-body-content")
    if not body_content:
        print("Nie znaleziono zawartości artykułu.")
        return []

    # Internal links
    internal_links = [a.get('title') for a in body_content.find_all('a', href=True)
                      if a['href'].startswith('/wiki/') and ':' not in a['href'][6:]][:5]
    details.append("Wewnętrzne odnośniki: " + (" | ".join(internal_links) if internal_links else "Brak"))

    # Images
    images = [img['src'] for img in body_content.find_all("img") if img['src'].startswith('//upload')][:3]
    details.append("Obrazy: " + (" | ".join(images) if images else "Brak"))

    # External links in references section
    references_section = soup.find("div", class_="mw-references-wrap") or soup.find("div", class_="refsection")
    external_links = []
    if references_section:
        for ref in references_section.find_all("li"):
            for link in ref.find_all("a", href=True):
                if link['href'].startswith("http"):
                    external_links.append(html.escape(link['href']))
                    if len(external_links) == 3:
                        break
    details.append("Zewnętrzne linki: " + (" | ".join(external_links) if external_links else "Brak"))

    # Categories
    category_section = soup.find("div", class_="mw-normal-catlinks")
    if category_section:
        category_links = [a.text.strip() for a in category_section.find('ul').find_all("a")[:3]]
        details.append("Kategorie: " + (" | ".join(category_links) if category_links else "Brak"))
    else:
        details.append("Kategorie: Brak")

    return details

def main():
    category_name = input("Podaj nazwę kategorii: ").replace(" ", '_')
    category_url = f'https://pl.wikipedia.org/wiki/Kategoria:{category_name}'

    response = requests.get(category_url)
    if response.status_code != 200:
        print("Błąd podczas pobierania strony kategorii:", response.status_code)
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    category_div = soup.find("div", class_="mw-category")
    if not category_div:
        print("Nie znaleziono kategorii na stronie.")
        return

    # Collect paths for the first two articles in the category
    article_paths = [a['href'] for a in category_div.find_all("a", href=True)[:2]]

    # Fetch and print details for each article
    for i, path in enumerate(article_paths, start=1):
        print(f"\n--- Artykuł {i} ---")
        article_details = fetch_article_details(path)
        for detail in article_details:
            print(detail)

if __name__ == "__main__":
    main()
