import json
import requests
import bs4
import fake_headers

headers_gen = fake_headers.Headers(browser='chrome', os='win')
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers_gen.generate(), proxies={})

main_html = response.text
main_soup = bs4.BeautifulSoup(main_html, 'lxml')

keywords = ['Django', 'Flask']

vacancies_all_list = main_soup.find(class_='vacancy-serp-content')
vacancies_all = vacancies_all_list.find_all(class_='serp-item')
vacancy_list = []

for vacancy in vacancies_all:
    link = vacancy.find('a')['href']
    salary = vacancy.find('span', class_='bloko-header-section-2')
    if salary is None:
        pay = f"Зарплата не указана"
    else:
        pay = salary.text
    company = vacancy.find('a', {'data-qa': 'serp-item__title'}).text
    city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    description = vacancy.find('a', class_='serp-item__title').text
    if (keyword in description for keyword in keywords):
        vacancy_list.append({
            'Ссылка': link,
            'Зарплата': pay,
            'Компания': company,
            'Город': city})

with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(vacancy_list, file, ensure_ascii=False, indent=4)
