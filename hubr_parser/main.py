import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

main_page = "https://habr.com/ru/articles/top/daily/"

def get_html (url: str) -> str:
    response = requests.get(url)
    return response.text

def get_soup (url: str) -> BeautifulSoup:
    return BeautifulSoup(get_html(url), 'lxml')

def main():
    html = get_html(main_page)
    soup = get_soup(html)
    print(soup.text)


if __name__ == '__main__':
    main()















