import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

main_page = "https://habr.com/ru/articles/top/daily/"

def get_html (url: str) -> str:
    response = requests.get(url,headers={'User-Agent': UserAgent().google})
    print("get response ...")
    return response.text

def get_soup (url: str) -> BeautifulSoup:
    return BeautifulSoup(url, 'lxml')

def main():
    print("start running ...")
    html = get_html(main_page)
    soup = get_soup(html)
    print(soup)


if __name__ == '__main__':
    main()















