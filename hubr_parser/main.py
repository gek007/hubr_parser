import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from dataclasses import dataclass
from pprint import pprint
from urllib.parse import urljoin


main_page = "https://habr.com/ru/articles/top/daily/"
base_url = "https://habr.com"

def get_html (url: str) -> str:
    response = requests.get(url,
                    headers={
                              'User-Agent': UserAgent().google
                             }
                            )
    print("get response ...")
    return response.text

def get_soup (url: str) -> BeautifulSoup:
    return BeautifulSoup(url, 'lxml')

@dataclass
class ArticleData:
    title: str
    views:str
    href: str
    text:str


def get_text(href: str) -> str:
    full_url = urljoin(base_url, href)
    resp = requests.get(full_url)
    soup = BeautifulSoup(resp.text, "html.parser")
    title = soup.find("h1").get_text(strip=True)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    article_text = " ".join(paragraphs)
    return article_text



def get_post_text(href: str) -> str:
    # join relative URL (like "/articles/12345/") with base
    full_url = urljoin(base_url, href)

    soup = get_soup(full_url)

    # On Habr, article text is inside <div class="tm-article-body">
    article_div = soup.find("div", class_="tm-article-body")

    if not article_div:
        return "No article text found"

    # Get plain text without HTML tags
    return article_div.get_text(separator="\n", strip=True)

def get_all_habr_posts(soup: BeautifulSoup)-> list[ArticleData]:
    posts_data =[]
    all_articles_soup = soup.find_all("article", class_ = "tm-articles-list__item")
    for article_soup in all_articles_soup:
        element = article_soup.find("a", class_="tm-title__link")
        article_title = element.find("span").text
        print(f"{article_title=}")
        href = element["href"]
        article_views = article_soup.find("span", class_="tm-icon-counter__value").text
        print(f"{article_views=}")
        text = get_text(href)
        posts_data.append(ArticleData(
            title= article_title,
            views = article_views,
            href = href,
            text = text
        ))

    return posts_data


def main():
    print("start running ...")
    html = get_html(main_page)
    soup = get_soup(html)
    posts = get_all_habr_posts(soup)
    pprint(posts)



if __name__ == '__main__':
    main()















