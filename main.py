import json
import requests
import bs4
import fake_headers
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint

headers_gen = fake_headers.Headers(browser='chrome', os='win')
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_gen.generate(), proxies={})

main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')

keywords = ['Django', 'Flask']

vacancies_all = main_soup.find_all(class_='vacancy-serp-content')
vacancy_list = []

for vacancy in vacancies_all:
    link = vacancy.find('a')['href']
    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
    company = vacancy.find('h3', {'data-qa': 'bloko-header-3'}).text
    city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    vacancy_list.append({
        'Ссылка': link,
        'Зарплата': salary,
        'Компания': company,
        'Город': city})

pprint(vacancy_list)



with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(vacancy_list, file, ensure_ascii=False, indent=4)
