from bs4 import BeautifulSoup
import json
import time
import asyncio
import aiohttp
import requests


start_time = time.time()
job_vacancy_data_list = []


def gather_data(items):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }

    url = f"https://hh.ru/vacancies/analitik-dannyh?page={items}"
    req = requests.get(headers=headers, url=url)

    vacancy_file = f"data/vacancy"

    with open(f'{vacancy_file}.html', 'w', encoding='utf-8') as file:
        file.write(req.text)

    with open(f'{vacancy_file}.html', 'r', encoding='utf-8') as file:
        scrap = file.read()

    soup = BeautifulSoup(scrap, "lxml")

    vacancy= soup.find_all(class_="serp-item__title")
    for el in vacancy:
        print(el)



def main():
    items = 0
    gather_data(items)


main()