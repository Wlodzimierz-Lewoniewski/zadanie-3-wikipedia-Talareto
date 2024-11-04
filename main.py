import requests
from bs4 import BeautifulSoup

def get_articles_from_category(category):
    url = f"https://pl.wikipedia.org/wiki/Kategoria:{category.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = []
    for link in soup.select('div.mw-category-group a'):
        title = link.get('title')
        if title and not title.startswith("Kategoria:"):
            articles.append(link.get('href'))

    return articles[:2]  # Zwracamy tylko pierwsze dwa artykuły

def extract_article_info(article_url):
    url = f"https://pl.wikipedia.org{article_url}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Ekstrakcja odnośników wewnętrznych
    internal_links = [a.get('title') for a in soup.select('a[href^="/wiki/"]') if a.get('title')][:5]
    
    # Ekstrakcja URL obrazków
    images = [img.get('src') for img in soup.select('img')][:3]
    
    # Ekstrakcja źródeł
    references = [ref.get('href') for ref in soup.select('ol.references a[href^="http"]')][:3]
    
    # Ekstrakcja kategorii
    categories = [cat.text for cat in soup.select('div#catlinks a')][:3]

    return internal_links, images, references, categories

def format_output(articles_info):
    output_lines = []
    
    for internal_links, images, references, categories in articles_info:
        # Formatuj wyniki dla każdego artykułu
        output_lines.append(" | ".join(internal_links) if internal_links else "")
        output_lines.append(" | ".join(images) if images else "")
        output_lines.append(" | ".join(references) if references else "")
        output_lines.append(" | ".join(categories) if categories else "")
    
    return "\n".join(output_lines)

def main():
    category = input().strip()  # Oczekujemy, że wejście będzie podane w odpowiednim formacie
    
    articles = get_articles_from_category(category)
    
    articles_info = []
    
    for article in articles:
        internal_links, images, references, categories = extract_article_info(article)
        articles_info.append((internal_links or [], images or [], references or [], categories or []))
    
    result = format_output(articles_info)
    
    print(result)

if __name__ == "__main__":
    main()
