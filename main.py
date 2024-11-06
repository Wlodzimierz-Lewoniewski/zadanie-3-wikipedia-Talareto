import requests
from bs4 import BeautifulSoup
import html

def fetch_article_details(article_path):
    url = f'https://pl.wikipedia.org{article_path}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        details = []
        body_content = soup.find("div", class_="mw-body-content")
        internal_links = [a.get('title') for a in body_content.find_all('a', href=True)
                          if a['href'].startswith('/wiki/') and ':' not in a['href'][6:]][:5]
        details.append(" | ".join(internal_links))
        images = [img['src'] for img in body_content.find_all("img") if img['src'].startswith('//upload')][:3]
        details.append(" | ".join(images) if images else "")


        references_section = soup.find("div", class_="mw-references-wrap") or soup.find("div", class_="refsection")
        external_links = []
        if references_section:
            for ref in references_section.find_all("li"):
                for link in ref.find_all("a", href=True):
                    if link['href'].startswith("http"):
                        external_links.append(html.escape(link['href']))
                        if len(external_links) == 3:
                            break
        details.append(" | ".join(external_links))


        category_section = soup.find("div", class_="mw-normal-catlinks")
        if category_section:
            category_links = [a.text.strip() for a in category_section.find('ul').find_all("a")[:3]]
            details.append(" | ".join(category_links))
        else:
            details.append("")

        return details
    else:
        print("Błąd podczas pobierania strony:", response.status_code)
        return []

def main():
    category_name = input("Podaj nazwę kategorii: ").replace(" ", '_')
    category_url = f'https://pl.wikipedia.org/wiki/Kategoria:{category_name}'

    response = requests.get(category_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        category_div = soup.find("div", class_="mw-category")
        
        article_paths = [a['href'] for a in category_div.find_all("a")[:2]]

        for path in article_paths:
            article_details = fetch_article_details(path)
            for detail in article_details:
                print(detail)
    else:
        print("Błąd podczas pobierania strony:", response.status_code)

if __name__ == "__main__":
    main()
