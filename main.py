import requests
from bs4 import BeautifulSoup
import json


SEARCH_QUERY = "Python"
CITIES = ["Москва", "Санкт-Петербург"]
KEYWORDS = ["Django", "Flask"]


BASE_URL = "https://spb.hh.ru/search/vacancy?text=python&area=1&area=2"
PARAMS = {
    "text": SEARCH_QUERY,
    "area": [1, 2],  # Moscow and St. Petersburg
    "page": 0
}


vacancies = []

while True:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/58.0.3029.110 ',
    }
    response = requests.get(BASE_URL, params=PARAMS, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')


    vacancy_cards = soup.find_all(class_='vacancy-serp-item')


    for card in vacancy_cards:

        link = card.find('a', class_='bloko-link')['href']
        title = card.find('a', class_='bloko-link').text


        company = card.find('a', class_='bloko-link').text
        city = card.find(class_='vacancy-serp-item__meta-info').text


        salary = card.find(class_='vacancy-serp-item__compensation')
        if salary:
            salary = salary.text.strip()
        else:
            salary = 'Не указана'


        description = card.find(class_='g-user-content').text


        if any(keyword.lower() in description.lower() for keyword in KEYWORDS):

            vacancies.append({
                "link": link,
                "title": title,
                "company": company,
                "city": city,
                "salary": salary
            })


    next_page_link = soup.find('a', class_='bloko-button', string='Далее')
    if not next_page_link:
        break
    PARAMS["page"] += 1


with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

