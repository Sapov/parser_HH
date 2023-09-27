import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

from .models import Parser


# import db
# from db import Database

def del_table():
    pars = Parser.objects.all()
    pars.delete()


def num_page(text: str) -> int:
    ''' Парсим пангинацию'''
    ua = fake_useragent.UserAgent()  # генерим новый user-agent
    data = requests.get(
        url=f'https://hh.ru/search/vacancy?text={text}&area=1&page=1',
        headers={'user-agent': ua.random}
    )
    if data.status_code != 200:  # проверяем ответ от сервера
        return 'Сервер не отвечает'
    soup = BeautifulSoup(data.content, 'lxml')
    # находим количество страниц
    try:
        page_count = int(
            soup.find('div', attrs={'class': 'pager'}).find_all('span', recursive=False)[-1].find('a').find(
                'span').text)
    except:
        return
    print('Количество страниц: ', page_count)  # выводим количество страниц
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
            for item in soup.find_all('div', attrs={'class': 'serp-item'}):
                title = item.find('a', attrs={'class': 'serp-item__title'})
                yield title.get('href').split('?')[0]

        except Exception as e:
            print(f"{e}")


def get_vacancy(link='https://voronezh.hh.ru/vacancy/77722681'):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={'user-agent': ua.random}
    )
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        title = soup.find(attrs={'class': 'vacancy-title'}).text
        t2 = soup.find('a', attrs={'class': 'serp-item__title'}).text.strip()

        salary = soup.find(attrs={'class': 'bloko-header-section-2 bloko-header-section-2_lite'}).text
        description = soup.find(attrs={'class': 'vacancy-description'}).text.strip()[:200]
        description = ' '.join(description.split())  # Удаляем мусор знаки переноса, пробелы
        company = soup.find('div', attrs={'class': 'vacancy-serp-item-company'}).text
        vacancy_description = soup.find('p', attrs={'class': 'vacancy-description-list-item'}).text
        vacancy_cretion = soup.find('p', attrs={'class': 'vacancy-creation-time-redesigned'}).text

        response = {
            'title': t2,
            'link': link,
            'vacancy_description': vacancy_description,
            'company': company,
            'salary': salary,
            'description': description,
            'vacancy_cretion': vacancy_cretion

        }

        # добавляем в базу django
        Parser.objects.create(title=t2, link=link, vacancy_description=vacancy_description, company=company,
                              salary=salary, description=description, add_date=vacancy_cretion)

        print(title)
        print(vacancy_cretion)

        print(t2)
        print(vacancy_description)
        print(link)
        print('COMPANY: ', company)
        print(salary)
        print(description, '\n')

    except:
        return
    return response


def check():
    '''проверка если запись уже есть пропускаем'''


def main(st: str):
    del_table()
    count_page = num_page(st)
    get_link(st, count_page)
    for link in get_link(st, count_page):
        response = get_vacancy(link)

        # Database('2h.db').add_base(response)
        time.sleep(1)


if __name__ == '__main__':
    main('python')
