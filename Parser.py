#!/usr/bin/env python
# -*- coding: utf-8 -*-


import urllib.request
from bs4 import BeautifulSoup
import csv


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    ul = soup.find('ul', {'class': "pagination hidden-xs"})
    li = ul.find_all('li')[-2]
    return int(li.text)
    # ul = nav.find('ul', class_='pagination hidden-xs')
    # return int(ul.find_all('li')[-2].text)


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', {'class': "col-md-8 col-left"})

    vacations = []

    for row in div.find_all('div', {'class': "card card-hover card-visited job-link"}):
        columns1 = row.find_all('h2')
        columns2 = row.find_all('div', class_='')

        vacations.append({
            'Vacation_name': columns1[0].a.text,
            'Company': columns2[0].span.text
        })
    return vacations

def save(vacations, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('Специализация', 'Компания'))

        for vacation in vacations:
            writer.writerow((vacation['Vacation_name'], vacation['Company']))

def main():
    page_c = page_count(get_html('https://www.work.ua/jobs-it-python/'))
    print("Страниц найдено: %d" % page_c)

    vacations = []

    for page in range(1, page_c + 1):
        print("Выполнено %d%%" % (page / page_c * 100))
        vacations.extend(parse(get_html('https://www.work.ua/jobs-it-python/' + '?page=%d' % page)))

    print("Вот что удалось найти:")

    for vacation in vacations:
        print(vacation)

    save(vacations, '1.csv')
        # print(parse(get_html('https://www.work.ua/jobs-kyiv-it-python/')))


if __name__ == '__main__':
    main()
