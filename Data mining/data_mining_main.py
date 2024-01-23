from bs4 import BeautifulSoup
import json
import time
import asyncio
import aiohttp


start_time = time.time()
job_vacancy_data_list = []


async def get_current_vacancy_data(session, vacancy_url, vacancy_title):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }
    async with session.get(url=vacancy_url, headers=headers) as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')

        """Get info for every vacancy"""
        """Get salary"""
        try:
            vacancy_salary = soup.find(class_="vacancy-title").find(class_='bloko-header-'
                                                                    'section-2 bloko-header-section-2_lite').text
        except Exception:
            vacancy_salary = "No salary info"

        """Get experience"""
        try:
            vacancy_experience = soup.find(class_="vacancy-description-list-item").text
        except Exception:
            vacancy_experience = "No experience info"

        print(vacancy_salary, vacancy_title, vacancy_url, vacancy_experience, sep='\n')
        print()




async def gather_data(page):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/"
                  "*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "91.0.4472.106 Safari/537.36"
    }

    url = f"https://hh.ru/vacancies/analitik-dannyh?page={page}"

    async with aiohttp.ClientSession(trust_env=True) as session:
        response = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await response.text(), "lxml")

        vacancy = soup.find_all(class_="vacancy-serp-item-body__main-info")
        vacancy_urls = []
        vacancy_titles = []
        for el in vacancy[1:5]:
            #get url of the current vacancy
            vacancy_url = el.find(class_="bloko-link").get("href")
            vacancy_urls.append(vacancy_url)
            #get title of the current vacancy
            vacancy_title = el.find(class_='serp-item__title').text
            vacancy_titles.append(vacancy_title)

        tasks = []

        for vacancy_url, vacancy_title in zip(vacancy_urls, vacancy_titles):
            task = asyncio.create_task(get_current_vacancy_data(session, vacancy_url, vacancy_title))
            tasks.append(task)
        await asyncio.gather(*tasks)



def main():
    page = 0
    asyncio.run(gather_data(page))


main()