
import requests
from bs4 import BeautifulSoup
import html


def extract_article_details(article_path):
    url = f'https://pl.wikipedia.org{article_path}'

    response = requests.get(url)

    if response.status_code == 200:
        content = response.text
        result = []

        soup = BeautifulSoup(content, 'html.parser')
        body_content = soup.find("div", class_="mw-body-content")

        internal_links = [link['title'] for link in body_content.find_all('a', href=True)
                          if link['href'].startswith('/wiki/') and ':' not in link['href'][6:]][:5]

        internal_links_str = " | ".join(internal_links)
        result.append(internal_links_str)

        images = body_content.find_all("img")
        image_sources = [img["src"] for img in images if '/wiki/' not in img['src']][:3]
        image_urls = " | ".join(image_sources) if image_sources else ""

        result.append(image_urls)

        ref_section = soup.find("div", class_="mw-references-wrap mw-references-columns")
        if ref_section is None:
            ref_section = soup.find("div", class_="do-not-make-smaller refsection")

        external_links = ""
        if ref_section:
            links = ref_section.find_all("li")
            external_links = [a['href'] for li in links
                              for span in li.find_all("span", class_="reference-text")
                              for a in span.find_all("a", href=True) if "http" in a['href']][:3]
            external_links = " | ".join(html.escape(link) for link in external_links)

        result.append(external_links)

        category_section = soup.find("div", class_="mw-normal-catlinks")
        if category_section:
            category_list = category_section.find('ul')
            categories = [cat.text.strip() for cat in category_list.find_all("a")[:3]]
            categories_str = " | ".join(categories)
            result.append(categories_str)

        return result

    else:
        print("Error fetching page:", response.status_code)


def main_process():
    query = input().replace(" ", '_')

    category_url = f'https://pl.wikipedia.org/wiki/Kategoria:{query}'
    response = requests.get(category_url)

    if response.status_code == 200:
        category_content = response.text
        soup = BeautifulSoup(category_content, 'html.parser')

        category_div = soup.find("div", class_="mw-category mw-category-columns")
        links = [link["href"] for link in category_div.find_all("a")[:2]]

        for link in links:
            for detail in extract_article_details(link):
                print(detail)

    else:
        print("Error fetching category page:", response.status_code)


if __name__ == "__main__":
    main_process()
