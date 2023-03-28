import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json


def num_page(text: str) -> int:
    ua = fake_useragent.UserAgent()  # генерим новый user-agent
    data = requests.get(
        url=f'https://hh.ru/search/vacancy?text={text}&area=1&page=1',
        headers={'user-agent': ua.random}
    )
    if data.status_code != 200:  # проверяем ответ от сервера
        return
    soup = BeautifulSoup(data.content, 'lxml')
    # находим количество страниц
    try:
        page_count = int(
            soup.find('div', attrs={'class': 'pager'}).find_all('span', recursive=False)[-1].find('a').find(
                'span').text)
    except:
        return
    print(page_count)  # выводим количество страниц
    return page_count


def get_link(text: str, page_count: int):
    for page in range(page_count):
        try:
            ua = fake_useragent.UserAgent()
            data = requests.get(
                url=f'https://hh.ru/search/vacancy?text={text}&area=1&page={page}',
                headers={'user-agent': ua.random}
            )
            soup = BeautifulSoup(data.content, 'lxml')
            # print(soup.find_all('div', attrs={'class': 'serp-item'}))
            for item in soup.find_all('div', attrs={'class': 'serp-item'}):
                # print(item.find('a', attrs={'class': 'serp-item__title'}).text.strip())
                title = item.find('a', attrs={'class': 'serp-item__title'})
                link = title.get('href').split('?')[0]
                title = item.find('a', attrs={'class': 'serp-item__title'}).text.strip()
                print('[TITLE]:', title)
                print('[LINK]:', link)
                try:
                    price = item.find('span', attrs={'class': 'bloko-header-section-3'}).text
                    print('[PRICE]:', price)
                except:
                    print('Не указана З/П')

                company = item.find('div', attrs={'class': 'vacancy-serp-item-company'}).text
                print('[COMPANY]:', company, '\n')

                info = item.find('div', attrs={'class': 'g-user-content'}).text
                print(info, '\n')


        # g-user-content

        except Exception as e:
            print(f"{e}")
        time.sleep(1)
        # print(page)
        # print(soup.find_all('div', attrs={'class': 'serp-item__title'}))


# <a class="serp-item__title" data-qa="serp-item__title" target="_blank" href="https://hh.ru/vacancy/72893267?from=vacancy_search_list&amp;query=Python">Руководитель бизнес-анализа</a>


def get_resume(link='https://voronezh.hh.ru/vacancy/77722681'):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={'user-agent': ua.random}
    )
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        name = soup.find(attrs={'class': 'vacancy-title'}).text
        salary = soup.find(attrs={'class': 'bloko-header-section-2 bloko-header-section-2_lite'})

        info = soup.find(attrs={'class': 'bloko-columns-row'}).text
        # info1 = soup.find_all('p')
        print(name)
        print(salary)

    except:
        return


if __name__ == '__main__':
    # st = 'python'
    # count_page = num_page(st)
    # get_link(st, count_page)
    get_resume()
